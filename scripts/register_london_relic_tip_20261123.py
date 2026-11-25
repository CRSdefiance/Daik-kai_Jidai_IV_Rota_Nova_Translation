"""Register the London relic clue through the cumulative release transaction."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_cartridge_title_20261123 as template
from scripts import register_genoa_alternate_dialogue_20261123 as parent
from scripts import replay_london_relic_tip_20261123 as played
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_london_relic_tip_20261123 as build
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.source_locked_derivation_v5118 import checked_text


PROFILE = "all-routes-london-relic-tip-v1-20261123"
CHECK = "registered_london_relic_tip_and_complete_parent_inverse"
ARM, COMMON = build.ARM, build.COMMON
ROM, WORK = build.ROM, build.ROOT
PATCH, PATCH_PROOF, REBUILT = played.PATCH, played.PATCH_PROOF, played.REBUILT
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_london_relic_tip_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_london_relic_tip.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA, STARTUP_CAPTURE = WORK / "own_startup_verification.json", WORK / "qa_passed.xml", played.STARTUP_CAPTURE
DOC = Path("docs/editorial_london_relic_tip_registered_20261123.md")
CHECKPOINT = "Registered Marie's revised two-direction relic tip after ordinary London Tavern replays."
PREVIEW = WORK / "portrait_sheet_01.png"
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=played.SHEET, PROOF=build.STORED)))


def verify(previous, visual_sha):
    stored, manuscript, live, patch = map(stage.read, (build.STORED, build.MANUSCRIPT, played.REPORT, PATCH_PROOF))
    candidate = stage.digest(ROM)
    assert candidate == stored["candidate_sha256"] == live["candidate_sha256"] == patch["candidate"]["sha256"] == stage.digest(REBUILT)
    assert patch["byte_exact"] and stage.reference(PATCH) == patch["patch"]
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == stage.digest(stage.CLEAN)
    assert stored["previous_sha256"] == previous["candidate_sha256"] == live["predecessor_sha256"]
    assert stage.digest(previous["candidate"]) == previous["candidate_sha256"] and stored["whole_parent_inverse"]
    assert stored["manuscript"] == stage.reference(build.MANUSCRIPT) and stored["allocations"].keys() == {str(build.KEY)}
    assert stored["allocations"][str(build.KEY)]["new_null_fields"] == 0 and stored["original_argument_count"] == 5
    assert stage.reference(stored["comparison"]["path"]) == stored["comparison"]
    assert stage.reference(stored["original_gameplay"]["path"]) == stored["original_gameplay"]
    assert live["ordinary_battery_save_gameplay"] and not live["fixture"] and live["returned_to_tavern_and_town"]
    assert len(live["identical_control_frames"]) == 48 and len(live["revised_tip_holds"]) == 3
    assert len(live["original_menu_highlight_frames"]) == 3
    visuals = [stage.reference(played.SHEET), stage.reference(PREVIEW)]
    assert visuals[0] == live["visual"] and visuals[1]["sha256"] == stored["sheets"][0]["sha256"]
    assert stage.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    old, new = map(stage.NdsImage.open, (previous["candidate"], ROM))
    arm, common = new.read_file(ARM), new.read_file(COMMON)
    old_common = old.read_file(COMMON)
    assert stage.sha256(arm).hexdigest() == previous["target_ARM9_sha256"] == stored["target_ARM9_sha256"]
    assert stage.sha256(common).hexdigest() == stored["target_COMMON_sha256"]
    new.replace_file(COMMON, old_common)
    assert bytes(new.rom.save()) == Path(previous["candidate"]).read_bytes()
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    code = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "london_relic_tip_common_only_verified_arm9_unchanged",
    })
    exec(compile(code, __file__ + "::startup-for-common-only", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)

    prior = stage.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    before, after = (common_rows(data, arm) for data in (old_common, common))
    assert [a.message_id for a, b in zip(before, after, strict=True) if a != b] == [build.KEY]
    for row in shared["records"]:
        key = row["message_ID"]
        assert before[key] == after[key] and row["exact_body_retained"]
        assert build.town.reference(after[key]) == row["installed"]
    records = manuscript["records"]
    assert len(records) == 12 and {row["message_id"] for row in records if row["decision"] == "revision"} == {build.KEY}
    assert all(row["installed_hex"] == after[row["message_id"]].text.hex() for row in records)
    outcome = manuscript | dict(candidate_sha256=candidate, target_COMMON_sha256=stored["target_COMMON_sha256"],
        source_credit_added=0, visual_review=visuals, stored_proof=stage.reference(build.STORED),
        gameplay=stage.reference(played.REPORT), shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_genoa_dialogue_predecessor=predecessor, genoa_alternate_dialogue_release=str(REVIEW)":
        "verified_genoa_alternate_dialogue_predecessor=predecessor, london_relic_tip_release=str(REVIEW)",
    "len(batches) == 1112 and len(checks) == 447": "len(batches) == 1113 and len(checks) == 448",
    "STORY in paths and STORY in records": "COMMON in paths and COMMON in records",
    "records[STORY]": "records[COMMON]",
    "list(build.IDS)": '[f"COMMON_MESSAGE_{build.KEY}"]',
    "snapshot_scope=STORY": "snapshot_scope=COMMON",
    "genoa_alternate_dialogue_release_proof": "london_relic_tip_release_proof",
    '"genoa_alternate_dialogue_pipeline"': '"london_relic_tip_pipeline"',
    "registered_manifest_entries=1113, passing_release_checks=448": "registered_manifest_entries=1114, passing_release_checks=449",
    "changed_internal_files=[STORY]": "changed_internal_files=[COMMON]",
    'target_SC1_sha256=outcome["target_SC1_sha256"]': 'target_COMMON_sha256=outcome["target_COMMON_sha256"]',
    "contextual_records_revisited=52, contextual_decisions_reused=48, previously_localized_records=52":
        "contextual_records_revisited=12, contextual_decisions_reused=11, previously_localized_records=12",
    "prose_revisions=2, justified_retentions=48, text_display_revisions=4, wrap_only_revisions=2":
        "prose_revisions=1, justified_retentions=11, text_display_revisions=1, wrap_only_revisions=0",
    "ordinary_genoa_alternate_choices=True": "ordinary_London_Tavern=True",
    "alternate_dialogue_revised=4, texts_retained=48": "relic_tip_revised=1, texts_retained=11",
    '"genoa_alternate_dialogue_20261123"': '"london_relic_tip_20261123"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# London relic tip testing candidate

Marie's revised directions preserve the five original substitutions. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Genoa alternate dialogue candidate": "Preserve the registered London relic tip candidate",
    "1,113 entries and 448 passing checks": "1,114 entries and 449 passing checks",
    doc: '''    DOC.write_text(f"""# Marie's London relic clue

Marie's reply picks up the relic's name and gives tentative directions from the current town. Both directions stay together in each of the three observed Blue Oak Shield replies. Eleven other Tavern lines retain their wording. [Exact clean and installed review](../{REVIEW.as_posix()})

The offline comparison applied the original formatter to all 218 stock item names crossed with 36 supplied direction and distance combinations. Breaks inside distance and direction phrases fell from 4,200 to 2,912. All tested variants fit the original page. Some substitutions still break inside direction phrases or leave a short final row. The replay matched 48 control frames exactly. Three Tavern menu returns differ only in the Order Drink highlight background, and the return to London matches exactly. [Paired playback](../{VERIFY.as_posix()}/{played.SHEET.name}) · [Native sample pages](../{VERIFY.as_posix()}/{PREVIEW.name})

The release passed 449 checks, its own startup and 17 focused regressions. The clean-input patch reconstructs the ROM byte for byte. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::london-relic-tip-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
