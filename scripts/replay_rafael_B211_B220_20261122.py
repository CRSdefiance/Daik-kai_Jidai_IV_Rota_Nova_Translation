"""Observe the original letter panels, parrot echoes, menus and upgraded stat notices."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_rafael_B208_B210_20261122 as previous
from scripts import verify_rafael_B211_B220_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, PATH = display.stage, display.base, display.native, display.PATH
ROOT = stage.INITIAL_STAGE / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = stage.INITIAL_STAGE / "startup/capture/capture_report.json"
SELECTED = (
    (211, 33), (211, 55), (211, 63), (211, 91), (212, 33), (212, 54), (212, 65),
    (213, 22), (213, 42), (213, "860"), (213, 81), (213, 107),
    (215, 32), (215, 61), (215, 83), (215, 87), (215, 92),
    (216, 31), (216, 35), (216, 47), (216, 54), (216, 64), (216, 68), (216, 71), (216, 74),
    (217, 9), (217, 13), (217, 17), (217, 20), (217, 24), (217, 29), (217, 33), (217, 52), (217, 56),
    (218, 37), (218, 48), (218, 51), (218, 55), (218, "836"), (218, 78), (218, "1006"), (218, 109),
    (220, 28), (220, 36), (220, 59), (220, 73), (220, 90),
)
schedule = previous.schedule
producer = checked_text(previous.producer, {
    'groups[210]["commands"]': 'groups[220]["commands"]',
    '"Rafael_B208_B210_FOCUSED_ONLY.nds"': '"Rafael_B211_B220_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '[(208, 0), (208, 1), (209, 0), (209, 1), (209, 2)]':
        '[(213, 0), (213, 1), (218, 0), (218, 1), (218, 0), (218, 1)]',
    '[f"DK4_MES_B210_R{n:04d}" for n in (18, 22, 26, 30, 34, 38)]':
        '[f"DK4_MES_B218_R{n:04d}" for n in (48, 51, 55)]',
    '    final, image = town.read_frame':
        '''    letter = [h for h in holds if h["id"] in [f"DK4_MES_B216_R{n:04d}" for n in (64, 68, 71, 74)]]
    assert len(letter) == 4 and all(h["system_FE"] for h in letter)
    assert [h["frame"] - letter[0]["frame"] for h in letter] == [0, 300, 600, 900]
    echo = [h for h in holds if h["id"] in [f"DK4_MES_B217_R{n:04d}" for n in (9, 13, 17, 20, 24, 29, 33)]]
    assert [h["system_FE"] for h in echo] == [False, True, False, True, False, False, True]
    assert [h["frame"] - echo[0]["frame"] for h in echo] == list(range(0, 2100, 300))
    final, image = town.read_frame''',
    'rafael_B208_B210_gameplay_': 'rafael_B211_B220_gameplay_',
    'exact_sampled_page_turn=turn, final_hold=final, sheets=sheets,':
        'exact_sampled_page_turn=turn, consecutive_letter_panels=letter, consecutive_parrot_exchange=echo, final_hold=final, sheets=sheets,',
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
