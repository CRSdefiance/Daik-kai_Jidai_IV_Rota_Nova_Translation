"""Exercise the complete revised contract lesson with the established Rafael prelude."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
import sys
from types import FunctionType

from scripts import replay_ceuta_lesson_20261119 as startup_template
from scripts import replay_rafael_sailing_modes_20261119 as fixture_template
from scripts import run_Rafael_B45_scenes_v7893 as runner
from scripts import stage_rafael_contract_and_proof_20261119 as build
from scripts.source_locked_derivation_v5118 import checked_text

base = build.base
ROOT = build.ROOT / "contract_replay"
FIXTURE, FIXTURES = ROOT / "Rafael_Contract_RESEARCH_ONLY.nds", ROOT / "fixtures.json"
STARTUP = build.ROOT / "startup_fixture"
FRAMES = 9001


def prepare():
    source = checked_text(getsource(fixture_template.prepare), {
        "(44, 46)": "(44, 45)",
        "len(commands) == 47 and len(speeches) == 24": "len(commands) == 34 and len(speeches) == 12",
        'group, = stored["groups"]': 'group, = (g for g in stored["groups"] if g["block"] == 45)',
        'assert [r["label"] for r in menu] == ["Please do.", "No, thanks."]': "assert not menu",
        "len(records) == 24 and len(command_ids) == 37": "len(records) == 12 and len(command_ids) == 24",
        'research_ROM_sha256=base.digest(FIXTURE), original_menu_records=menu,':
            'research_ROM_sha256=base.digest(FIXTURE), original_menu_records=menu,\n'
            '            source_block=45, fixture_block=44, original_opening_prelude_commands=commands[:10],',
        "Original block 46 runs after the preserved block 44 New Game prelude.":
            "The Ceuta contract lesson runs after the original Rafael New Game prelude.",
        "Prepared the entire sailing tutorial behind the original Rafael prelude.":
            "Prepared all 24 original contract lesson commands after the preserved prelude.",
    })
    scope = vars(fixture_template) | dict(ROOT=ROOT, stage=build, FIXTURE=FIXTURE, FIXTURES=FIXTURES)
    exec(compile(source, __file__ + "::whole-contract-lesson", "exec"), scope)
    scope["prepare"]()


def capture():
    source = checked_text(Path(runner.__file__).read_text(encoding="utf-8"), {
        "ROOT=Path('work/analysis/Rafael_B45_scene_runs_v7893')": "ROOT=ACTIVE_ROOT",
        "FIXTURES=Path('work/analysis/Rafael_B45_scene_fixtures_v7892/two_complete_source_English_original_Rafael_prelude_fixtures.json')":
            "FIXTURES=ACTIVE_FIXTURES",
        "cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Rafael_B45_route{route}_{version}_v7893'":
            "cap=folder/'capture'",
        "range(4000,15501,240)": "range(4000,FRAME_LIMIT-1,240)",
        "range(2350,16001,60))|{16000}": "range(2350,FRAME_LIMIT,45))|{FRAME_LIMIT-1}",
        "'16001'": "str(FRAME_LIMIT)",
        "16001": "FRAME_LIMIT",
    })
    scope = dict(__name__="__main__", __file__=__file__, ACTIVE_ROOT=ROOT, ACTIVE_FIXTURES=FIXTURES,
                 FRAME_LIMIT=FRAMES)
    previous = sys.argv
    try:
        sys.argv = [__file__, "--route", "0", "--version", "English"]
        exec(compile(source, __file__ + "::contract-replay", "exec"), scope)
    finally:
        sys.argv = previous


def startup():
    FunctionType(startup_template.startup.__code__, vars(startup_template) | {"build": build, "STARTUP": STARTUP})()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "startup"))
    globals()[parser.parse_args().action]()
