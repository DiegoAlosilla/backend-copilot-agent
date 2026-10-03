"""Behavioral tests in isolated repositories; no company repository/services used."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("backend", ROOT / "engineering/backend/scripts/backend.py")
backend = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend)
POLICY = backend.read_json(ROOT / "engineering/backend/quality-policy.json")


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="backend-reports-")
        self.root = Path(self.temp.name).resolve()

    def tearDown(self):
        self.temp.cleanup()

    def report(self, name, content):
        path = self.root / name
        path.write_text(content, encoding="utf-8")
        return path

    def jacoco(self, covered, missed, child=False):
        body = '<package name="a"><class name="a/Foo"/>'
        if child:
            body += '<counter type="INSTRUCTION" covered="10000" missed="0"/>'
        return ('<report name="test">' + body + '</package>'
                f'<counter type="INSTRUCTION" covered="{covered}" missed="{missed}"/>'
                '<counter type="BRANCH" covered="1" missed="1"/></report>')

    def test_949_does_not_round_up(self):
        result = backend.parse_reports("jacoco-xml", [self.report("a.xml", self.jacoco(949, 51, True))], POLICY)
        self.assertFalse(result["pass"])
        self.assertEqual(result["covered"], 949)

    def test_950_passes_and_branch_separate(self):
        result = backend.parse_reports("jacoco-xml", [self.report("a.xml", self.jacoco(950, 50))], POLICY)
        self.assertTrue(result["pass"])
        self.assertEqual(result["branchRatio"], .5)

    def test_jacoco_overlap_rejected(self):
        paths = [self.report("a.xml", self.jacoco(95, 5)), self.report("b.xml", self.jacoco(95, 5))]
        with self.assertRaisesRegex(ValueError, "solapados"):
            backend.parse_reports("jacoco-xml", paths, POLICY)

    def test_jacoco_wrong_counter_rejected(self):
        path = self.report("a.xml", '<report><counter type="LINE" covered="100" missed="0"/></report>')
        with self.assertRaises(ValueError):
            backend.parse_reports("jacoco-xml", [path], POLICY)

    def test_zero_coverage_rejected(self):
        with self.assertRaises(ValueError):
            backend.parse_reports("jacoco-xml", [self.report("a.xml", self.jacoco(0, 0))], POLICY)

    def test_junit_zero_tests_rejected(self):
        with self.assertRaises(ValueError):
            backend.parse_reports("junit-xml", [self.report("a.xml", '<testsuite tests="0"/>')], POLICY)

    def test_junit_aggregate_not_double_counted(self):
        content = '<testsuites><testsuite tests="1"><testcase name="a"/></testsuite></testsuites>'
        result = backend.parse_reports("junit-xml", [self.report("a.xml", content)], POLICY)
        self.assertEqual(result["tests"], 1)
        self.assertTrue(result["pass"])

    def test_junit_failures_rejected(self):
        content = '<testsuite tests="1" failures="1"><testcase><failure/></testcase></testsuite>'
        with self.assertRaises(ValueError):
            backend.parse_reports("junit-xml", [self.report("a.xml", content)], POLICY)

    def test_junit_skipped_fails(self):
        result = backend.parse_reports("junit-xml", [self.report("a.xml", '<testsuite><testcase><skipped/></testcase></testsuite>')], POLICY)
        self.assertFalse(result["pass"])

    def test_junit_inconsistent_summary_rejected(self):
        with self.assertRaisesRegex(ValueError, "inconsistentes"):
            backend.parse_reports("junit-xml", [self.report("a.xml", '<testsuite tests="2"><testcase/></testsuite>')], POLICY)

    def test_karate_failure_and_empty_fail(self):
        for passed, failed in [(1, 1), (0, 0)]:
            path = self.report("a.json", json.dumps({"scenariosPassed": passed, "scenariosFailed": failed}))
            self.assertFalse(backend.parse_reports("karate-json", [path], POLICY)["pass"])

    def test_karate_feature_failure_rejected(self):
        path = self.report("a.json", json.dumps({"scenariosPassed": 1, "scenariosFailed": 0, "featuresFailed": 1}))
        with self.assertRaises(ValueError):
            backend.parse_reports("karate-json", [path], POLICY)

    def test_karate_unknown_format_rejected(self):
        with self.assertRaises(ValueError):
            backend.parse_reports("karate-json", [self.report("a.json", '{"success":true}')], POLICY)

    def test_checkstyle_empty_or_violation_fail(self):
        for content in ['<checkstyle/>', '<checkstyle><file name="A"><error severity="warning"/></file></checkstyle>']:
            self.assertFalse(backend.parse_reports("checkstyle-xml", [self.report("a.xml", content)], POLICY)["pass"])

    def test_build_skip_flags_rejected(self):
        for flag in ["-DskipTests", "-Dmaven.test.skip=true", "-DskipITs=true", "-Dtest=Foo", "-pl", "-Djacoco.skip=true"]:
            with self.assertRaises(ValueError):
                backend.validate_build(["clean", "install", flag])
        backend.validate_build(["clean", "install", "-DskipTests=false"])


FAKE_BUILD = '''import os, pathlib, sys
p = pathlib.Path('target'); p.mkdir(exist_ok=True)
if os.environ.get('BACKEND_FAKE_WRITE', '1') == '1':
    (p/'unit.xml').write_text('<testsuite tests="1"><testcase name="ok"/></testsuite>')
    (p/'karate.json').write_text('{"scenariosPassed":1,"scenariosFailed":0}')
    (p/'checkstyle.xml').write_text('<checkstyle><file name="Foo.java"/></checkstyle>')
    (p/'jacoco.xml').write_text('<report><package name="a"><class name="a/Foo"/></package><counter type="INSTRUCTION" covered="95" missed="5"/></report>')
print('fixture-build')
sys.exit(int(os.environ.get('BACKEND_FAKE_RC', '0')))
'''


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="backend-runtime-")
        self.repo = Path(self.temp.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True, capture_output=True)
        (self.repo / "builder.py").write_text(FAKE_BUILD)
        self.profile = {"schemaVersion": 1, "toolchainFile": ".assistant-local/backend/toolchain.json",
                        "commands": {"build": {"executable": sys.executable,
                                                "args": ["builder.py", "clean", "install"],
                                                "gates": list(POLICY["requiredGates"])}},
                        "reports": {"unit": {"kind": "junit-xml", "patterns": ["target/unit.xml"]},
                                    "karate": {"kind": "karate-json", "patterns": ["target/karate.json"]},
                                    "checkstyle": {"kind": "checkstyle-xml", "patterns": ["target/checkstyle.xml"]},
                                    "coverage": {"kind": "jacoco-xml", "patterns": ["target/jacoco.xml"]}}}
        self.save_profile()
        backend.write_json(self.repo / "engineering/backend/quality-policy.json", POLICY)

    def tearDown(self):
        self.temp.cleanup()

    def save_profile(self):
        backend.write_json(self.repo / "engineering/backend/repository-profile.json", self.profile)

    def run_build(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return backend.run_check(self.repo, "build", "TEST-1")

    def verify(self):
        with contextlib.redirect_stdout(io.StringIO()):
            code = backend.verify(self.repo, "TEST-1")
        return code, backend.read_json(self.repo / ".assistant-local/backend/runs/TEST-1/verification.json")

    def test_green_full_run(self):
        self.assertEqual(self.run_build(), 0)
        code, result = self.verify()
        self.assertEqual(code, 0, result)
        self.assertTrue(all(x["status"] == "PASS" for x in result["gates"].values()))

    def test_missing_karate_is_not_run(self):
        self.profile["commands"]["build"]["gates"].remove("karate")
        # The shared policy must not be changed when the command loses a gate.
        backend.write_json(self.repo / "engineering/backend/quality-policy.json", backend.read_json(ROOT / "engineering/backend/quality-policy.json"))
        self.save_profile()
        self.run_build()
        code, result = self.verify()
        self.assertEqual(code, 1)
        self.assertEqual(result["gates"]["karate"]["status"], "NOT_RUN")

    def test_old_reports_rejected(self):
        subprocess.run([sys.executable, "builder.py"], cwd=self.repo, check=True, capture_output=True)
        self.profile["commands"]["build"]["environment"] = {"BACKEND_FAKE_WRITE": "0"}
        self.save_profile()
        self.run_build()
        code, result = self.verify()
        self.assertEqual(code, 1)
        self.assertIn("no regenerado", result["gates"]["unit"]["reason"])

    def test_source_change_invalidates_evidence(self):
        self.run_build()
        (self.repo / "New.java").write_text("class New {}")
        code, result = self.verify()
        self.assertEqual(code, 1)
        self.assertEqual(result["gates"]["build"]["status"], "FAIL")

    def test_report_modified_rejected(self):
        self.run_build()
        (self.repo / "target/unit.xml").write_text('<testsuite tests="2"><testcase/><testcase/></testsuite>')
        code, result = self.verify()
        self.assertEqual(code, 1)
        self.assertIn("Reporte cambió", result["gates"]["unit"]["reason"])

    def test_command_failure_blocks_even_with_good_reports(self):
        self.profile["commands"]["build"]["environment"] = {"BACKEND_FAKE_RC": "1"}
        self.save_profile()
        self.assertEqual(self.run_build(), 1)
        self.assertEqual(self.verify()[0], 1)

    def test_not_applicable_incomplete_rejected(self):
        self.profile["notApplicable"] = {"karate": {"reason": "not present"}}
        self.save_profile()
        code, result = self.verify()
        self.assertEqual(code, 1)
        self.assertEqual(result["gates"]["karate"]["status"], "FAIL")

    def test_snapshot_tracks_new_files_and_ignores_docs_logs(self):
        first = backend.snapshot(self.repo)
        backend.write_json(self.repo / ".assistant-local/log.json", {"data": "local"})
        (self.repo / "docs/engineering").mkdir(parents=True)
        (self.repo / "docs/engineering/service-map.md").write_text("map")
        self.assertEqual(first["fingerprint"], backend.snapshot(self.repo)["fingerprint"])
        (self.repo / "api.yaml").write_text("openapi: 3.0.3")
        self.assertNotEqual(first["fingerprint"], backend.snapshot(self.repo)["fingerprint"])

    def test_external_path_rejected(self):
        with self.assertRaises(ValueError):
            backend.contained(self.repo, "../outside")

    def test_ignored_toolchain_change_invalidates_evidence(self):
        backend.write_json(self.repo / ".assistant-local/backend/toolchain.json", {"javaHome": ""})
        self.run_build()
        backend.write_json(self.repo / ".assistant-local/backend/toolchain.json", {"javaHome": "changed"})
        self.assertEqual(self.verify()[0], 1)

    def test_timeout_is_recorded_as_failure(self):
        (self.repo / "builder.py").write_text("import time; time.sleep(20)")
        self.profile["commands"]["build"]["timeoutSeconds"] = 1
        self.save_profile()
        self.assertEqual(self.run_build(), 1)
        self.assertEqual(self.verify()[0], 1)
        records = list((self.repo / ".assistant-local/backend/runs/TEST-1").glob("*.evidence.json"))
        self.assertTrue(backend.read_json(records[0])["timedOut"])

    def test_check_and_run_id_cannot_escape(self):
        for check, run_id in [("../build", "SAFE"), ("build", "../outside")]:
            with self.assertRaises(ValueError):
                backend.run_check(self.repo, check, run_id)

    def test_metrics_distinguishes_commits_and_pending(self):
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "BACKEND Test"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "add", "builder.py", "engineering"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "baseline"], check=True)
        base = backend.git(self.repo, "rev-parse", "HEAD").decode().strip()
        path = self.repo / "Foo.java"
        path.write_text("class Foo {}\n")
        subprocess.run(["git", "-C", str(self.repo), "add", "Foo.java"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "add foo"], check=True)
        path.write_text("class Foo { int value; }\n")
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            backend.metrics(self.repo, base)
        value = json.loads(stream.getvalue())
        self.assertEqual(value["commits"], 1)
        self.assertEqual(value["prNetDelta"]["lines"], 1)
        self.assertEqual(value["pendingTrackedDelta"]["lines"], 2)
        self.assertEqual(value["projectedCommits"], 2)


@unittest.skipUnless(os.name == "nt", "Windows installer")
class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="backend-install-")
        self.repo = Path(self.temp.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True, capture_output=True)
        (self.repo / ".github").mkdir()
        (self.repo / ".github/copilot-instructions.md").write_text("Existing team instructions\n")

    def tearDown(self):
        self.temp.cleanup()

    def install(self, plan=False, support=False, package=ROOT):
        cmd = [shutil.which("pwsh") or shutil.which("powershell"), "-NoProfile", "-File",
               str(package / "Install-Backend.ps1"), "-RepositoryPath", str(self.repo)]
        if plan:
            cmd.append("-PlanOnly")
        if support:
            cmd.append("-SupportOnly")
        return subprocess.run(cmd, capture_output=True, text=True)

    def test_plan_does_not_write_then_install_preserves_and_is_idempotent(self):
        self.assertEqual(self.install(True).returncode, 0)
        self.assertFalse((self.repo / "engineering").exists())
        first = self.install()
        self.assertEqual(first.returncode, 0, first.stderr)
        path = self.repo / ".github/copilot-instructions.md"
        original = path.read_bytes()
        self.assertIn("Existing team instructions", path.read_text())
        second = self.install()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(original, path.read_bytes())
        backend.write_json(self.repo / ".assistant-local/check.json", {"secret": "test-only"})
        ignored = subprocess.run(["git", "-C", str(self.repo), "check-ignore", ".assistant-local/check.json"], capture_output=True)
        self.assertEqual(ignored.returncode, 0)

    def test_conflict_aborts_without_partial_install(self):
        path = self.repo / ".github/agents/backend-java.agent.md"
        path.parent.mkdir()
        path.write_text("Different existing agent")
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.repo / "engineering").exists())
        self.assertEqual(path.read_text(), "Different existing agent")

    def package_copy(self):
        package = self.repo.parent / (self.repo.name + "-package")
        # Isolated sibling created only for this test; cleanup is scoped to it.
        self.addCleanup(shutil.rmtree, package)
        shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns(".git", "__pycache__", ".assistant-local"))
        return package

    def test_support_only_does_not_copy_agents_or_workflows(self):
        result = self.install(support=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.repo / "engineering/backend/scripts/backend.py").is_file())
        self.assertFalse((self.repo / ".github/agents").exists())
        self.assertFalse((self.repo / ".github/workflows").exists())
        self.assertEqual((self.repo / ".github/copilot-instructions.md").read_text(), "Existing team instructions\n")

    def test_managed_update_preserves_service_profile_and_policy(self):
        package = self.package_copy()
        first = self.install(support=True, package=package)
        self.assertEqual(first.returncode, 0, first.stderr)
        profile = self.repo / "engineering/backend/repository-profile.json"
        policy = self.repo / "engineering/backend/quality-policy.json"
        profile.write_text('{"myProfile":"keep"}')
        policy.write_text('{"myPolicy":"keep"}')
        source = package / "engineering/backend/OPERACION.md"
        source.write_text(source.read_text(encoding="utf-8") + "\nUpdated procedure\n", encoding="utf-8")
        plugin = backend.read_json(package / "plugin.json")
        plugin["version"] = "0.4.1"
        backend.write_json(package / "plugin.json", plugin)
        second = self.install(support=True, package=package)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(profile.read_text(), '{"myProfile":"keep"}')
        self.assertEqual(policy.read_text(), '{"myPolicy":"keep"}')
        self.assertIn("Updated procedure", (self.repo / "engineering/backend/OPERACION.md").read_text(encoding="utf-8"))
        self.assertEqual(backend.read_json(self.repo / ".assistant-local/backend/installation.json")["packageVersion"], "0.4.1")

    def test_modified_managed_file_blocks_update_without_partial_copy(self):
        package = self.package_copy()
        self.assertEqual(self.install(support=True, package=package).returncode, 0)
        destination = self.repo / "engineering/backend/OPERACION.md"
        destination.write_text("Local customization")
        (package / "engineering/backend/new-resource.md").write_text("New resource")
        result = self.install(support=True, package=package)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.repo / "engineering/backend/new-resource.md").exists())
        self.assertEqual(destination.read_text(), "Local customization")

    def test_instruction_update_preserves_text_outside_block(self):
        package = self.package_copy()
        self.assertEqual(self.install(package=package).returncode, 0)
        destination = self.repo / ".github/copilot-instructions.md"
        destination.write_text(destination.read_text(encoding="utf-8") + "\nExtra team rule\n", encoding="utf-8")
        source = package / "rules/backend.instructions.md"
        source.write_text(source.read_text(encoding="utf-8") + "\nNew BACKEND rule\n", encoding="utf-8")
        result = self.install(package=package)
        self.assertEqual(result.returncode, 0, result.stderr)
        text = destination.read_text(encoding="utf-8")
        self.assertIn("Existing team instructions", text)
        self.assertIn("Extra team rule", text)
        self.assertIn("New BACKEND rule", text)
        self.assertEqual(text.count("<!-- backend-package:start -->"), 1)


class ToolchainTests(unittest.TestCase):
    setUp = RuntimeTests.setUp
    tearDown = RuntimeTests.tearDown
    save_profile = RuntimeTests.save_profile
    run_build = RuntimeTests.run_build
    verify = RuntimeTests.verify
    def test_explicit_homes_override_only_child_and_preserve_custom_path(self):
        java = self.repo / "jdk"
        maven = self.repo / "maven"
        java.mkdir()
        maven.mkdir()
        backend.write_json(self.repo / self.profile["toolchainFile"],
                           {"javaHome": str(java), "mavenHome": str(maven)})
        spec = dict(self.profile["commands"]["build"], environment={"PATH": "CUSTOM"})
        original = dict(os.environ)
        _, _, _, env, _ = backend.execution_context(self.repo, self.profile, spec)
        self.assertEqual(env["JAVA_HOME"], str(java))
        self.assertEqual(env["MAVEN_HOME"], str(maven))
        self.assertEqual(env["M2_HOME"], str(maven))
        self.assertEqual(env["PATH"], str(java / "bin") + os.pathsep + str(maven / "bin") + os.pathsep + "CUSTOM")
        self.assertEqual(dict(os.environ), original)

    def test_inherits_environment_without_overrides(self):
        with mock.patch.dict(os.environ, {"JAVA_HOME": "EXISTING_JDK", "MAVEN_OPTS": "-Xmx1g"}):
            _, _, overrides, env, _ = backend.execution_context(self.repo, self.profile, self.profile["commands"]["build"])
        self.assertEqual(overrides, {})
        self.assertEqual(env["JAVA_HOME"], "EXISTING_JDK")
        self.assertEqual(env["MAVEN_OPTS"], "-Xmx1g")

    def test_invalid_explicit_home_blocks_without_running(self):
        backend.write_json(self.repo / self.profile["toolchainFile"], {"javaHome": str(self.repo / "absent")})
        with self.assertRaises(ValueError):
            self.run_build()
        self.assertFalse((self.repo / "target").exists())

    def test_changed_effective_environment_invalidates_evidence(self):
        self.assertEqual(self.run_build(), 0)
        with mock.patch.dict(os.environ, {"MAVEN_OPTS": "-Xmx1234m"}):
            code, report = self.verify()
        self.assertEqual(code, 1)
        self.assertIn("entorno efectivo", report["gates"]["build"]["reason"])

    def test_doctor_checks_maven_java_instead_of_assuming_editor_runtime(self):
        java_home = self.repo / "jdk"
        java_bin = java_home / "bin"
        java_bin.mkdir(parents=True)
        (java_bin / ("java.exe" if os.name == "nt" else "java")).write_text("fixture")
        backend.write_json(self.repo / self.profile["toolchainFile"], {"javaHome": str(java_home)})
        self.profile["service"] = {"javaMajor": 17}
        self.save_profile()
        results = [{"exitCode": 0, "output": 'openjdk version "17"'},
                   {"exitCode": 0, "output": "Apache Maven 3.9.9\nJava version: 21.0.2"}]
        with mock.patch.object(backend, "probe", side_effect=results), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(backend.doctor(self.repo), 1)
        report = backend.read_json(self.repo / ".assistant-local/backend/doctor.json")
        self.assertEqual(report["mavenJavaMajor"], 21)
        self.assertEqual(report["status"], "BLOCKED")

    def test_doctor_accepts_legacy_java_version_when_expected(self):
        java_home = self.repo / "jdk"
        (java_home / "bin").mkdir(parents=True)
        (java_home / "bin" / ("java.exe" if os.name == "nt" else "java")).write_text("fixture")
        backend.write_json(self.repo / self.profile["toolchainFile"], {"javaHome": str(java_home)})
        self.profile["service"] = {"javaMajor": 8}
        self.save_profile()
        results = [{"exitCode": 0, "output": 'java version "1.8.0"'},
                   {"exitCode": 0, "output": "Apache Maven 3.9.9\nJava version: 1.8.0_202"}]
        with mock.patch.object(backend, "probe", side_effect=results), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(backend.doctor(self.repo), 0)


if __name__ == "__main__":
    unittest.main()
