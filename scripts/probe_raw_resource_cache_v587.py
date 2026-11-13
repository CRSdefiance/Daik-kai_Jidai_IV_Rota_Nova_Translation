"""Reuse the exact SDK-bridged native cache test with a metadata-only16-bit reader."""

import json
import struct
from pathlib import Path
from types import SimpleNamespace

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_standalone_resource_compatibility_v550 as probe

ROOT = Path("work/analysis/raw_direct_color_v587")


class HeaderExtent:
    @staticmethod
    def from_bytes(data):
        depth, words, height, _, pixels = struct.unpack_from("<5I", data)
        depth &= 255
        assert depth in (4, 8, 16)
        width = words * (4 if depth == 4 else 2 if depth == 8 else 1)
        assert len(data) - pixels == width * height * depth // 8
        return SimpleNamespace(width=width, height=height)


def main():
    original_paths, original_parser = probe.PATHS, probe.PxlImage
    rows = []
    try:
        probe.PATHS, probe.PxlImage = ("/_pxl/logo.pxl",), HeaderExtent
        for fixture in json.loads((ROOT / "fixture_manifest.json").read_text(encoding="utf-8")):
            image = NdsImage.open(fixture["research_ROM"])
            assert sha(image.source.read_bytes()) == fixture["research_ROM_sha256"]
            result = probe.native_compatibility(image)
            assert len(result["cases"]) == 1
            rows.append({"mode": fixture["mode"], "result": result})
    finally:
        probe.PATHS, probe.PxlImage = original_paths, original_parser
    result = {"cases": rows,
              "native_loader_and_copy_helper_sha256": sha(Path(probe.__file__).read_bytes()),
              "metadata_only_decoder_supplies_width_height_not_any_native_result": True,
              "only_SDK_filesystem_operations_bridged": True,
              "no_actual_GPU_or_original_comic_consumer_claim": True,
              "script_sha256": sha(Path(__file__).read_bytes()), "production_ROM_changed": False}
    (ROOT / "native_cache_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"V587: all{len(rows)} exact resource loads/native view copies pass;actual renderer diagnostic remains separate.")


if __name__ == "__main__":
    main()
