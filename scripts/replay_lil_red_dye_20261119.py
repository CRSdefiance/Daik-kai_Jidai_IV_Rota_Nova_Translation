"""Open the Amsterdam conversation after Lil's original New Game prelude."""
from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
import sys
from types import FunctionType

from scripts import replay_hodram_mihwa_crown_20261119 as workflow
from scripts import replay_story_market_terms_20261119 as startup_workflow
from scripts import run_Hodram_scenes_v8280 as runner
from scripts import stage_lil_red_dye_20261119 as build
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "amsterdam_replay"
FIXTURE, FIXTURES = ROOT / "Lil_Amsterdam_RESEARCH_ONLY.nds", ROOT / "fixtures.json"
STARTUP = build.ROOT / "startup_fixture"
STARTUP_PROOF = build.ROOT / "own_startup_verification.json"
FILE = "/data/SC2.DK4"
FRAMES = 11501


def prepare():
    source = checked_text(getsource(workflow.prepare), {
        '(42, 89)': '(22, 129)',
        '.blocks[42]': '.blocks[22]',
        'first == 42': 'first == 56',
        'len(initializers) == 8 and len(prelude) == 34': 'len(initializers) == 9 and len(prelude) == 48',
        'len(text) == 18': 'len(text) == 27',
        'group, = stored["groups"]': 'group, = (g for g in stored["groups"] if g["block"] == 129)',
        'len(records) == 18': 'len(records) == 27',
        'route=1, version="revised_English", source_block=89, fixture_block=42':
            'route=2, version="revised_English", source_block=129, fixture_block=22',
        "Prepared 18 original Hodram speech commands behind the verified opening prelude.":
            "Prepared 27 original Amsterdam speech commands behind the verified opening prelude.",
    })
    scope = vars(workflow) | globals()
    exec(compile(source, __file__ + "::amsterdam_scene_fixture", "exec"), scope)
    scope["prepare"]()


def capture():
    source = checked_text(Path(runner.__file__).read_text(encoding="utf-8"), {
        "ROOT=Path('work/analysis/Hodram_scene_runs_v8280')": "ROOT=OUTPUT",
        "FIXTURES=Path('work/analysis/Hodram_scene_fixtures_v8279/six_complete_clean_revised_SC1_scripts_original_Hodram_prelude_fixtures.json')":
            "FIXTURES=MANIFEST",
        "choices=[1]": "choices=[2]",
        "choices=[137,45,46]": "choices=[129]",
        "frames={137:24001,45:10001,46:16001}[block]": "frames=FRAME_LIMIT",
        "cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Hodram_B{block}_route{route}_{version}_v8280'": "cap=folder/'capture'",
        "work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json":
            "work/analysis/movie_viewport_v303/lil_start_inputs.json",
    })
    previous = sys.argv
    try:
        sys.argv = [__file__, "--route", "2", "--block", "129", "--version", "revised_English"]
        scope = dict(__file__=__file__, __name__="__main__", OUTPUT=ROOT, MANIFEST=FIXTURES, FRAME_LIMIT=FRAMES)
        exec(compile(source, __file__ + "::amsterdam_controller_replay", "exec"), scope)
    finally:
        sys.argv = previous


def startup():
    FunctionType(startup_workflow.startup.__code__, vars(startup_workflow) | globals())()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "startup"))
    globals()[parser.parse_args().action]()
