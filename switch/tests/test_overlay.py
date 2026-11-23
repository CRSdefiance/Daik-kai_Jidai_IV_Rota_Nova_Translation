from __future__ import annotations

import importlib.util
import json
from pathlib import Path, PurePosixPath
import shutil
from tempfile import TemporaryDirectory
import unittest

from switch.overlay import digest, rebuild, relative_path
from switch.prepare_release import prepare


class OverlayTests(unittest.TestCase):
    def setUp(self):
        scratch = TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.romfs = self.root / "stock"
        self.romfs.mkdir()
        self.release = self.root / "release"
        self.manifest = self.release / "manifest.json"
        ips = self.release / "patches" / "test.ips"
        ips.parent.mkdir(parents=True)
        ips.write_bytes(b"PATCHEOF")
        self.entry = {
            "output": "exefs/test.ips",
            "patch": "patches/test.ips",
            "patch_sha256": digest(ips),
            "output_sha256": digest(ips),
            "format": "ips",
        }
        self.out = self.root / "overlay"

    def write_manifest(self, *entries):
        self.manifest.write_text(
            json.dumps({"schema": 1, "game_version": "1.0.2", "files": entries}),
            encoding="utf-8",
        )

    def test_rebuild_copies_and_verifies_ips(self):
        self.write_manifest(self.entry)
        self.assertEqual(rebuild(self.romfs, self.out, self.manifest), 1)
        self.assertEqual((self.out / "exefs/test.ips").read_bytes(), b"PATCHEOF")

    def test_rejects_path_traversal(self):
        self.assertEqual(relative_path("romfs/JP/Sc0.dk4", "romfs"),
                         PurePosixPath("romfs/JP/Sc0.dk4"))
        for raw in ("romfs/../bad", "romfs//bad", "romfs\\bad", "/romfs/bad", "romfs/C:bad"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                relative_path(raw, "romfs")

    def test_rejects_case_insensitive_duplicate_outputs(self):
        self.write_manifest(self.entry, self.entry | {"output": "exefs/TEST.ips"})
        with self.assertRaisesRegex(ValueError, "Duplicate overlay path"):
            rebuild(self.romfs, self.out, self.manifest)
        self.assertFalse(self.out.exists())

    def test_changed_stock_is_rejected_before_writing(self):
        (self.romfs / "sample").write_bytes(b"wrong game revision")
        self.write_manifest(
            self.entry | {"output": "romfs/sample", "format": "xdelta", "source_sha256": "0" * 64},
        )
        with self.assertRaisesRegex(ValueError, "stock RomFS v1.0.2"):
            rebuild(self.romfs, self.out, self.manifest)
        self.assertFalse(self.out.exists())

    def test_failed_output_verification_cleans_staging(self):
        self.write_manifest(self.entry | {"output_sha256": "0" * 64})
        with self.assertRaisesRegex(ValueError, "built overlay"):
            rebuild(self.romfs, self.out, self.manifest)
        self.assertFalse(self.out.exists())
        self.assertEqual(list(self.root.glob(".dk4-switch-*")), [])

    @unittest.skipUnless(
        shutil.which("xdelta3") or importlib.util.find_spec("pyxdelta"), "xdelta implementation",
    )
    def test_packaged_delta_reconstructs_overlay(self):
        source = self.romfs / "JP" / "test.dk4"
        source.parent.mkdir()
        source.write_bytes(b"source " * 5000)
        edited = self.out / "romfs" / "JP" / "test.dk4"
        edited.parent.mkdir(parents=True)
        edited.write_bytes(b"source " * 3000 + b"translation" + b"source " * 2000)
        inventory = self.root / "build.json"
        inventory.write_text(json.dumps({
            "switch_version": "1.0.2",
            "title_id": "0100F0E0136BE000",
            "mod_files": {"romfs/JP/test.dk4": digest(edited)},
        }), encoding="utf-8")
        packaged = self.root / "packaged"
        self.assertEqual(prepare(self.romfs, self.out, inventory, packaged, "test"), 1)
        recipe = packaged / "manifest.json"
        entry, = json.loads(recipe.read_text(encoding="utf-8"))["files"]
        self.assertEqual((packaged / entry["patch"]).read_bytes()[4] & 0x04, 0)
        rebuilt = self.root / "rebuilt"
        self.assertEqual(rebuild(self.romfs, rebuilt, recipe), 1)
        self.assertEqual((rebuilt / "romfs/JP/test.dk4").read_bytes(), edited.read_bytes())


if __name__ == "__main__":
    unittest.main()
