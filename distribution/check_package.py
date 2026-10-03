"""Validate this package's flat string frontmatter using only the standard library.

This is intentionally not a general YAML parser. Unsupported YAML structures
fail so a future format change requires a deliberate validator update.
"""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def frontmatter(body):
    if not body.startswith("---\n") or "\n---\n" not in body[4:]:
        raise ValueError("Missing frontmatter boundaries")
    header = body[4:].split("\n---\n", 1)[0]
    result = {}
    for line in header.splitlines():
        match = re.fullmatch(r"([a-z][a-z-]*): (.+)", line)
        if not match:
            raise ValueError("Only flat string frontmatter is supported")
        key, value = match.groups()
        if key in result:
            raise ValueError("Duplicate frontmatter key: " + key)
        if value.startswith("'"):
            if not value.endswith("'"):
                raise ValueError("Unclosed quoted scalar")
            inner = value[1:-1]
            if "'" in inner.replace("''", ""):
                raise ValueError("Invalid single quoted scalar")
            value = inner.replace("''", "'")
        elif value.startswith('"'):
            value = json.loads(value)
        elif (value.startswith(tuple("[{&*!|>")) or ": " in value or " #" in value
              or value.lower() in {"true", "false", "null", "~"}):
            raise ValueError("Quote scalar or extend the validator deliberately")
        if not isinstance(value, str) or not value:
            raise ValueError("Empty/non-string frontmatter value")
        result[key] = value
    return result


def main():
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == "backend-java"
    assert re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"])
    for key in ("agents", "skills", "commands"):
        path = (ROOT / manifest[key]).resolve()
        assert path.is_relative_to(ROOT) and path.is_dir(), key
    documents = [*ROOT.glob(".github/skills/*/SKILL.md"),
                 *ROOT.glob(".github/agents/*.md"), *ROOT.glob(".github/prompts/*.md")]
    for path in documents:
        body = path.read_text(encoding="utf-8")
        assert body.startswith("---\n"), path
        data = frontmatter(body)
        assert isinstance(data.get("description"), str) and data["description"], path
        if path.name == "SKILL.md":
            assert data["name"] == path.parent.name, path
        assert len(body) < 30000, path
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", body):
            if "://" in link or link.startswith("#"):
                continue
            target = (path.parent / link.split("#")[0]).resolve()
            assert target.is_relative_to(ROOT) and target.exists(), (path, link)
    for path in ROOT.rglob("*.json"):
        if any(part in {".git", ".assistant-local", "__pycache__"} for part in path.parts):
            continue
        json.loads(path.read_text(encoding="utf-8"))
    print(f"PACKAGE_PASS: {len(documents)} definitions; plugin {manifest['version']}")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, ValueError, KeyError, OSError) as exc:
        print("PACKAGE_FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
