"""Run Rafael's introduction to Hans and the cumulative candidate's cold boot."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
import sys
from types import FunctionType, SimpleNamespace

from scripts import replay_ceuta_lesson_20261119 as tutorial
from scripts import replay_rafael_sailing_modes_20261119 as fixture_builder
from scripts import run_Rafael_B48_scenes_v8050 as runner
from scripts import stage_naturalist_aliases_and_shield_20261119 as build
from scripts.source_locked_derivation_v5118 import checked_text

base = build.base
ROOT = build.ROOT / "rafael_athens"
FIXTURE = ROOT / "Rafael_Athens_RESEARCH_ONLY.nds"
FIXTURES = ROOT / "fixtures.json"
STARTUP = build.ROOT / "startup_fixture"


def prepare():
    source = checked_text(getsource(fixture_builder.prepare), {
        "(44, 46)": "(44, 48)",
        "len(commands) == 47 and len(speeches) == 24": "len(commands) == 173 and len(speeches) == 91",
        'group, = stored["groups"]':
            'group, = (g for g in stored["groups"] if g["route"] == 0 and g["block"] == 48)',
        'assert [r["label"] for r in menu] == ["Please do.", "No, thanks."]': "assert not menu",
        "len(records) == 24 and len(command_ids) == 37": "len(records) == 91 and len(command_ids) == 163",
        'research_ROM_sha256=base.digest(FIXTURE), original_menu_records=menu,':
            'research_ROM_sha256=base.digest(FIXTURE), original_menu_records=menu,\n'
            '            source_block=48, fixture_block=44, original_opening_prelude_commands=commands[:10],',
        "Original block 46 runs after the preserved block 44 New Game prelude.":
            "The Athens block runs after the original Rafael New Game prelude.",
        "Prepared the entire sailing tutorial behind the original Rafael prelude.":
            "Prepared the entire Athens scene and its four modal notices.",
    })
    staged = SimpleNamespace(PROOF=build.PROOF, ROM=build.ROM, logical_end=build.stage.logical_end)
    scope = vars(fixture_builder) | dict(ROOT=ROOT, stage=staged, FIXTURE=FIXTURE, FIXTURES=FIXTURES)
    exec(compile(source, __file__ + "::whole-athens-block", "exec"), scope)
    scope["prepare"]()


def capture():
    source = checked_text(Path(runner.__file__).read_text(encoding="utf-8"), {
        "ROOT=Path('work/analysis/Rafael_B48_scene_runs_v8050')": "ROOT=ACTIVE_ROOT",
        "FIXTURES=Path('work/analysis/Rafael_B48_scene_fixtures_v8049/two_complete_source_English_original_Rafael_prelude_fixtures.json')":
            "FIXTURES=ACTIVE_FIXTURES",
        "cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Rafael_B48_route{route}_{version}_v8050'":
            "cap=folder/'capture'",
        "range(2350,40001,60)": "range(2350,40001,120)",
        ",*map(str,captures),'--dump-ram']": ",*map(str,captures)]",
    })
    scope = dict(__name__="__main__", __file__=__file__, ACTIVE_ROOT=ROOT, ACTIVE_FIXTURES=FIXTURES)
    previous = sys.argv
    try:
        sys.argv = [__file__, "--route", "0", "--version", "English"]
        exec(compile(source, __file__ + "::athens-replay", "exec"), scope)
    finally:
        sys.argv = previous


def startup():
    scope = vars(tutorial) | {"build": build, "STARTUP": STARTUP}
    FunctionType(tutorial.startup.__code__, scope)()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "startup"))
    globals()[parser.parse_args().action]()
