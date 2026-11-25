"""Check both recovery variants and the guildmaster's directions in focused gameplay."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_rafael_B161_B169_20261121 as previous
from scripts import verify_rafael_B306_B309_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, PATH = display.stage, display.base, display.native, display.PATH
ROOT = stage.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
SELECTED = (
    (306, 5), (306, 9), (306, 22), (306, 34), (306, 47), (306, 58), (306, 67),
    (306, 105), (306, 109), (306, 112), (306, 116), (306, 127), (306, 134), (306, 137),
    (307, 19), (307, 25), (307, 41),
    (308, 5), (308, 23), (308, 27), (308, 30), (308, 34), (308, 45), (308, 52), (308, 55),
    (309, 5), (309, 8), (309, 11), (309, 27), (309, 47), (309, 50), (309, 54),
)

producer = checked_text(previous.producer, {
    'groups[169]["commands"]': 'groups[309]["commands"]',
    '"Rafael_B161_B169_FOCUSED_ONLY.nds"': '"Rafael_B306_B309_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '["DK4_MES_B165_R0016", "DK4_MES_B166_R0069", "DK4_MES_B166_R0072"]':
        '[f"DK4_MES_B308_R{index:04d}" for index in (23, 27, 30, 34, 45, 52, 55)]',
    'assert [h[0] for h in turn] == [transition_ids[0], *transition_ids]':
        'assert [h[0] for h in turn] == transition_ids',
    'assert [h[1] for h in turn] == [1, 2, 1, 1]':
        'assert all(h[1] == 1 for h in turn)',
    '1200, 300': 'len(turn) * 300, 300',
    'len(SELECTED) + 1': 'len(SELECTED)',
    '    paths = (fixture_file':
        '    assert all(row["decision"] != "revision" or row["id"] in observed for row in draft["records"])\n'
        '    paths = (fixture_file',
    'rafael_B161_B169_gameplay_': 'rafael_B306_B309_gameplay_',
})
scope = previous.scope | globals() | dict(stage=SimpleNamespace(
    PROOF=stage.PROOF, ROM=stage.ROM, ROOT=stage.ROOT, OUTPUT=stage.MANUSCRIPT,
    review=SimpleNamespace(TOKEN=stage.TOKEN)))
for source in (producer, check):
    exec(compile(source, __file__ + "::focused-recovery-excerpts", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
