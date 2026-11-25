"""Replay the speakers, menus, page turns and original comic glyphs in context."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B151_B160_20261122 as previous
from scripts import verify_hodram_B161_B170_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (161,18), (161,26), (161,29), (161,38), (161,41), (161,45), (161,56),
    (162,11), (162,24), (162,71), (162,104),
    (163,5), (163,30), (164,6), (166,5), (166,17), (166,56), (166,113), (166,189),
    (167,86), (167,"1308"), (167,122), (167,125),
    (168,93), (168,96), (168,104), (168,124), (168,127), (168,130),
    (168,161), (168,166), (168,170), (168,191), (168,195), (168,209), (168,225),
    (168,296), (168,304), (168,308), (168,317), (168,329),
    (169,20), (169,24), (169,"356"), (169,108), (169,111), (169,114), (169,117), (169,143), (169,211),
    (170,13), (170,72), (170,"894"), (170,109), (170,"1314"), (170,149),
    (170,164), (170,168), (170,184), (170,188), (170,203), (170,207),
)
test_name = ["DK4_MES_B168_R0161", "DK4_MES_B168_R0166", "DK4_MES_B168_R0170"]
PAGE_TURN = ("DK4_MES_B167_R0122", "DK4_MES_B167_R0125")
JULIO_TURN = ("DK4_MES_B170_R0164", "DK4_MES_B170_R0168")
MENU_BLOCKS = (167,169,170,170)


def match_panel(plane, system, image, ident):
    if ident != writer.OPAQUE:
        return previous.match_panel(plane, system, image, ident)
    # These native CP932 glyphs use a lighter edge palette than ASCII dialogue.
    pixels = image.crop((16, 296, 232, 360)).get_flattened_data()
    assert len(pixels) == len(plane) and not system and set(plane) == {0, 1, 15}
    return all(bytes(value == index for value in plane) == bytes(pixel == color for pixel in pixels)
               for index, color in ((1, (0, 8, 0)), (15, (197, 198, 197))))


producer = checked_text(previous.producer, {
    '"Hodram_B151_B160_FOCUSED_ONLY.nds"': '"Hodram_B161_B170_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '{"DK4_MES_B156_R0188","DK4_MES_B156_R0256","DK4_MES_B159_R0069","DK4_MES_B160_R0219"}':
        '{writer.OPAQUE,"DK4_MES_B161_R0029","DK4_MES_B168_R0304","DK4_MES_B169_R0211","DK4_MES_B170_R0203"}',
    'hodram_B151_B160_gameplay_': 'hodram_B161_B170_gameplay_',
    '(PAGE_TURN, CARLO_TURN)': '(PAGE_TURN, JULIO_TURN)',
    '        else:\n            if checked.get("layouts"):': '''        elif ident == writer.OPAQUE:
            symbol = checked["retained_mixed_glyphs"]
            plane = Path(symbol["plane"]).read_bytes()
            assert native.digest(plane) == symbol["plane_sha256"]
            panel.complete_mask(name_font, row["speaker"], image, 16, 277, town.INKS[1])
        else:
            if checked.get("layouts"):''',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::ship-and-tavern", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()

