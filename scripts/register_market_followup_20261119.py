"""Register the updated Market dialogue and exact clean-input patch."""

from pathlib import Path
from types import SimpleNamespace

from scripts import audit_market_followup_20261119 as game
from scripts import register_battle_dialogue_followup_20261119 as parent
from scripts import stage_market_followup_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-market-followup-v1-20261119"
ROOT = Path("out/market_followup_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Market_Followup_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_market_followup_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_market_followup_registered_20261119.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
CHECKPOINT = "The Market follow-up is registered with four revisions, 18 retentions and a verified recommendation, instructions and farewell."
verified = SimpleNamespace(PROOF=stage.PROOF, LIVE=game.PROOF)

verification = checked_text(parent.verification, {
    '== ["madeira_cancel"]': '== ["market_recommendation"]',
    '== [1]': '== [3]',
    'assert all(r["original_cancel_transition"] for r in playback["outcomes"])':
        'assert all(r["original_return_screen_matches"] for r in playback["outcomes"])',
    '{2129}': '{775}',
    'len(records) == 29 and len(changed) == 4': 'len(records) == 22 and len(changed) == 4',
})
publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 896 and len(manifest["checks"]) == 231':
        'len(manifest["batches"]) == 897 and len(manifest["checks"]) == 232',
    "release_stack_before_battle_dialogue_followup.json": "release_stack_before_market_followup.json",
    "release_stack_with_battle_dialogue_followup.json": "release_stack_with_market_followup.json",
    "verified_sea_hazard_dialogue_predecessor": "verified_battle_dialogue_followup_predecessor",
    "battle_dialogue_followup_release": "market_followup_release",
    "registered_battle_dialogue_followup_and_complete_parent_inverse": "registered_market_followup_and_complete_parent_inverse",
    "battle_dialogue_followup_pipeline": "market_followup_pipeline",
    "justified_retentions=25": "justified_retentions=18",
    "initialized_Madeira_first_mate_confirmation_and_cancel=True": "initialized_Market_recommendation_and_return=True",
    "previously_localized_records=29": "previously_localized_records=22",
    'ledger["battle_dialogue_followup_20261119"]': 'ledger["market_followup_20261119"]',
    'candidates = [ROM, stage.ROM, *DRAFTS, stage.ROOT / "clean_rebuilt.nds"]':
        'candidates = [ROM, stage.ROM, stage.ROOT / "clean_rebuilt.nds"]',
    "Preserve battle-dialogue ROM or clean reconstruction": "Preserve Market follow-up ROM or clean reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Market follow-up test candidate

The [local ROM](../../{ROM.as_posix()}) carries the revised investment, market-share favor, letter of recommendation and extra-reward dialogue, along with the previous cumulative fixes.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 {candidate} byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Market follow-up registered

Twenty-two Market records were compared with the clean Japanese and their original reactions and follow-ups. Four revisions give the trader's flattery and investment question their own lines, keep market share together and smooth the recommendation and extra-reward offers. Eighteen retentions preserve the contract requirement, refusal and thank-you branches, and the distinct uses of the two letters. [Exact review ledger](../{REVIEW.as_posix()})

All 23 format cases passed, including the two original facility-name substitutions. The four revised pages passed direct visual review. A focused emulator replay rendered the full recommendation, its instructions and the trader's farewell, then matched the original town screen after leaving the Market. The terminal frame differed only within the selected Port label highlight. The replay used the established cargo, share, demand and qualification inputs. The other three revisions received offline checks. COMMON 750–752 remain open for other callers. [Replay](../{(VERIFY / 'market_reward_replay.png').as_posix()})

The clean-input patch reconstructs the cumulative candidate byte for byte. Six startup holds, 24 protected name getters and 34 focused tests passed. The release preserves 114 accepted layers, the ASCII right-bound correction and all 276 pending shared payloads and locations. All 22 records already had credit, so the tally remains at 27,700. Main awaits acceptance. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
