"""Replay the revised Lisbon trade lesson and the registered startup."""
from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType
import sys

from scripts import audit_square_shop_followup_20261119 as startup_audit
from scripts import replay_rafael_sailing_modes_20261119 as lesson
from scripts import replay_sea_hazard_dialogue_20261119 as boot
from scripts import stage_story_market_terms_20261119 as build
from scripts.source_locked_derivation_v5118 import checked_text

base = build.base
ROOT = build.ROOT / "lisbon_lesson"
FIXTURE = ROOT / "Lisbon_Trade_Lesson_RESEARCH_ONLY.nds"
FIXTURES = ROOT / "fixtures.json"
STARTUP = build.ROOT / "startup_fixture"
STARTUP_PROOF = build.ROOT / "own_startup_verification.json"


def prepare():
    source = checked_text(getsource(lesson.prepare), {
        "(44, 46)": "(44, 137)",
        "len(commands) == 47 and len(speeches) == 24": "len(commands) == 30 and len(speeches) == 12",
        'group, = stored["groups"]': 'group, = (g for g in stored["groups"] if g["route"] == 0 and g["block"] == 137)',
        '["Please do.", "No, thanks."]': '["Market share?", "Got it."]',
        "len(records) == 24 and len(command_ids) == 37": "len(records) == 12 and len(command_ids) == 20",
        "Original block 46 runs after the preserved block 44 New Game prelude.":
            "Original Lisbon trade lesson runs after the Rafael New Game prelude. Natural activation is untested.",
        "Prepared the entire sailing tutorial behind the original Rafael prelude.":
            "Prepared the original 20-command Lisbon trade lesson with its native choice and return.",
    })
    scope = vars(lesson) | globals() | {"stage": build}
    exec(compile(source, __file__ + "::lisbon_trade_lesson", "exec"), scope)
    scope["prepare"]()


def capture():
    source = checked_text(getsource(lesson.capture), {
        '    prior = sys.argv': '    prior = sys.argv',
        '        "16001": "FRAME_LIMIT",':
            '        "16001": "FRAME_LIMIT",\n'
            '        "displayed_original_block=46": "displayed_original_block=137",\n'
            '        "original_exchange_commands=37,original_exchange_stored_speeches=24":\n'
            '            "original_exchange_commands=20,original_exchange_stored_speeches=12",',
    })
    scope = vars(lesson) | globals() | {"FRAMES": 9251}
    exec(compile(source, __file__ + "::lisbon_trade_replay", "exec"), scope)
    scope["capture"]("accept")


def startup():
    play = type("Startup", (), {"STARTUP": STARTUP})
    run = FunctionType(boot.previous.startup.__code__, vars(boot.previous) |
                       {"stage": build, "STARTUP": STARTUP})
    run()
    verify = FunctionType(startup_audit.startup.__code__, vars(startup_audit) |
                          {"build": build, "play": play, "STARTUP": STARTUP_PROOF})
    # This stage uses the common story predecessor field.
    source = checked_text(getsource(startup_audit.startup), {
        '''"proof['registered_input']['candidate_sha256']": "proof['previous_sha256']"''':
            '''"proof['registered_input']['candidate_sha256']": "proof['predecessor_sha256']"''',
    })
    scope = verify.__globals__
    exec(compile(source, __file__ + "::startup_verification", "exec"), scope)
    scope["startup"]()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "startup"))
    globals()[parser.parse_args().action]()
