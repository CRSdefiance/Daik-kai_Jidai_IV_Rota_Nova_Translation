"""Observe the opening fight, the rescue, the elegy, and Aziza's decision."""

from argparse import ArgumentParser
from inspect import getsource
from types import SimpleNamespace

from scripts import replay_hodram_opening_20261122 as previous
from scripts import verify_hodram_B0_B23_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (0, 9), (2, 6), (3, 6), (3, 13), (3, 20), (3, 26), (3, 36), (3, 47), (3, 51),
    (4, 52), (5, 5), (6, 8), (9, 9), (10, 11), (11, 17), (12, 12),
    (15, 56), (15, 60), (15, 64), (15, 77), (15, 141), (15, 164), (15, 168), (15, 171),
    (15, 208), (15, 212), (15, 215), (16, 25), (16, 32), (16, 35), (16, 39), (16, 42),
    (17, 6), (17, 41), (17, 49), (17, 60), (17, 95), (17, 125), (17, 146), (17, 160), (17, 171),
    (17, 200), (17, 204), (17, 211), (17, 218), (17, 229), (17, 236), (17, 240),
    (17, 251), (17, 259), (17, 262), (17, 266), (17, 269), (17, 272), (19, 41), (23, 12),
)
producer = checked_text(getsource(previous.replay), {
    '"Hodram_B24_B53_FOCUSED_ONLY.nds"': '"Hodram_B0_B23_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    'assert [(m["block"], m["highlight"]) for m in menus] == [(49, 0), (49, 1), (52, 0), (52, 1)]':
        'assert not menus',
    '["DK4_MES_B42_R0093", "DK4_MES_B42_R0096", "DK4_MES_B42_R0100"]':
        '["DK4_MES_B15_R0164", "DK4_MES_B15_R0168", "DK4_MES_B15_R0171"]',
    '    final, image = town.read_frame': '''    elegy = [(h["id"], h["frame"]) for h in holds if h["id"] in ELEGY]
    assert [a for a, _ in elegy] == ELEGY
    assert [f - elegy[0][1] for _, f in elegy] == [0, 300, 600]
    final, image = town.read_frame''',
    'len(holds) == len(expected_speech) + 1': 'len(holds) == len(expected_speech)',
    'sum("_STYLE_" in hold["id"] for hold in holds) == 1': 'not any("_STYLE_" in hold["id"] for hold in holds)',
    'hodram_B24_B53_gameplay_': 'hodram_B0_B23_gameplay_',
    'initialized_excerpts=True, natural_activation=False,': 'initialized_excerpts=True, natural_activation=False, exact_elegy_holds=elegy,',
})
ELEGY = [f"DK4_MES_B16_R{index:04d}" for index in (32, 35, 39)]
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::Hodram-opening-excerpts", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
