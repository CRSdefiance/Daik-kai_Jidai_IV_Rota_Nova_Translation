"""Replay the revised dispatch, choice, letter and map text on the native consumer."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_rafael_palace_and_alliance_20261121 as reuse
from scripts import replay_rafael_rescue_and_lessons_20261121 as precedent
from scripts import verify_rafael_homeland_and_maps_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, PATH = display.stage, display.base, display.native, display.PATH
ROOT = stage.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
SELECTED = (
    (151, 330), (151, 334), (151, 337), (152, 144), (155, 39), (155, 94), (159, 47), (159, 118),
)

producer = checked_text(precedent.producer, {
    'groups[139]["commands"]': 'groups[160]["commands"]',
    "Rafael_Rescue_And_Lessons_RESEARCH_ONLY.nds": "Rafael_Homeland_And_Maps_RESEARCH_ONLY.nds",
})
schedule = checked_text(precedent.schedule, {
    '{127: 1, 136: 1}[command["fixture_block"]]': '{154: 1}[command["fixture_block"]]',
})
checker = checked_text(precedent.check, {
    '[(127, 0), (127, 1), (136, 0), (136, 1)]': '[]',
    '    assert sum(h["id"].startswith(("SC0_B121_STYLE_", "SC0_B125_STYLE_")) for h in holds) == 4\n': '',
    '["DK4_MES_B127_R0029", "DK4_MES_B127_R0049", "DK4_MES_B127_R0054"]':
        '["DK4_MES_B151_R0330", "DK4_MES_B151_R0334", "DK4_MES_B151_R0337"]',
    '[0, 900, 1200]': '[0, 300, 600]',
    'if m["block"] in (127, 136)': 'if m["block"] == 154',
    'rafael_rescue_gameplay_': 'refined_homeland_gameplay_',
    ' and four highlights across the sailing and Guiding Staff menus': ' across the final homeland excerpts',
})
scope = precedent.scope | globals() | {"prior": precedent.scope["prior"]}
for code in (producer, schedule, checker):
    exec(compile(code, __file__ + "::gameplay", "exec"), scope)

merge = checked_text(getsource(reuse.verify_and_reuse_prior_play), {
    'len(previous["menus"]) == len(menu_ids) == 6': 'len(previous["menus"]) == len(menu_ids) == 2',
    'reused_menu_highlights=6,': 'reused_menu_highlights=2,',
    'and six exact menu highlights': 'and two exact menu highlights',
    '    observed = exact | renewed': '''    observed = exact | renewed
    message_turn = previous["exact_sampled_page_turn"]
    assert [r[0] for r in message_turn] == ["DK4_MES_B159_R0126", "DK4_MES_B159_R0129", "DK4_MES_B159_R0132"]
    assert {r[0] for r in message_turn} <= exact
    current["exact_reused_message_turn"] = message_turn''',
})
exec(compile(merge, __file__ + "::exact-reuse", "exec"), globals())


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    if parser.parse_args().action == "replay":
        scope["replay"]()
    else:
        verify_and_reuse_prior_play()
