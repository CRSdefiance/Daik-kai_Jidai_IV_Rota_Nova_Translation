"""Replay representative item encounters, letters, menus, and the parrot dialogue."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B131_B150_20261122 as previous
from scripts import verify_hodram_B201_B220_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (201, 14), (201, 21), (201, "230"), (201, 85), (201, 101), (201, 109),
    (202, 10), (202, 14), (202, 18), (202, 22), (202, 30), (202, 84),
    (203, 18), (203, 21), (203, 36), (203, 51),
    (204, 5), (204, 17), (204, 33), (204, 65), (204, 72),
    (205, 19), (205, 28), (205, 46), (205, "844"), (205, 78), (205, 81), (205, 101),
    (206, 55), (206, 68), (206, 72), (207, 35), (207, 75), (207, 78), (207, 81),
    (208, 13), (208, 16), (208, 28), (208, 54), (208, 61), (208, 65), (208, 68), (208, 71),
    (209, 5), (209, 17), (209, 20), (209, 24), (209, 28), (209, 32), (209, 51), (209, 63),
    (210, 37), (210, 70), (210, 73), (210, "956"), (210, 99), (210, "1126"), (210, 121),
    (211, 29), (211, 36), (211, 40), (212, 59), (212, 70), (212, 90),
    (213, "style8"), (213, 27), (213, 30), (213, 33), (213, "style702"), (213, 71),
    (214, 15), (214, 23), (215, 13), (215, 24), (215, 40), (215, 46),
    (216, "64"), (216, 32), (216, "230"), (216, 58), (216, 78),
    (217, 38), (217, 42), (217, 59), (218, "style8"), (218, 44), (218, 68), (218, 87),
    (219, 19), (219, 29), (220, 12), (220, 16),
)
test_name = ["DK4_MES_B209_R0017", "DK4_MES_B209_R0020", "DK4_MES_B209_R0024"]
PAGE_TURN = ("DK4_MES_B213_R0030", "DK4_MES_B213_R0033")
SERA_NAME = ("DK4_MES_B209_R0017", "DK4_MES_B209_R0020")
MENUS = ((201, 3), (205, 2), (210, 2), (210, 2), (216, 2), (216, 3))
MENU_OFFSETS = (230, 844, 956, 1126, 64, 230)
match_panel = previous.match_panel
producer = checked_text(previous.producer, {
    '"Hodram_B131_B150_FOCUSED_ONLY.nds"': '"Hodram_B201_B220_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    'for block in MENU_BLOCKS for slot in range(2)': 'for block, count in MENUS for slot in range(count)',
    '{"DK4_MES_B143_R0033","DK4_MES_B143_R0079","DK4_MES_B143_R0087","DK4_MES_B137_R0074"}':
        '{"DK4_MES_B208_R0071", "DK4_MES_B209_R0020", "DK4_MES_B215_R0040", "DK4_MES_B218_R0087"}',
    'hodram_B131_B150_gameplay_': 'hodram_B201_B220_gameplay_',
    'assert len(styles) == 1 and styles[0].startswith("SC1_B133_STYLE_10_")':
        'assert len(styles) == 3 and all(ident.startswith(f"SC1_B{block}_STYLE_{offset}_")\n'
        '        for ident, (block, offset) in zip(styles, ((213, 8), (213, 702), (218, 8)), strict=True))',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::encounters-and-letters", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
