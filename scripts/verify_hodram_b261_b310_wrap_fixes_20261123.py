"""Verify the final Hodram wrap pages and retained native controls."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import stage_hodram_b261_b310_wrap_fixes_20261123 as staged
from scripts import verify_hodram_b221_b260_wrap_fixes_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text


stage = SimpleNamespace(**(vars(staged) | {"established": prior.stage.established, "typed": prior.stage.typed}))
base, native, gameplay = stage.base, stage.native, prior.gameplay
ROOT = stage.ROOT / "focused_gameplay"
LIVE, GLYPHS = ROOT / "verified_gameplay.json", stage.ROOT / "glyph_and_sheet_verification.json"
CHOICES, STYLES = stage.ROOT / "original_choice_tables.json", stage.ROOT / "original_style_alternatives.json"
ROLES = stage.ROOT / "speaker_roles.json"
MODAL_SAMPLES = {"DK4_MES_B274_R0030", "DK4_MES_B309_R0174"}
NOTES = {
    1: "Keep Hodram Bergstrom for the Swedish commander on both sides of the royal audience.",
    16: "Keep Gerhard Adernkatz for Hodram's officer and the cautious expedition companion.",
    18: "Keep Charles Rochefort for the crewman sourcing ingredients and reconsidering the expedition clues.",
    66: "Keep Jean Ramusio for the smuggler who disputes the guildmaster's accusation.",
    71: "Keep William Clive for the pirate brought in after the bounty.",
    120: "Keep Guard for the attendant who summons and greets Hodram at the royal court.",
    125: "Keep King for the Swedish monarch who explains the national purpose of the Proofs.",
    147: "Keep Guildmaster for the unnamed person commissioning the bounty and discussing William.",
    148: "Keep Guildmaster for the unnamed officeholder who gives the other bounties and rewards.",
    151: "Keep Sailor for the unnamed crew voice in the expedition dialogue.",
    179: "Keep Villager for the visitor who asks Hodram to find the ruins without revealing a personal name.",
    203: "Keep Sakura for the person inviting Hodram along and identifying the temple.",
}


def report(run):
    return ROOT / run / "capture/capture_report.json"


def samples():
    return {1: tuple((row["block"], int(row["id"].rsplit("R", 1)[1]))
                     for row in base.load(stage.REVIEW)["records"]
                     if row["decision"] == "revision" or row["id"] in MODAL_SAMPLES)}


route_rom = FunctionType(prior.route_rom.__code__, globals())
scope = prior.scope | globals()
for name in ("route_config", "replay", "verify_excerpts", "display_context", "panel_mask"):
    scope[name] = FunctionType(prior.scope[name].__code__, scope)

style_source = checked_text(getsource(prior.styles), {
    'prior.compiler': 'stage.established',
    'prior.typed': 'prior.prior.typed',
    'assert selector == 208': 'assert selector in (208, 211, 214, 215, 216, 218)',
    'len(records) == 37': 'len(records) == 115',
    'for r in records) == 40': 'for r in records) == 144',
    'Verified 37 retained personality variants and all 40 slot assignments.':
        'Verified 115 retained personality variants and all 144 slot assignments.',
})
exec(compile(style_source, __file__ + "::native-style-tables", "exec"), scope)

formatting_source = checked_text(getsource(prior.formatting), {
    "'len(records) == 50': 'len(records) == 16'": "'len(records) == 50': 'len(records) == 15'",
    'Verified 16 retained speakerless': 'Verified 15 retained speakerless',
    "'len(choices) == 8': 'len(choices) == 11'": "'len(choices) == 8': 'len(choices) == 7'",
    'all eleven original choice captions': 'all seven original choice captions',
    'prior.retained_panels': 'prior.prior.retained_panels',
    'prior.typed': 'prior.prior.typed',
    'prior.nameplates': 'prior.prior.nameplates',
    'prior.compiler': 'prior.prior.compiler',
})
exec(compile(formatting_source, __file__ + "::native-controls-verification", "exec"), scope)


def verify():
    observations, pictures, reports, exits = scope["verify_excerpts"]()
    sheets = []
    for offset in range(0, len(pictures), 6):
        path, digest = gameplay.make_sheet(ROOT / f"hodram_b261_b310_excerpts_{1 + offset // 6}.png", pictures[offset:offset + 6])
        sheets.append(dict(path=path, sha256=digest))
    changed = {r["id"] for r in base.load(stage.REVIEW)["records"] if r["decision"] == "revision"}
    assert changed | MODAL_SAMPLES == {r["id"] for r in observations} and len(observations) == 20
    base.save(LIVE, dict(candidate_sha256=base.digest(stage.ROM), observed_speech_pages=len(observations),
        observations=observations, original_menu_choices=[], report_sha256=reports, return_frames=exits, sheets=sheets,
        initialized_excerpts=True, natural_story_triggers_claimed=False, hardware=False))
    print("Verified 20 focused holds, the surname substitution, and the original opening host exit.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("formatting", "replay", "verify"))
    action = cli.parse_args().action
    scope["SAMPLES"] = samples()
    if action == "replay":
        scope["replay"](1)
    elif action == "formatting":
        scope["formatting"]()
    else:
        verify()
