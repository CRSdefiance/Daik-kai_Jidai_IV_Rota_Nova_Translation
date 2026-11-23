"""Replay representative pages of Rafael's reading and Maria's training and convoy scenes."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_all_routes_next_review_wraps_20261118 as previous
from scripts import stage_all_routes_remaining_phrase_wraps_20261118 as stage
from scripts import verify_all_routes_remaining_phrase_wraps_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
regional, rafael, template = previous.regional, previous.rafael, previous.template
ROOT = stage.ROOT / "initialized_replays"
LIVE = ROOT / "replay.json"
R_ROOT, M_ROOT = ROOT / "rafael", ROOT / "maria"
ROM = R_ROOT / "Rafael_Arabian_Nights_RESEARCH_ONLY.nds"
MARIA_ROM = M_ROOT / "Maria_Sword_Training_And_Convoy_RESEARCH_ONLY.nds"
SETUP, MARIA_SETUP = R_ROOT / "rafael_fixture.json", M_ROOT / "maria_fixture.json"
RAFAEL = ((317, (100, 103, 107)), (318, (137, 141, 146, 151, 160)))
MARIA = ((200, (12, 15, 18, 21)), (208, (40, 43, 46)))


def prepare():
    FunctionType(rafael.prepare.__code__, vars(rafael) | globals())("rafael")
    FunctionType(regional.prepare.__code__, vars(regional) | globals())("maria")


def capture_rafael():
    FunctionType(rafael.capture.__code__, vars(rafael) | globals())("rafael")


def capture_maria():
    FunctionType(regional.capture.__code__, vars(regional) | globals())("maria")


old_assertions = '''    assert len(observed) == 10
    for owner in ("DK4_MES_B116_R0041", "DK4_MES_B116_R0051"):
        first, = [i for i, row in enumerate(observed) if row["id"] == owner]
        assert observed[first + 1]["id"] == owner + "_P2"
    strictness, = [row for row in observed if row["id"] == "DK4_MES_B116_R0024"]
    assert strictness["page"] == 1 and b"about rewards and punishments." in bytes.fromhex(strictness["body_hex"])'''
new_assertions = '''    assert len(observed) == 7
    for record, phrase in (("DK4_MES_B200_R0015", b"You've got to keep your nerve."),
                           ("DK4_MES_B208_R0043", b"The convoy managed to escape.")):
        index, = [i for i, row in enumerate(observed) if row["id"] == record]
        row = observed[index]
        assert row["page"] == 1 and phrase in bytes.fromhex(row["body_hex"])
        assert observed[index + 1]["page"] == 1 and observed[index + 1]["frame"] > row["frame"]'''
source = checked_text(getsource(previous.verify), {
    old_assertions: new_assertions,
    "both_FE_page_transitions_observed": "training_and_convoy_advance_in_one_page",
})
env = vars(previous) | globals()
exec(compile(source, __file__ + "::initialized-page-count", "exec"), env)

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture_rafael", "capture_maria", "verify"))
    env[parser.parse_args().action]()
