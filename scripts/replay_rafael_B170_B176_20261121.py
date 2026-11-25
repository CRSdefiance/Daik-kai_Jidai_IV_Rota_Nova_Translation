"""Observe the family conversation, the four dance panels, and Jam's joke on cold boot."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_rafael_B161_B169_20261121 as previous
from scripts import verify_rafael_B170_B176_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, PATH = display.stage, display.base, display.native, display.PATH
ROOT = stage.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
SELECTED = (
    (170, 32), (170, 206), (170, 229), (170, 232), (170, 241), (170, 244), (170, 248), (170, 253),
    (170, 297), (170, 305),
    (171, 39), (171, 44), (171, 47), (171, 61), (171, 64), (171, 68), (171, 103),
    (172, 99), (172, 114), (172, 118), (172, 141),
    (173, 62), (173, 66), (176, 44), (176, 91), (176, 119), (176, 131), (176, 140), (176, 148),
)

producer = checked_text(previous.producer, {
    'groups[169]["commands"]': 'groups[176]["commands"]',
    '"Rafael_B161_B169_FOCUSED_ONLY.nds"': '"Rafael_B170_B176_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '["DK4_MES_B165_R0016", "DK4_MES_B166_R0069", "DK4_MES_B166_R0072"]':
        '[f"DK4_MES_B171_R{n:04d}" for n in (44, 47, 61, 64, 68)]',
    '    assert [h[0] for h in turn] == [transition_ids[0], *transition_ids]\n'
    '    assert [h[1] for h in turn] == [1, 2, 1, 1]':
        '    assert [h[0] for h in turn] == transition_ids\n'
        '    assert [h[1] for h in turn] == [1] * len(transition_ids)',
    '1200, 300': '1500, 300',
    'rafael_B161_B169_gameplay_': 'rafael_B170_B176_gameplay_',
    'len(holds) == len(SELECTED) + 1': 'len(holds) == len(SELECTED)',
})
scope = previous.scope | globals() | dict(stage=SimpleNamespace(
    PROOF=stage.PROOF, ROM=stage.ROM, ROOT=stage.ROOT, OUTPUT=stage.MANUSCRIPT,
    review=SimpleNamespace(TOKEN=stage.TOKEN)))
for script in (producer, check):
    exec(compile(script, __file__ + "::focused-native-excerpts", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
