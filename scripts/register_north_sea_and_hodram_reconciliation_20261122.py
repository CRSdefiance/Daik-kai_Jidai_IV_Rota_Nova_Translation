"""Register the North Sea meeting and the first Hodram reconciliation."""

from types import FunctionType

from scripts import register_palace_eirene_pereira_london_20261122 as parent
from scripts import replay_north_sea_and_hodram_reconciliation_20261122 as live
from scripts import stage_north_sea_and_hodram_reconciliation_20261122 as stage
from scripts import verify_palace_london_glyphs_20261122 as glyph_template
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ARM, COMMON = parent.ARM, parent.COMMON
PROFILE = "all-routes-north-sea-and-hodram-reconciliation-v1-20261122"
ROOT = parent.ROOT.with_name("north_sea_and_hodram_reconciliation_registered_20261122")
ROM = ROOT / "Translation_DS_North_Sea_And_Hodram_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_north_sea_and_hodram_reconciliation_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_north_sea_and_hodram_reconciliation_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
GLYPHS = EVIDENCE / "glyph_and_sheet_verification.json"
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Rafael’s North Sea meeting with Lil and reconciled Hodram’s encounter with Camille."
FIRST_STAGE = stage.BATCH.parent / "staged" / stage.ROM.name
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)
check_glyphs = FunctionType(glyph_template.verify.__code__, vars(glyph_template) | dict(stage=stage, OUTPUT=GLYPHS))


def native_count():
    display, proof = map(base.load, (DISPLAY, GLYPHS))
    assert proof["candidate_sha256"] == display["candidate_sha256"]
    assert proof["native_report_sha256"] == base.digest(DISPLAY)
    assert proof["complete_font_pixels"] and proof["exact_contact_sheet_pixels"]
    assert len(proof["pages"]) == display["pages"]
    return display["pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


def verified_reconciliation(records):
    tracked = [r for r in records if "earlier_registered_comparison" in r]
    assert sorted(r["id"][-4:] for r in tracked) == ["0006", "0026", "0045", "0056", "0068", "0072"]
    assert sum(r["decision"] == "revision" for r in tracked) == 4
    assert all(r["earlier_registered_comparison"]["evidence_sha256"] == base.digest(stage.HISTORICAL) for r in tracked)
    mark = next(r for r in tracked if r["id"].endswith("0068"))
    assert mark["english"] == "?" and mark["decision"] == "retention"
    assert mark["current_reference"]["exact_command_hex"] == mark["registered_reference"]["exact_command_hex"]
    return dict(source_comparison=str(stage.HISTORICAL), reconciled_differences=[r["id"] for r in tracked],
                native_ascii_question_mark_preserved=True)


verify_source = checked_text(parent.verify_source, {
    'checked["sheets"] + played["sheets"] + verify_town(candidate)["sheets"]': 'checked["sheets"] + played["sheets"]',
    'observed_count() == 23': 'observed_count() == 13',
    'native_count() == 27': 'native_count() == 9',
    'len(records) == 275': 'len(records) == 74',
    'len(changed) == 25': 'len(changed) == 9',
    'native_controls=preserved_scene_controls(records, b, candidate), ordinary_town_visits=verify_town(candidate),':
        'historical_Hodram_B66_reconciliation=verified_reconciliation(records),',
    'wording_revisions=25, wrap_only_revisions=0': 'wording_revisions=9, wrap_only_revisions=0',
    'justified_retentions=250': 'justified_retentions=65',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1064 and len(checks) == 399": "len(batches) == 1065 and len(checks) == 400",
    "previously_localized_records=277, contextual_records_revisited=277": "previously_localized_records=74, contextual_records_revisited=74",
    "prior_records_reviewed=277": "prior_records_reviewed=74",
    "justified_retentions=250, retained_choice_labels=2": "justified_retentions=65, retained_choice_labels=0",
    "prose_revisions=25": "prose_revisions=9",
    "ordinary_saved_town_visits=True": "ordinary_saved_town_visits=False",
    "(live.LIVE, DISPLAY, stage.PROOF, ORDINARY, stage.CHOICE_PROOF, glyphs.OUTPUT)":
        "(live.LIVE, DISPLAY, stage.PROOF, GLYPHS, stage.HISTORICAL)",
    "DISPLAY, ORDINARY, stage.CHOICE_PROOF, glyphs.OUTPUT, args.visual_review,":
        "DISPLAY, GLYPHS, args.visual_review,",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# North Sea and Hodram reconciliation testing candidate

The [testing ROM](../../{ROM.as_posix()}) carries nine dialogue revisions in two complete exchanges. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("palace_eirene_pereira_london", "north_sea_and_hodram_reconciliation").replace(
    "verified_aziza_shamshir_predecessor", "verified_palace_eirene_pereira_london_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
old_pins = parent.commit[parent.commit.index("    earlier = ["):parent.commit.index("    research =")]
commit = checked_text(parent.commit, {
    old_pins: "    earlier = [live.ROM, live.HODRAM_ROM, FIRST_STAGE]\n",
    "Preserve the palace and London candidate, predecessor and unique focused ROMs":
        "Preserve the North Sea and Hodram candidate, predecessor and unique focused ROMs",
    old_doc:'''    DOC.write_text(f"""# Rafael’s North Sea meeting and Hodram’s encounter with Camille

The complete clean-Japanese review covers 74 spoken lines. Nine have revised prose and 65 have specific retention reasons. Lil’s pact proposal keeps the distinction between her territorial claim and what she asks Rafael to do. Camille says that he and Lil are traveling separately for the time being. The earlier registered Hodram review supplies a source-bound comparison for six differing payloads in this exchange. [Coverage ledger](../{REVIEW.as_posix()})

All nine changed pages passed native and exact-font checks. Focused cold-boot replays verified 13 story panels and their nameplates, including Hodram’s normal-width question mark, the Port Worker’s warning and Lil’s one-line question. Startup and 17 focused repository tests passed. The original scene triggers, conditional variants outside the samples and handheld display remain unvisited for this batch. [Testing ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("palace_eirene_pereira_london", "north_sea_and_hodram_reconciliation")
scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::register", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
