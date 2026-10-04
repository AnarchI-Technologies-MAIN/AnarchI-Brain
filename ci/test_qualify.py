"""Adversarial tests for the CI invoking handoff (not historical corpus edits)."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("ci_qualify", Path(__file__).with_name("qualify.py"))
q = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(q)


class QualificationBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="brain-ci-regression-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.base = Path(cls.temporary.name)
        cls.candidate = cls.base / "candidate"
        cls.source_status = q.git(q.ROOT, "status", "--porcelain")
        cls.source_head = q.git(q.ROOT, "rev-parse", "HEAD")
        cls.manifest = q.prepare_candidate(q.ROOT, cls.candidate)

    def snapshot(self, mode="false"):
        temporary = tempfile.TemporaryDirectory(prefix="brain-ci-checkout-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / "repo"
        q.checkout_candidate(self.candidate, root, mode, self.manifest)
        return root

    def test_full_manifest_survives_both_real_checkout_modes(self):
        for mode in ("false", "true"):
            with self.subTest(autocrlf=mode):
                root = self.snapshot(mode)
                self.assertEqual(q.git(root, "config", "core.autocrlf").strip(), mode.encode())
                q.verify_checkout(root, self.manifest)
                self.assertEqual(len(self.manifest["bound_files"]), self.manifest["bound_file_count"])

    def test_launcher_tampering_never_executes_in_either_python_mode(self):
        root = self.snapshot()
        marker = root / "unverified-executed"
        (root / "qualify_m01_r3.py").write_text(
            "from pathlib import Path\nPath(__file__).with_name('unverified-executed').touch()\n",
            encoding="utf-8")
        for optimized in (False, True):
            with self.subTest(optimized=optimized):
                result = subprocess.run(q.child_command(root, self.manifest, optimized, "probe-code"),
                                        capture_output=True, text=True, timeout=30)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("LAUNCHER_IDENTITY_MISMATCH", result.stderr)
                self.assertFalse(marker.exists())

    def test_nonlauncher_bound_file_change_rejects(self):
        root = self.snapshot()
        name = "qualification/m01_r3/model.py"
        path = root / name
        path.write_bytes(path.read_bytes() + b"\n# altered\n")
        with self.assertRaisesRegex(ValueError, "SOURCE_DIGEST_MISMATCH:" + name):
            q.verify_checkout(root, self.manifest)

    def test_changed_manifest_cannot_supply_new_launcher_pin(self):
        root = self.snapshot()
        manifest = dict(self.manifest)
        manifest["bound_files"] = dict(manifest["bound_files"])
        manifest["bound_files"]["qualify_m01_r3.py"] = "0" * 64
        (root / q.MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Historical R3 manifest changed"):
            q.read_manifest(root)

    def test_publication_preimages_match_original_pin(self):
        for name, preserved in q.PREIMAGES.items():
            self.assertEqual(hashlib.sha256(q.plain_bytes(self.candidate, preserved)).hexdigest(),
                             self.manifest["bound_files"][name])
            self.assertEqual(q.plain_bytes(self.candidate, name),
                             q.plain_bytes(self.candidate, preserved))

    def test_tampered_preimage_rejected_before_candidate_staging(self):
        root = self.snapshot()
        (root / q.PREIMAGES["README.md"]).write_bytes(b"forged historical README")
        q.git(root, "add", "--all", "--force", ".")
        q.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
              "-c", "commit.gpgsign=false", "commit", "-m", "Tamper fixture")
        target = root.parent / "tampered-candidate"
        with self.assertRaisesRegex(ValueError, "Historical preimage mismatch:README.md"):
            q.prepare_candidate(root, target)
        self.assertFalse((target / ".git").exists())

    def test_autocrlf_conversion_without_bound_attributes_is_detected(self):
        root = self.snapshot()
        name = "qualification/m01_r3/model.py"
        original = (root / name).read_bytes()
        (root / ".gitattributes").unlink()
        q.git(root, "add", "--all", "--force", ".")
        q.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
              "-c", "commit.gpgsign=false", "commit", "-m", "Remove checkout policy fixture")
        target = root.parent / "converted"
        with self.assertRaises((ValueError, FileNotFoundError)):
            q.checkout_candidate(root, target, "true", self.manifest)
        self.assertNotEqual((target / name).read_bytes(), original)

    def test_source_checkout_and_index_remain_unchanged(self):
        self.assertEqual(q.git(q.ROOT, "status", "--porcelain"), self.source_status)
        self.assertEqual(q.git(q.ROOT, "rev-parse", "HEAD"), self.source_head)


if __name__ == "__main__":
    unittest.main()
