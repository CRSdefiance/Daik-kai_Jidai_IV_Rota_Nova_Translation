"""Verify Rafael's initialized excerpts, cold boot, and clean-input reconstruction."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import replay_london_guild_assignments_20261118 as startup_probe
from scripts import replay_papal_states_titis_20261118 as prior
from scripts import replay_story_phrase_continuity_20261118 as excerpt
from scripts import replay_story_tag_wraps_20261118 as masks
from scripts import stage_rafael_early_phrase_wraps_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
ROOT = stage.ROOT / "initialized_replays"
R_ROOT = ROOT / "rafael"
ROM = R_ROOT / "Rafael_Early_Phrase_Excerpts_RESEARCH_ONLY.nds"
SETUP, LIVE = R_ROOT / "rafael_fixture.json", ROOT / "replay.json"
RAFAEL = ((0, (5, 10, 20)), (9, (36, 40)), (26, (259, 262)), (64, (333, 337)), (67, (9,)))


def patch():
    delta, rebuilt = stage.ROOT / "clean_input.xdelta", stage.ROOT / "clean_rebuilt.nds"
    assert not delta.exists() and not rebuilt.exists()
    make_xdelta(native.CLEAN, stage.ROM, delta)
    apply_xdelta(native.CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == stage.ROM.read_bytes()
    print(f"Exact clean-input reconstruction: {base.digest(rebuilt)}")


def prepare():
    FunctionType(excerpt.prepare.__code__, vars(excerpt) | globals())("rafael")


def capture():
    FunctionType(excerpt.capture.__code__, vars(excerpt) | globals())("rafael")


def verify():
    assert not LIVE.exists()
    result = FunctionType(masks.verify_one.__code__, vars(masks) | {"stage": stage})(
        R_ROOT, ROM, SETUP, "Rafael", "Castor", 10)
    assert result["candidate_sha256"] == base.digest(stage.ROM)
    assert result["exact_native_panel_masks"]
    identifiers = [row["id"] for row in result["holds"]]
    assert identifiers[0:3] == ["DK4_MES_B0_R0005", "DK4_MES_B0_R0010", "DK4_MES_B0_R0020"]
    assert identifiers[7:9] == ["DK4_MES_B64_R0333", "DK4_MES_B64_R0337"]
    assert b"Africa's Proof of Conquest!" in bytes.fromhex(result["holds"][0]["body_hex"])
    fixture = base.load(SETUP)
    assert fixture["initialized_route"] == 0 and fixture["exact_ROM_inverse"]
    assert fixture["original_excerpt_commands_preserved"]
    proof = result | dict(initialized_Rafael=True, exact_original_commands=True, hardware=False,
        natural_activation=False, early_proof_and_charlotte_reply_observed=True)
    proof["evidence"].update({str(p): base.digest(p) for p in (ROM, result["receipt"])})
    base.save(LIVE, proof)


def startup():
    FunctionType(startup_probe.startup.__code__, vars(startup_probe) | {"stage": stage})()


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("patch", "prepare", "capture", "verify", "startup"))
    globals()[cli.parse_args().action]()
