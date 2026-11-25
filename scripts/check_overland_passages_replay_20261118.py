"""Verify the two original quicksand branches against exact native display planes."""

from inspect import getsource

from scripts import check_jungle_caves_replay_20261118 as previous
from scripts import replay_overland_passages_20261118 as replay
from scripts import verify_overland_passages_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

stage, base, native, parent = replay.stage, replay.base, replay.native, replay.stage.parent
MENU = display.MENU_ROOT / "SC3_B269_640"
OUTPUT = replay.ROOT / "verified.json"
APPROACH = (392, 552, 592, 606)
ARRIVAL = (1266, 1584)
PULL = APPROACH + (692, 740, 1018) + ARRIVAL
CALL = APPROACH + (1050, 1104, 1224) + ARRIVAL


def maria_group(proof):
    return next(g for g in proof["groups"] if (g["route"], g["block"]) == (3, 269))


def visible_selection(photos, menu, index):
    for frame in range(5925, 5774, -25):
        try:
            previous.pixels.selected_option(photos[frame][1], menu, index)
        except AssertionError:
            continue
        return frame
    raise AssertionError("No complete menu hold with the expected selected option")


branch = checked_text(getsource(previous.images_for_case), {
    "replay.previous.quest.prior": "previous.replay.previous.quest.prior",
    "records[1090]": "records[640]",
    '["Attack!", "Run!"]': '["Pull him out yourself", "Call the others"]',
    "menu_frame = 7275": "menu_frame = visible_selection(photos, menu, wanted_index)",
    "menu_frame < item[\"start\"] <= 7450] == [7350]": 'menu_frame < item["start"] <= 6000] == [5950]',
    "offset > 1090": "offset > 640",
    "max(cursor, 7350)": "max(cursor, 5950)",
    "confirmed_at=7350": "confirmed_at=5950",
})
audit = checked_text(getsource(previous.verify), {
    "replay.previous.quest.prior": "previous.replay.previous.quest.prior",
    'plane = fe(raw)["physical"]': 'plane = fe(raw.replace(b"FI", b"Maria"))["physical"]',
    'attack = images_for_case("attack", menu, 0, ATTACK, group, body)':
        'attack = images_for_case("pull", menu, 0, PULL, group, body)',
    'retreat = images_for_case("run", menu, 1, RETREAT, group, body)':
        'retreat = images_for_case("call", menu, 1, CALL, group, body)',
    'hold["source_offset"] == 2144': 'hold["source_offset"] == 1018',
    'hold["source_offset"] == 2186': 'hold["source_offset"] == 1224',
    "Attack holds": "solo-rescue holds",
    "Run holds": "group-rescue holds",
})
scope = vars(previous) | globals()
for source, label in ((branch, "original-branch-display"), (audit, "quicksand-holds")):
    exec(compile(source, __file__ + "::" + label, "exec"), scope)

if __name__ == "__main__":
    scope["verify"]()
