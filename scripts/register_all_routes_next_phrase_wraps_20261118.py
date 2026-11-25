"""Register the revised phrases across the four routes on the cumulative candidate."""

from pathlib import Path

from scripts import register_rafael_next_phrase_wraps_20261118 as parent
from scripts import replay_all_routes_next_phrase_wraps_20261118 as replay
from scripts import stage_all_routes_next_phrase_wraps_20261118 as stage
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-contextual-phrase-review-v1-20261118"
ROOT = Path("out/all_routes_contextual_phrase_review_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Contextual_Phrase_Review_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_contextual_phrase_review_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_all_routes_contextual_phrase_review_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"

bind = checked_text(parent.bind, {
    "len(retentions) == 118": "len(retentions) == 136",
    "initialized Rafael excerpt replay": "initialized Lil or Maria excerpt replay",
})
verify = checked_text(parent.verify, {
    'live["initialized_Rafael"] and live["exact_original_commands"] and live["picador_transition_and_trade_lesson_observed"]':
        'live["initialized_Lil_and_Maria"] and live["exact_original_commands"] and live["actual_company_names_and_shared_accusation"]',
    'len(live["holds"]) == 10': 'len(live["holds"]) == 13',
    'native_proof["revision_count"] == 14 and native_proof["fresh_page_count"] == 14 and native_proof["retention_count"] == 118':
        'native_proof["revision_count"] == 15 and native_proof["fresh_page_count"] == 21 and native_proof["retention_count"] == 136',
    'for item in r["layouts"]) == 14': 'for item in r["layouts"]) == 21',
    '    assert native_proof["native_runtime_assets_byte_identical"]':
        '    assert native_proof["native_runtime_assets_byte_identical"]\n'
        '    reused = native_proof["dependency_exact_reuse"]\n'
        '    assert base.digest(reused["path"]) == reused["sha256"]\n'
        '    assert (reused["revised_pages"], reused["retained_records"]) == (13, 136)\n'
        '    assert len(native_proof["refreshed_punctuation_records"]) == 2',
    'len(draft["records"]) == 132': 'len(draft["records"]) == 151',
    '{"revision": 14, "retention": 118}': '{"revision": 15, "retention": 136}',
    '{"prose": 14, "retention": 118}': '{"prose": 14, "wrap": 1, "retention": 136}',
    'len(draft["resolved_wrap_leads"]) == 8': 'len(draft["resolved_wrap_leads"]) == 13',
})
publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
pins = publish[publish.index("    candidates = ["):publish.index("    for path in candidates:")]
main = checked_text(publish, {
    'len(manifest["batches"]) == 879 and len(manifest["checks"]) == 214':
        'len(manifest["batches"]) == 880 and len(manifest["checks"]) == 215',
    "replay.LIVE, replay.SETUP, args.visual_review":
        "replay.LIVE, replay.LIL_SETUP, replay.MARIA_SETUP, args.visual_review",
    "release_stack_before_rafael_trade_lesson_and_scenes.json": "release_stack_before_contextual_phrase_review.json",
    "release_stack_with_rafael_trade_lesson_and_scenes.json": "release_stack_with_contextual_phrase_review.json",
    "verified_rafael_early_phrase_wraps_predecessor": "verified_rafael_trade_lesson_and_scenes_predecessor",
    "rafael_trade_lesson_and_scenes_release": "all_routes_contextual_phrase_review_release",
    "registered_rafael_trade_lesson_and_scenes_and_complete_parent_inverse":
        "registered_all_routes_contextual_phrase_review_and_complete_parent_inverse",
    "rafael_trade_lesson_and_scenes_pipeline": "all_routes_contextual_phrase_review_pipeline",
    "prose_revisions=14, wrap_only_revisions=0, justified_retentions=118":
        "prose_revisions=14, wrap_only_revisions=1, justified_retentions=136",
    "text_display_revisions=14, pagination_fixes=0": "text_display_revisions=15, pagination_fixes=0",
    "initialized_Rafael_trade_lesson_and_scenes_excerpts": "initialized_Lil_and_Maria_phrase_excerpts",
    "Julio's trading lesson and seven other Rafael exchanges have passed the dialogue and wrap review.":
        "Thirteen wrap leads and their dialogue exchanges are reviewed across all four routes.",
    "rafael_trade_lesson_and_scenes_20261118": "all_routes_contextual_phrase_review_20261118",
    "existing_credit=132": "existing_credit=151",
    "Preserve Rafael dialogue ROM or replay fixture": "Preserve all-routes phrase review ROM or replay fixture",
    pins: '''    candidates = [ROM, stage.ROM, replay.LIL_ROM, replay.MARIA_ROM, stage.ROOT / "clean_rebuilt.nds"]
    earlier = stage.ROOT.with_name("research_v1")
    candidates.extend(earlier / path.relative_to(stage.ROOT) for path in
                      (stage.ROM, replay.LIL_ROM, replay.MARIA_ROM, stage.ROOT / "clean_rebuilt.nds"))
''',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# All-routes contextual phrase review test candidate

The [local ROM](../../{ROM.as_posix()}) includes the cumulative work through the latest Rafael, Hodram, Lil and Maria exchanges.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Natural scene activation and hardware remain unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# All-routes contextual phrase review

Reviewed 151 turns in 12 story blocks across the four routes. The ledger records 14 wording revisions, one reflow and 136 exact retentions. The batch resolves 13 flagged wraps. Aziza's crew makes the same two accusations in Lil's and Maria's routes, with the native company-name substitution and the Bloodstained Shamshir title intact. Hodram's reply keeps the distinction between confidence and a bluff, and Maria's rush to help Lil uses the existing wording with cleaner breaks. [Exact review ledger](../{REVIEW.as_posix()})

The original renderer verified all 15 revised pages, six additional company-name-width pages and the 136 exact retentions. All 21 revised and stress pages received direct visual review. The proof binds 13 unchanged revised pages and 136 retentions to identical commands, plans and renderer assets. The remaining eight pages were rendered again after moving the company name inside the sentence to avoid a doubled period. Initialized Lil and Maria excerpts matched 13 complete panels. They show both default company names in the Shamshir accusation, the map's regional Proof title and Camille's reference to Maria. Maria used the existing system-only unlock. The Rafael and Hodram pages received offline checks. Natural activation, combat, quest effects and hardware remain unverified. [Native layout sheets](../{(VERIFY / 'before_after_1.png').as_posix()}) · [Lil excerpt](../{(VERIFY / 'lil_live_1.png').as_posix()}) · [Maria excerpt](../{(VERIFY / 'maria_live_1.png').as_posix()})

The clean-input patch reconstructs the candidate byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. Six startup holds, 24 protected name getters and 32 targeted tests passed. The 151 turns already had credit. The ledger stands at 27,700 with 276 stored shared keys open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
for source, label in ((bind, "exact-records"), (verify, "release-gates"), (main, "register")):
    exec(compile(source, __file__ + "::" + label, "exec"), env)

if __name__ == "__main__":
    env["main"]()
