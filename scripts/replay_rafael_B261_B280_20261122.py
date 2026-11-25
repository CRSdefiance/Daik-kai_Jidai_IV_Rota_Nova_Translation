"""Observe the native cave-in displays, stone menu, and figurehead choice."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_rafael_B221_B240_20261122 as previous
from scripts import verify_rafael_B261_B280_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, PATH = display.stage, display.base, display.native, display.PATH
ROOT = stage.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
SELECTED = (
    (261, 6), (261, 9), (261, 12), (261, "270"),
    (261, 31), (261, "style342"), (261, 54), (261, 72), (261, "style852"), (261, 95),
    (261, 114), (261, 121), (261, 125), (261, 129),
    (261, 140), (261, 144), (261, 148), (261, 152), (261, 155), (261, "1664"),
    (261, 170), (261, 178), (261, 195), (261, 206), (261, 218),
    (262, 7), (270, 5), (276, 16),
)
schedule = previous.schedule
producer = checked_text(previous.producer, {
    'groups[239]["commands"]': 'groups[280]["commands"]',
    '"Rafael_B221_B240_FOCUSED_ONLY.nds"': '"Rafael_B261_B280_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '[(224, 0), (224, 1), (224, 0), (224, 1), (224, 2), (233, 0), (233, 1)]':
        '[(261, 0), (261, 1), (261, 2), (261, 0), (261, 1)]',
    '["DK4_MES_B233_R0064", "DK4_MES_B233_R0067"]':
        '["DK4_MES_B261_R0148", "DK4_MES_B261_R0152", "DK4_MES_B261_R0155"]',
    '[transition_ids[0], *transition_ids]': 'transition_ids',
    '[1, 2, 1]': '[1, 1, 1]',
    'len(expected_speech) + 6': 'len(expected_speech) + 2',
    'sum("_STYLE_" in hold["id"] for hold in holds) == 4': 'sum("_STYLE_" in hold["id"] for hold in holds) == 2',
    'rafael_B221_B240_gameplay_': 'rafael_B261_B280_gameplay_',
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
