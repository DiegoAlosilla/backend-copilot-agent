#!/usr/bin/env python3
"""BACKEND local evidence helpers. Python 3.10+, standard library only.

Does not access corporate services, mutate Git, install dependencies or decide
whether a functional change is correct. Commands must be configured and reviewed.
"""
import argparse
import datetime as dt
from decimal import Decimal
import glob
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time
import uuid
import xml.etree.ElementTree as ET

PACKAGE = Path(__file__).resolve().parents[1]
REPORT_KINDS = {"junit-xml", "karate-json", "jacoco-xml", "checkstyle-xml"}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(repo, *args):
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=False)
    if proc.returncode:
        raise ValueError("Git falló: " + " ".join(args))
    return proc.stdout


def repo_root(value):
    repo = Path(value).resolve()
    actual = Path(git(repo, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    if actual != repo:
        raise ValueError("--repo debe ser la raíz Git, no un subdirectorio")
    return repo


def contained(repo, relative):
    path = (repo / relative).resolve()
    if not path.is_relative_to(repo):
        raise ValueError("Ruta fuera del repositorio: " + str(relative))
    return path


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def excluded(name):
    parts = Path(name).parts
    return (any(p in {".git", ".assistant-local", "target", "__pycache__", ".pytest_cache"}
                for p in parts) or name.startswith("docs/engineering/"))


def snapshot(repo):
    names = set(git(repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
                .decode("utf-8").split("\0")) - {""}
    files = {}
    for name in sorted(names):
        if excluded(name):
            continue
        path = repo / name
        if path.is_symlink():
            files[name] = hashlib.sha256(os.readlink(path).encode()).hexdigest()
        elif path.is_file():
            files[name] = sha(path)
        else:
            files[name] = "DELETED"
    profile_path = repo / "engineering/backend/repository-profile.json"
    if profile_path.is_file():
        profile = read_json(profile_path)
        local_inputs = list(profile.get("fingerprintInputs", []))
        if profile.get("toolchainFile"):
            local_inputs.append(profile["toolchainFile"])
        for name in local_inputs:
            path = contained(repo, name)
            files[name] = sha(path) if path.is_file() else "MISSING_LOCAL_INPUT"
    fingerprint = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    try:
        head = git(repo, "rev-parse", "HEAD").decode().strip()
    except ValueError:
        head = None
    return {"schemaVersion": 1, "head": head, "fingerprint": fingerprint,
            "files": files, "observedAt": dt.datetime.now(dt.timezone.utc).isoformat()}


def profiles(repo):
    profile = read_json(repo / "engineering/backend/repository-profile.json")
    policy = read_json(repo / "engineering/backend/quality-policy.json")
    if profile.get("schemaVersion") != 1 or policy.get("schemaVersion") != 1:
        raise ValueError("schemaVersion no soportado")
    return profile, policy


def report_files(repo, spec):
    if spec.get("kind") not in REPORT_KINDS or not spec.get("patterns"):
        raise ValueError("Formato/patrones de reporte no configurados")
    paths = set()
    for pattern in spec["patterns"]:
        if not isinstance(pattern, str) or Path(pattern).is_absolute() or ".." in Path(pattern).parts:
            raise ValueError("Patrón de reporte inválido")
        for found in glob.glob(str(repo / pattern), recursive=True):
            path = contained(repo, Path(found).relative_to(repo))
            if path.is_file():
                paths.add(path)
    return sorted(paths)


def report_inventory(repo, spec):
    return {p.relative_to(repo).as_posix(): {"sha256": sha(p), "mtimeNs": p.stat().st_mtime_ns}
            for p in report_files(repo, spec)}


def count_value(value):
    number = int(value)
    if number < 0:
        raise ValueError("Contador negativo")
    return number


def parse_reports(kind, paths, policy):
    if not paths:
        raise ValueError("Sin reportes")
    if kind == "junit-xml":
        totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
        for path in paths:
            root = ET.parse(path).getroot()
            if root.tag not in {"testsuite", "testsuites"}:
                raise ValueError("XML no es JUnit testsuite(s)")
            cases = list(root.iter("testcase"))
            if not cases:
                raise ValueError("JUnit sin testcase descubierto")
            # Leaf cases avoid counting aggregate testsuites a second time.
            totals["tests"] += len(cases)
            for case in cases:
                for field, tag in (("failures", "failure"), ("errors", "error"), ("skipped", "skipped")):
                    totals[field] += int(case.find(tag) is not None)
            for suite in root.iter("testsuite"):
                suite_cases = list(suite.iter("testcase"))
                observed = {"tests": len(suite_cases),
                            "failures": sum(c.find("failure") is not None for c in suite_cases),
                            "errors": sum(c.find("error") is not None for c in suite_cases),
                            "skipped": sum(c.find("skipped") is not None for c in suite_cases)}
                for field, amount in observed.items():
                    if field in suite.attrib and count_value(suite.attrib[field]) != amount:
                        raise ValueError("JUnit contadores inconsistentes: " + field)
                if observed["failures"] or observed["errors"]:
                    raise ValueError("JUnit reporta fallo de suite")
        totals["pass"] = (not totals["failures"] and not totals["errors"]
                          and totals["skipped"] <= policy["allowedSkippedTests"])
        return totals
    if kind == "karate-json":
        passed = failed = 0
        for path in paths:
            data = read_json(path)
            if "scenariosPassed" not in data or "scenariosFailed" not in data:
                raise ValueError("Summary Karate sin scenariosPassed/scenariosFailed")
            passed += count_value(data["scenariosPassed"])
            failed += count_value(data["scenariosFailed"])
            if count_value(data.get("featuresFailed", 0)):
                raise ValueError("Karate reporta feature fallida")
        return {"passed": passed, "failed": failed, "pass": passed > 0 and failed == 0}
    if kind == "checkstyle-xml":
        violations = checked = 0
        for path in paths:
            root = ET.parse(path).getroot()
            if root.tag != "checkstyle":
                raise ValueError("XML no es Checkstyle")
            checked += len(root.findall("file"))
            violations += len(list(root.iter("error")))
        return {"checkedFiles": checked, "violations": violations,
                "pass": checked > 0 and violations <= policy["checkstyleAllowedViolations"]}
    if kind == "jacoco-xml":
        covered = missed = 0
        branches_covered = branches_missed = 0
        classes = set()
        for path in paths:
            root = ET.parse(path).getroot()
            if root.tag != "report":
                raise ValueError("XML no es JaCoCo report")
            # Reject overlapping module/aggregate reports by qualified class name.
            current = {c.attrib["name"] for c in root.iter("class")}
            if classes.intersection(current):
                raise ValueError("Reportes JaCoCo solapados; no sumar aggregate y módulos")
            classes.update(current)
            counters = [c for c in root.findall("counter") if c.attrib.get("type") == "INSTRUCTION"]
            if len(counters) != 1:
                raise ValueError("JaCoCo necesita un contador INSTRUCTION raíz")
            covered += count_value(counters[0].attrib["covered"])
            missed += count_value(counters[0].attrib["missed"])
            for counter in root.findall("counter"):
                if counter.attrib.get("type") == "BRANCH":
                    branches_covered += count_value(counter.attrib["covered"])
                    branches_missed += count_value(counter.attrib["missed"])
        if not covered + missed:
            raise ValueError("JaCoCo sin instrucciones elegibles")
        ratio = Decimal(covered) / Decimal(covered + missed)
        minimum = Decimal(str(policy["instructionMinimum"]))
        return {"counter": "INSTRUCTION", "covered": covered, "missed": missed,
                "ratio": float(ratio), "minimum": float(minimum),
                "branchRatio": (branches_covered / (branches_covered + branches_missed)
                                if branches_covered + branches_missed else None),
                "pass": ratio >= minimum}
    raise ValueError("Formato no soportado")


def substitute(text, values):
    def replace(match):
        value = values.get(match.group(1))
        if not isinstance(value, str) or not value:
            raise ValueError("Toolchain pendiente: " + match.group(1))
        return value
    return re.sub(r"\$\{([a-zA-Z]+)\}", replace, text)


def validate_build(args):
    if "clean" not in args or "install" not in args or args.index("clean") > args.index("install"):
        raise ValueError("Gate build exige clean antes de install")
    for arg in args:
        low = arg.lower()
        if (re.match(r"-d(?:skiptests|maven\.test\.skip|skipits|checkstyle\.skip|jacoco\.skip)(?:=|$)", low)
                and not low.endswith("=false")) or low.startswith(("-dtest=", "-dit.test=", "-pl", "-rf")):
            raise ValueError("Gate build no acepta omisiones o selección parcial de suite/reactor")


def execution_context(repo, profile, spec):
    toolchain_path = contained(repo, profile["toolchainFile"])
    values = read_json(toolchain_path) if toolchain_path.exists() else {}
    executable = substitute(spec["executable"], values)
    args = [substitute(a, values) for a in spec.get("args", [])]
    overrides = dict(spec.get("environment", {}))
    if not all(isinstance(k, str) and isinstance(v, str) for k, v in overrides.items()):
        raise ValueError("environment debe contener strings")
    path = overrides.get("PATH", os.environ.get("PATH", ""))
    for key, variables in (("mavenHome", ("MAVEN_HOME", "M2_HOME")),
                           ("javaHome", ("JAVA_HOME",))):
        home = values.get(key)
        if home:
            if not isinstance(home, str) or not Path(home).is_absolute() or not Path(home).is_dir():
                raise ValueError("Toolchain contiene un directorio inexistente/no absoluto: " + key)
            for variable in variables:
                overrides[variable] = home
            path = str(Path(home) / "bin") + os.pathsep + path
            overrides["PATH"] = path
    env = dict(os.environ, **overrides)
    # Resolve command names now, using the same PATH the child will receive.
    if not Path(executable).is_absolute():
        local = contained(repo, spec.get("workingDirectory", ".")) / executable
        if local.is_file():
            executable = str(local.resolve())
        elif os.path.dirname(executable):
            raise ValueError("Ejecutable relativo no encontrado: " + executable)
        else:
            found = shutil.which(executable, path=env.get("PATH"))
            if not found:
                raise ValueError("Ejecutable no encontrado en el PATH efectivo: " + executable)
            executable = found
    if not Path(executable).is_file():
        raise ValueError("Ejecutable inexistente: " + executable)
    relevant = {k: env.get(k) for k in ("JAVA_HOME", "MAVEN_HOME", "M2_HOME", "PATH",
                                       "JAVA_TOOL_OPTIONS", "JDK_JAVA_OPTIONS", "MAVEN_OPTS")}
    fingerprint = hashlib.sha256(json.dumps({"executable": executable, "args": args,
                                           "environment": relevant}, sort_keys=True).encode()).hexdigest()
    return executable, args, overrides, env, fingerprint


def probe(repo, executable, args, env):
    command = [executable, *args]
    if os.name == "nt":
        shell = shutil.which("pwsh") or shutil.which("powershell")
        if not shell:
            raise ValueError("PowerShell no disponible")
        path = repo / ".assistant-local/backend/doctor" / (uuid.uuid4().hex + ".json")
        # Only the process-local changes required for version discovery are saved.
        overrides = {k: env[k] for k in ("JAVA_HOME", "MAVEN_HOME", "M2_HOME", "PATH") if k in env}
        write_json(path, {"executable": executable, "arguments": args,
                          "workingDirectory": str(repo), "environment": overrides})
        command = [shell, "-NoProfile", "-NonInteractive", "-File",
                   str(Path(__file__).with_name("Invoke-Command.ps1")), "-SpecPath", str(path)]
    proc = subprocess.Popen(command, cwd=repo, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, start_new_session=os.name != "nt")
    try:
        output, _ = proc.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True)
        else:
            os.killpg(proc.pid, signal.SIGKILL)
        proc.communicate()
        raise ValueError("Diagnóstico de versión excedió 30 segundos")
    return {"exitCode": proc.returncode, "output": output.decode("utf-8", errors="replace").strip()}


def doctor(repo):
    profile, _ = profiles(repo)
    spec = profile.get("commands", {}).get("build")
    if not spec:
        raise ValueError("Configura el comando build real antes de doctor")
    executable, _, _, env, fingerprint = execution_context(repo, profile, spec)
    if env.get("JAVA_HOME"):
        java = Path(env["JAVA_HOME"]) / "bin" / ("java.exe" if os.name == "nt" else "java")
        if not java.is_file():
            raise ValueError("JAVA_HOME no contiene bin/java")
        java = str(java)
    else:
        java = shutil.which("java", path=env.get("PATH"))
        if not java:
            raise ValueError("Java no encontrado en el PATH efectivo")
    java_result = probe(repo, java, ["-version"], env)
    maven_result = probe(repo, executable, ["--version"], env)
    expected = profile.get("service", {}).get("javaMajor")
    match = re.search(r"Java version:\s*(\d+)(?:\.(\d+))?", maven_result["output"], re.I)
    actual = (int(match.group(2)) if match and match.group(1) == "1"
              else int(match.group(1)) if match else None)
    passed = (java_result["exitCode"] == 0 and maven_result["exitCode"] == 0
              and "Apache Maven" in maven_result["output"] and actual is not None
              and (expected is None or int(expected) == actual))
    report = {"status": "TOOLCHAIN_PASS" if passed else "BLOCKED", "python": sys.version.split()[0],
              "javaExecutable": java, "java": java_result, "mavenExecutable": executable,
              "maven": maven_result, "expectedJavaMajor": expected, "mavenJavaMajor": actual,
              "environmentFingerprint": fingerprint,
              "note": "Verifica versiones; no instala herramientas ni valida dependencias/settings Maven"}
    write_json(repo / ".assistant-local/backend/doctor.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if passed else 1


def run_check(repo, check, run_id):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", check):
        raise ValueError("check inválido")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", run_id):
        raise ValueError("run-id inválido")
    profile, _ = profiles(repo)
    spec = profile.get("commands", {}).get(check)
    if not isinstance(spec, dict):
        raise ValueError("Comando no configurado/revisado: " + check)
    executable, args, env_overrides, env, context_fingerprint = execution_context(repo, profile, spec)
    gates = spec.get("gates", [])
    if "build" in gates:
        validate_build(args)
    before = snapshot(repo)
    prior = {gate: report_inventory(repo, profile["reports"][gate]) for gate in gates if gate != "build"}
    folder = repo / ".assistant-local/backend/runs" / run_id
    folder.mkdir(parents=True, exist_ok=True)
    execution_id = check + "-" + uuid.uuid4().hex[:12]
    log = folder / (execution_id + ".log")
    workdir = contained(repo, spec.get("workingDirectory", "."))
    command = [executable, *args]
    if os.name == "nt":
        shell = shutil.which("pwsh") or shutil.which("powershell")
        if not shell:
            raise ValueError("PowerShell no disponible")
        execution_file = folder / (execution_id + ".execution.json")
        write_json(execution_file, {"executable": executable, "arguments": args,
                                  "workingDirectory": str(workdir), "environment": env_overrides})
        command = [shell, "-NoProfile", "-NonInteractive", "-File",
                   str(Path(__file__).with_name("Invoke-Command.ps1")), "-SpecPath", str(execution_file)]
    started = time.time()
    timeout = int(spec.get("timeoutSeconds", 1800))
    if timeout <= 0 or timeout > 7200:
        raise ValueError("timeoutSeconds debe estar entre 1 y 7200")
    timed_out = False
    print("Ejecutando " + check + "; log local: " + str(log), flush=True)
    with log.open("wb") as stream:
        proc = subprocess.Popen(command, cwd=workdir, stdout=stream, stderr=subprocess.STDOUT,
                                env=env, start_new_session=os.name != "nt")
        try:
            code = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True)
            else:
                os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            code = 124
    after = snapshot(repo)
    reports = {}
    for gate in gates:
        if gate == "build":
            continue
        inventory = report_inventory(repo, profile["reports"][gate])
        for name, item in inventory.items():
            item["fresh"] = prior[gate].get(name) != {k: v for k, v in item.items() if k != "fresh"}
        reports[gate] = inventory
    record = {"schemaVersion": 1, "check": check, "gates": gates, "runId": run_id,
              "startedAt": started, "finishedAt": time.time(), "exitCode": code,
              "timedOut": timed_out, "inputBefore": before["fingerprint"],
              "inputAfter": after["fingerprint"], "head": after["head"],
              "executable": executable, "args": args, "workingDirectory": str(workdir),
              "environmentFingerprint": context_fingerprint,
              "reports": reports, "log": log.relative_to(repo).as_posix()}
    path = folder / (execution_id + ".evidence.json")
    write_json(path, record)
    print(json.dumps({"exitCode": code, "record": str(path)}, ensure_ascii=False))
    return 0 if code == 0 else 1


def verify(repo, run_id):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", run_id):
        raise ValueError("run-id inválido")
    profile, policy = profiles(repo)
    current = snapshot(repo)["fingerprint"]
    folder = repo / ".assistant-local/backend/runs" / run_id
    records = sorted((read_json(p) for p in folder.glob("*.evidence.json")), key=lambda x: x["startedAt"])
    result = {}
    for gate in policy["requiredGates"]:
        na = profile.get("notApplicable", {}).get(gate)
        if na:
            if gate in {"build", "coverage"}:
                result[gate] = {"status": "FAIL", "reason": "No admite excepción automática de build/cobertura"}
            elif all(na.get(k) for k in ("reason", "approvedBy", "trackingReference")):
                result[gate] = {"status": "NOT_APPLICABLE", "exception": na}
            else:
                result[gate] = {"status": "FAIL", "reason": "Excepción incompleta"}
            continue
        candidates = [r for r in records if gate in r["gates"]]
        if not candidates:
            result[gate] = {"status": "NOT_RUN", "reason": "Sin ejecución registrada"}
            continue
        record = candidates[-1]
        try:
            if record["exitCode"] != 0:
                raise ValueError("Comando falló")
            if record["inputBefore"] != record["inputAfter"] or record["inputAfter"] != current:
                raise ValueError("Código/config cambió durante o después de ejecución")
            spec = profile["commands"][record["check"]]
            if record.get("environmentFingerprint") != execution_context(repo, profile, spec)[4]:
                raise ValueError("Toolchain/entorno efectivo cambió; vuelve a ejecutar")
            if record["gates"] != spec.get("gates", []):
                raise ValueError("Declaración de gates cambió")
            if gate == "build":
                validate_build(record["args"])
                detail = {"pass": True, "command": record["check"]}
            else:
                report_spec = profile["reports"][gate]
                inventory = record["reports"].get(gate, {})
                if not inventory or not all(v.get("fresh") for v in inventory.values()):
                    raise ValueError("Reporte ausente o no regenerado en esta ejecución")
                paths = []
                for name, item in inventory.items():
                    path = contained(repo, name)
                    if not path.is_file() or sha(path) != item["sha256"]:
                        raise ValueError("Reporte cambió/desapareció después de ejecución")
                    paths.append(path)
                # Reject reports added outside the recorded execution as well.
                if set(inventory) != {p.relative_to(repo).as_posix() for p in report_files(repo, report_spec)}:
                    raise ValueError("Inventario de reportes cambió después de ejecución")
                detail = parse_reports(report_spec["kind"], paths, policy)
            result[gate] = {"status": "PASS" if detail["pass"] else "FAIL", "detail": detail,
                            "check": record["check"], "log": record["log"]}
        except (ValueError, KeyError, ET.ParseError, OSError, TypeError) as exc:
            result[gate] = {"status": "FAIL", "reason": str(exc)}
    passed = all(item["status"] in {"PASS", "NOT_APPLICABLE"} for item in result.values()) and bool(result)
    report = {"schemaVersion": 1, "runId": run_id, "fingerprint": current,
              "status": "LOCAL_GATES_PASS" if passed else "BLOCKED", "gates": result,
              "limits": "No valida aceptación funcional, autenticidad, exclusiones, CI, Sonar o despliegue"}
    write_json(folder / "verification.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if passed else 1


def numstat(data):
    added = removed = binary = 0
    lines = data.decode("utf-8").splitlines()
    for line in lines:
        a, d, _ = line.split("\t", 2)
        if a == "-" or d == "-":
            binary += 1
        else:
            added += int(a)
            removed += int(d)
    return {"files": len(lines), "added": added, "removed": removed,
            "lines": added + removed, "binaryFiles": binary}


def metrics(repo, base):
    merge = git(repo, "merge-base", base, "HEAD").decode().strip()
    commits = git(repo, "rev-list", merge + "..HEAD").decode().splitlines()
    total = numstat(git(repo, "diff", "--numstat", merge, "HEAD"))
    pending = numstat(git(repo, "diff", "--numstat", "HEAD"))
    per_commit = [numstat(git(repo, "diff", "--numstat", c + "^1", c))
                  for c in commits]
    count = len(commits)
    result = {"base": base, "mergeBase": merge, "commits": count, "prNetDelta": total,
              "pendingTrackedDelta": pending,
              "untrackedFiles": git(repo, "ls-files", "--others", "--exclude-standard").decode().splitlines(),
              "averageFilesPerCommit": sum(x["files"] for x in per_commit) / count if count else 0,
              "averageLinesPerCommit": sum(x["lines"] for x in per_commit) / count if count else 0,
              "projectedCommits": count + int(bool(pending["files"])),
              "note": "Archivos nuevos y binarios requieren revisión; no incluidos como líneas de texto"}
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    for action in ("snapshot", "run", "verify", "metrics", "doctor"):
        command = sub.add_parser(action)
        command.add_argument("--repo", required=True)
        if action == "snapshot":
            command.add_argument("--output")
            command.add_argument("--compare")
        if action in {"run", "verify"}:
            command.add_argument("--run-id", required=True)
        if action == "run":
            command.add_argument("--check", required=True)
        if action == "metrics":
            command.add_argument("--base", required=True)
    args = parser.parse_args()
    try:
        repo = repo_root(args.repo)
        if args.action == "snapshot":
            value = snapshot(repo)
            if args.compare:
                old = read_json(contained(repo, args.compare))
                value["changedFiles"] = sorted(k for k in set(old["files"]) | set(value["files"])
                                               if old["files"].get(k) != value["files"].get(k))
            if args.output:
                write_json(contained(repo, args.output), value)
                print(json.dumps({"fingerprint": value["fingerprint"], "output": args.output,
                                  "changedFiles": value.get("changedFiles", [])}))
            else:
                print(json.dumps(value, ensure_ascii=False, indent=2))
        elif args.action == "run":
            return run_check(repo, args.check, args.run_id)
        elif args.action == "verify":
            return verify(repo, args.run_id)
        elif args.action == "doctor":
            return doctor(repo)
        else:
            metrics(repo, args.base)
        return 0
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
        print("BACKEND_BLOCKED: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
