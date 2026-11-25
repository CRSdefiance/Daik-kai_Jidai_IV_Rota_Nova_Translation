"""Replay the representative convoy, figurehead, reward, and puzzle displays."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B221_B240_20261122 as previous
from scripts import verify_hodram_B241_B260_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (238, 35), (238, 38),
    (241, 12), (241, 44), (241, 62),
    (242, 18), (242, 36), (242, 57), (242, 79), (242, 84),
    (243, 14), (243, 36), (243, 64), (243, "674"), (243, 143), (243, 163),
    (244, 18), (245, 7), (246, 15), (247, 6), (247, 17),
    (248, 9), (248, 16), (249, 18), (250, 10), (250, 34),
    (251, 9), (251, "432"), (251, 53), (251, 64), (251, 67), (251, 70),
    (251, 85), (251, 89), (251, 110), (251, 113), (251, 117),
    (252, 6), (252, 9), (252, 12), (252, "270"), (252, "style340"), (252, 53),
    (252, "style822"), (252, 106), (252, 112), (252, 130), (252, 134), (252, 138),
    (252, 145), (252, "1606"), (252, 160), (252, 168), (252, 174), (252, 184), (252, 195), (252, 207),
    (253, 7), (254, 9), (256, 12), (257, 6), (258, 19), (258, 23), (258, 27),
    (259, 13), (259, 21), (259, 49), (259, 86), (259, 94), (260, 17),
)
test_name = ["DK4_MES_B258_R0019", "DK4_MES_B258_R0023", "DK4_MES_B258_R0027"]
PAGE_TURN = (writer.CONVOY_ID, "DK4_MES_B238_R0038")
SERA_NAME = ("DK4_MES_B251_R0064", "DK4_MES_B251_R0067")
MENUS = ((243, 2), (251, 2), (252, 3), (252, 2))
MENU_OFFSETS = (674, 432, 270, 1606)
match_panel = previous.match_panel
producer = checked_text(previous.producer, {
    '"Hodram_B221_B240_FOCUSED_ONLY.nds"': '"Hodram_B241_B260_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '{writer.SIGNATURE_ID, "DK4_MES_B225_R0005", "DK4_MES_B227_R0011", "DK4_MES_B237_R0005"}':
        '{writer.CONVOY_ID, "DK4_MES_B252_R0009", "DK4_MES_B252_R0012", "DK4_MES_B259_R0049"}',
    'hodram_B221_B240_gameplay_': 'hodram_B241_B260_gameplay_',
    'len(styles) == 3': 'len(styles) == 2',
    '((226, 8), (238, 8), (239, 8))': '((252, 340), (252, 822))',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::ruins-and-guild", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
