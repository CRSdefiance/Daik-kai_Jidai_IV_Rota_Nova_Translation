"""Replay Rafael's natural New Game departure and original guided preparation."""

from argparse import ArgumentParser
from pathlib import Path
import sys
from types import FunctionType

from scripts import replay_ceuta_lesson_20261119 as startup_template
from scripts import run_Rafael_B45_scenes_v7893 as runner
from scripts import stage_rafael_first_voyage_debrief_20261119 as build
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "ordinary_opening"
STARTUP = build.ROOT / "startup_fixture"
SETUP = build.ROOT / "ordinary_opening_setup.json"
FRAMES = 27801


def capture():
    assert not ROOT.exists() and not SETUP.exists()
    stored = base.load(build.PROOF)
    assert base.digest(build.ROM) == stored["candidate_sha256"]
    filename = "/data/SC0.DK4"
    item, = (g for g in stored["groups"] if g["block"] == 44)
    assert item["file_path"] == filename and len(item["commands"]) > 117
    image = base.NdsImage.open(build.ROM)
    block = native.IlnkContainer.parse(image.read_file(filename)).blocks[44]
    assert native.digest(block) == item["after"]
    base.save(SETUP, dict(candidate_sha256=stored["candidate_sha256"], original_new_game_opening=True,
        fixtures=[dict(route=0, version="English", research_ROM=str(build.ROM), research_ROM_sha256=base.digest(build.ROM),
                       source_file=filename, source_block=44, fixture_block=44,
                       original_opening_prelude_commands=item["commands"][:10])]))
    source = checked_text(Path(runner.__file__).read_text(encoding="utf-8"), {
        "ROOT=Path('work/analysis/Rafael_B45_scene_runs_v7893')": "ROOT=ACTIVE_ROOT",
        "FIXTURES=Path('work/analysis/Rafael_B45_scene_fixtures_v7892/two_complete_source_English_original_Rafael_prelude_fixtures.json')":
            "FIXTURES=ACTIVE_SETUP",
        "cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Rafael_B45_route{route}_{version}_v7893'":
            "cap=folder/'capture'",
        "range(4000,15501,240)": "range(4000,FRAME_LIMIT-300,165)",
        "range(2350,16001,60))|{16000}": "range(2350,FRAME_LIMIT,55))|{FRAME_LIMIT-1}",
        "original_exchange_commands=24,original_exchange_speeches=12":
            "original_exchange_commands=OPENING_COMMANDS,original_exchange_speeches=115",
        "disclosed_ROM_entry_fixture_not_natural_optional_activation_ororiginal_location=True":
            "original_natural_New_Game_entry=True",
        "not_natural_optional_activation_location_earned_progress_full_route_orhardware_coverage=True":
            "native_New_Game_opening_only=True",
        "'16001'": "str(FRAME_LIMIT)",
        "16001": "FRAME_LIMIT",
    })
    scope = dict(__name__="__main__", __file__=__file__, ACTIVE_ROOT=ROOT, ACTIVE_SETUP=SETUP,
                 FRAME_LIMIT=FRAMES, OPENING_COMMANDS=len(item["commands"]))
    previous = sys.argv
    try:
        sys.argv = [__file__, "--route", "0", "--version", "English"]
        exec(compile(source, __file__ + "::ordinary-opening-replay", "exec"), scope)
    finally:
        sys.argv = previous


def startup():
    FunctionType(startup_template.startup.__code__, vars(startup_template) | {"build": build, "STARTUP": STARTUP})()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("capture", "startup"))
    globals()[parser.parse_args().action]()
