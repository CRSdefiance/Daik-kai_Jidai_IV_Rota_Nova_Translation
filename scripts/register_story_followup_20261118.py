"""Register the follow-up localization and exact clean-input patch."""

from pathlib import Path

from scripts import register_story_phrase_continuity_20261118 as previous
from scripts import replay_story_followup_20261118 as replay
from scripts import stage_story_followup_20261118 as stage
from scripts import verify_story_followup_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent = stage.base, stage.native, stage.parent
workflow = parent.workflow
PROFILE = "all-routes-story-followup-v1-20261118"
ROOT = Path("out/story_followup_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Story_Followup_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_story_followup_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_story_followup_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"

bind = checked_text(previous.bind_source, {
    "stage.paired.paired.text_records": "stage.paired.text_records",
    "len(retentions) == 4": "len(retentions) == 29",
    "Rafael or Hodram replay": "Rafael replay",
    "Byte-identical retention with fresh native and visual checks":
        "Byte-identical retention with original native renderer verification",
})
verify = checked_text(previous.verify_source, {
    'live["initialized_Rafael_and_Hodram"] and live["exact_original_commands"] and live["actual_given_name_and_pagination"]':
        'live["initialized_Rafael"] and live["exact_native_panel_masks"] and live["exact_page_transitions"]',
    'len(live["holds"]) == 16': 'len(live["holds"]) == 12',
    'native_proof["revision_count"] == 27 and native_proof["fresh_page_count"] == 39 and native_proof["retention_page_count"] == 4':
        'native_proof["revision_count"] == 28 and native_proof["fresh_page_count"] == 28 and len(native_proof["retained_records"]) == 29',
    "== 39": "== 28",
    '{"DK4_MES_B143_R0380": [2, 1]}': '{"DK4_MES_B249_R0031": [2, 1], "DK4_MES_B221_R0027": [2, 1]}',
    'len(draft["records"]) == 31': 'len(draft["records"]) == 57',
    '{"revision": 27, "retention": 4}': '{"revision": 28, "retention": 29}',
    '{"prose": 19, "wrap": 8, "retention": 4}': '{"prose": 27, "wrap": 1, "retention": 29}',
})
publish = previous.publish_source
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index("    base.save(PACKAGE / \"checksums.json\"")]
main = checked_text(publish, {
    'len(manifest["batches"]) == 874 and len(manifest["checks"]) == 209':
        'len(manifest["batches"]) == 875 and len(manifest["checks"]) == 210',
    "replay.LIVE, replay.SETUP, replay.HODRAM_SETUP, args.visual_review":
        "replay.LIVE, replay.SETUP, args.visual_review",
    "release_stack_before_story_phrase_continuity.json": "release_stack_before_story_followup.json",
    "release_stack_with_story_phrase_continuity.json": "release_stack_with_story_followup.json",
    "verified_story_tag_wraps_predecessor": "verified_story_phrase_continuity_predecessor",
    "story_phrase_continuity_release": "story_followup_release",
    "registered_story_phrase_continuity_and_complete_parent_inverse":
        "registered_story_followup_and_complete_parent_inverse",
    "story_phrase_continuity_pipeline": "story_followup_pipeline",
    "prose_revisions=19, wrap_only_revisions=8, justified_retentions=4":
        "prose_revisions=27, wrap_only_revisions=1, justified_retentions=29",
    "text_display_revisions=27, pagination_fixes=1": "text_display_revisions=28, pagination_fixes=2",
    "initialized_Rafael_and_Hodram_story_excerpts": "initialized_Rafael_followup_excerpts",
    "Thirty-one phrase-wrap leads are reviewed, including Rafael's sea-battle tutorial.":
        "The trade and diplomacy follow-up, Brass Lamp discovery, royal audience, signed letter and four Arrow exchanges are reviewed.",
    "story_phrase_continuity_20261118": "story_followup_20261118",
    "existing_credit=31": "existing_credit=57",
    'candidates += [replay.HODRAM_ROM, stage.ROOT / "clean_rebuilt.nds"]':
        'candidates += [stage.ROOT / "clean_rebuilt.nds", stage.ROOT.with_name("research_v1") / stage.ROM.name,\n'
        '                   stage.ROOT.with_name("research_v1") / "clean_rebuilt.nds",\n'
        '                   stage.ROOT.with_name("research_v1") / replay.ROM.relative_to(stage.ROOT)]',
    "Preserve phrase-continuity ROM or replay fixture": "Preserve story follow-up ROM or replay fixture",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Follow-up exchanges test candidate

The [local ROM](../../{ROM.as_posix()}) includes the cumulative work through the dialogue and page follow-up.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Natural scene activation and hardware remain unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Story follow-up exchanges

Reviewed 57 records across nine story blocks. The ledger records 27 wording revisions, one wrap-only fix and 29 justified retentions. The original port-contract lesson and the limits of Duarte's support stay clear. Rafael's question keeps “King of Spain” together. The Brass Lamp exchange preserves the heat revealing the map and the crew's repeated joke about the accident. The royal audience keeps the Pope's intended support and the scope of Rafael's appointment. [Exact review ledger](../{REVIEW.as_posix()})

The Demon-Piercing Arrow's rumored effect, the sailors' speculation about cannons and Cesare's complaint fit on one page across all four routes. Yukihisa's opening report also fits on one page and keeps the threat to the blades, the curse and Tokugawa's title. The signature, blank line and ceremonial name remain byte-identical. The renderer checked all 28 revised pages and the 29 exact retentions. Direct visual review covered all revised pages and the signed letter. [Native pages](../{(VERIFY / 'before_after_1.png').as_posix()})

Rafael's initialized replay matched 12 actual panels spanning the diplomacy question, map discovery, signed letter and Cesare's complaint. It verifies that the revised opening of the letter and the complaint each advance directly to the next dialogue record. The original story activation and hardware remain unverified. [Rafael replay](../{(VERIFY / 'rafael_live_1.png').as_posix()})

The clean-input patch reconstructs this candidate byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. Six startup frames, 24 protected name getters and 32 targeted tests passed. The 57 records already had credit. The ledger remains at 27,700 with 276 stored shared keys open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = vars(previous.precedent) | globals()
for source, label in ((bind, "exact-records"), (verify, "release-gates"), (main, "register")):
    exec(compile(source, __file__ + "::" + label, "exec"), env)

if __name__ == "__main__":
    env["main"]()
