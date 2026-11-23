"""Bind ordinary Square gameplay and startup checks to the staged candidate."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import audit_ceuta_lesson_20261119 as startup_template
from scripts import checkpoint_square_country_briefings_20261115 as precedent
from scripts import replay_square_shop_followup_20261119 as play
from scripts import stage_square_shop_followup_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, build = stage.base, stage
PROOF = OUTPUT = stage.ROOT / "verified_amsterdam_gameplay.json"
SHEET = stage.ROOT / "gameplay_lower_screens.png"
STARTUP = stage.ROOT / "own_startup_verification.json"


def gameplay():
    source = checked_text(getsource(precedent.main), {
        'offline_only_changed_keys=sorted(set(stage.PROSE) - {657, 689})':
            'offline_only_changed_keys=sorted(set(stage.EDITS) - {657})',
        'observed_changed_keys=[657, 689]': 'observed_changed_keys=[657]',
        'hardware=False, gameplay_sheet=str(SHEET),':
            'hardware=False, original_shop_choices_replayed=True,\n'
            '        sheets=[dict(path=str(SHEET), sha256=evidence[str(SHEET)])], gameplay_sheet=str(SHEET),',
    })
    scope = vars(precedent) | globals()
    exec(compile(source, __file__ + "::amsterdam-square-verification", "exec"), scope)
    scope["main"]()


def startup():
    source = checked_text(getsource(startup_template.startup), {
        '''"proof['registered_input']['candidate_sha256']": "proof['predecessor_sha256']"''':
            '''"proof['registered_input']['candidate_sha256']": "proof['previous_sha256']"''',
    })
    scope = vars(startup_template) | globals()
    exec(compile(source, __file__ + "::square-startup-verification", "exec"), scope)
    scope["startup"]()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("gameplay", "startup"))
    globals()[parser.parse_args().action]()
