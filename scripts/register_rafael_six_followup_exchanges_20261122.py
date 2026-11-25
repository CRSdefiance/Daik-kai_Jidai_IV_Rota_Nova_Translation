"""Register Rafael's six complete follow-up exchanges and their verified layouts."""

from types import FunctionType

from scripts import register_rafael_proof_and_financing_20261122 as parent
from scripts import replay_rafael_six_followup_exchanges_20261122 as live
from scripts import stage_rafael_six_followup_exchanges_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
PROFILE = "all-routes-rafael-six-followup-exchanges-v1-20261122"
ROOT = parent.ROOT.with_name("rafael_six_followup_exchanges_registered_20261122")
ROM = ROOT / "Translation_DS_Rafael_Six_Followup_Exchanges_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_rafael_six_followup_exchanges_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_six_followup_exchanges_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
GLYPHS, FE = live.GLYPH_PROOF, stage.FE_PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Rafael's exchanges from Lil's farewell through the scabbard."
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | globals())
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | globals())
REPORT = live.scope["report_path"](0)


def retained_modal(records, candidate):
    proof = base.load(FE)
    assert proof["candidate_sha256"] == candidate and proof["original_modal_consumer"]
    checked = {r["id"]: r for r in proof["records"]}
    assert set(checked) == {"DK4_MES_B55_R0036", "DK4_MES_B55_R0054", "DK4_MES_B61_R0113"}
    owners = [r for r in records if r["kind"] == "system"]
    assert len(owners) == 3
    assert all(r["decision"] == "retention" for r in owners)
    for row in owners:
        ref, rendered = row["registered_reference"], checked[row["id"]]
        assert ref["exact_command_hex"] == row["current_reference"]["exact_command_hex"] == rendered["exact_command_hex"]
        assert ref["command_offset"] == rendered["stored_offset"] and not rendered["second_page"]
    return dict(pages=proof["complete_stored_page_count"], sha256=base.digest(FE), records=list(checked))


verify_source = checked_text(parent.verify_source, {
    'checked["sheets"] + base.load(FE)["sheets"] + base.load(CHOICE)["sheets"] + played["sheets"] + ordinary_opening(candidate)["sheets"]':
        'checked["sheets"] + base.load(FE)["sheets"] + played["sheets"]',
    'observed_count() == 21': 'observed_count() == 19',
    'played["report_sha256"] == {run:base.digest(live.report(run)) for run in live.RUNS}':
        'played["report_sha256"] == {"0":base.digest(REPORT)}',
    'len(records) == 142': 'len(records) == 129',
    'retained_native_controls=retained_controls(records, played, candidate, banks["/data/SC0.DK4"].blocks[44]),\n'
    '        ordinary_lisbon_opening=ordinary_opening(candidate),':
        'retained_modal_notices=retained_modal(records, candidate),',
    'justified_retentions=126, choice_label_retentions=2': 'justified_retentions=113',
    'historical_source_credit=historical_credit(records)':
        'historical_source_credit=dict(by_census_id={}, direct_keys=len(records))',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1070 and len(checks) == 405": "len(batches) == 1071 and len(checks) == 406",
    "previously_localized_records=144, contextual_records_revisited=144": "previously_localized_records=129, contextual_records_revisited=129",
    "prior_records_reviewed=144": "prior_records_reviewed=129",
    "justified_retentions=126, retained_choice_labels=2": "justified_retentions=113, retained_choice_labels=0",
    "retained_modal_pages=1, original_preparation_branches=2, ordinary_Lisbon_opening=True": "retained_modal_pages=3",
    "verified_rafael_athens_predecessor": "verified_rafael_lisbon_predecessor",
    "stage.paired.OUTPUT, FE, CHOICE, display.MENU_PROOF, ordinary.OUTPUT": "stage.REVIEW, FE",
    "DISPLAY, GLYPHS, FE, CHOICE, display.MENU_PROOF, ordinary.OUTPUT, args.visual_review,": "DISPLAY, GLYPHS, FE, args.visual_review,",
    '        assert all(("/data/SC0.DK4", row["historical_credit_id"]) in credited\n'
    '                   for row in draft["retained_native_controls"]["original_choice"]["captions"])\n': '',
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael's six follow-up exchanges

The [testing ROM](../../{ROM.as_posix()}) carries 16 wording revisions. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("rafael_proof_and_financing", "rafael_six_followup_exchanges")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'earlier = [Path(base.load(live.ROOT / kind / "fixture.json")["rom"]) for kind in ("speech", "choice")]':
        'earlier = [Path(base.load(live.scope["receipt"](0))["rom"])]',
    "Preserve the Rafael financing candidate, predecessor and focused ROMs":
        "Preserve the Rafael follow-up candidate, predecessor and focused ROM",
    old_doc:'''    DOC.write_text(f"""# Rafael's six follow-up exchanges

The clean-Japanese pass covers 129 records, with 16 revisions and 113 individual retentions. Lil's parting news stays unspecified, the summons keeps Albuquerque's official affiliation, and Silveira's reward still conceals his deduction. The visit to Emilio preserves Claudio's uncertainty and Arcadius's kindness. The scabbard remains a clue. [Exact review](../{REVIEW.as_posix()})

All 17 revised native variants passed the complete glyph checks. Focused controller playback verified 19 panels, including three original modal notices and the return to port. Both surname widths passed offline, and the default surname appeared in the replay. Natural story triggers and handheld display remain unvisited on this candidate. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("rafael_proof_and_financing", "rafael_six_followup_exchanges")
scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::registered-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
