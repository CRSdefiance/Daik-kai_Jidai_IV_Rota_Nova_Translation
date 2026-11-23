"""Register the assigned Fleet Info captions and their bounded native report layout."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_cartridge_title_20261123 as template
from scripts import register_seoul_shop_rumor_20261123 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts.check_assigned_fleet_release_20261123 import PATCH, PATCH_PROOF, REBUILT, ROM, STARTUP_CAPTURE, WORK
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_azores_wording_20261123 import COMMON
from scripts.verify_assigned_fleet_detail_20261123 import ARM, OUT

PROFILE = "all-routes-assigned-fleet-info-v1-20261123"
CHECK = "registered_assigned_fleet_info_bounds_format_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_assigned_fleet_info_candidate")
VERIFY = PACKAGE / "verification"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
MANIFEST = ROM.with_suffix(".manifest.json")
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_with_assigned_fleet_info.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA = WORK / "own_startup_verification.json", WORK / "qa_passed.xml"
DOC = Path("docs/editorial_assigned_fleet_info_registered_20261123.md")
CHECKPOINT = "Registered English destination and finance captions in the assigned Fleet Info panel."
SHEET = OUT.with_suffix(".png")
STORED = WORK / "stage.json"
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=STORED)))


def verify(previous, visual_sha):
    gameplay, reconstruction, stored = map(stage.read, (OUT, PATCH_PROOF, STORED))
    candidate = stage.digest(ROM)
    assert candidate == reconstruction["candidate"]["sha256"] == stored["staged"]["sha256"] == stage.digest(REBUILT)
    assert reconstruction["byte_exact"] and stage.reference(PATCH) == reconstruction["patch"]
    assert stage.digest(stage.CLEAN) == previous["clean_input_sha256"] == stored["clean"]["sha256"]
    assert stage.digest(previous["candidate"]) == previous["candidate_sha256"] == gameplay["original_ROM_sha256"]
    assert stored["registered_predecessor"]["sha256"] == previous["candidate_sha256"]
    assert stage.digest(SHEET) == gameplay["screenshot"]["sha256"] == visual_sha
    verified = gameplay["trials"]["packed_report"]
    assert verified["rom"]["sha256"] == candidate and stored["exact_inverse"]
    assert [row["label"] for row in verified["formatted"]["report_rows"]] == ["Income", "Expenses", "Invested"]
    assert len(verified["formatted"]["offline"]["destination_names"]) == 115
    assert len(verified["formatted"]["offline"]["finance_cases"]) == 11
    assert all(verified[k] for k in ("seven_prechange_frames_match", "report_closes_to_exact_fleet_detail",
                                    "fleet_detail_closes_to_exact_list"))
    original, current = (Path(p).read_bytes() for p in (previous["candidate"], ROM))
    restored = bytearray(current)
    for row in stored["records"]:
        at = row["rom_offset"]
        installed, old = (bytes.fromhex(row[k]) for k in ("staged_hex", "current_hex"))
        assert len(installed) == len(old) and restored[at:at + len(old)] == installed
        restored[at:at + len(old)] = old
    assert restored == original
    image = stage.NdsImage.open(ROM)
    arm = image.read_file(ARM)
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    assert all(stage.sha256(image.read_file(f"/data/SC{i}.DK4")).hexdigest() == previous[f"target_SC{i}_sha256"]
               for i in range(4))
    assert stage.sha256(image.read_file(COMMON)).hexdigest() == previous["target_COMMON_sha256"]
    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    startup_scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    startup_code = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "assigned_fleet_info_only_owned_spans_changed",
    })
    exec(compile(startup_code, __file__ + "::startup", "exec"), startup_scope)
    startup_scope["startup_proof"](previous, candidate, arm)
    review = stage.read(parent.REVIEW)
    shared = review["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    records = []
    for row, key, meaning, context, span in zip(gameplay["records"], ("DESTINATION", "REPORT"),
            ("The target city of the fleet.", "Income, expenses, and the amount invested."),
            ("Fleet Info shows the selected fleet's current patrol destination.",
             "Report opens from the selected fleet's detail screen and shows the three original unsigned totals."),
            stored["records"][:2], strict=True):
        records.append(row | dict(id="ARM9_ASSIGNED_FLEET_" + key, speaker="System",
            context=context, source_meaning=meaning, english=row["proposed_English"], decision="revision",
            installed=dict(component=ARM, offset=span["staged_offset"], exact_hex=span["staged_hex"]),
            review=dict.fromkeys(("source", "context", "localization", "naturalness", "formatting"), True)))
    records.append(dict(id="ARM9_ASSIGNED_FLEET_LEVEL", speaker="System", decision="retention",
        context="On the fleet detail screen the upper panel identifies Hodram and his level.",
        source_meaning="The selected character's level as a four-column integer field.",
        source=dict(component=ARM, offset=0x13710C, Japanese="レベル%4d", exact_hex="838c8378838b25346400"),
        current=dict(component=ARM, offset=0x13710C, exact_hex="4c6576656c2025346400"),
        installed=dict(component=ARM, offset=0x137904, exact_hex="4c6576656c2025346400"),
        english="Level %4d", localization_note="Keep the existing label and width. Its stored bytes match an existing caption.",
        review=dict.fromkeys(("source", "context", "localization", "naturalness", "formatting"), True)))
    stored_review = dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=list(records[0]["review"]), records=records,
        candidate_sha256=candidate, target_ARM9_sha256=stage.sha256(arm).hexdigest(), source_credit_added=0,
        visual_review=stage.reference(SHEET), gameplay=stage.reference(OUT), owned_spans=stored["records"],
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=review["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=review["retained_editorial_coverage_sha256"],
        full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(stored_review)
    return stored_review


prepare_source = getsource(template.prepare)
finish_source = getsource(template.finish)
readme = prepare_source[prepare_source.index('    (PACKAGE / "README.md")'):prepare_source.index('    stage.write(PACKAGE / "checksums.json"')]
doc = finish_source[finish_source.index("    DOC.write_text"):finish_source.index("    prefix =")]
prepare = checked_text(prepare_source, {
    "with mapped(base.REGISTRY) as data:": "with mapped(REGISTRY_BEFORE) as data:",
    "with mapped(base.LEDGER) as data:": "with mapped(LEDGER_BEFORE) as data:",
    "verified_azores_wording_predecessor=predecessor, cartridge_title_release=str(REVIEW)":
        "verified_seoul_shop_rumor_predecessor=predecessor, assigned_fleet_info_release=str(REVIEW)",
    "len(batches) == 1102 and len(checks) == 437": "len(batches) == 1105 and len(checks) == 440",
    'assert stage.BANNER not in paths and stage.BANNER not in records and CHECK not in checks':
        'assert ARM in paths and ARM in records and CHECK not in checks',
    'records[stage.BANNER] = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]':
        'revised = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]\n'
        '        assert revised == ["ARM9_ASSIGNED_FLEET_DESTINATION", "ARM9_ASSIGNED_FLEET_REPORT"]\n'
        '        records[ARM] = [*records[ARM], *revised]',
    'assert len(records[stage.BANNER]) == 5': 'assert records[ARM][-len(revised):] == revised',
    "changed_paths=sorted([*paths, stage.BANNER])": "changed_paths=paths",
    "snapshot_scope=stage.BANNER": "snapshot_scope=ARM",
    "banner_release_proof": "fleet_info_release_proof",
    'cartridge_title_pipeline': 'assigned_fleet_info_pipeline',
    "stage.SHEET, stage.PROOF": "stage.SHEET, stage.PROOF, OUT",
    "registered_manifest_entries=1103, passing_release_checks=438, changed_components=1, changed_internal_files=[stage.BANNER]":
        "registered_manifest_entries=1106, passing_release_checks=441, changed_components=1, changed_internal_files=[ARM],\n"
        '        target_ARM9_sha256=outcome["target_ARM9_sha256"]',
    "reviewed_UI_labels=5": "reviewed_UI_labels=4",
    "contextual_records_revisited=0, contextual_decisions_reused=0, previously_localized_records=0":
        "contextual_records_revisited=3, contextual_decisions_reused=1, previously_localized_records=1",
    "text_display_revisions=5": "text_display_revisions=4",
    "host_preview_of_all_six_banner_fields=True": "ordinary_assigned_fleet_info=True",
    "handheld_firmware_display=False, launcher_GUI_display=False": "handheld=False",
    "English_launcher_fields=5, original_Japanese_title_retained=True": "English_fleet_fields=4, existing_level_retained=True",
    '"cartridge_title_20261123"': '"assigned_fleet_info_20261123"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Assigned Fleet Info testing candidate

Fleet Info now displays the assigned destination in English. Report displays Income, Expenses, and Invested in three aligned rows. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(finish_source, {
    "Preserve the registered cartridge-title candidate": "Preserve the registered assigned Fleet Info candidate",
    doc: '''    DOC.write_text(f"""# Assigned Fleet Info localization

