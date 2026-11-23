"""Replay Rafael's Ceuta controls and wind question on the staged story ROM."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
import sys
from types import FunctionType

from scripts import replay_rafael_sailing_modes_20261119 as earlier
from scripts import replay_sea_hazard_dialogue_20261119 as startup_entry
from scripts import stage_story_short_phrase_wraps_20261119 as build
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage = build.base, build.native, build
ROOT = build.ROOT / "ceuta_play"
FIXTURE = ROOT / "Rafael_Ceuta_Lesson_RESEARCH_ONLY.nds"
FIXTURES = ROOT / "fixtures.json"
STARTUP = build.ROOT / "startup_fixture"
FRAMES = 9301
DOWN_FRAME = 5860


def prepare():
    source = checked_text(getsource(earlier.prepare), {
        "(44, 46)": "(44, 127)",
        "len(commands) == 47 and len(speeches) == 24": "len(commands) == 39 and len(speeches) == 17",
        "group, = stored[\"groups\"]": 
            'group, = (item for item in stored["groups"] if item["route"] == 0 and item["block"] == 127)',
        '''["Please do.", "No, thanks."]''': '''["I've got it!", "The wind might be against us..."]''',
        "len(records) == 24 and len(command_ids) == 37": "len(records) == 17 and len(command_ids) == 29",
        "Original block 46 runs after the preserved block 44 New Game prelude.":
            "Original Ceuta lesson block 127 runs after the preserved block 44 New Game prelude.",
        "Prepared the entire sailing tutorial behind the original Rafael prelude.":
            "Prepared the complete Ceuta lesson, keeping its original choices and branches.",
    })
    scope = vars(earlier) | dict(ROOT=ROOT, stage=build, FIXTURE=FIXTURE, FIXTURES=FIXTURES)
    exec(compile(source, __file__ + "::ceuta-original-lesson", "exec"), scope)
    scope["prepare"]()


def capture():
    workflow = earlier.workflow
    recipe = checked_text(Path(workflow.__file__).read_text(encoding="utf-8"), {
        "ROOT=Path('work/analysis/Rafael_B46_scene_runs_v7945')": "ROOT=ACTIVE_ROOT",
        "FIXTURES=Path('work/analysis/Rafael_B46_scene_fixtures_v7944/two_complete_source_English_original_Rafael_prelude_fixtures.json')":
            "FIXTURES=ACTIVE_FIXTURES",
        "cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Rafael_B46_route{route}_{version}_{choice}_v7945'":
            "cap=folder/'capture'",
        "MENU_SNAPSHOT_FRAMES=[4810,4870,4930]": "MENU_SNAPSHOT_FRAMES=[5770,5830,5890]",
        "4725<=args.down_frame<4960": "5685<=args.down_frame<5920",
        "range(2350,16001,60))|{16000,*MENU_SNAPSHOT_FRAMES}":
            "range(2350,FRAME_LIMIT,45))|{FRAME_LIMIT-1,*MENU_SNAPSHOT_FRAMES}",
        "range(4000,15501,240)": "range(4000,FRAME_LIMIT-1,240)",
        "'16001'": "str(FRAME_LIMIT)",
        "16001": "FRAME_LIMIT",
        "displayed_original_block=46": "displayed_original_block=127",
        "original_exchange_commands=37,original_exchange_stored_speeches=24":
            "original_exchange_commands=29,original_exchange_stored_speeches=17",
        "B46 {version} {choice}": "B127 {version} {choice}",
    })
    env = {"__name__": "__main__", "__file__": __file__, "ACTIVE_ROOT": ROOT,
           "ACTIVE_FIXTURES": FIXTURES, "FRAME_LIMIT": FRAMES}
    previous = sys.argv
    try:
        sys.argv = [__file__, "--route", "0", "--version", "English", "--choice", "decline",
                    "--down-frame", str(DOWN_FRAME)]
        exec(compile(recipe, __file__ + "::ceuta-wind-choice", "exec"), env)
    finally:
        sys.argv = previous


def startup():
    """Use the registered parent startup contract on the final staged ROM."""
    from types import SimpleNamespace

    staged = SimpleNamespace(base=base, native=native, ROOT=build.ROOT, ROM=build.ROM,
                             PROOF=build.PROOF, parent=build.parent)
    # The story stage records its predecessor under the story pipeline key.
    # The generic startup verifier consumes the exact registered parent directly.
    run = FunctionType(startup_entry.previous.startup.__code__, vars(startup_entry.previous) |
                       {"stage": staged, "STARTUP": STARTUP})
    run()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "startup"))
    globals()[parser.parse_args().action]()
