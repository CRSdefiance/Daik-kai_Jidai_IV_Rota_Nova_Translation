"""V608 research runner: same source terrain/location contract, new text layout."""

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_portrait_wrap import transform
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts.native_village_water_v607 import relocate as original_relocate


def relocate(arm, raw, village):
    original = NdsImage.open("out/all_routes_combined_v604_candidate.nds").read_file("/__arm9__.bin")
    expected, _ = transform(original)
    assert arm == expected
    # All getters, the complete original location/discovery logic and world map
    # are exact V604. Only village text and its staged storage metadata differ.
    after, proof = original_relocate(original, raw, village)
    proof["actual_candidate_ARM9_sha256"] = sha(arm)
    proof["V607_source_getters_and_terrain_identical_in_V608"] = True
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
