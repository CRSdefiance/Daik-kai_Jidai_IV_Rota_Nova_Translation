"""Register the scoped battle-dialogue updates and exact clean-input patch."""

from pathlib import Path
from types import SimpleNamespace

from scripts import audit_battle_dialogue_followup_20261119 as game
from scripts import register_sea_hazard_dialogue_20261119 as parent
from scripts import stage_battle_dialogue_followup_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-battle-dialogue-followup-v1-20261119"
ROOT = Path("out/battle_dialogue_followup_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Battle_Dialogue_Followup_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_battle_dialogue_followup_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_battle_dialogue_registered_20261119.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
CHECKPOINT = "The battle-dialogue candidate is registered with four revisions, 25 retentions and a verified First Mate confirmation and cancel path."
verified = SimpleNamespace(PROOF=stage.PROOF, LIVE=game.PROOF)
DRAFTS = [Path("work") / name / stage.ROM.name for name in
          ("battle_dialogue_followup_20261119", "battle_dialogue_followup_20261119_v2",
           "battle_dialogue_followup_20261119_v3")]

verification = checked_text(parent.verification, {
    '== ["whirlpool_sighting", "whirlpool_contact"]': '== ["madeira_cancel"]',
    '== [0, 1]': '== [1]',
    'assert all(r["selector_restored"] for r in playback["outcomes"])':
        'assert all(r["original_cancel_transition"] for r in playback["outcomes"])',
    '{2409}': '{2129}',
    'len(records) == 61 and len(changed) == 12': 'len(records) == 29 and len(changed) == 4',
})
publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 895 and len(manifest["checks"]) == 230':
        'len(manifest["batches"]) == 896 and len(manifest["checks"]) == 231',
    "release_stack_before_sea_hazard_dialogue.json": "release_stack_before_battle_dialogue_followup.json",
    "release_stack_with_sea_hazard_dialogue.json": "release_stack_with_battle_dialogue_followup.json",
    "verified_fleet_encounter_dialogue_predecessor": "verified_sea_hazard_dialogue_predecessor",
    "sea_hazard_dialogue_release": "battle_dialogue_followup_release",
    "registered_sea_hazard_dialogue_and_complete_parent_inverse": "registered_battle_dialogue_followup_and_complete_parent_inverse",
    "sea_hazard_dialogue_pipeline": "battle_dialogue_followup_pipeline",
    "prose_revisions=12, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=49":
        "prose_revisions=4, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=25",
    "text_display_revisions=12": "text_display_revisions=4",
    "initialized_whirlpool_sighting_and_contact=True": "initialized_Madeira_first_mate_confirmation_and_cancel=True",
    "previously_localized_records=61": "previously_localized_records=29",
    'ledger["sea_hazard_dialogue_20261119"]': 'ledger["battle_dialogue_followup_20261119"]',
    'candidates = [ROM, stage.ROM, DRAFT_ROM, stage.ROOT / "clean_rebuilt.nds"]':
        'candidates = [ROM, stage.ROM, *DRAFTS, stage.ROOT / "clean_rebuilt.nds"]',
    "Preserve sea-hazard ROM or clean reconstruction": "Preserve battle-dialogue ROM or clean reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Battle dialogue test candidate

The [local ROM](../../{ROM.as_posix()}) carries the revised First Mate attack confirmation, ram impact and flagship defeat dialogue, along with the preceding cumulative fixes.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 {candidate} byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Battle dialogue registered

The 29-record review compares ram impacts, town attack confirmation, flagship defeat and special-target victory with the clean Japanese. Four revisions keep the rough side-impact report together, distinguish the more formal First Mate and preserve the difference between a defeated flagship and an explicit sinking. All 25 retentions have individual reasons. [Exact review ledger](../{REVIEW.as_posix()})

The 66 original portrait cases checked stored text, substitutions and complete glyphs. Eight revised pages passed direct visual review. The emulator selected “May we strike Madeira?” from the original First Mate table, rendered the complete question and returned to target selection on cancel. The replay supplied the established position and one existing First Mate assignment. The other three changed lines received offline checks. Earlier traces identify the independent allied no-target panel and leave other possible callers of stored COMMON 300 and 304 open. [Emulator evidence](../{(VERIFY / 'madeira_confirmation_replay.png').as_posix()})

The patch reconstructs the ROM byte for byte. Six startup holds, 24 protected name getters and 34 focused tests passed. All 114 accepted layers and the ASCII right-bound correction carry forward. The 276 pending shared payloads and locations pass exact checks. All 29 variants already had editorial credit. The ledger remains at 27,700. Main awaits acceptance. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
