"""Register the original Market Info cultural-region renderer repair."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_market_english_region_20261120 as game
from scripts import register_amsterdam_tavern_editorial_20261120 as boot
from scripts import register_market_report_status_20261120 as parent
from scripts import stage_market_english_region_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch, native = parent.base, parent.batch, parent.native
PROFILE = "all-routes-market-english-region-v1-20261120"
ROOT = Path("out/market_english_region_registered_20261120_v1")
ROM = ROOT / "Translation_DS_Market_English_Region_20261120_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261120_market_english_region_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_market_english_region_registered_20261120.md")
STARTUP, QA, VISUAL = (stage.ROOT / n for n in ("own_startup_verification.json", "qa_retry.xml", "visual_review.json"))
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
SHEETS = (game.SHEET, game.NATIVE_SHEET)
CHECKPOINT = "Registered London’s English Region heading and centered all 21 Market Info region headings."


def verify(registry, previous, viewed):
    stored, result = map(base.load, (stage.PROOF, game.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == result["candidate_sha256"]
    assert stored["parent_sha256"] == result["parent_sha256"] == base.digest(parent.ROM) == previous["candidate_sha256"]
    assert base.digest(stage.CLEAN) == stored["clean_input_sha256"] == previous["clean_input_sha256"]
    assert stored["whole_parent_inverse"] and stored["clean_input_patch_byte_exact"]
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    assert base.digest(stage.ROOT / "translation.xdelta") == stored["clean_input_patch_sha256"]
    assert viewed == result["sheets"] == {str(p): base.digest(p) for p in SHEETS}
    assert all(base.digest(p) == sha for p, sha in result["evidence"].items())
    assert result["checked_ordinary_return"] and len(result["actual_London_report_holds"]) == 1
    assert len(result["retrospective_actor_alias_references"]) == 2
    records = [row | {"file_path": stage.ARM} for row in result["records"]]
    assert len(records) == 21 and {i for row in records for i in row["original_town_indices"]} == set(range(90))
    assert [row["english"] for row in records if row["decision"] == "revision"] == ["English Region"]
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [32, 0, 0, 2]

    clean, prior, target = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(stage.report.files, (prior, target))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.ARM}
    arm, common = after[stage.ARM], after[batch.COMMON]
    rebuilt, slot = stage.patch(clean.read_file(stage.ARM), before[stage.ARM])
    assert rebuilt == arm and slot == stored["changed_slot"] and batch.digest(arm) == stored["target_ARM9_sha256"]
    assert stage.cache_plan(arm) == stage.cache_plan(before[stage.ARM])
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(stage.report.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    table = batch.owned_entries(common, arm, batch.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET]))
    pending = base.load(parent.parent.parent.parent.parent.PENDING)["records"]
    assert len(pending) == 276 and all(batch.reference(table[r["message_ID"]]) == r["current_reference"]
        and table[r["message_ID"]].text.hex() == r["current_hex"] for r in pending)
    proof = FunctionType(boot.startup_proof.__code__, boot.startup_proof.__globals__ |
                         {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE})
    proof(previous, candidate, arm)
    draft = result | dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=batch.GATES, records=records,
        checked_story_format_guard=controls, shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"],
        changed_slot=slot, new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {batch.ARM: batch.digest(arm)}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 942 and len(manifest["checks"]) == 277':
        'len(manifest["batches"]) == 943 and len(manifest["checks"]) == 278',
    "stage.PROOF, STARTUP, QA, game.chart.OUTPUT, game.PROOF, args.visual_review":
        "stage.PROOF, STARTUP, QA, game.PROOF, args.visual_review",
    "release_stack_before_market_report.json": "release_stack_before_market_english_region.json",
    "release_stack_with_market_report.json": "release_stack_with_market_english_region.json",
    "verified_sound_sirens_predecessor=predecessor, market_report_status_release=str(REVIEW)":
        "verified_market_report_status_predecessor=predecessor, market_english_region_release=str(REVIEW)",
    "registered_market_report_status_and_complete_parent_inverse": "registered_market_english_region_and_complete_parent_inverse",
    'manifest["market_report_status_pipeline"]': 'manifest["market_english_region_pipeline"]',
    'owned_chart_slots=stored["chart_rows"], owned_report_rectangles=stored["status_geometry"]':
        'owned_region_slot=stored["changed_slot"]',
    "reviewed_UI_labels=7, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1":
        "reviewed_UI_labels=21, new_contextual_records=0, prose_revisions=0, spacing_revisions=1, wrap_only_revisions=0, justified_retentions=20",
    "text_display_revisions=7, pagination_fixes=0": "text_display_revisions=1, pagination_fixes=0",
    "ordinary_Lisbon_report=True, initialized_hidden_fields=True,\n                                       natural_activation=False":
        "ordinary_London_report=True, offline_native_town_cases=90,\n                                       natural_activation=True",
    'ledger["market_report_status_20261120"]': 'ledger["market_english_region_20261120"]',
    "ui_labels_reviewed=7, display_revisions=7, actual_paired_states=4, new_contextual_credit=0,\n        prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1":
        "ui_labels_reviewed=21, display_revisions=1, actual_paired_states=1, new_contextual_credit=0,\n        prose_revisions=0, spacing_revisions=1, wrap_only_revisions=0, justified_retentions=20",
    "Preserve the Market Info ROM or reconstruction": "Preserve the Market Info region ROM or reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Market Info English Region candidate

The [local ROM](../../{ROM.as_posix()}) displays **English Region** in London and centers all 21 cultural-region headings within the Market Info panel.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Market Info cultural-region headings

London’s Market Info panel now displays **English Region**. The Japanese identifies the cultural and economic grouping used by the town’s report. The original renderer used spacing for the shorter Japanese suffix. Centering the English headings restores all of the final letters within the original 108-pixel window, including West Africa Region and East Africa Region. Twenty heading names retain their established wording with individual reasons. [Exact decisions](../{REVIEW.as_posix()})

The paired ordinary London emulator replay verified the complete heading and the return to the route chart. The native offline check executed all 90 town selections across 21 cultural regions and matched the entire glyph plane for each title. The two actor table aliases for Alexandria and Sao Jorge already render in English in the earlier joined-name proof. This batch binds those unchanged fields to the current ROM. [London comparison](../{(VERIFY / game.SHEET.name).as_posix()}) · [All 21 native headings](../{(VERIFY / game.NATIVE_SHEET.name).as_posix()})

The clean-input patch rebuilds the cumulative candidate byte for byte. Six startup frames, 24 protected name getters and 30 focused tests passed. Two optional historical tests skipped. The dialogue coverage remains 27,700 credited records with 276 stored shared keys open for display-owner adjudication. Hardware was outside the gameplay check. [Registered candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + "::register", "exec"), env)


if __name__ == "__main__":
    env["main"]()
