"""Observe Narvik menus and dialogue after a source-checked test position."""

import sys
from inspect import getsource
from pathlib import Path
from struct import pack_into
from types import FunctionType, SimpleNamespace

from scripts import native_location_fixture_v519 as location
from scripts import native_village_location_v606 as center
from scripts import native_village_water_v607 as terrain
from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import register_tripoli_hodram_warning_20261124 as active
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = replay.ROOT.with_name("narvik_focused_visit_checked_20261124")
HISTORY = Path("work/emulation_v193/village_ui_v609_compact_probe/capture_report.json")
FIRST_PAUSE = 5200
CONTROLLER = ROOT / "controller.jsonl"
NARVIK = 15


def visit_position(arm, raw, index):
    assert index == NARVIK
    release = replay.base.load(active.RELEASE)
    assert center.sha(arm) == release["target_ARM9_sha256"]
    azores = replay.base.load(Path("releases/all_routes_editorial_20261123_azores_wording_candidate/"
                                    "verification/registered_release_verification.json"))
    assert replay.base.digest(azores["candidate"]) == azores["candidate_sha256"]
    from dk4tool.rom.nds import NdsImage
    approved = NdsImage.open(azores["candidate"]).read_file("/__arm9__.bin")

    def qualified_span(current, clean, lo, hi):
        call_site = 0x78788
        if not lo <= call_site < hi:
            return current[lo:hi] == clean[lo:hi]
        return (current[lo:call_site] == clean[lo:call_site]
                and current[call_site:call_site + 4] == approved[call_site:call_site + 4]
                and current[call_site + 4:hi] == clean[call_site + 4:hi])

    derivation = checked_text(getsource(center.relocate), {
        "arm[lo:hi] == clean[lo:hi]": "qualified_span(arm, clean, lo, hi)",
    })
    deployment = vars(center) | dict(ARM_SHA=center.sha(arm), qualified_span=qualified_span)
    exec(compile(derivation, __file__ + "::qualified-coordinate-lookup", "exec"), deployment)
    initial = deployment["relocate"]
    _, proof = initial(arm, raw, index)
    x, y = (value + 16 for value in proof["village_point"])
    water = (x, y - 22)
    queries = FunctionType(terrain.terrain_queries.__code__, vars(terrain) | dict(ROM=release["candidate"]))
    collision = queries(arm, [water])
    assert collision["queries"][0]["collision_free"]
    offset = proof["active_ship"] - center.BASE + 16
    after = bytearray(raw)
    pack_into("<ii", after, offset, *(value * 128 for value in water))
    assert raw[:offset] == after[:offset] and raw[offset + 8:] == after[offset + 8:]
    proof.update(approved_azores_name_call_hex=approved[0x78788:0x7878C].hex(), terrain_proof=collision, expected_selector_point_after_original_update=water,
        after_ship_fixed_point=[value * 128 for value in water], after_RAM_sha256=center.sha(after),
        changes=[dict(address=center.BASE + i, before=raw[i], after=after[i])
                 for i in range(offset, offset + 8) if raw[i] != after[i]])
    return bytes(after), proof


if __name__ == "__main__":
    release = replay.base.load(active.RELEASE)
    driver = checked_text(getsource(replay.main), {
        '"--dump-pause-ram"]': '"--allow-location-fixtures"]',
        'assert not any(value for key, value in receipt.items() if key.startswith("synthetic_"))':
            '''assert len(receipt["synthetic_location_fixtures"]) == 1
    event, = receipt["synthetic_location_fixtures"]
    assert event["village_id"] == NARVIK and event["only_eight_ship_coordinate_bytes_owned"]
    assert not any(value for key, value in receipt.items() if key.startswith("synthetic_") and key != "synthetic_location_fixtures")''',
        'ordinary_controller_inputs=True': 'ordinary_controller_inputs_after_location_setup=True',
        "Path(__file__))": "Path(__file__), CONTROLLER)",
    })
    context = vars(replay) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE, NARVIK=NARVIK,
        CONTROLLER=CONTROLLER, current=SimpleNamespace(RELEASE=active.RELEASE, ROM=Path(release["candidate"])),
        __file__=__file__)
    exec(compile(driver, __file__ + "::source-checked-Narvik", "exec"), context)
    original, relocator = sys.stdin, location.relocate
    commands = GrowingCommands(CONTROLLER)
    try:
        sys.stdin, location.relocate = commands, visit_position
        context["main"]()
    finally:
        sys.stdin, location.relocate = original, relocator
        commands.close()
