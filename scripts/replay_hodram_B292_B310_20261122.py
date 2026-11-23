"""Replay selected tentatively hidden ruins, map choices, and expedition displays."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B261_B291_20261122 as previous
from scripts import verify_hodram_B292_B310_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (277, 66), (283, 39), (286, 19),
    (292, 12), (292, 16), (293, 9), (293, 12), (293, 20), (293, 63),
    (294, "style28"), (294, 64), (294, 75), (294, "820"), (294, 96), (294, 99), (294, 103),
    (294, 107), (294, 111), (294, 135),
    (296, 37), (296, 40), (296, 70), (297, 213), (297, 232), (297, 243),
    (298, 165), (298, 169), (299, 269), (299, 278),
    (300, 50), (300, "560"), (300, 155), (300, 174), (300, 178), (300, 197), (300, 201),
    (302, "style596"), (302, "1226"), (302, 137), (302, "style1786"), (302, "2272"), (302, 203),
    (302, "style2900"), (303, 12), (304, "576"), (304, 137), (304, 155),
    (305, 13), (305, 31), (304, 30),
    (307, 34), (307, 42), (307, 49), (307, 59), (308, "style8"),
    (309, "style422"), (309, 98), (309, "738"), (309, 174), (309, 178),
    (309, "style1368"), (309, "style1590"), (309, 280), (310, 16),
)
test_name = ["DK4_MES_B294_R0099", "DK4_MES_B294_R0103", "DK4_MES_B294_R0107"]
PAGE_TURN = ("DK4_MES_B300_R0174", "DK4_MES_B300_R0178")
SERA_NAME = ("DK4_MES_B305_R0031", "DK4_MES_B304_R0030")
MENUS = ((294, 2), (300, 2), (302, 2), (302, 2), (304, 2), (309, 3))
MENU_OFFSETS = (820, 560, 1226, 2272, 576, 738)
STYLE_OBJECTS = tuple((block, int(index[5:])) for block, index in SELECTED
                      if isinstance(index, str) and index.startswith("style"))
FALLBACK_NAMES = previous.FALLBACK_NAMES | {214:"Sailor", 218:"Sailor"}
match_panel = previous.match_panel
producer = checked_text(previous.producer, {
    '"Hodram_B261_B291_FOCUSED_ONLY.nds"': '"Hodram_B292_B310_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '{"DK4_MES_B243_R0029", "DK4_MES_B243_R0044", "DK4_MES_B291_R0119", "DK4_MES_B290_R0305"}':
        '{"DK4_MES_B277_R0066", "DK4_MES_B283_R0039", "DK4_MES_B286_R0019", "DK4_MES_B309_R0174"}',
    'hodram_B261_B291_gameplay_': 'hodram_B292_B310_gameplay_',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::ruins-and-expeditions", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
