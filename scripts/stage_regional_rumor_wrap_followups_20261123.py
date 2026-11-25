"""Reflow the two Square rumors identified during ordinary regional visits."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_hodram_b261_b310_wrap_fixes_20261123 as parent
from scripts import stage_square_rumor_followup_20261122 as prior
from scripts import verify_current_regional_towns_20261123 as observed
from scripts.source_locked_derivation_v5118 import checked_text


base, native, town, CLEAN, ARM, COMMON = parent.base, parent.native, prior.town, prior.CLEAN, prior.ARM, prior.COMMON
ROOT = Path(".codex-release-work/regional_rumor_wrap_followups_20261123/staged")
ROM, PROOF = ROOT / "Regional_Rumor_Wrap_Followups_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
WITNESSES = ROOT / "ordinary_town_replays"
HOLDS = prior.HOLDS
PROSE = {
    714: "Spain's navy is a formidable sight under Admiral Valdes. That's why they call it the Invincible Armada.",
    715: "Back then, the Centurione Company traded far and wide. Their ships sailed all over the Mediterranean, as if they owned it.",
}
PHRASES = {
    714: "they call it the Invincible Armada.",
    715: "as if they owned it.",
}
NOTES = prior.NOTES | {
    710: "Keep the speaker's surprise about women sailing to trade and the separate exclamation about changing times.",
    713: "Keep the shopkeeper's hearsay about Albuquerque's ancestor, his naval reputation and the Indian Ocean.",
    714: "The shopkeeper links Spain's admiral and formidable fleet to the Invincible Armada nickname. Keep the complete naming clause on one row.",
    715: "Back then fits the shopkeeper's familiar account of former trade. Keep the Mediterranean cruise and end on the complete figurative comparison.",
}

source = checked_text(getsource(prior.stage), {
    '    prior = base.load(earlier.MANUSCRIPT)':
        '    observed_review = base.load(observed.OUT)\n'
        '    assert observed_review["candidate_sha256"] == previous["candidate_sha256"]\n'
        '    findings = {"valencia": 714, "syracuse": 715}\n'
        '    for city, key in findings.items():\n'
        '        held, = [r for r in observed_review["town_visits"][city]["verified_common"] if r["message_ID"] == key]\n'
        '        assert held["installed_hex"] == before[key].text.hex() and held["source_hex"] == sources[key].text.hex()\n'
        '    prior = base.load(earlier.MANUSCRIPT)',
    'assert old[n]["source_hex"] == source.text.hex() and old[n]["staged_hex"] == current.text.hex()':
        'assert old[n]["source_hex"] == source.text.hex()',
    'all(len(v)>9 for v in lines)':
        'all(len(v) > 15 for v in lines) and any(PHRASES[n] in line for line in lines)',
    '    ROOT.mkdir()': '    ROOT.mkdir(parents=True)',
    'unchanged_wrap_leads=[710,713]':
        'unchanged_wrap_leads=[], ordinary_discovery_sha256=base.digest(observed.OUT),\n'
        '        regional_display_dispatch_unchanged=True',
    'all three revised pages': 'both revised pages',
})
scope = vars(prior) | globals()
exec(compile(source, __file__ + "::regional-rumor-stage", "exec"), scope)
replay = FunctionType(prior.replay.__code__, scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup", *HOLDS))
    action = cli.parse_args().action
    if action == "stage":
        scope["stage"]()
    elif action in HOLDS:
        replay(action)
    else:
        step = getattr(prior.release_tools, action)
        FunctionType(step.__code__, step.__globals__ | globals())()
