"""Match both Maria navigation options and their original results against native pixels."""

from types import SimpleNamespace

from scripts import check_overland_passages_replay_20261118 as previous
from scripts import replay_temple_supply_shipyard_20261118 as current
from scripts import verify_temple_supply_shipyard_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

final = current.stage
prior_root = final.ROOT.with_name("remaining_three_routes_research_v1")
stage = SimpleNamespace(**(vars(final) | {
    "ROOT": prior_root, "ROM": prior_root / final.ROM.name, "PROOF": prior_root / final.PROOF.name,
}))
root = prior_root / current.ROOT.name
replay = SimpleNamespace(**(vars(current) | {
    "ROOT": root, "ROM": root / current.ROM.name, "FIXTURE": root / current.FIXTURE.name, "stage": stage,
}))
base, native, parent = replay.base, replay.native, stage.parent
MENU = display.MENU_ROOT / "SC3_B274_864"
OUTPUT = replay.ROOT / "verified.json"
APPROACH = (106, 156, 180, 334, 838)
COMPASS = APPROACH + (902, 928, 996, 1046, 1398)
INSTINCT = APPROACH + (1082, 1280, 1304, 1340, 1398)


def maria_group(proof):
    return next(g for g in proof["groups"] if (g["route"], g["block"]) == (3, 274))


def visible_selection(photos, menu, index):
    for frame in range(6275, 6124, -25):
        try:
            previous.previous.pixels.selected_option(photos[frame][1], menu, index)
        except AssertionError:
            continue
        return frame
    raise AssertionError("No complete menu hold with the expected selected option")


branch = checked_text(previous.branch, {
    "records[640]": "records[864]",
    '["Pull him out yourself", "Call the others"]': '["Use the compass", "Trust your instincts"]',
    "menu_frame < item[\"start\"] <= 6000] == [5950]": 'menu_frame < item["start"] <= 6350] == [6300]',
    "offset > 640": "offset > 864",
    "max(cursor, 5950)": "max(cursor, 6300)",
    "confirmed_at=5950": "confirmed_at=6300",
})
audit = checked_text(previous.audit, {
    'images_for_case("pull", menu, 0, PULL, group, body)':
        'images_for_case("compass", menu, 0, COMPASS, group, body)',
    'images_for_case("call", menu, 1, CALL, group, body)':
        'images_for_case("hunch", menu, 1, INSTINCT, group, body)',
    '    assert attack["holds"][-2]["id"] == retreat["holds"][-2]["id"]\n': '',
    'hold["source_offset"] == 1018': 'hold["source_offset"] == 996',
    'hold["source_offset"] == 1224': 'hold["source_offset"] == 1280',
    "solo-rescue holds": "compass holds",
    "group-rescue holds": "instinct holds",
})
scope = previous.scope | globals() | {"previous": previous.previous}
for source, label in ((branch, "native-menu-and-body"), (audit, "navigation-holds")):
    exec(compile(source, __file__ + "::" + label, "exec"), scope)

if __name__ == "__main__":
    scope["verify"]()


