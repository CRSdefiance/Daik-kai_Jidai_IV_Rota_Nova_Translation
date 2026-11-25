"""Run the unchanged startup and the complete Sofala appointment fixture."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_rafael_contract_and_proof_20261119 as previous
from scripts import stage_rafael_iberian_aftermath_20261119 as build
from scripts.source_locked_derivation_v5118 import checked_text

base = build.base
ROOT, STARTUP = build.ROOT / "sofala_fixture", build.ROOT / "startup_fixture"
FIXTURE = ROOT / "Rafael_Sofala_Appointment_RESEARCH_ONLY.nds"
FIXTURES = ROOT / "fixtures.json"
FRAMES = 12501


def prepare():
    template = previous.fixture_template
    source = checked_text(getsource(template.prepare), {
        "(44, 46)": "(44, 55)",
        "len(commands) == 47 and len(speeches) == 24": "len(commands) == 84 and len(speeches) == 30",
        'group, = stored["groups"]': 'group, = (g for g in stored["groups"] if g["block"] == 55)',
        'assert [r["label"] for r in menu] == ["Please do.", "No, thanks."]': "assert not menu",
        "len(records) == 24 and len(command_ids) == 37": "len(records) == 30 and len(command_ids) == 74",
        'research_ROM_sha256=base.digest(FIXTURE), original_menu_records=menu,':
            'research_ROM_sha256=base.digest(FIXTURE), original_menu_records=menu,\n'
            '            source_block=55, fixture_block=44, original_opening_prelude_commands=commands[:10],',
        "Original block 46 runs after the preserved block 44 New Game prelude.":
            "Original block 55 runs after the preserved Rafael New Game prelude. Optional scene activation is untested.",
        "Prepared the entire sailing tutorial behind the original Rafael prelude.":
            "Prepared all 74 Sofala appointment commands behind the original Rafael prelude.",
    })
    scope = vars(template) | globals() | {"stage": build}
    exec(compile(source, __file__ + "::appointment-fixture", "exec"), scope)
    scope["prepare"]()


def capture():
    # The inherited runner supplies readonly original-interpreter evidence.
    source = checked_text(getsource(previous.capture), {
        '        "16001": "FRAME_LIMIT",':
            '        "16001": "FRAME_LIMIT",\n'
            '        "original_exchange_commands=24,original_exchange_speeches=12":\n'
            '            "original_exchange_commands=74,original_exchange_speeches=30",',
        "::contract-replay": "::sofala-appointment-replay",
    })
    scope = vars(previous) | globals()
    exec(compile(source, __file__ + "::replay", "exec"), scope)
    scope["capture"]()


def startup():
    FunctionType(previous.startup.__code__, vars(previous) | globals())()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "startup"))
    globals()[parser.parse_args().action]()
