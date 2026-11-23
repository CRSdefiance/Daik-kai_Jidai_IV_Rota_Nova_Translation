"""Register the complete Rafael Mediterranean and Maria crew dialogue updates."""

from types import FunctionType

from scripts import register_hodram_sera_nagarpur_and_kuhn_20261122 as parent
from scripts import replay_rafael_athens_and_maria_crew_20261122 as live
from scripts import stage_rafael_athens_and_maria_crew_20261122 as stage
from scripts import verify_rafael_athens_and_maria_crew_20261122 as layouts
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
PROFILE = "all-routes-rafael-athens-and-maria-crew-v1-20261122"
ROOT = parent.ROOT.with_name("rafael_athens_and_maria_crew_registered_20261122")
ROM = ROOT / "Translation_DS_Rafael_Athens_And_Maria_Crew_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_rafael_athens_and_maria_crew_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_athens_and_maria_crew_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
GLYPHS, FE = layouts.GLYPH_PROOF, stage.FE_PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
TRIAL = stage.BATCH.parent / "final/staged" / stage.ROM.name
CHECKPOINT = "Registered Rafael's Mediterranean advice and Athens meeting, and Maria's crew story."
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | globals())
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | globals())


def retained_modal(records, candidate):
    proof = base.load(FE)
    assert proof["candidate_sha256"] == candidate and proof["original_modal_consumer"]
    by_key = {(r["route"], r["id"]): r for r in records if r["source_selector"] == 254}
    assert len(by_key) == 8 and len(proof["records"]) == proof["complete_stored_page_count"] == 10
    assert all(r["decision"] == "retention" for r in by_key.values())
    for page in proof["records"]:
        row = by_key[page["route"], page["id"]]
        if not page["second_page"]:
            assert page["exact_command_hex"] == row["current_reference"]["exact_command_hex"]
            assert page["exact_command_hex"] == row["registered_reference"]["exact_command_hex"]
            assert page["stored_offset"] == row["registered_reference"]["command_offset"]
        elif page["route"] == 3:
            assert page["exact_command_hex"][10:].startswith(row["retained_FE_pages"][1]["exact_stored_hex"])
    return dict(exact_panel_proof=str(FE), sha256=base.digest(FE), pages=10, two_page_owners=2)


verify_source = checked_text(parent.verify_source, {
    'checked["sheets"] + played["sheets"]': 'checked["sheets"] + base.load(FE)["sheets"] + played["sheets"]',
    'observed_count() == 12': 'observed_count() == 29',
    'played["report_sha256"] == base.digest(live.REPORT)':
        'played["report_sha256"] == {str(r):base.digest(live.report_path(r)) for r in live.SAMPLE}',
    'native_count() == 9': 'native_count() == 21',
    'archives = {"/data/SC1.DK4"}': 'archives = {"/data/SC0.DK4", "/data/SC3.DK4"}',
    'observed = {("/data/SC1.DK4", r["id"]): r for r in played["observations"]}':
        'observed = {(r["file_path"], r["id"]): r for r in played["observations"] if r["page"] == 1}',
    'len(records) == 108': 'len(records) == 132',
    'len(changed) == 8': 'len(changed) == 19',
    'assert all(r["change_class"] == "prose" for r in changed)':
        'assert sum(r["change_class"] == "wrap_only" for r in changed) == 1',
    'historical_Hodram_B61_B64_B68_B70_reconciliation=verified_reconciliation(records),':
        'retained_modal_pages=retained_modal(records, candidate),',
    'wording_revisions=8, wrap_only_revisions=0': 'wording_revisions=18, wrap_only_revisions=1',
    'justified_retentions=100': 'justified_retentions=113',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1068 and len(checks) == 403": "len(batches) == 1069 and len(checks) == 404",
    "previously_localized_records=108, contextual_records_revisited=108": "previously_localized_records=132, contextual_records_revisited=132",
    "prior_records_reviewed=108": "prior_records_reviewed=132",
    "justified_retentions=100": "justified_retentions=113",
    "prose_revisions=8": "prose_revisions=18",
    "wrap_only_revisions=0": "wrap_only_revisions=1",
    "changed_components=1": "changed_components=2",
    "focused_initialized_Hodram=True": "focused_initialized_Rafael_and_Maria=True, retained_modal_pages=10",
    "verified_hodram_dialogue_predecessor": "verified_hodram_reconciliation_predecessor",
    "stage.HISTORICAL": "stage.maria.OUTPUT, FE",
    "DISPLAY, GLYPHS, args.visual_review,": "DISPLAY, GLYPHS, FE, args.visual_review,",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael in Athens and Maria's crew story

The [testing ROM](../../{ROM.as_posix()}) contains 18 prose revisions and one layout-only revision. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("hodram_sera_nagarpur_and_kuhn", "rafael_athens_and_maria_crew")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "earlier = [live.ROM]":
        'earlier = [Path(base.load(live.receipt(r))["rom"]) for r in live.SAMPLE] + [TRIAL]',
    "Preserve the Hodram reconciliation candidate, predecessor and unique focused ROM":
        "Preserve the Rafael and Maria candidate, predecessor, retained trial and focused ROMs",
    old_doc:'''    DOC.write_text(f"""# Rafael in Athens and Maria's crew story

The clean-source pass covers 132 records across three exchanges. It revises the wording of 18 lines, improves one layout and records 113 individual retentions. Julio's Mediterranean advice and first mention of the Proof of Conquest read as complete thoughts. Hans's introduction distinguishes passage from his shipboard role. The crew's account of Maria preserves the distinction between the rewards for victory and the sentence for desertion. [Coverage ledger](../{REVIEW.as_posix()})

The candidate passed exact checks for 21 revised layout variants and all ten original modal pages. Focused controller replays verified 29 panels and their visible speaker labels. Rafael's fixture returns to port and Maria's continues into the original recruitment notice. Both original two-page stories advance by controller input. Natural story triggers and handheld display remain unvisited for this batch. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("hodram_sera_nagarpur_and_kuhn", "rafael_athens_and_maria_crew")
scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::registered-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
