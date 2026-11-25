"""Replay the dialogue, page transitions and signed letter in Rafael's initialized route."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_story_phrase_continuity_20261118 as precedent
from scripts import stage_story_followup_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
ROOT = stage.ROOT / "initialized_replay"
R_ROOT = ROOT / "rafael"
ROM, SETUP = R_ROOT / "Rafael_Followup_Excerpts_RESEARCH_ONLY.nds", R_ROOT / "rafael_fixture.json"
LIVE = ROOT / "replay.json"
RAFAEL = ((152, (128, 131, 136)), (163, (23, 32, 40)), (221, (27, 30, 33)), (249, (27, 31, 34)))

env = vars(precedent) | globals()
for fn, edits in ((precedent.prepare, {"6526 if route == 0": "7601 if route == 0"}),
                  (precedent.capture, {"SETUP, 6701": "SETUP, 7951"})):
    exec(compile(checked_text(getsource(fn), edits), __file__ + "::exact-excerpts", "exec"), env)


def verify():
    assert not LIVE.exists()
    matcher = precedent.earlier.verify_one
    verifier = FunctionType(matcher.__code__, matcher.__globals__ | {"stage": stage})
    result = verifier(R_ROOT, ROM, SETUP, "Rafael", "Castor", 12)
    assert result["candidate_sha256"] == base.digest(stage.ROM)
    holds = {row["id"]: row for row in result["holds"]}
    assert len(holds) == 12
    assert all(holds[key]["page"] == 1 for key in ("DK4_MES_B221_R0027", "DK4_MES_B249_R0031"))
    assert holds["DK4_MES_B221_R0030"]["frame"] > holds["DK4_MES_B221_R0027"]["frame"]
    assert holds["DK4_MES_B249_R0034"]["frame"] > holds["DK4_MES_B249_R0031"]["frame"]
    assert b"the King of Spain?" in bytes.fromhex(holds["DK4_MES_B152_R0131"]["body_hex"])
    base.save(LIVE, result | dict(exact_page_transitions=True, unmodified_letter_signature=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("prepare", "capture", "verify"))
    action = cli.parse_args().action
    verify() if action == "verify" else env[action]("rafael")
