"""Register the Fleet Info destination name after the focused display checks."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_cartridge_title_20261123 as template
from scripts import register_london_relic_tip_20261123 as parent
from scripts import replay_missionary_destination_20261123 as played
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_missionary_destination_20261123 as build
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.source_locked_derivation_v5118 import checked_text


PROFILE = "all-routes-missionary-destination-v1-20261123"
CHECK = "registered_missionary_destination_literal_and_complete_parent_inverse"
RECORD = "ARM9_FLEET_DESTINATION_MISSIONARY"
ARM, COMMON = build.ARM, parent.COMMON
ROM, WORK = build.ROM, build.ROOT
PATCH, PATCH_PROOF, REBUILT = played.PATCH, played.PATCH_PROOF, played.REBUILT
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_missionary_destination_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_missionary_destination.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA, STARTUP_CAPTURE = WORK / "own_startup_verification.json", WORK / "qa_passed.xml", played.STARTUP_CAPTURE
DOC = Path("docs/editorial_missionary_destination_registered_20261123.md")
CHECKPOINT = "Registered Missionary for the conditional Fleet Info destination."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=played.SHEET, PROOF=build.STORED)))


def verify(previous, visual_sha):
    stored, live, patch = map(stage.read, (build.STORED, played.REPORT, PATCH_PROOF))
    candidate = stage.digest(ROM)
    assert candidate == stored["candidate_sha256"] == live["candidate_sha256"] == patch["candidate"]["sha256"] == stage.digest(REBUILT)
    assert patch["byte_exact"] and stage.reference(PATCH) == patch["patch"]
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == stage.digest(stage.CLEAN)
    assert stored["exact_whole_parent_inverse"]
    assert stored["predecessor_sha256"] == live["predecessor_sha256"] == previous["candidate_sha256"] == stage.digest(previous["candidate"])
    assert stored["ordinary_town_controls"] == 114 and stored["offline_destination_cases"] == 116
    assert stored["formatted_destination"]["output_hex"] == b"To: Missionary".hex()
    assert live["ordinary_controller_navigation_after_fixture"] and not live["naturally_reached_destination_114"]
    assert live["exact_return_to_fleet_list"] and len(live["views"]) == 3
    assert all(stage.reference(row["path"]) == row for row in live["evidence"])
    visual = stage.reference(played.SHEET)
    assert visual == live["visual"] and visual["sha256"] == visual_sha

    before, after = Path(previous["candidate"]).read_bytes(), bytearray(ROM.read_bytes())
    at = stored["rom_offset"]
    original, revised = (bytes.fromhex(stored[key]) for key in ("current_hex", "staged_hex"))
    assert len(original) == len(revised) == 4 and after[at:at+4] == revised
    after[at:at+4] = original
    assert after == before
    image = stage.NdsImage.open(ROM)
    arm, common = image.read_file(ARM), image.read_file(COMMON)
    assert stage.sha256(arm).hexdigest() == stored["target_ARM9_sha256"]
    assert stage.sha256(common).hexdigest() == previous["target_COMMON_sha256"]
    assert all(stage.sha256(image.read_file(f"/data/SC{i}.DK4")).hexdigest() == previous[f"target_SC{i}_sha256"]
               for i in range(4))
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    code = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "missionary_only_destination_getter_literal_changed",
    })
    exec(compile(code, __file__ + "::startup-for-one-literal", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)
    snapshot = stage.read(STARTUP)["read_only_snapshot"]
    raw = build.read_ram(snapshot)
    literal, label = build.LITERAL - build.BASE, build.RESIDENT_NAME - build.BASE
    assert raw[literal:literal + 4] == revised and raw[label:label + len(build.TARGET)] == build.TARGET

    earlier = stage.read(parent.REVIEW)
    shared = earlier["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    entries = common_rows(common, arm)
    assert all(parent.build.town.reference(entries[row["message_ID"]]) == row["installed"] for row in shared["records"])
    record = dict(id=RECORD, file_path=ARM, decision="revision", speaker="System",
        context="The older Fleet Info panel displays the selected fleet's destination. Slot 114 names the separate in-game missionary object.",
        source_meaning="A missionary who spreads a faith.",
        localization_note="Use the established Missionary wording for the same occupation. The English label retains the game's generic role and discloses no invented rank or denomination.",
        english=build.ENGLISH, review=dict.fromkeys(files.GATES, True),
        source_reference=stored["original_japanese"], current_reference=dict(component=ARM, address=build.LITERAL, exact_hex=stored["current_hex"]),
        registered_reference=dict(component=ARM, address=build.LITERAL, exact_hex=stored["staged_hex"],
                                  text_address=build.RESIDENT_NAME, exact_C_string_hex=build.TARGET.hex()))
    outcome = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=[record], candidate_sha256=candidate, target_ARM9_sha256=stored["target_ARM9_sha256"],
        source_credit_added=0, visual_review=visual, stored_proof=stage.reference(build.STORED), gameplay=stage.reference(played.REPORT),
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=earlier["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=earlier["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_genoa_alternate_dialogue_predecessor=predecessor, london_relic_tip_release=str(REVIEW)":
        "verified_london_relic_tip_predecessor=predecessor, missionary_destination_release=str(REVIEW)",
    "len(batches) == 1113 and len(checks) == 448": "len(batches) == 1114 and len(checks) == 449",
    "COMMON in paths and COMMON in records": "ARM in paths and ARM in records",
    'assert all(item in records[COMMON] for item in revised)\n        assert sorted(revised) == [f"COMMON_MESSAGE_{build.KEY}"]':
        'assert revised == [RECORD] and RECORD not in records[ARM]\n        records[ARM] = [*records[ARM], RECORD]',
    "snapshot_scope=COMMON": "snapshot_scope=ARM",
    "london_relic_tip_release_proof": "missionary_destination_release_proof",
    '"london_relic_tip_pipeline"': '"missionary_destination_pipeline"',
    ", played.REPORT, PREVIEW": ", played.REPORT",
    "registered_manifest_entries=1114, passing_release_checks=449": "registered_manifest_entries=1115, passing_release_checks=450",
    "changed_internal_files=[COMMON]": "changed_internal_files=[ARM]",
    'target_COMMON_sha256=outcome["target_COMMON_sha256"]': 'target_ARM9_sha256=outcome["target_ARM9_sha256"]',
    "reviewed_UI_labels=0, contextual_records_revisited=12, contextual_decisions_reused=11, previously_localized_records=12":
        "reviewed_UI_labels=1, contextual_records_revisited=1, contextual_decisions_reused=0, previously_localized_records=0",
    "prose_revisions=1, justified_retentions=11": "prose_revisions=0, justified_retentions=0",
    "ordinary_London_Tavern=True": "focused_Fleet_Info_destination_fixture=True",
    "relic_tip_revised=1, texts_retained=11": "display_label_revised=1",
    '"london_relic_tip_20261123"': '"missionary_destination_20261123"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Missionary destination testing candidate

Fleet Info shows the established Missionary label for destination 114. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered London relic tip candidate": "Preserve the registered Missionary destination candidate",
    "1,114 entries and 449 passing checks": "1,115 entries and 450 passing checks",
    doc: '''    DOC.write_text(f"""# Fleet Info Missionary destination

Fleet Info now shows **To: Missionary** for the separate missionary destination object. The getter uses the existing resident English string. Its original Japanese source and the crew-role selector are recorded separately. [Exact source, current and installed references](../{REVIEW.as_posix()})

Offline native checks preserved all 114 town names, the no-target case and the original regional picker. A focused replay supplied slot 114 in Manuel Fleet's destination byte. The complete revised label fit the original detail and Report screens, and the list returned with the same pixels. This verifies the display with a supplied input. Ordinary reachability of slot 114 remains unverified. [Focused emulator evidence](../{VERIFY.as_posix()}/{played.SHEET.name})

The cumulative release passed 450 checks, its own startup and 17 focused regressions. The clean-input patch reconstructs it byte for byte. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    cli = template.ArgumentParser(description=__doc__)
    cli.add_argument("--visual-sha256")
    cli.add_argument("--finish-only", action="store_true")
    args = cli.parse_args()
    assert args.finish_only or args.visual_sha256
    scope = vars(template) | vars(parent) | globals()
    exec(compile(prepare + "\n" + finish, __file__ + "::missionary-destination-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
