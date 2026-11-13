"""Authorized coordinate-only fixture runner for the source-owned V610 layout."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_portrait_wrap import transform as portrait
from dk4tool.patch.village_ui_compact import transform as ui
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts.native_village_water_v607 import relocate as source_relocate


def relocate(arm, raw, village):
    source = NdsImage.open("out/all_routes_combined_v604_candidate.nds").read_file("/__arm9__.bin")
    inherited, _ = portrait(source)
    route = NdsImage.open("out/all_routes_combined_v608_candidate.nds").read_file("/data/SC2.DK4")
    expected, _, _ = ui(inherited, route, json.loads(Path("translations/village_ui_manuscript_v1.json").read_text(encoding="utf-8")))
    assert arm == expected
    after, proof = source_relocate(source, raw, village)
    proof["actual_candidate_ARM9_sha256"] = sha(arm)
    proof["original_location_terrain_discovery_and_menu_action_code_preserved"] = True
    return after, proof


def main():
    original = location.relocate
    location.relocate = relocate
    try:
        harness.main()
    finally:
        location.relocate = original


if __name__ == "__main__":
    main()
