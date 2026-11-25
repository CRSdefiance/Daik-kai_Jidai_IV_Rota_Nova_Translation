"""Register Rafael's mosque sequence with exact source and clean-patch verification."""

from inspect import getsource
from pathlib import Path

from scripts import register_london_guild_assignments_20261118 as previous
from scripts import replay_rafael_mosque_20261118 as replay
from scripts import verify_rafael_mosque_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

stage, base, native, parent = display.build, display.base, display.native, display.parent
workflow = parent.workflow
PROFILE = "all-routes-rafael-mosque-v1-20261118"
ROOT = Path("out/rafael_mosque_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Rafael_Mosque_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_rafael_mosque_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_mosque_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
LATER = Path("releases/all_routes_editorial_20261114_rafael_final_wraps_candidate/verification/registered_review.json")
LATER_RETENTIONS = {ident: LATER for ident in ("DK4_MES_B318_R0079", "DK4_MES_B318_R0176")}

bind_source = checked_text(getsource(previous.bind), {
    'values = stage.paired.text_records(raw, word)': 'values = stage.review.current.paired.text_records(raw, word)',
})
verify_source = checked_text(getsource(previous.verify), {
    'live["actual_Castor_and_Rafael_macro_glyphs"]': 'live["actual_Rafael_macro_and_speakerless_FE"]',
    'len(live["holds"]) == 16': 'len(live["holds"]) == 31',
    'native_proof["revision_count"] == 40 and native_proof["fresh_page_count"] == 18':
        'native_proof["revision_count"] == 27 and native_proof["fresh_page_count"] == 27',
    '== 61': '== 27',
    '    assert base.digest(native_proof["prior_proof"]["path"]) == native_proof["prior_proof"]["sha256"]\n': '',
    'native_proof["previous_sheets"] + native_proof["contact_sheets"]': 'native_proof["contact_sheets"]',
    'len(draft["records"]) == 151': 'len(draft["records"]) == 139',
    '{"revision": 40, "retention": 111}': '{"revision": 27, "retention": 112}',
})
publish = getsource(previous.main)
doc_start = publish.index("    DOC.write_text")
doc_end = publish.index("    prefix =", doc_start)
doc = """    DOC.write_text(f\"""# Rafael's dancer and mosque rescue

Reviewed 139 records in seven Rafael blocks. The ledger records 27 revisions and 112 justified retentions. Safia's dancing rumor now fits on one native page, and the English distinguishes the patron's account of the curse from what Rafael later witnesses. The mosque dialogue keeps Al's reported experience and the translated book title clue. The recitation preserves the invocation to Allah and Scheherazade's framing. [Exact review ledger](../{REVIEW.as_posix()})

Native checks covered 24 progressive pages and three speakerless notices. The compiler preserved the two detour choices, character selectors, substitutions and relative branches. The first four review gates and stored formatting gate are recorded separately for each record. [Final layout pages](../{(VERIFY / 'before_after_1.png').as_posix()})

An initialized Rafael opening played 31 original speech excerpts from Safia's conversation through the curse, recitation and reward. Complete body planes match the native renders, including the speakerless calls and the Rafael name substitution. The original triggering conditions, branch routes and hardware remain unverified. [Excerpts](../{(VERIFY / 'live_1.png').as_posix()})

The clean-input patch reconstructs the exact candidate. All 114 baseline layers and the registered ASCII right-bound correction carry forward. Six cold-boot holds, 24 protected name getters and 32 targeted tests passed. The records already had credit. The ledger remains at 27,700 with 276 pending shared keys. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
\""", encoding="utf-8", newline="\\n")
"""
first = publish.index("    for version in (1, 2, 3):")
after = publish.index("    for path in candidates:", first)
publish_source = checked_text(publish, {
    publish[doc_start:doc_end]: doc,
    publish[first:after]: "",
    'len(manifest["batches"]) == 862 and len(manifest["checks"]) == 197':
        'len(manifest["batches"]) == 866 and len(manifest["checks"]) == 201',
    "release_stack_before_guild_assignments.json": "release_stack_before_rafael_mosque.json",
    "release_stack_with_guild_assignments.json": "release_stack_with_rafael_mosque.json",
    "verified_forest_expeditions_predecessor=predecessor, london_malacca_guild_assignments_release=str(REVIEW)":
        "verified_overland_passages_predecessor=predecessor, rafael_mosque_release=str(REVIEW)",
    "registered_london_malacca_guild_assignments_and_complete_parent_inverse":
        "registered_rafael_mosque_and_complete_parent_inverse",
    "london_malacca_guild_assignments_pipeline": "rafael_mosque_pipeline",
    "prose_revisions=40, justified_retentions=111": "prose_revisions=27, justified_retentions=112",
    "final_phrase_refinements_within_revised_prose=6": "final_phrase_refinements_within_revised_prose=5",
    "initialized_Rafael_guild_and_riddle=True": "initialized_Rafael_mosque_excerpts=True",
    '**{f"target_SC{i}_sha256": archives[f"/data/SC{i}.DK4"] for i in range(4)}':
        '**{f"target_SC{i}_sha256": archives.get(f"/data/SC{i}.DK4", previous[f"target_SC{i}_sha256"]) for i in range(4)}',
    "Rafael's ruins investigation and the related London and Malacca guild assignments are reviewed.":
        "Rafael's dancer and mosque rescue are reviewed.",
    'ledger["london_malacca_guild_assignments_20261118"]': 'ledger["rafael_mosque_20261118"]',
    "existing_credit=151": "existing_credit=139",
    "# London and Malacca guild assignments test candidate": "# Rafael mosque rescue test candidate",
    "includes all four reviewed assignments.": "includes Rafael's revised dancer and mosque scenes.",
    "Natural quest activation": "Natural scene activation",
    "Preserve guild assignment ROM or replay fixture": "Preserve Rafael mosque ROM or replay fixture",
})
scope = vars(previous) | globals()
for source, label in ((bind_source, "bound-ledger"), (verify_source, "verified-release"), (publish_source, "registered-release")):
    exec(compile(source, __file__ + "::" + label, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
