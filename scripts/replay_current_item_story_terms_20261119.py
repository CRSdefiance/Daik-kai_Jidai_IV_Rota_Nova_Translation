"""Replay the complete Glassmaking Guide handover behind Rafael's opening."""
from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_rafael_sailing_modes_20261119 as lesson
from scripts import replay_rafael_contract_and_proof_20261119 as fixture_workflow
from scripts import replay_story_market_terms_20261119 as startup_workflow
from scripts import stage_current_item_story_terms_20261119 as build
from scripts.source_locked_derivation_v5118 import checked_text

base=build.base
ROOT=build.ROOT/"glassmaking_replay"
FIXTURE=ROOT/"Rafael_Glassmaking_Guide_RESEARCH_ONLY.nds"
FIXTURES=ROOT/"fixtures.json"
STARTUP=build.ROOT/"startup_fixture"
STARTUP_PROOF=build.ROOT/"own_startup_verification.json"
FRAMES=10801


def prepare():
    source=checked_text(getsource(lesson.prepare),{
        "(44, 46)":"(44, 214)",
        "len(commands) == 47 and len(speeches) == 24":"len(commands) == 36 and len(speeches) == 19",
        'group, = stored["groups"]':'group, = (g for g in stored["groups"] if g["route"] == 0 and g["block"] == 214)',
        'assert [r["label"] for r in menu] == ["Please do.", "No, thanks."]':"assert not menu",
        "len(records) == 24 and len(command_ids) == 37":"len(records) == 19 and len(command_ids) == 26",
        "research_ROM_sha256=base.digest(FIXTURE), original_menu_records=menu,":
           "research_ROM_sha256=base.digest(FIXTURE), original_menu_records=menu,\n"
           "            source_block=214, fixture_block=44, original_opening_prelude_commands=commands[:10],",
        "Original block 46 runs after the preserved block 44 New Game prelude.":
           "The original Glassmaking Guide scene runs after the Rafael New Game prelude.",
        "Prepared the entire sailing tutorial behind the original Rafael prelude.":
           "Prepared the complete original Glassmaking Guide scene.",
    })
    scope=vars(lesson)|globals()|{"stage":build}
    exec(compile(source,__file__+"::glassmaking_guide_fixture","exec"),scope)
    scope["prepare"]()


def capture():
    source=checked_text(getsource(fixture_workflow.capture),{
        '        "16001": "FRAME_LIMIT",':
           '        "16001": "FRAME_LIMIT",\n'
           '        "original_exchange_commands=24,original_exchange_speeches=12":\n'
           '            "original_exchange_commands=26,original_exchange_speeches=19",',
    })
    scope=vars(fixture_workflow)|globals()
    exec(compile(source,__file__+"::glassmaking_guide_capture","exec"),scope)
    scope["capture"]()


def startup():
    FunctionType(startup_workflow.startup.__code__,vars(startup_workflow)|globals())()


if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("prepare","capture","startup"))
    globals()[parser.parse_args().action]()
