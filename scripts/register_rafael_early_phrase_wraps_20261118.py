"""Register the Rafael dialogue and wrap review with the cumulative candidate."""

from pathlib import Path

from scripts import register_papal_states_titis_20261118 as parent
from scripts import replay_rafael_early_phrase_wraps_20261118 as replay
from scripts import stage_rafael_early_phrase_wraps_20261118 as stage
from scripts import verify_rafael_early_phrase_wraps_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-rafael-early-phrase-wraps-v1-20261118"
ROOT = Path("out/rafael_early_phrase_wraps_registered_20261118_v1")
ROM = ROOT / "Translation_DS_Rafael_Early_Phrase_Wraps_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_rafael_early_phrase_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_early_phrase_wraps_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"

bind = checked_text(parent.bind, {
    "len(retentions) == 35": "len(retentions) == 148",
    "initialized Rafael or Maria excerpt replay": "initialized Rafael excerpt replay",
    '                    scope = "Native renderer and direct visual check"':
        '''                    diagnostics = proof["informational_source_row_differences"]
                    row["base_QA_issues"] = diagnostics
                    if diagnostics:
                        assert {d["code"] for d in diagnostics} == {"line-break-count"}
                        row["qa_waivers"] = ["line-break-count"]
                        row["qa_waiver_reason"] = (
                            row["localization_note"] + " The original renderer verified the complete revised "
                            "English in one page at its native width. The row-count warning compares against "
                            "the Japanese line count."
                        )
                    scope = "Native renderer and direct visual check"''',
})
verify = checked_text(parent.verify, {
    'live["initialized_Rafael_and_Maria"] and live["exact_original_commands"] and live["actual_given_name_substitutions"]':
        'live["initialized_Rafael"] and live["exact_original_commands"] and live["early_proof_and_charlotte_reply_observed"]',
    'len(live["holds"]) == 16': 'len(live["holds"]) == 10',
    'native_proof["revision_count"] == 49 and native_proof["fresh_page_count"] == 61 and native_proof["retention_page_count"] == 35':
        'native_proof["revision_count"] == 12 and native_proof["fresh_page_count"] == 12 and native_proof["retention_count"] == 148',
    "== 61": "== 12",
    '    assert native_proof["pagination_before_after"] == {}':
        '    assert native_proof["native_runtime_assets_byte_identical"]',
    'len(draft["records"]) == 84': 'len(draft["records"]) == 160',
    '{"revision": 49, "retention": 35}': '{"revision": 12, "retention": 148}',
    '{"prose": 44, "wrap": 5, "retention": 35}': '{"prose": 12, "retention": 148}',
    '    draft.update(approved_source25=bound, direct_visual_review=sheets)':
        '    assert len(draft["resolved_wrap_leads"]) == 8\n'
        '    draft.update(approved_source25=bound, direct_visual_review=sheets)',
})
publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 877 and len(manifest["checks"]) == 212':
        'len(manifest["batches"]) == 878 and len(manifest["checks"]) == 213',
    'stage.ROOT / "translation.xdelta"': 'stage.ROOT / "clean_input.xdelta"',
    "replay.LIVE, replay.SETUP, replay.MARIA_SETUP, args.visual_review":
        "replay.LIVE, replay.SETUP, args.visual_review",
    "release_stack_before_papal_states_titis.json": "release_stack_before_rafael_early_phrase_wraps.json",
    "release_stack_with_papal_states_titis.json": "release_stack_with_rafael_early_phrase_wraps.json",
    "verified_regional_proof_dialogue_predecessor": "verified_papal_states_titis_predecessor",
    "papal_states_titis_release": "rafael_early_phrase_wraps_release",
    "registered_papal_states_titis_and_complete_parent_inverse":
        "registered_rafael_early_phrase_wraps_and_complete_parent_inverse",
    "papal_states_titis_pipeline": "rafael_early_phrase_wraps_pipeline",
    "prose_revisions=44, wrap_only_revisions=5, justified_retentions=35":
        "prose_revisions=12, wrap_only_revisions=0, justified_retentions=148",
    "text_display_revisions=49, pagination_fixes=0": "text_display_revisions=12, pagination_fixes=0",
    "initialized_Rafael_and_Maria_papal_titis_excerpts": "initialized_Rafael_early_phrase_excerpts",
    'archives[f"/data/SC{i}.DK4"]': 'archives.get(f"/data/SC{i}.DK4", previous[f"target_SC{i}_sha256"])',
    "The Papal States and Titis exchanges are reviewed across all four routes.":
        "Eight Rafael wrap leads and their dialogue exchanges are reviewed, starting with Africa's Proof of Conquest.",
    "papal_states_titis_20261118": "rafael_early_phrase_wraps_20261118",
    "existing_credit=84": "existing_credit=160",
    'candidates += [replay.MARIA_ROM, stage.ROOT / "clean_rebuilt.nds"]':
        'candidates += [stage.ROOT / "clean_rebuilt.nds"]',
    "Preserve Papal States and Titis ROM or replay fixture": "Preserve Rafael dialogue ROM or replay fixture",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael early dialogue and wrap test candidate

The [local ROM](../../{ROM.as_posix()}) includes the cumulative work through eight Rafael exchanges.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Natural scene activation and hardware remain unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael early dialogue and wrap review

Reviewed 160 turns across eight exchanges. The ledger records eight flagged wraps corrected through natural phrasing, four additional wording revisions and 148 exact retentions. Rafael's discovery puts “Africa's Proof of Conquest!” on one line and lets Clau's celebration answer it. Aziza still hesitates before saying what the sword meant to her. The shopkeeper's report about Fernan Silveira is hearsay, and the governor's office is moving to Sofala. Charlotte's reply explains that the Romani had no country of their own to return to. [Exact review ledger](../{REVIEW.as_posix()})

The original renderer and visual review covered all twelve revised pages. Offline checks also verified stored bytes, bounds and complete glyphs for the 148 retentions. The original speaker controls, branches and name substitutions remain intact. Initialized Rafael excerpts matched ten complete panels including the Proof reveal and Charlotte's reply. Natural activation, battle and quest effects, and hardware remain unverified. [Native layout sheets](../{(VERIFY / 'before_after_1.png').as_posix()}) · [Rafael excerpts](../{(VERIFY / 'rafael_live_1.png').as_posix()})

The patch reconstructs the candidate byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. Six startup holds, 24 protected name getters and 32 targeted tests passed. The 160 records already had credit. The ledger stands at 27,700 with 276 stored shared keys open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
for source, label in ((bind, "exact-records"), (verify, "release-gates"), (main, "register")):
    exec(compile(source, __file__ + "::" + label, "exec"), env)

if __name__ == "__main__":
    env["main"]()
