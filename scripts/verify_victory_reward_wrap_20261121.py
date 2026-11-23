"""Replay the same victory and verify the captured-gold phrase in gameplay."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import stage_victory_reward_wrap_20261121 as stage
from scripts import verify_clifford_declaration_wrap_20261121 as fleet
from scripts import verify_victory_reward_digits_20261121 as digits
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = stage.ROOT / "playback"
RUN = ROOT / "attack"
PROOF = stage.ROOT / "verified_gameplay.json"
SHEET = stage.ROOT / "captured_gold_live.png"
HOLDS = {9100: (301, ("6055",)), 9200: (301, ("6055",))}


def verify():
    source = checked_text(getsource(digits.verify), {
        '(1024, 2 * 248)': '(1024, 248)',
        'if frame in (8800, 9200):': 'if frame == 9200:',
        'top = 248 if frame == 9200 else 0': 'top = 0',
        'outcome = "Food and water" if frame == 8800 else "Captured gold"': 'outcome = "Captured gold"',
        'assert len(changed) == 3 and len(unchanged) == 19': 'assert len(changed) == 2 and len(unchanged) == 20',
        'changed_number_calls=4,': 'supplies_screen_unchanged=8800 in unchanged,',
        'Food, water and capture proceeds render in the regular font. The other 19 frames match.':
            'The captured-gold phrase remains intact. The other 20 frames match.',
    })
    env = vars(digits) | globals() | {"history": digits}
    exec(compile(source, __file__ + "::paired-reward-wrap-check", "exec"), env)
    env["verify"]()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true", help="Verify a completed paired capture.")
    if not parser.parse_args().verify_only:
        FunctionType(fleet.playback.__code__, vars(fleet) | {"ROOT": ROOT, "stage": stage, "__file__": __file__})()
    verify()
