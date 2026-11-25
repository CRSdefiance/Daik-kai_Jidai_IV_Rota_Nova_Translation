"""Register the final six Hodram historical reconciliation exchanges."""

from types import FunctionType

from scripts import register_hodram_farewells_and_maria_20261122 as parent
from scripts import replay_hodram_sera_nagarpur_and_kuhn_20261122 as live
from scripts import stage_hodram_sera_nagarpur_and_kuhn_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
PROFILE = "all-routes-hodram-sera-nagarpur-and-kuhn-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_sera_nagarpur_and_kuhn_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_Sera_Nagarpur_And_Kuhn_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_sera_nagarpur_and_kuhn_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_sera_nagarpur_and_kuhn_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
GLYPHS = EVIDENCE / "glyph_and_sheet_verification.json"
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered the six remaining Hodram exchanges in the historical reconciliation."
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)
check_glyphs = FunctionType(parent.check_glyphs.__code__, parent.check_glyphs.__globals__ | dict(stage=stage, OUTPUT=GLYPHS))
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | globals())
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | globals())


def verified_reconciliation(records):
    tracked = [row for row in records if "earlier_registered_comparison" in row]
    assert len(tracked) == 46 and {row["block"] for row in tracked} == set(stage.BLOCKS)
    assert all(row["earlier_registered_comparison"]["evidence_sha256"] == base.digest(stage.HISTORICAL) for row in tracked)
    mixed = [row for row in records if not row["previous_English"].isascii()]
    assert mixed
    assert all(row["decision"] == "retention" and row["current_reference"]["exact_command_hex"]
               == row["registered_reference"]["exact_command_hex"] for row in mixed)
    return dict(source_comparison=str(stage.HISTORICAL), reconciled_differences=[row["id"] for row in tracked],
                original_mixed_glyphs_retained=[row["id"] for row in mixed])


verify_source = checked_text(parent.verify_source, {
    'observed_count() == 19': 'observed_count() == 12',
    'native_count() == 17': 'native_count() == 9',
    'len(records) == 103': 'len(records) == 108',
    'len(changed) == 16': 'len(changed) == 8',
    'historical_Hodram_B65_B67_B69_reconciliation': 'historical_Hodram_B61_B64_B68_B70_reconciliation',
    'wording_revisions=16': 'wording_revisions=8',
    'justified_retentions=87': 'justified_retentions=100',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1067 and len(checks) == 402": "len(batches) == 1068 and len(checks) == 403",
    "previously_localized_records=103, contextual_records_revisited=103": "previously_localized_records=108, contextual_records_revisited=108",
    "prior_records_reviewed=103": "prior_records_reviewed=108",
    "justified_retentions=87": "justified_retentions=100",
    "prose_revisions=16": "prose_revisions=8",
    "verified_rafael_B84_training_predecessor": "verified_hodram_dialogue_predecessor",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Sera, Nagarpur, and Kuhn

The [testing ROM](../../{ROM.as_posix()}) carries eight dialogue revisions. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("hodram_farewells_and_maria", "hodram_sera_nagarpur_and_kuhn")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'earlier = [live.ROM, EARLIER_STAGE / stage.ROM.name, EARLIER_STAGE / "focused_gameplay/route1" / live.ROM.name]':
        'earlier = [live.ROM]',
    'Preserve the Hodram farewells candidate, predecessor and unique focused ROM':
        'Preserve the Hodram reconciliation candidate, predecessor and unique focused ROM',
    old_doc:'''    DOC.write_text(f"""# Sera, Nagarpur, and Kuhn

Six exchanges add 108 source comparisons, eight prose revisions and 100 contextual retentions. Together with the earlier two batches they account for all 96 historical Hodram differences. The revisions keep Hodram's questions and apology in character, clarify Nagarpur's taunt and Gerhard's answer, and preserve Sera's legend and the original surname substitution. [Exact review](../{REVIEW.as_posix()})

Nine native layout variants passed the exact font checks, including the default and maximum supported surname width. A focused emulator replay verified 12 panels with their nameplates and the return to port. The natural scene triggers and handheld display remain unvisited in this batch. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("hodram_farewells_and_maria", "hodram_sera_nagarpur_and_kuhn")
scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::register-remaining-Hodram-exchanges", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
