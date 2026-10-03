"""Packaging validation must work without third-party Python modules."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("package_check", Path(__file__).resolve().parents[1] / "distribution/check_package.py")
package_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package_check)


class FrontmatterTests(unittest.TestCase):
    def test_actual_plain_and_quoted_scalars(self):
        text = "---\nname: backend-sanity\ndescription: 'Checks: status and body; it''s scoped.'\napplyTo: \"**\"\n---\nContent\n"
        parsed = package_check.frontmatter(text)
        self.assertEqual(parsed["description"], "Checks: status and body; it's scoped.")
        self.assertEqual(parsed["applyTo"], "**")

    def test_unsupported_yaml_and_duplicate_keys_fail_explicitly(self):
        for header in ("name: a\nname: b", "description: |\n  multiline", "description: [one, two]", "description: missing: quote"):
            with self.subTest(header=header), self.assertRaises(ValueError):
                package_check.frontmatter("---\n" + header + "\n---\nContent\n")
