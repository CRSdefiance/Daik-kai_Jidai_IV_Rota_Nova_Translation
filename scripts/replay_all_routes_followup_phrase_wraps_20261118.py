"""Verify the new pages in initialized Hodram and Lil excerpts."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_all_routes_next_phrase_wraps_20261118 as scenes
from scripts import replay_rafael_early_phrase_wraps_20261118 as service
from scripts import replay_regional_proof_dialogue_20261118 as lil_fixture
from scripts import replay_story_phrase_continuity_20261118 as hodram_fixture
from scripts import replay_story_tag_wraps_20261118 as masks
from scripts import stage_all_routes_followup_phrase_wraps_20261118 as stage

base, native = stage.base, stage.native
ROOT = stage.ROOT / "initialized_replays"
LIVE = ROOT / "replay.json"
H_ROOT, L_ROOT = ROOT / "hodram", ROOT / "lil"
HODRAM_ROM = H_ROOT / "Hodram_Dialogue_Followup_RESEARCH_ONLY.nds"
LIL_ROM = L_ROOT / "Lil_Dialogue_Followup_RESEARCH_ONLY.nds"
HODRAM_SETUP, LIL_SETUP = H_ROOT / "hodram_fixture.json", L_ROOT / "lil_fixture.json"
HODRAM = ((17, (225, 229, 232)), (79, (90,)), (91, (27, 31, 61)), (238, (44,)))
LIL = ((66, (105, 109, 113, 128)), (72, (98, 101, 115)))


def fixture(route, action):
    template = hodram_fixture if route == "hodram" else lil_fixture
    FunctionType(getattr(template, action).__code__, vars(template) | globals())(route)


def patch():
    FunctionType(service.patch.__code__, vars(service) | {"stage": stage})()


def startup():
    FunctionType(service.startup.__code__, vars(service) | {"stage": stage})()


def verify():
    assert not LIVE.exists()
    tool = FunctionType(masks.verify_one.__code__, vars(masks) | {"stage": stage})
    h = tool(H_ROOT, HODRAM_ROM, HODRAM_SETUP, "Hodram", "Bergstrom", 8)
    l = tool(L_ROOT, LIL_ROM, LIL_SETUP, "Lil", "Argot", 7)
    assert h["candidate_sha256"] == l["candidate_sha256"] == base.digest(stage.ROM)
    assert h["exact_native_panel_masks"] and l["exact_native_panel_masks"]
    hodram, lil = map(base.load, (HODRAM_SETUP, LIL_SETUP))
    assert hodram["exact_ROM_inverse"] and hodram["original_excerpt_commands_preserved"]
    assert lil["whole_source_ROM_inverse"] and lil["exact_original_commands"]
    letter = h["holds"][-1]
    assert letter["id"] == "DK4_MES_B238_R0044" and letter["page"] == 1
    assert b"The convoy managed to escape." in bytes.fromhex(letter["body_hex"])
    assert [r["id"] for r in l["holds"][:4]] == [f"DK4_MES_B66_R{i:04}" for i in (105, 109, 113, 128)]
    assert bytes.fromhex(l["holds"][3]["body_hex"]).strip() == b"Dad!"
    evidence = h["evidence"] | l["evidence"]
    evidence.update({str(p): base.digest(p) for p in (HODRAM_ROM, LIL_ROM, h["receipt"], l["receipt"])})
    base.save(LIVE, dict(candidate_sha256=h["candidate_sha256"], initialized_Hodram_and_Lil=True,
        exact_original_commands=True, convoy_letter_and_camille_exchange_observed=True,
        natural_activation=False, hardware=False, holds=h["holds"] + l["holds"],
        sheets=h["sheets"] + l["sheets"], evidence=evidence))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("prepare", "capture", "patch", "startup", "verify"))
    cli.add_argument("route", nargs="?", choices=("hodram", "lil"))
    args = cli.parse_args()
    if args.action in ("prepare", "capture"):
        assert args.route
        fixture(args.route, args.action)
    else:
        globals()[args.action]()
