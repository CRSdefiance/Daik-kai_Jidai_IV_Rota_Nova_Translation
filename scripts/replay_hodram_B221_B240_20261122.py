"""Replay representative rumor exchanges, pauses, letter signoffs, and choice states."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B201_B220_20261122 as previous
from scripts import verify_hodram_B221_B240_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (218, 68), (218, 75),
    (221, 11), (221, 40), (223, 39), (223, 42), (223, 57), (223, 65),
    (224, 12), (224, "138"), (224, 34), (224, 47), (224, 61), (224, 64),
    (225, 5), (225, 9), (225, 12), (225, 40),
    (226, "style8"), (226, 31), (226, 48), (226, 56),
    (227, 11), (227, 18), (227, 54),
    (228, 5), (228, 9), (228, 16), (228, 37),
    (229, 44), (229, 57), (230, 16), (230, 28),
    (231, 5), (231, 28), (231, 46),
    (232, 5), (232, 34), (232, 38), (232, 59),
    (233, 5), (233, 24), (233, 42), (233, 61),
    (234, 20), (234, 35), (236, 27), (236, 37),
    (237, 5), (237, 9), (237, 19), (237, 64),
    (238, "style8"), (238, 35), (238, 50),
    (239, "style8"), (239, 49), (239, 64), (239, 70),
    (240, 18), (240, 28), (240, 38),
)
test_name = ["DK4_MES_B225_R0005", "DK4_MES_B225_R0009", "DK4_MES_B225_R0012"]
PAGE_TURN = ("DK4_MES_B224_R0061", "DK4_MES_B224_R0064")
SERA_NAME = (writer.SIGNATURE_ID, "DK4_MES_B218_R0075")
MENUS, MENU_OFFSETS = ((224, 2),), (138,)
match_panel = previous.match_panel
producer = checked_text(previous.producer, {
    '"Hodram_B201_B220_FOCUSED_ONLY.nds"': '"Hodram_B221_B240_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '{"DK4_MES_B208_R0071", "DK4_MES_B209_R0020", "DK4_MES_B215_R0040", "DK4_MES_B218_R0087"}':
        '{writer.SIGNATURE_ID, "DK4_MES_B225_R0005", "DK4_MES_B227_R0011", "DK4_MES_B237_R0005"}',
    'hodram_B201_B220_gameplay_': 'hodram_B221_B240_gameplay_',
    '((213, 8), (213, 702), (218, 8))': '((226, 8), (238, 8), (239, 8))',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::rumors-and-letters", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
