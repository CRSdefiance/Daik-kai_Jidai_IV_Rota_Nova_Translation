"""Replay representative pages and dialogue transitions in the four linked scenes."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts.analyze_rafael557_actual_v1 import ELLIPSIS
from scripts import replay_hodram_B54_B60_20261122 as previous
from scripts import verify_hodram_B61_B64_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (61, 32), (61, 36), (61, 40), (61, 44), (61, 48),
    (62, 73), (62, 76), (62, 79), (62, 83), (62, 104), (62, 107),
    (63, 5), (63, 15), (63, 45), (63, 48), (63, 52), (63, 75),
    (64, 11), (64, 17), (64, 63), (64, 66), (64, 78), (64, 81),
    (64, 84), (64, 87), (64, 90), (64, 93), (64, 97), (64, 101), (64, 104),
)
test_name = ["DK4_MES_B62_R0076", "DK4_MES_B62_R0079", "DK4_MES_B62_R0083"]
legend_ids = [f"DK4_MES_B64_R{number:04d}" for number in (78, 81, 84, 87, 90, 93, 97, 101, 104)]
ELLIPSIS_SHA = "d2cc8cb26c6e8de3cc478467f11c7a0a90c3444122b81b81b5daa1e94739c53b"


def match_panel(plane, system, image, ident):
    if ident != "DK4_MES_B64_R0093":
        return previous.scope["match_panel"](plane, system, image, ident)
    pixels = image.crop((16, 296, 232, 360)).get_flattened_data()
    assert len(pixels) == len(plane) and not system and set(plane) == {0, 1, 15}
    assert plane.count(1) == plane.count(15) == 6
    return all(bytes(value == index for value in plane) == bytes(pixel == color for pixel in pixels)
               for index, color in ((1, (0, 8, 0)), (15, (197, 198, 197))))

producer = checked_text(previous.producer, {
    '"Hodram_B54_B60_FOCUSED_ONLY.nds"': '"Hodram_B61_B64_FOCUSED_ONLY.nds"',
})
page_check = previous.check[previous.check.index('    relief = "DK4_MES_B60_R0015"'):
                            previous.check.index("    final, image =")]
check = checked_text(previous.check, {
    'current = bytes.fromhex(checked["body_hex"])[int(item["word"] != 0x4100):].decode("ascii")\n'
    '                body = stage.review.TOKEN.sub(lambda m: native_report["default_names"][m[0]], current).encode("ascii")':
        '''stored = bytes.fromhex(checked["body_hex"])[int(item["word"] != 0x4100):]
                if stored == b"\\x81\\x63":
                    assert ident == "DK4_MES_B64_R0093" and row["decision"] == "retention"
                    assert stored == bytes.fromhex(row["source_hex"])[1:]
                    body = stored
                else:
                    current = stored.decode("ascii")
                    body = stage.review.TOKEN.sub(lambda m: native_report["default_names"][m[0]], current).encode("ascii")''',
    '''            view = paint(arm, font, body)
            assert view["complete_consumed_bytes"] == len(body)
            plane = bytes.fromhex(view["pages"][page - 1]["native_plane_hex"])
''': '''            if body == b"\\x81\\x63":
                assert page == 1 and base.digest(ELLIPSIS) == ELLIPSIS_SHA
                plane = ELLIPSIS.read_bytes()
            else:
                view = paint(arm, font, body)
                assert view["complete_consumed_bytes"] == len(body)
                plane = bytes.fromhex(view["pages"][page - 1]["native_plane_hex"])
''',
    page_check: '''    turn_results = [(h["id"], h["page"], h["frame"]) for h in holds if h["id"] in legend_ids]
    assert [ident for ident, _, _ in turn_results] == legend_ids
    assert all(page == 1 for _, page, _ in turn_results)
    assert [frame - turn_results[0][2] for _, _, frame in turn_results] == list(range(0, 300 * len(legend_ids), 300))
''',
    'len(holds) == len(expected_speech) + 1': 'len(holds) == len(expected_speech)',
    'exact_turn_and_following=turn_results,': 'exact_legend_argument=turn_results,',
    'paths = (fixture_file, inputs, REPORT, display.PROOF, fixture["fixture_ROM"])':
        'paths = (fixture_file, inputs, REPORT, display.PROOF, fixture["fixture_ROM"], ELLIPSIS)',
    'hodram_B54_B60_gameplay_': 'hodram_B61_B64_gameplay_',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::Hodram-linked-excerpts", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
