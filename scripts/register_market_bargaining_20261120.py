"""Register the Market confirmation and bargaining batch on the exact current build."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_market_bargaining_20261120 as game
from scripts import register_amsterdam_tavern_editorial_20261120 as boot
from scripts import register_market_english_region_20261120 as parent
from scripts import stage_market_bargaining_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch, native = parent.base, parent.batch, parent.native
PROFILE = "all-routes-market-bargaining-v1-20261120"
ROOT = Path("out/market_bargaining_registered_20261120_v1")
ROM = ROOT / "Translation_DS_Market_Bargaining_20261120_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261120_market_bargaining_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_market_bargaining_registered_20261120.md")
STARTUP, QA, VISUAL = (stage.ROOT / n for n in ("own_startup_verification.json", "qa.xml", "visual_review.json"))
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
PENDING = Path("translations/editorial_checkpoints/SharedText_20261110_v1/shared_display_owners_20261119_v1.json")
CHECKPOINT = "Registered the natural Market trade confirmation and one-line bargaining reply."


def location_changes(old, new):
    workflow = stage.workflow
    shifted = {}
    for n, (before, after) in enumerate(zip(old, new, strict=True)):
        if n in stage.REVISIONS:
            continue
        previous, current = workflow.reference(before), workflow.reference(after)
        assert before.text == after.text
        if previous != current:
            assert {key for key in previous if previous[key] != current[key]} == {"record_index"}
            shifted[n] = dict(previous_reference=previous, current_reference=current, exact_hex=after.text.hex())
    return shifted


def verify(registry, previous, viewed):
    stored, draft, result = map(base.load, (stage.STORED, stage.MANUSCRIPT, game.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == draft["candidate_sha256"] == result["candidate_sha256"]
    assert base.digest(parent.ROM) == previous["candidate_sha256"] == stored["previous_sha256"] == result["previous_sha256"]
    assert base.digest(stage.CLEAN) == previous["clean_input_sha256"] == draft["clean_sha256"]
    assert stored["whole_parent_inverse"] and (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    assert base.digest(stage.MANUSCRIPT) == stored["manuscript_sha256"]
    assert viewed == {str(game.SHEET): result["sheet_sha256"], **{p["path"]: p["sha256"] for p in stored["sheets"]}}
    assert all(base.digest(p) == sha for p, sha in (viewed | result["evidence"]).items())
    assert [r["message_ID"] for r in result["actual_no_then_yes_confirmation_holds"]] == [14, 14]
    assert result["offline_only_message_IDs"] == [25]
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [32, 0, 0, 2]

    workflow = stage.workflow
    clean, prior, target = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(workflow.files, (prior, target))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.COMMON}
    arm, common = before[stage.ARM], before[stage.COMMON]
    assert workflow.digest(arm) == stored["target_ARM9_sha256"] == previous["target_ARM9_sha256"]
    directory = workflow.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    original = workflow.owned_entries(common, arm, directory)
    revised = {n: text.encode("ascii") for n, text in stage.REVISIONS.items()}
    rebuilt, entries, slots = workflow.owned_deployment(common, arm, original, revised)
    assert rebuilt == after[stage.COMMON] and workflow.digest(rebuilt) == stored["target_COMMON_sha256"]
    assert {str(n): slot for n, slot in slots.items()} == stored["allocations"]
    assert [i for i, (a, b) in enumerate(zip(original, entries, strict=True)) if a.text != b.text] == [14, 25]
    target.replace_file(stage.COMMON, common)
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()

    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(workflow.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    changed_refs = location_changes(original, entries)
    assert len(changed_refs) == 91
    pending = base.load(PENDING)["records"]
    assert len(pending) == 276
    for row in pending:
        n = row["message_ID"]
        assert workflow.reference(original[n]) == row["current_reference"]
        assert entries[n].text.hex() == row["current_hex"]

    proof = FunctionType(boot.startup_proof.__code__, boot.startup_proof.__globals__ |
                         {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE})
    proof(previous, candidate, arm)
    for row in draft["records"]:
        n = row["message_ID"]
        assert row["staged_hex"] == entries[n].text.hex()
        row["review"]["formatting"] = True
        row["registered_reference"] = row["staged_reference"] | {"candidate_sha256": candidate}
    draft.update(gameplay=result, checked_story_format_guard=controls, new_contextual_credit=0,
        prior_shared_display_ledger=str(PENDING), prior_shared_display_sha256=base.digest(PENDING),
        physical_reference_index_updates=changed_refs,
        shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    validate_natural_dialogue_batch(draft)
    return stored, draft, {stage.COMMON: workflow.digest(rebuilt)}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 943 and len(manifest["checks"]) == 278':
        'len(manifest["batches"]) == 944 and len(manifest["checks"]) == 279',
    "release_stack_before_market_english_region.json": "release_stack_before_market_bargaining.json",
    "release_stack_with_market_english_region.json": "release_stack_with_market_bargaining.json",
    "for source in (stage.PROOF, STARTUP, QA, game.PROOF, args.visual_review,":
        "for source in (stage.STORED, STARTUP, QA, game.PROOF, args.visual_review,",
    "stored_proof_sha256=base.digest(stage.PROOF)": "stored_proof_sha256=base.digest(stage.STORED)",
    "verified_market_report_status_predecessor=predecessor, market_english_region_release=str(REVIEW)":
        "verified_market_english_region_predecessor=predecessor, market_bargaining_release=str(REVIEW)",
    "registered_market_english_region_and_complete_parent_inverse": "registered_market_bargaining_and_complete_parent_inverse",
    'manifest["market_english_region_pipeline"]': 'manifest["market_bargaining_pipeline"]',
    '    ids = manifest["changed_records"][batch.ARM]': '    ids = manifest["changed_records"][stage.COMMON]',
    "    assert not any(new in ids for new in new_ids)\n    ids.extend(new_ids)":
        '    assert all((stage.COMMON, key) in credited for key in new_ids)\n    ids.extend(key for key in new_ids if key not in ids)',
    'owned_region_slot=stored["changed_slot"], target_ARM9_sha256=archives[batch.ARM]':
        'owned_COMMON_allocations=stored["allocations"], target_COMMON_sha256=archives[stage.COMMON]',
    "changed_components=1, target_ARM9_sha256=archives[batch.ARM]":
        "changed_components=1, target_COMMON_sha256=archives[stage.COMMON]",
    "ARM9_sha256=archives[batch.ARM], MESFILE_sha256=previous[\"target_COMMON_sha256\"]":
        'ARM9_sha256=previous["target_ARM9_sha256"], MESFILE_sha256=archives[stage.COMMON]',
    "reviewed_UI_labels=21, new_contextual_records=0, prose_revisions=0, spacing_revisions=1, wrap_only_revisions=0, justified_retentions=20":
        "reviewed_UI_labels=0, previously_localized_records=19, new_contextual_records=0, prose_revisions=2, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=17",
    "text_display_revisions=1, pagination_fixes=0": "text_display_revisions=0, pagination_fixes=0",
    "ordinary_London_report=True, offline_native_town_cases=90":
        "ordinary_Lisbon_trade_no_and_yes=True, alternate_bargaining_voice_offline_only=True",
    'ledger["market_english_region_20261120"]': 'ledger["market_bargaining_20261120"]',
    "ui_labels_reviewed=21, display_revisions=1, actual_paired_states=1, new_contextual_credit=0,\n        prose_revisions=0, spacing_revisions=1, wrap_only_revisions=0, justified_retentions=20":
        "prior_records_reviewed=19, actual_paired_states=2, new_contextual_credit=0,\n        prose_revisions=2, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=17",
    '    pending["candidate_sha256"] = candidate':
        '    pending["candidate_sha256"] = candidate\n    pending["physical_reference_index_updates"] = str(REVIEW)',
    "Preserve the Market Info region ROM or reconstruction": "Preserve the Market Bargaining ROM or reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Market bargaining candidate

The [local ROM](../../{ROM.as_posix()}) carries the revised Trade confirmation and the one-line bargaining request alongside the preceding fixes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Market trade confirmation and bargaining

The crew member now asks **“All set, then?”** before a pending trade is finalized. The more insistent voice asks **“Come on, can’t you do a bit better?”**, which works for both purchases and sales. Both replies fit on single lines. Seventeen other lines retain their established wording, including the trader’s fee explanation and farewell. [Exact decisions](../{REVIEW.as_posix()})

Paired ordinary Lisbon replays verified the full confirmation twice, the return to the same pending trade after No, and the farewell and menu return after Yes. The revised bargaining alternative passed the original native formatter and full glyph checks offline. [Lisbon replay](../{(VERIFY / game.SHEET.name).as_posix()}) · [Native pages](../{(VERIFY / "portrait_sheet_01.png").as_posix()})

The cumulative patch reconstructs the verified ROM byte for byte. Six startup frames, 24 protected getters and 30 focused tests passed. Two optional legacy tests skipped. The existing review count remains 27,700, with 276 stored shared keys open for display-owner adjudication. Hardware remains outside this pass. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + "::register", "exec"), env)


if __name__ == "__main__":
    env["main"]()
