"""Replay representative town exchanges, forecasts, and bargaining controls."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B131_B150_20261122 as previous
from scripts import verify_hodram_B181_B200_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (181, 9), (181, 12), (181, 20), (181, 37),
    (182, 10), (182, 13), (182, 21), (182, 40), (182, 51),
    (183, 13), (183, 54), (184, 28), (184, 73), (185, 27), (185, 39),
    (186, 5), (186, 17), (186, 62),
    (187, 28), (187, 35), (187, 53), (187, 61), (187, 95),
    (188, 18), (188, 22), (188, 26), (188, 36),
    (189, 6), (189, 26), (189, 29), (190, 40), (190, 63),
    (191, 45), (191, 60), (192, 30), (192, 45),
    (193, 46), (193, 49), (193, 65), (194, 59), (194, 85),
    (195, 64), (195, 68), (195, 100), (196, 30),
    (197, 25), (197, 37), (197, 59),
    (198, 46), (198, 49), (198, 56), (199, 24), (199, 58), (199, 77),
    (200, 12), (200, 24), (200, "218"), (200, 42), (200, 45),
    (200, 62), (200, 74), (200, 107), (200, 257), (200, "1588"),
    (200, 287), (200, 302), (200, 306),
)
test_name = ["DK4_MES_B188_R0018", "DK4_MES_B188_R0022", "DK4_MES_B188_R0026"]
PAGE_TURN = ("DK4_MES_B200_R0074", "DK4_MES_B200_R0107")
CHARM_TURN = (writer.CHARM_PANEL, "DK4_MES_B200_R0062")
MENU_BLOCKS = (200, 200)
match_panel = previous.match_panel
producer = checked_text(previous.producer, {
    '"Hodram_B131_B150_FOCUSED_ONLY.nds"': '"Hodram_B181_B200_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '{"DK4_MES_B143_R0033","DK4_MES_B143_R0079","DK4_MES_B143_R0087","DK4_MES_B137_R0074"}':
        '{writer.CHARM_PANEL,"DK4_MES_B182_R0051","DK4_MES_B187_R0053","DK4_MES_B188_R0022"}',
    'hodram_B131_B150_gameplay_': 'hodram_B181_B200_gameplay_',
    '(PAGE_TURN, SERA_NAME)': '(PAGE_TURN, CHARM_TURN)',
    '        expected = native_rows[pair[0]]["layouts"][0]["page_sha256"]\n        assert pages == (*range(1,len(expected)+1),1)':
        '        assert pages == (1, 1)',
    'assert len(styles) == 1 and styles[0].startswith("SC1_B133_STYLE_10_")': 'assert not styles',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::town-and-bargaining", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
