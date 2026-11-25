"""Observe Sera's first words, Espinosa's admission, and Manuel's page turn."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B0_B23_20261122 as previous
from scripts import verify_hodram_B54_B60_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (54, 6), (54, 14), (54, 18), (55, 6), (56, 7), (56, 10), (56, 13),
    (57, 7), (57, 15), (57, 19), (57, 23), (57, 31), (57, 35),
    (58, 18), (58, 39), (58, 42), (58, 46), (58, 93), (58, 97), (58, 105),
    (58, 108), (58, 116), (58, 120), (58, 124), (58, 127), (58, 137), (58, 141),
    (58, 168), (58, 172), (58, 175), (58, 190), (58, 194), (58, 202), (58, 206),
    (58, 224), (58, 239), (59, 13), (59, 23), (59, 26), (59, 30),
    (60, 5), (60, 8), (60, 12), (60, 15), (60, 19), (60, 26), (60, 29), (60, 33), (60, 36),
)
producer = checked_text(previous.producer, {
    '"Hodram_B0_B23_FOCUSED_ONLY.nds"': '"Hodram_B54_B60_FOCUSED_ONLY.nds"',
})
test_name = ["DK4_MES_B56_R0007", "DK4_MES_B56_R0010", "DK4_MES_B56_R0013"]
PAGE_TURN = "DK4_MES_B60_R0012"
page_check = previous.check[previous.check.index("    elegy ="):previous.check.index("    final, image =")]
check = checked_text(previous.check, {
    '["DK4_MES_B15_R0164", "DK4_MES_B15_R0168", "DK4_MES_B15_R0171"]': "test_name",
    page_check: '''    relief = "DK4_MES_B60_R0015"
    turn_results = [(h["id"], h["page"], h["frame"]) for h in holds if h["id"] in (PAGE_TURN, relief)]
    assert [(ident, page) for ident, page, _ in turn_results] == [(PAGE_TURN, 1), (PAGE_TURN, 2), (relief, 1)]
    assert [frame - turn_results[0][2] for _, _, frame in turn_results] == [0, 300, 600]
''',
    'len(holds) == len(expected_speech)': 'len(holds) == len(expected_speech) + 1',
    'exact_elegy_holds=elegy,': 'exact_turn_and_following=turn_results,',
    'hodram_B0_B23_gameplay_': 'hodram_B54_B60_gameplay_',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::Hodram-linked-excerpts", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
