"""Observe representative scenes and Aziza's speakerless-to-named transitions."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_rafael_B170_B176_20261121 as previous
from scripts import verify_rafael_B181_B187_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, PATH = display.stage, display.base, display.native, display.PATH
ROOT = stage.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
SELECTED = (
    (181, 40), (181, 82), (181, 132), (181, 136), (181, 144), (181, 147),
    (182, 75), (182, 82), (182, 87), (182, 91),
    (183, 31), (183, 59), (183, 62), (183, 65), (183, 97), (183, 101),
    (184, 56), (184, 59), (184, 63), (185, 35), (185, 43),
    (186, 19), (186, 22), (186, 79), (186, 111), (186, 168), (186, 171),
    (187, 15), (187, 19), (187, 23), (187, 26), (187, 75), (187, 87),
    (187, 91), (187, 96), (187, 100), (187, 104), (187, 109), (187, 118), (187, 121),
)

producer = checked_text(previous.producer, {
    'groups[176]["commands"]': 'groups[187]["commands"]',
    '"Rafael_B170_B176_FOCUSED_ONLY.nds"': '"Rafael_B181_B187_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '[f"DK4_MES_B171_R{n:04d}" for n in (44, 47, 61, 64, 68)]':
        '[f"DK4_MES_B187_R{n:04d}" for n in (87, 91, 96, 100, 104)]',
    'rafael_B170_B176_gameplay_': 'rafael_B181_B187_gameplay_',
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
