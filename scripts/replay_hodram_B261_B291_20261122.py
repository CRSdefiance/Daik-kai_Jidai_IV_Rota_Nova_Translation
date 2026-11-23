"""Replay the figurehead, guild, audience, and expedition display changes."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B241_B260_20261122 as previous
from scripts import verify_hodram_B261_B291_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (243, 29), (243, 36), (243, 44), (243, "674"), (243, 163),
    (264, 5), (264, 9), (264, 12), (264, 32), (264, 41),
    (265, 9), (265, 13), (265, 17), (265, 21), (265, 26), (265, 49),
    (266, 9), (267, 5), (267, 8), (267, 59),
    (271, 8), (271, 12), (271, 19), (271, 23),
    (274, 8), (274, 11), (274, 19), (274, 22),
    (280, 5), (280, 8), (280, 61),
    (282, 6), (282, 19), (283, 9), (283, 19), (283, 56), (283, 85), (283, 93), (283, 97),
    (286, 5), (286, 43), (286, 75), (287, 61), (287, 96), (287, 108), (287, 125),
    (290, "style24"), (290, "style328"), (290, 92), (290, 96), (290, "876"), (290, "style1166"),
    (290, "1876"), (290, "style2398"), (290, 305), (290, "style3300"),
    (291, 49), (291, 70), (291, 77), (291, 100), (291, "1114"),
    (291, 119), (291, "style1246"), (291, 152), (291, "style2194"), (291, 225),
)
test_name = ["DK4_MES_B264_R0005", "DK4_MES_B264_R0009", "DK4_MES_B264_R0012"]
PAGE_TURN = ("DK4_MES_B266_R0009", "DK4_MES_B267_R0005")
SERA_NAME = ("DK4_MES_B243_R0029", "DK4_MES_B243_R0036")
MENUS = ((243, 2), (290, 3), (290, 2), (291, 2))
MENU_OFFSETS = (674, 876, 1876, 1114)
STYLE_OBJECTS = tuple((block, int(index[5:])) for block, index in SELECTED
                      if isinstance(index, str) and index.startswith("style"))
FALLBACK_NAMES = {207:"Hodram Bergstrom", 208:"Sailor", 211:"Sailor", 215:"Sailor", 216:"Sailor"}
match_panel = previous.match_panel
producer = checked_text(previous.producer, {
    '"Hodram_B241_B260_FOCUSED_ONLY.nds"': '"Hodram_B261_B291_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    'panel.complete_mask(name_font, "Sailor" if item["word"] == 0x4100 else row["speaker"], image, 16, 277, town.INKS[1])':
        'panel.complete_mask(name_font, FALLBACK_NAMES.get(row["source_selector"], row["speaker"]), image, 16, 277, town.INKS[1])',
    '{writer.CONVOY_ID, "DK4_MES_B252_R0009", "DK4_MES_B252_R0012", "DK4_MES_B259_R0049"}':
        '{"DK4_MES_B243_R0029", "DK4_MES_B243_R0044", "DK4_MES_B291_R0119", "DK4_MES_B290_R0305"}',
    'hodram_B241_B260_gameplay_': 'hodram_B261_B291_gameplay_',
    'len(styles) == 2': 'len(styles) == len(STYLE_OBJECTS)',
    '((252, 340), (252, 822))': 'STYLE_OBJECTS',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::guild-forest-and-cave", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
