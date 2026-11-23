"""Register the reviewed Papal States and Titis exchanges with the cumulative ROM."""

from pathlib import Path

from scripts import register_story_phrase_continuity_20261118 as previous
from scripts import replay_papal_states_titis_20261118 as replay
from scripts import stage_papal_states_titis_20261118 as stage
from scripts import verify_papal_states_titis_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent = stage.base, stage.native, stage.parent
workflow = parent.workflow
PROFILE = "all-routes-papal-states-titis-v1-20261118"
ROOT = Path("out/papal_states_titis_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Papal_States_Titis_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_papal_states_titis_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_papal_states_titis_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"

bind = checked_text(previous.bind_source, {
    "stage.paired.paired.text_records": "stage.paired.text_records",
    "len(retentions) == 4": "len(retentions) == 35",
    "Rafael or Hodram replay": "Rafael or Maria excerpt replay",
    "Byte-identical retention with fresh native and visual checks":
        "Byte-identical retention with complete native rendering check",
})
verify = checked_text(previous.verify_source, {
    'live["initialized_Rafael_and_Hodram"] and live["exact_original_commands"] and live["actual_given_name_and_pagination"]':
        'live["initialized_Rafael_and_Maria"] and live["exact_original_commands"] and live["actual_given_name_substitutions"]',
    'native_proof["revision_count"] == 27 and native_proof["fresh_page_count"] == 39 and native_proof["retention_page_count"] == 4':
        'native_proof["revision_count"] == 49 and native_proof["fresh_page_count"] == 61 and native_proof["retention_page_count"] == 35',
    "== 39": "== 61",
    '{"DK4_MES_B143_R0380": [2, 1]}': '{}',
    'len(draft["records"]) == 31': 'len(draft["records"]) == 84',
    '{"revision": 27, "retention": 4}': '{"revision": 49, "retention": 35}',
    '{"prose": 19, "wrap": 8, "retention": 4}': '{"prose": 44, "wrap": 5, "retention": 35}',
})
publish = previous.publish_source
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 874 and len(manifest["checks"]) == 209':
        'len(manifest["batches"]) == 877 and len(manifest["checks"]) == 212',
    'stage.ROOT / "clean_input.xdelta"': 'stage.ROOT / "translation.xdelta"',
    "replay.LIVE, replay.SETUP, replay.HODRAM_SETUP, args.visual_review":
        "replay.LIVE, replay.SETUP, replay.MARIA_SETUP, args.visual_review",
    "release_stack_before_story_phrase_continuity.json": "release_stack_before_papal_states_titis.json",
    "release_stack_with_story_phrase_continuity.json": "release_stack_with_papal_states_titis.json",
    "verified_story_tag_wraps_predecessor": "verified_regional_proof_dialogue_predecessor",
    "story_phrase_continuity_release": "papal_states_titis_release",
    "registered_story_phrase_continuity_and_complete_parent_inverse":
        "registered_papal_states_titis_and_complete_parent_inverse",
    "story_phrase_continuity_pipeline": "papal_states_titis_pipeline",
    "prose_revisions=19, wrap_only_revisions=8, justified_retentions=4":
        "prose_revisions=44, wrap_only_revisions=5, justified_retentions=35",
    "text_display_revisions=27, pagination_fixes=1": "text_display_revisions=49, pagination_fixes=0",
    "initialized_Rafael_and_Hodram_story_excerpts": "initialized_Rafael_and_Maria_papal_titis_excerpts",
    "Thirty-one phrase-wrap leads are reviewed, including Rafael's sea-battle tutorial.":
        "The Papal States and Titis exchanges are reviewed across all four routes.",
    "story_phrase_continuity_20261118": "papal_states_titis_20261118",
    "existing_credit=31": "existing_credit=84",
    'candidates += [replay.HODRAM_ROM, stage.ROOT / "clean_rebuilt.nds"]':
        'candidates += [replay.MARIA_ROM, stage.ROOT / "clean_rebuilt.nds"]',
    "Preserve phrase-continuity ROM or replay fixture": "Preserve Papal States and Titis ROM or replay fixture",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Papal States and Titis test candidate

The [local ROM](../../{ROM.as_posix()}) contains the cumulative editorial work through the Papal States and Titis exchanges.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Natural scene activation and hardware remain unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Papal States and Titis exchanges

Reviewed 84 turns in eight story blocks across all four routes. The ledger records 44 prose revisions, five reflows and 35 exact retentions. Filippo remembers a story from his great-grandfather about land the pope once ruled directly. The exchange keeps Carlo and Filippo's teasing, the competition among donors, the family's profits and the possibility of a blessing. Titis addresses each captain by name and makes an exception when she shares the location of the ruins. [Exact review ledger](../{REVIEW.as_posix()})

The original renderer checked 49 revised pages, 12 additional name-width cases and all 35 retentions. Every distinct revised and name-width page was visually inspected with byte-identical images mapped to their record IDs. The four silent openings preserve the original three ellipsis glyphs. Original speaker and layout controls and all four captain-name substitutions passed. Initialized Rafael and Maria excerpts matched 16 complete panels. Maria used the existing system-only unlock. Hodram and Lil's substitutions were checked offline. Natural activation, quest effects and hardware remain unverified. [Native layout sheets](../{(VERIFY / 'before_after_1.png').as_posix()}) · [Rafael replay](../{(VERIFY / 'rafael_live_1.png').as_posix()}) · [Maria replay](../{(VERIFY / 'maria_live_1.png').as_posix()})

The patch reconstructs the full candidate byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. Six startup frames, 24 protected name getters and 32 targeted tests passed. These 84 records already had credit. The ledger stands at 27,700 with 276 shared keys open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = vars(previous.precedent) | globals()
for source, label in ((bind, "exact-records"), (verify, "release-gates"), (main, "register")):
    exec(compile(source, __file__ + "::" + label, "exec"), env)

if __name__ == "__main__":
    env["main"]()

