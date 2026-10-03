"""Workflow closure against isolated Git repositories and real evidence runner."""
import argparse
import contextlib
import io
from pathlib import Path
import unittest

import test_runtime as runtime

backend, ROOT = runtime.backend, runtime.ROOT


class WorkflowTests(unittest.TestCase):
    setUp = runtime.RuntimeTests.setUp
    tearDown = runtime.RuntimeTests.tearDown
    save_profile = runtime.RuntimeTests.save_profile
    run_build = runtime.RuntimeTests.run_build

    def call(self, action, **values):
        args = dict(action=action, task="TEST-1", request_file=".assistant-local/request.txt",
                    mode="complete", scope_quote="", phase=1, status="DONE", evidence=[],
                    skill=[], reason="", run_id="TEST-1", acceptance_evidence=None)
        args.update(values)
        with contextlib.redirect_stdout(io.StringIO()):
            return backend.workflow(self.repo, argparse.Namespace(**args))

    def start(self, **kwargs):
        file = self.repo / ".assistant-local/request.txt"
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("Corrige el error. Solo diagnóstico si lo pido expresamente.", encoding="utf-8")
        return self.call("workflow-start", **kwargs)

    def phase(self, number, **kwargs):
        relative = f"docs/engineering/changes/TEST-1/phase-{number}.md"
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("Fixture: evidencia para probar consistencia, no aceptación real.", encoding="utf-8")
        skills = [str(ROOT / "skills" / name / "SKILL.md") for name in backend.PHASE_SKILLS[number]]
        return self.call("workflow-phase", phase=number, evidence=[relative], skill=skills, **kwargs)

    def complete_phases(self):
        for number in range(1, 9):
            self.phase(number)
        for relative in ("docs/engineering/service-map.md", "docs/engineering/changes/TEST-1/change.md"):
            path = self.repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Fixture document", encoding="utf-8")

    def state(self):
        return backend.read_json(self.repo / ".assistant-local/backend/workflows/TEST-1/workflow.json")

    def test_default_complete_missing_phases_blocks(self):
        self.start()
        self.phase(1)
        self.assertEqual(self.call("workflow-close"), 1)
        self.assertEqual(self.state()["status"], "BLOCKED")
        self.assertEqual(self.state()["mode"], "complete")

    def test_individual_requires_quote_in_original_request(self):
        for quote in ("", "Auditoría completa inventada por el agente"):
            with self.assertRaises(ValueError):
                self.start(mode="individual", scope_quote=quote)

    def test_existing_scope_cannot_be_reinitialized(self):
        self.start()
        with self.assertRaises(ValueError):
            self.call("workflow-start", mode="individual", scope_quote="Solo diagnóstico")

    def test_individual_closes_without_unrelated_gates(self):
        self.start(mode="individual", scope_quote="Solo diagnóstico")
        self.phase(1)
        self.assertEqual(self.call("workflow-close"), 0)
        self.assertEqual(self.state()["status"], "SCOPED_TASK_DONE")

    def test_implementation_requires_prior_plan(self):
        self.start()
        with self.assertRaises(ValueError):
            self.phase(4)

    def test_empty_evidence_or_missing_skill_rejected(self):
        self.start()
        with self.assertRaises(ValueError):
            self.call("workflow-phase", skill=[str(ROOT / "skills/backend-contexto/SKILL.md")])
        with self.assertRaises(ValueError):
            self.call("workflow-phase", evidence=["builder.py"], skill=[])

    def test_required_phase_cannot_be_not_applicable(self):
        self.start()
        with self.assertRaises(ValueError):
            self.call("workflow-phase", phase=5, status="NOT_APPLICABLE", reason="Es un arreglo pequeño")
        self.call("workflow-phase", phase=3, status="NOT_APPLICABLE", reason="Contrato ya declara 204")

    def test_real_gates_and_all_phases_close(self):
        self.start()
        self.complete_phases()
        self.assertEqual(self.run_build(), 0)
        self.assertEqual(self.call("workflow-close", acceptance_evidence="target/karate.json"), 0)
        self.assertEqual(self.state()["status"], "LOCAL_VERIFIED")

    def test_failed_build_blocks_even_with_all_phases(self):
        self.start()
        self.complete_phases()
        self.profile["commands"]["build"]["environment"] = {"BACKEND_FAKE_RC": "1"}
        self.save_profile()
        self.assertEqual(self.run_build(), 1)
        self.assertEqual(self.call("workflow-close", acceptance_evidence="target/karate.json"), 1)
        self.assertEqual(self.state()["status"], "BLOCKED")

    def test_changed_code_invalidates_previous_success(self):
        self.start()
        self.complete_phases()
        self.run_build()
        self.call("workflow-close", acceptance_evidence="target/karate.json")
        (self.repo / "builder.py").write_text("changed code", encoding="utf-8")
        self.assertEqual(self.call("workflow-close", acceptance_evidence="target/karate.json"), 1)

    def test_changed_phase_evidence_blocks(self):
        self.start(mode="individual", scope_quote="Solo diagnóstico")
        self.phase(1)
        (self.repo / "docs/engineering/changes/TEST-1/phase-1.md").write_text("Changed")
        self.assertEqual(self.call("workflow-close"), 1)


if __name__ == "__main__":
    unittest.main()
