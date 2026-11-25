"""Verify the revised page turns, modal notices, and Sera's mixed-script exchange."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from scripts import replay_hodram_B65_B70_20261122 as previous
from scripts import verify_hodram_B71_B80_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (71, 15), (72, 48), (72, 51), (72, 55), (72, 58), (72, 69), (72, 73), (74, 58),
    (75, 25), (75, 39), (75, 47), (75, 51), (75, 55),
    (76, 6), (76, 9), (76, 27),
    (77, 12), (77, 33), (77, 36), (77, 17), (77, 42), (77, 45),
    (78, 13), (78, 17), (78, 21), (78, 28), (78, 62), (78, 85),
    (79, 5), (79, 14), (79, 21), (79, 26), (79, 61), (79, 64), (79, 67), (79, 71), (79, 90),
    (80, 18), (80, 26), (80, 37), (80, 41), (80, 53), (80, 69), (80, 83), (80, 109), (80, 123),
)
test_name = ["DK4_MES_B76_R0006", "DK4_MES_B76_R0009", "DK4_MES_B76_R0027"]
PAGE_TURNS = (("DK4_MES_B72_R0055", "DK4_MES_B72_R0058"), ("DK4_MES_B79_R0064", "DK4_MES_B79_R0067"))
ELLIPSIS_ID = "DK4_MES_B80_R0053"


def match_panel(plane, system, image, ident):
    if ident not in display.SYMBOLS and ident != ELLIPSIS_ID:
        return previous.scope["match_panel"](plane, system, image, ident)
    pixels = image.crop((16, 296, 232, 360)).get_flattened_data()
    assert len(pixels) == len(plane) and not system and set(plane) == {0, 1, 15}
    return bytes(value == 1 for value in plane) == bytes(pixel == (0, 8, 0) for pixel in pixels) and (
        bytes(value == 15 for value in plane) == bytes(pixel in {(197, 198, 197), (98, 97, 98)} for pixel in pixels))


producer = checked_text(previous.producer, {
    '"Hodram_B65_B70_FOCUSED_ONLY.nds"': '"Hodram_B71_B80_FOCUSED_ONLY.nds"',
})
page_check = previous.check[previous.check.index('    turn_results = [(h["id"]'):
                            previous.check.index("    final, image =")]
check = checked_text(previous.check, {
    'assert stored == bytes.fromhex(row["source_hex"])[1:]':
        'assert stored == bytes.fromhex(row["source_hex"])[1:].replace(b"\\n", b" ")',
    'len(holds) == len(expected_speech)': 'len(holds) == len(expected_speech) + 2',
    page_check: '''    turn_results = []
    for changed, following in PAGE_TURNS:
        observed_turn = [(h["id"], h["page"], h["frame"]) for h in holds if h["id"] in (changed, following)]
        assert [(ident, page) for ident, page, _ in observed_turn] == [(changed, 1), (changed, 2), (following, 1)]
        assert [frame - observed_turn[0][2] for _, _, frame in observed_turn] == [0, 300, 600]
        turn_results.append(observed_turn)
''',
    'exact_long_speech_and_following=turn_results,': 'exact_two_page_transitions=turn_results,',
    'hodram_B65_B70_gameplay_': 'hodram_B71_B80_gameplay_',
    'assert display.SYMBOLS <= speech_ids':
        'assert display.SYMBOLS <= speech_ids and sum(h["system_FE"] for h in holds) == 4',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::Hodram-war-excerpts", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
