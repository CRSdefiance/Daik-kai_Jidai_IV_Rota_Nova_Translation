"""Register the shared sea-hazard dialogue and its byte-exact clean-input patch."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import audit_sea_hazard_dialogue_20261119 as game
from scripts import register_fleet_encounter_dialogue_20261119 as parent
from scripts import stage_sea_hazard_dialogue_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-sea-hazard-dialogue-v1-20261119"
ROOT = Path("out/sea_hazard_dialogue_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Sea_Hazard_Dialogue_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_sea_hazard_dialogue_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_sea_hazard_dialogue_registered_20261119.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
CHECKPOINT = "Shared weather and sea-hazard dialogue is registered with 12 revisions, 49 retentions and a verified whirlpool contact replay."
verified = SimpleNamespace(PROOF=stage.PROOF, LIVE=game.PROOF)
DRAFT_ROM = Path("work/sea_hazard_dialogue_20261119/Sea_Hazard_Dialogue_RESEARCH_ONLY.nds")

verification = checked_text(getsource(parent.verify), {
    '== ["dolphins", "sirens", "mermaid"]': '== ["whirlpool_sighting", "whirlpool_contact"]',
    'assert [len(r["observed"]) for r in playback["outcomes"]] == [3, 2, 2]':
        'assert [len(r["observed"]) for r in playback["outcomes"]] == [0, 1]',
    'prior_review["verified_shared_text_storage"]["sha256"]': 'prior_review["shared_storage_scope"]["evidence_sha256"]',
    '{449, 2366}': '{2409}',
    'len(records) == 46 and len(changed) == 10': 'len(records) == 61 and len(changed) == 12',
})
publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 894 and len(manifest["checks"]) == 229':
        'len(manifest["batches"]) == 895 and len(manifest["checks"]) == 230',
    "release_stack_before_fleet_encounter_dialogue.json": "release_stack_before_sea_hazard_dialogue.json",
    "release_stack_with_fleet_encounter_dialogue.json": "release_stack_with_sea_hazard_dialogue.json",
    "verified_rafael_sailing_modes_predecessor": "verified_fleet_encounter_dialogue_predecessor",
    "fleet_encounter_dialogue_release": "sea_hazard_dialogue_release",
    "registered_fleet_encounter_dialogue_and_complete_parent_inverse": "registered_sea_hazard_dialogue_and_complete_parent_inverse",
    "fleet_encounter_dialogue_pipeline": "sea_hazard_dialogue_pipeline",
    "changed_components=1": "changed_components=2",
    "prose_revisions=10, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=36":
        "prose_revisions=12, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=49",
    "text_display_revisions=10": "text_display_revisions=12",
    "initialized_dolphin_sirens_mermaid_replays=True": "initialized_whirlpool_sighting_and_contact=True",
    "previously_localized_records=46": "previously_localized_records=61",
    'ledger["fleet_encounter_dialogue_20261119"]': 'ledger["sea_hazard_dialogue_20261119"]',
    'candidates = [ROM, stage.ROM, stage.ROOT / "clean_rebuilt.nds"]':
        'candidates = [ROM, stage.ROM, DRAFT_ROM, stage.ROOT / "clean_rebuilt.nds"]',
    "Preserve fleet encounter ROM or clean reconstruction": "Preserve sea-hazard ROM or clean reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Sea-hazard dialogue test candidate

The [local ROM](../../{ROM.as_posix()}) carries the revised shared weather, whirlpool, reef and drift-ice dialogue and the preceding cumulative fixes.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Shared weather and sea-hazard dialogue registered

Reviewed 61 voice variants in their original sequences. Twelve revisions clarify the immediate danger or the equipment outcome and improve breaks around phrases such as “broke up the drift ice.” Forty-nine retentions preserve alarm, stammers, youthful images and distinct degrees of formality. [Exact review ledger](../{REVIEW.as_posix()})

All 61 portrait cases passed offline. Every revised page received a direct visual review. The first initialized emulator run showed the whirlpool sighting, the order to steer clear and the next port sighting. In a second run, moving one existing whirlpool contact zone onto the ship let the original collision handler display the complete revised line “Whoa! We're caught in the whirlpool!” The remaining 11 revised variants were checked offline. Natural event selection and hardware remain unverified. [Sighting](../{(VERIFY / 'whirlpool_sighting.png').as_posix()}) · [Contact](../{(VERIFY / 'whirlpool_contact.png').as_posix()})

The clean-input patch reconstructs the ROM byte for byte. Six startup holds, 24 protected name getters and 34 focused tests passed. The release preserves the accepted ASCII right-bound correction and binds all 276 pending shared records to their unchanged payloads and locations. All 61 reviewed variants already had credit, so the ledger remains at 27,700. Main awaits acceptance. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
