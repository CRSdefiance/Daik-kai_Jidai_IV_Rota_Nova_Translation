"""Register Hodram's farewells and first private meeting with Maria."""

from types import FunctionType

from scripts import register_north_sea_and_hodram_reconciliation_20261122 as established
from scripts import register_rafael_B84_training_20261122 as parent
from scripts import replay_hodram_farewells_and_maria_20261122 as live
from scripts import stage_hodram_farewells_and_maria_20261122 as stage
from scripts import verify_palace_london_glyphs_20261122 as glyph_template
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ARM, COMMON = parent.ARM, parent.COMMON
PROFILE = "all-routes-hodram-farewells-and-maria-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_farewells_and_maria_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_Farewells_And_Maria_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_farewells_and_maria_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_farewells_and_maria_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
GLYPHS = EVIDENCE / "glyph_and_sheet_verification.json"
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Hodram’s farewell, private meeting with Maria, and Camille’s return to Lil."
EARLIER_STAGE = stage.BATCH.parent / "corrected/staged"
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)
check_glyphs = FunctionType(glyph_template.verify.__code__, vars(glyph_template) | dict(stage=stage, OUTPUT=GLYPHS))
native_count = FunctionType(established.native_count.__code__, established.native_count.__globals__ | globals())
observed_count = FunctionType(established.observed_count.__code__, established.observed_count.__globals__ | globals())


def verified_reconciliation(records):
    tracked = [r for r in records if "earlier_registered_comparison" in r]
    assert len(tracked) == 44 and {r["block"] for r in tracked} == set(stage.BLOCKS)
    assert all(r["earlier_registered_comparison"]["evidence_sha256"] == base.digest(stage.HISTORICAL) for r in tracked)
    artistic = [row for row in records if not row["previous_English"].isascii()]
    assert len(artistic) >= 14
    assert all(row["decision"] == "retention" and row["current_reference"]["exact_command_hex"]
               == row["registered_reference"]["exact_command_hex"] for row in artistic)
    return dict(source_comparison=str(stage.HISTORICAL), reconciled_differences=[r["id"] for r in tracked],
                original_mixed_glyphs_retained=[r["id"] for r in artistic])


verify_source = checked_text(established.verify_source, {
    'observed_count() == 13': 'observed_count() == 19',
    '(played["rafael_report_sha256"], played["hodram_report_sha256"]) == (base.digest(live.REPORT), base.digest(live.HODRAM_REPORT))':
        'played["report_sha256"] == base.digest(live.REPORT)',
    'native_count() == 9': 'native_count() == 17',
    'archives = {"/data/SC0.DK4", "/data/SC1.DK4"}': 'archives = {"/data/SC1.DK4"}',
    '(r["file_path"], r["id"]): r for r in played["observations"]':
        '("/data/SC1.DK4", r["id"]): r for r in played["observations"]',
    'len(records) == 74': 'len(records) == 103',
    'len(changed) == 9': 'len(changed) == 16',
    'historical_Hodram_B66_reconciliation': 'historical_Hodram_B65_B67_B69_reconciliation',
    'wording_revisions=9': 'wording_revisions=16',
    'justified_retentions=65': 'justified_retentions=87',
})
readme = established.build[established.build.index('    (PACKAGE / "README.md").write_text'):established.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(established.build, {
    "len(batches) == 1065 and len(checks) == 400": "len(batches) == 1067 and len(checks) == 402",
    "previously_localized_records=74, contextual_records_revisited=74": "previously_localized_records=103, contextual_records_revisited=103",
    "prior_records_reviewed=74": "prior_records_reviewed=103",
    "justified_retentions=65": "justified_retentions=87",
    "prose_revisions=9": "prose_revisions=16",
    "changed_components=2": "changed_components=1",
    "focused_initialized_Rafael_and_Hodram=True": "focused_initialized_Hodram=True",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Hodram's farewells and first meeting with Maria

The [testing ROM](../../{ROM.as_posix()}) carries 16 dialogue revisions. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("north_sea_and_hodram_reconciliation", "hodram_farewells_and_maria").replace(
    "verified_palace_eirene_pereira_london_predecessor", "verified_rafael_B84_training_predecessor")
old_doc = established.commit[established.commit.index("    DOC.write_text"):established.commit.index("    prefix =")]
commit = checked_text(established.commit, {
    "earlier = [live.ROM, live.HODRAM_ROM, FIRST_STAGE]":
        'earlier = [live.ROM, EARLIER_STAGE / stage.ROM.name, EARLIER_STAGE / "focused_gameplay/route1" / live.ROM.name]',
    "Preserve the North Sea and Hodram candidate, predecessor and unique focused ROMs":
        "Preserve the Hodram farewells candidate, predecessor and unique focused ROM",
    old_doc:'''    DOC.write_text(f"""# Hodram’s farewells and first meeting with Maria

Three complete exchanges cover 103 spoken texts and 44 comparisons to the earlier registered wording. The review records 16 revisions and 87 justified retentions. It restores the reunion and Hodram's ambition to build a navy, clarifies Maria's case against Kuhn and Pereira, and retains the warmth and hesitations in Camille's return. The stylized speech in the farewell keeps its original glyphs and sequence. [Registered review](../{REVIEW.as_posix()})

Seventeen native layout variants passed exact font checks, including Camille's thanks at default and maximum name widths. Focused cold-boot replays verified 19 complete dialogue panels, their speaker labels, and return to the host scene. Ordinary story triggers and handheld display remain unvisited for this batch. Startup and 17 focused tests passed. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("north_sea_and_hodram_reconciliation", "hodram_farewells_and_maria")
scope = established.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::registered-Hodram-release", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