After assigning Manuel Fleet to patrol Stockholm, ordinary controls opened **Info**, **Fleet Info**, **Manuel Fleet**, and **Report**. The prepared save supplied the existing fleet. The revised panels show **To: Stockholm**, **Income**, **Expenses**, and **Invested**. The three amounts stay right aligned. The Level caption keeps its existing text.

The paired replay verified both closures, seven unchanged control frames and every revised glyph on the observed panels. The offline formatter checks preserved 115 destination arguments and 11 sets of financial amounts, including the unsigned maximum. The isolated Missionary argument stays tracked because ordinary orders use town slots 0–89. Six startup comparisons, 24 protected name getters, eight right-bound spans, 17 focused tests and byte-exact patch reconstruction passed. [Exact source and installed references](../{REVIEW.as_posix()}) · [Clean-input patch](../{PACKAGE.as_posix()}/translation.xdelta)
""", encoding="utf-8")
''',
    "1,103 entries and 438 passing checks": "1,106 entries and 441 passing checks",
})


if __name__ == "__main__":
    parser = template.ArgumentParser(description=__doc__)
    parser.add_argument("--visual-sha256")
    parser.add_argument("--finish-only", action="store_true")
    args = parser.parse_args()
    assert args.finish_only or args.visual_sha256
    scope = vars(template) | globals()
    exec(compile(prepare + "\n" + finish, __file__ + "::registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
