"""Verify the three-choice desert menu and Maria's observed Fight branch."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import check_jungle_caves_replay_20261118 as inherited
from scripts import replay_maria_desert_20261118 as game
from scripts.source_locked_derivation_v5118 import checked_text

stage, base, native, parent = game.stage, game.stage.base, game.stage.native, game.stage.parent
MENU = game.ROOT.parent.with_name("research_v1") / game.ROOT.name / "native_menu"
OUTPUT = game.ROOT / "verified.json"
OFFSETS = (376, 474, 532, 558, 740, 776, 862, 888, 2914)
replay = SimpleNamespace(**(vars(game) | {"previous": game.inherited}))

group = checked_text(getsource(inherited.maria_group), {'g["block"] == 259': 'g["block"] == 285'})
menu = checked_text(getsource(inherited.check_menu), {'c["word"] == 0x2100': 'c["word"] == 0x2200'})
cases = checked_text(getsource(inherited.images_for_case), {
    'menu["versions"][-1]': 'menu["menus"][0]["versions"][-1]',
    'menu["native_choice_object_hex"] == records[1090]': 'menu["menus"][0]["target_object_hex"] == records[814]',
    '["Attack!", "Run!"]': '["Fight", "Drive them off", "Run"]',
    'menu_frame = 7275': 'menu_frame = 6650',
    'menu_frame < item["start"] <= 7450] == [7350]': 'menu_frame < item["start"] <= 7100] == [7000]',
    'offset > 1090': 'offset > 814',
    'max(cursor, 7350)': 'max(cursor, 7000)',
    'confirmed_at=7350': 'confirmed_at=7000',
})
source = getsource(inherited.verify)
start = source.index('    attack = images_for_case(')
verify = source[:start] + """    fight = images_for_case("fight", menu, 0, OFFSETS, group, body)
    assert fight["holds"][-1]["source_offset"] == 2914
    base.save(OUTPUT, dict(candidate_sha256=candidate["candidate_sha256"], actual_initialized_Maria=True,
        natural_activation=False, hardware=False, native_menu_proof=str(menu_path),
        native_menu_proof_sha256=base.digest(menu_path), holds=fight["holds"], sheets=fight["sheets"],
        menu_capture=fight["menu_capture"], selected_label=fight["selected_label"], evidence=fight["evidence"]))
    print(f"Verified the Maria Fight branch and {len(fight['holds'])} dialogue holds.", flush=True)
"""
scope = vars(inherited) | globals()
for text, label in ((group, "owner"), (menu, "three-choice"), (cases, "fight-branch"), (verify, "captured-pixels")):
    exec(compile(text, __file__ + "::" + label, "exec"), scope)

if __name__ == "__main__":
    if not MENU.exists():
        scope["check_menu"]()
    scope["verify"]()
