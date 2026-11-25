"""Observe the farewell symbols and representative transitions in the six scenes."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from scripts import replay_hodram_B61_B64_20261122 as previous
from scripts import verify_hodram_B65_B70_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (65, 6), (65, 10), (65, 14), (65, 18), (65, 22), (65, 30), (65, 38), (65, 42),
    (65, 46), (65, 68), (65, 74), (65, 77), (65, 89), (65, 97),
    (65, 116), (65, 120), (65, 124), (65, 128), (65, 132),
    (66, 6), (66, 45), (66, 49), (66, 68),
    (67, 5), (67, 15), (67, 63), (67, 66), (67, 73), (67, 89), (67, 111), (67, 165), (67, 168), (67, 238),
    (68, 5), (68, 20), (68, 27), (68, 30),
    (69, 6), (69, 11), (69, 23), (69, 42), (69, 45),
    (70, 6), (70, 9), (70, 12), (70, 15),
)
test_name = ["DK4_MES_B65_R0116", "DK4_MES_B65_R0120", "DK4_MES_B65_R0124"]
long_speech = [f"DK4_MES_B67_R{number:04d}" for number in (63, 66, 73)]
ELLIPSIS_ID = "DK4_MES_B65_R0097"


def match_panel(plane, system, image, ident):
    if ident not in display.SYMBOLS and ident != ELLIPSIS_ID:
        return previous.scope["match_panel"](plane, system, image, ident)
    pixels = image.crop((16, 296, 232, 360)).get_flattened_data()
    assert len(pixels) == len(plane) and not system and set(plane) == {0, 1, 15}
    assert plane.count(1) > 0 and plane.count(15) > 0
    assert bytes(value == 1 for value in plane) == bytes(pixel == (0, 8, 0) for pixel in pixels)
    return bytes(value == 15 for value in plane) == bytes(pixel in {(197, 198, 197), (98, 97, 98)} for pixel in pixels)


producer = checked_text(previous.producer, {
    '"Hodram_B61_B64_FOCUSED_ONLY.nds"': '"Hodram_B65_B70_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    'candidate = base.digest(stage.ROM)':
        'candidate = base.digest(stage.ROM)\n'
        '    symbols = base.load(display.OPAQUE)\n'
        '    assert symbols["candidate_sha256"] == candidate and set(symbols["records"]) == display.SYMBOLS',
    'if stored == b"\\x81\\x63":\n                    assert ident == "DK4_MES_B64_R0093"':
        'if ident in display.SYMBOLS or ident == ELLIPSIS_ID:\n'
        '                    assert (ident in display.SYMBOLS or stored == b"\\x81\\x63")',
    '            if body == b"\\x81\\x63":':
        '''            if ident in display.SYMBOLS:
                ref = symbols["records"][ident]
                assert page == 1 and body.hex() == ref["exact_body_hex"][2:]
                assert base.digest(ref["plane"]) == ref["plane_sha256"]
                plane = Path(ref["plane"]).read_bytes()
            elif ident == ELLIPSIS_ID:''',
    'legend_ids': 'long_speech',
    'exact_legend_argument=turn_results,': 'exact_long_speech_and_following=turn_results,',
    'hodram_B61_B64_gameplay_': 'hodram_B65_B70_gameplay_',
    'paths = (fixture_file, inputs, REPORT, display.PROOF, fixture["fixture_ROM"], ELLIPSIS)':
        'assert display.SYMBOLS <= speech_ids\n'
        '    paths = (fixture_file, inputs, REPORT, display.PROOF, fixture["fixture_ROM"], ELLIPSIS, display.OPAQUE)',
    'exact_native_glyph_matches=True,': 'exact_native_glyph_matches=True, opaque_source_symbols=sorted(display.SYMBOLS),',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::Hodram-farewell-excerpts", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
