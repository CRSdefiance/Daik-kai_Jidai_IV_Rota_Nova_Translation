"""Replay selected tentatively hidden ruins, map choices, and expedition displays."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B292_B310_20261122 as previous
from scripts import verify_hodram_B311_B324_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (294, 58), (301, 21), (302, "style1786"), (302, "2272"), (309, "style24"),
    (311, "style654"), (311, "style838"), (311, "1086"), (311, "1306"),
    (311, 180), (311, 193), (311, "style1578"), (311, 284),
    (312, 6), (312, 10), (312, 16),
    (313, "style546"), (313, "782"), (313, "style856"), (313, "style1252"),
    (313, "style1756"), (313, 228), (313, 236), (313, 275), (313, 279), (313, 336),
    (314, 10), (314, 30), (314, 39), (314, 43), (315, 10), (315, 26),
    (316, "674"), (316, "934"), (316, 254), (316, 258),
    (317, 93), (317, "764"), (317, 116), (317, 127), (317, 180),
    (318, 44), (318, 66), (318, 75), (318, 94), (318, 109), (318, 114), (318, 117), (318, 125),
    (319, 13), (319, 25), (320, 16), (320, 24), (321, 14), (322, 71), (322, 76), (323, 10),
    (324, 13), (324, 16), (324, 24), (324, 58), (324, 65), (324, 105), (324, 109), (324, 133), (324, 148),
)
test_name = ["DK4_MES_B318_R0109", "DK4_MES_B318_R0114", "DK4_MES_B318_R0117"]
PAGE_TURN = ("DK4_MES_B318_R0109", "DK4_MES_B318_R0114")
SERA_NAME = ("DK4_MES_B324_R0013", "DK4_MES_B324_R0016")
MENUS = ((302, 2), (311, 2), (311, 2), (313, 3), (316, 2), (316, 2), (317, 2))
MENU_OFFSETS = (2272, 1086, 1306, 782, 674, 934, 764)
STYLE_OBJECTS = tuple((block, int(index[5:])) for block, index in SELECTED
                      if isinstance(index, str) and index.startswith("style"))
FALLBACK_NAMES = previous.FALLBACK_NAMES | {209:"Sailor"}
match_panel = previous.match_panel
producer = checked_text(previous.producer, {
    '"Hodram_B292_B310_FOCUSED_ONLY.nds"': '"Hodram_B311_B324_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '{"DK4_MES_B277_R0066", "DK4_MES_B283_R0039", "DK4_MES_B286_R0019", "DK4_MES_B309_R0174"}':
        '{"DK4_MES_B294_R0058", "DK4_MES_B301_R0021", "DK4_MES_B313_R0228", "DK4_MES_B318_R0109", "DK4_MES_B324_R0058"}',
    'hodram_B292_B310_gameplay_': 'hodram_B311_B324_gameplay_',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::ruins-and-expeditions", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
