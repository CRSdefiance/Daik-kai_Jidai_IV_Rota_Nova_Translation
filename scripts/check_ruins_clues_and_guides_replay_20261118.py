"""Check both map-guide menu returns against their native captions and body planes."""

from inspect import getsource
from types import SimpleNamespace

from scripts import check_jungle_caves_replay_20261118 as inherited
from scripts import replay_ruins_clues_and_guides_20261118 as replay
from scripts import verify_ruins_clues_and_guides_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, parent = replay.stage, replay.base, replay.native, replay.stage.parent
MENU = display.MENU
PRIOR = stage.ROOT.with_name("research_v2")
CASES = PRIOR / replay.ROOT.name
OUTPUT = CASES / "verified.json"
COMMON = (516, 560, 584, 678, 702)
PUSH = COMMON + (748, 1156, 1224, 1414)
LOOK = COMMON + (1284, 1314, 1414)


group = checked_text(getsource(inherited.maria_group), {'g["block"] == 259': 'g["block"] == 264'})
cases = checked_text(getsource(inherited.images_for_case), {
    'replay.previous.quest.prior': 'replay.previous.previous.quest.prior',
    'records[1090]': 'records[716]',
    '["Attack!", "Run!"]': '["Push through", "Look around"]',
    'menu_frame = 7275': 'menu_frame = 6250 if wanted_index == 0 else 6200',
    'menu_frame < item["start"] <= 7450] == [7350]': 'menu_frame < item["start"] <= 6450] == [6300]',
    'offset > 1090': 'offset > 716',
    'max(cursor, 7350)': 'max(cursor, 6300)',
    'confirmed_at=7350': 'confirmed_at=6300',
})
verify = checked_text(getsource(inherited.verify), {
    'replay.previous.quest.prior': 'replay.previous.previous.quest.prior',
    'attack = images_for_case("attack", menu, 0, ATTACK, group, body)':
        'push = images_for_case("push", menu, 0, PUSH, group, body)',
    'retreat = images_for_case("run", menu, 1, RETREAT, group, body)':
        'look = images_for_case("look", menu, 1, LOOK, group, body)',
    '    assert attack["holds"][-2]["id"] == retreat["holds"][-2]["id"]\n': '',
    'attack["holds"][-1]["id"] == retreat["holds"][-1]["id"]':
        'push["holds"][-1]["id"] == look["holds"][-1]["id"]',
    'hold["source_offset"] == 2144 for hold in attack["holds"]':
        'hold["source_offset"] == 1224 for hold in push["holds"]',
    'hold["source_offset"] == 2186 for hold in retreat["holds"]':
        'hold["source_offset"] == 1284 for hold in look["holds"]',
    'cases=[attack, retreat]': 'cases=[push, look]',
    '''print(f"Matched {len(attack['holds'])} Attack holds and {len(retreat['holds'])} Run holds.", flush=True)''':
        '''print(f"Matched {len(push['holds'])} Push through holds and {len(look['holds'])} Look around holds.", flush=True)''',
})
prior_stage = SimpleNamespace(**(vars(stage) | {"ROOT": PRIOR, "ROM": PRIOR / stage.ROM.name,
                                                "PROOF": PRIOR / stage.PROOF.name}))
prior_replay = SimpleNamespace(**(vars(replay) | {"ROOT": CASES, "ROM": CASES / replay.ROM.name,
    "FIXTURE": CASES / replay.FIXTURE.name, "stage": prior_stage}))
scope = vars(inherited) | globals() | {"replay": prior_replay, "stage": prior_stage}
for source, label in ((group, "group"), (cases, "branch"), (verify, "capture-comparison")):
    exec(compile(source, __file__ + "::" + label, "exec"), scope)


if __name__ == "__main__":
    scope["verify"]()
