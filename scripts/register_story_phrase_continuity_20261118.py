"""Register the editorial phrase-continuity batch after native and replay checks."""

from inspect import getsource
from pathlib import Path

from scripts import register_london_guild_assignments_20261118 as precedent
from scripts import replay_story_phrase_continuity_20261118 as replay
from scripts import stage_story_phrase_continuity_20261118 as stage
from scripts import verify_story_phrase_continuity_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent = stage.base, stage.native, stage.parent
workflow = parent.workflow
PROFILE = "all-routes-story-phrase-continuity-v1-20261118"
ROOT = Path("out/story_phrase_continuity_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Story_Phrase_Continuity_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_story_phrase_continuity_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_story_phrase_continuity_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"

bind = getsource(precedent.bind)
history = bind[bind.index("    later = "):bind.index("    for group in stored")]
retention = bind[bind.index('                    if row["historical_layout_matches_current"]:'):bind.index('                if ident in visited:')]
bind_source = checked_text(bind, {
    history: '    retentions = {(r["file_path"], r["id"]): r for r in report["retained_records"]}\n    seen = set()\n',
    retention: '''                    assert retentions[path, ident]["stored_hex"] == payload.hex()
                    scope = "Byte-identical retention with fresh native and visual checks"
                    receipt = dict(path=str(display.PROOF), sha256=base.digest(display.PROOF), id=ident)
''',
    "assert seen == rows.keys() and rebound == LATER_RETENTIONS.keys()":
        'assert seen == rows.keys() and len(retentions) == 4',
    "stage.paired.text_records": "stage.paired.paired.text_records",
    "initialized Rafael replay": "initialized Rafael or Hodram replay",
    "initialized_rafael=live": "initialized_phrase_excerpts=live",
})
verify_source = checked_text(getsource(precedent.verify), {
    'live["initialized_Rafael"] and live["exact_original_commands"] and live["actual_Castor_and_Rafael_macro_glyphs"]':
        'live["initialized_Rafael_and_Hodram"] and live["exact_original_commands"] and live["actual_given_name_and_pagination"]',
    'native_proof["revision_count"] == 40 and native_proof["fresh_page_count"] == 18':
        'native_proof["revision_count"] == 27 and native_proof["fresh_page_count"] == 39 and native_proof["retention_page_count"] == 4',
    "== 61": "== 39",
    '    assert base.digest(native_proof["prior_proof"]["path"]) == native_proof["prior_proof"]["sha256"]\n':
        '    assert native_proof["pagination_before_after"] == {"DK4_MES_B143_R0380": [2, 1]}\n',
    'native_proof["previous_sheets"] + native_proof["contact_sheets"]': 'native_proof["contact_sheets"]',
    'len(draft["records"]) == 151': 'len(draft["records"]) == 31',
    '{"revision": 40, "retention": 111}': '{"revision": 27, "retention": 4}',
    "draft.update(approved_source25=bound, direct_visual_review=sheets)":
        'assert Counter(r["finding"] for r in draft["records"]) == {"prose": 19, "wrap": 8, "retention": 4}\n'
        '    draft.update(approved_source25=bound, direct_visual_review=sheets)',
})
publish = getsource(precedent.main)
pins = publish[publish.index("    for version in (1, 2, 3):"):publish.index("    for path in candidates:")]
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index("    base.save(PACKAGE / \"checksums.json\"")]
publish_source = checked_text(publish, {
    'len(manifest["batches"]) == 862 and len(manifest["checks"]) == 197':
        'len(manifest["batches"]) == 874 and len(manifest["checks"]) == 209',
    'display.PROOF, replay.LIVE, replay.SETUP, args.visual_review':
        'display.PROOF, replay.LIVE, replay.SETUP, replay.HODRAM_SETUP, args.visual_review',
    'draft["initialized_rafael"]': 'draft["initialized_phrase_excerpts"]',
    "release_stack_before_guild_assignments.json": "release_stack_before_story_phrase_continuity.json",
    "release_stack_with_guild_assignments.json": "release_stack_with_story_phrase_continuity.json",
    "verified_forest_expeditions_predecessor=predecessor, london_malacca_guild_assignments_release=str(REVIEW)":
        "verified_story_tag_wraps_predecessor=predecessor, story_phrase_continuity_release=str(REVIEW)",
    "registered_london_malacca_guild_assignments_and_complete_parent_inverse":
        "registered_story_phrase_continuity_and_complete_parent_inverse",
    "london_malacca_guild_assignments_pipeline": "story_phrase_continuity_pipeline",
    "prose_revisions=40, justified_retentions=111": "prose_revisions=19, wrap_only_revisions=8, justified_retentions=4",
    "name_label_revisions=0, text_display_revisions=0, final_phrase_refinements_within_revised_prose=6":
        "name_label_revisions=0, text_display_revisions=27, pagination_fixes=1",
    "initialized_Rafael_guild_and_riddle=True": "initialized_Rafael_and_Hodram_story_excerpts=True",
    "Rafael's ruins investigation and the related London and Malacca guild assignments are reviewed.":
        "Thirty-one phrase-wrap leads are reviewed, including Rafael's sea-battle tutorial.",
    "london_malacca_guild_assignments_20261118": "story_phrase_continuity_20261118",
    "existing_credit=151": "existing_credit=31",
    pins: '''    candidates += [replay.HODRAM_ROM, stage.ROOT / "clean_rebuilt.nds"]
''',
    "Preserve guild assignment ROM or replay fixture": "Preserve phrase-continuity ROM or replay fixture",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Story phrase continuity test candidate

The [local ROM](../../{ROM.as_posix()}) includes the cumulative localization through the new phrase-wrap review.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits user acceptance. Natural scene activation and hardware remain unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Story phrase continuity

Reviewed 31 leads in 28 story blocks across the four routes. The ledger records 19 wording revisions, eight reflows that keep the wording, and four exact retentions. Fernan's diplomacy lesson keeps the wartime condition and explains both consequences of winning a sea battle in one page. The following reply still tells Rafael to secure a port contract. The captured excerpt confirms the text transition. The test did not run a sea battle or alter market share. [Exact review ledger](../{REVIEW.as_posix()})

Duarte keeps his Portuguese office and his obligation to the King of Spain. Cesare uses the same account of the Demon-Piercing Arrow where the Japanese matches, and all three affected Verisa greetings preserve the celadon clue, the location rumor and the given-name substitution. The unchanged Rigveda, Albuquerque, local specialty and Silla Gold Crown layouts keep their phrase boundaries for the reasons recorded in the ledger. [Native pages](../{(VERIFY / 'before_after_1.png').as_posix()})

Native and direct visual review covered all 27 revised pages, 12 name-width examples and four exact retentions. The original speaker and relative branch controls and the name-catalog routing remain intact. Two initialized emulator excerpts matched 16 full panels, including the new single-page tutorial and its next reply, and Verisa's “Hodram” greeting. Lil and Maria's corresponding name variants were checked offline. Natural scene activation and hardware remain unverified. [Rafael tutorial](../{(VERIFY / 'rafael_live_1.png').as_posix()}) · [Hodram excerpt](../{(VERIFY / 'hodram_live_1.png').as_posix()})

The clean-input patch reconstructs the candidate byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. Six startup frames, 24 protected name getters and 32 targeted tests passed. The 31 selected records already had credit. The ledger remains at 27,700 with 276 shared keys open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})

scope = vars(precedent) | globals()
for code, label in ((bind_source, "exact-records"), (verify_source, "release-gates"), (publish_source, "register")):
    exec(compile(code, __file__ + "::" + label, "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
