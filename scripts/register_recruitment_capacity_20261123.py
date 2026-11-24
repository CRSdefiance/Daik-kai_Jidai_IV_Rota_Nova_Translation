"""Register the verified spare-capacity replies on the cumulative Azores candidate."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_cartridge_title_20261123 as template
from scripts import register_azores_return_20261123 as parent
from scripts import replay_recruitment_capacity_20261123 as checks
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_recruitment_capacity_wraps_20261123 as build
from scripts import verify_recruitment_capacity_20261123 as played
from scripts.source_locked_derivation_v5118 import checked_text


PROFILE = "all-routes-recruitment-capacity-wraps-v1-20261123"
CHECK = "registered_recruitment_capacity_original_loader_wrap_and_complete_parent_inverse"
ARM, COMMON, ROM, WORK = build.ARM, build.COMMON, build.ROM, build.ROOT
PATCH, PATCH_PROOF, REBUILT = checks.PATCH, checks.PATCH_PROOF, checks.REBUILT
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_recruitment_capacity_candidate")
VERIFY = PACKAGE / "verification"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
MANIFEST = ROM.with_suffix(".manifest.json")
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_recruitment_capacity.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA = WORK / "own_startup_verification.json", WORK / "qa_passed.xml"
STARTUP_CAPTURE = checks.STARTUP_CAPTURE
DOC = Path("docs/editorial_recruitment_capacity_registered_20261123.md")
CHECKPOINT = "Reflowed all seven Recruit Crew spare-capacity replies and verified Manuel and Charles in ordinary play."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=played.SHEET, PROOF=build.PROOF)))


def verify(previous, visual_sha):
    stored, gameplay, rebuilt = map(stage.read, (build.PROOF, played.REPORT, PATCH_PROOF))
    sha = stage.digest(ROM)
    assert sha == stored["candidate_sha256"] == gameplay["candidate_sha256"] == rebuilt["candidate"]["sha256"] == stage.digest(REBUILT)
    assert rebuilt["byte_exact"] and stage.reference(PATCH) == rebuilt["patch"]
    assert rebuilt["clean_input_sha256"] == previous["clean_input_sha256"] == stage.digest(stage.CLEAN)
    assert previous["candidate_sha256"] == gameplay["previous_sha256"] == stored["verified_predecessor_sha256"]
    assert previous["candidate_sha256"] == stage.digest(previous["candidate"])
    assert stored["whole_parent_inverse"] and len(stored["records"]) == 14
    visual = stage.reference(played.SHEET)
    sheets = stored["sheets"]
    assert all(stage.reference(row["path"])["sha256"] == row["sha256"] for row in sheets)
    combined = [visual] + [stage.reference(row["path"]) for row in sheets]
    assert stage.sha256("".join(row["sha256"] for row in combined).encode("ascii")).hexdigest() == visual_sha
    assert visual == gameplay["screenshot"]
    live = gameplay["ordinary_play"]
    assert [live[key]["message_ID"] for key in ("azores", "istanbul")] == [1048, 1042]
    assert sum(len(row["holds"]) for row in live.values()) == 3

    old, candidate = map(stage.NdsImage.open, (previous["candidate"], ROM))
    arm, common = (candidate.read_file(path) for path in (ARM, COMMON))
    assert stage.sha256(arm).hexdigest() == previous["target_ARM9_sha256"] == stored["target_ARM9_sha256"]
    assert stage.sha256(common).hexdigest() == stored["target_COMMON_sha256"]
    old_common = old.read_file(COMMON)
    assert old_common != common
    candidate.replace_file(COMMON, old_common)
    assert bytes(candidate.rom.save()) == Path(previous["candidate"]).read_bytes()
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    for route in range(4):
        assert stage.sha256(candidate.read_file(f"/data/SC{route}.DK4")).hexdigest() == previous[f"target_SC{route}_sha256"]

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(f, "0")) for f in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    code = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "recruitment_common_only_verified_arm9_unchanged",
    })
    exec(compile(code, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, sha, arm)

    earlier = stage.read(parent.REVIEW)
    shared = earlier["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    followups = [row for row in stored["records"] if row["decision"] == "wrap lead"]
    records = [row for row in stored["records"] if row["decision"] != "wrap lead"]
    assert len(records) == 12 and [row["message_id"] for row in followups] == [1039, 1041]
    before, after = (build.recruitment.catalogue(arm, archive) for archive in (old_common, common))
    for row in shared["records"]:
        key = row["message_ID"]
        assert before[key] == after[key] and row["exact_body_retained"]
        assert build.batch.reference(after[key]) == row["installed"]
    result = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=stored["review_gates"], records=records, candidate_sha256=sha,
        target_COMMON_sha256=stored["target_COMMON_sha256"], source_credit_added=0, visual_review=combined,
        stored_proof=stage.reference(build.PROOF), gameplay=stage.reference(played.REPORT),
        pending_shortfall_wraps=followups, shared_consumer_binding=shared | dict(candidate_sha256=sha),
        retained_four_route_census_sha256=earlier["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=earlier["retained_editorial_coverage_sha256"],
        full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


prep, seal = getsource(template.prepare), getsource(template.finish)
readme = prep[prep.index('    (PACKAGE / "README.md")'):prep.index('    stage.write(PACKAGE / "checksums.json"')]
doc = seal[seal.index("    DOC.write_text"):seal.index("    prefix =")]
prepare = checked_text(prep, {
    "verified_azores_wording_predecessor=predecessor, cartridge_title_release=str(REVIEW)":
        "verified_developed_azores_predecessor=predecessor, recruitment_capacity_release=str(REVIEW)",
    "len(batches) == 1102 and len(checks) == 437": "len(batches) == 1108 and len(checks) == 443",
    'assert stage.BANNER not in paths and stage.BANNER not in records and CHECK not in checks':
        'assert COMMON in paths and COMMON in records and CHECK not in checks',
    'records[stage.BANNER] = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]':
        'revised = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]\n'
        '        assert all(item in records[COMMON] for item in revised)',
    'assert len(records[stage.BANNER]) == 5': 'assert revised == [f"COMMON_MESSAGE_{key}" for key in build.DRAFTS]',
    "changed_paths=sorted([*paths, stage.BANNER])": "changed_paths=paths",
    "Path(stage.__file__)": "Path(build.__file__)",
    "snapshot_scope=stage.BANNER": "snapshot_scope=COMMON, revised_records=revised",
    "banner_release_proof": "recruitment_capacity_release_proof",
    '"cartridge_title_pipeline"': '"recruitment_capacity_pipeline"',
    "stage.SHEET, stage.PROOF": "stage.SHEET, stage.PROOF, played.REPORT, *(Path(row['path']) for row in outcome['visual_review'][1:])",
    "registered_manifest_entries=1103, passing_release_checks=438, changed_components=1, changed_internal_files=[stage.BANNER]":
        'registered_manifest_entries=1109, passing_release_checks=444, changed_components=1, changed_internal_files=[COMMON],\n'
        '        target_COMMON_sha256=outcome["target_COMMON_sha256"]',
    "reviewed_UI_labels=5, contextual_records_revisited=0, contextual_decisions_reused=0, previously_localized_records=0":
        "reviewed_UI_labels=0, contextual_records_revisited=14, contextual_decisions_reused=5, previously_localized_records=14",
    "new_contextual_records=0, prose_revisions=0, justified_retentions=1, text_display_revisions=5":
        "new_contextual_records=0, prose_revisions=7, justified_retentions=5, text_display_revisions=7, wrap_only_revisions=0",
    "host_preview_of_all_six_banner_fields=True": "ordinary_azores_and_istanbul_tavern=True",
    "handheld_firmware_display=False, launcher_GUI_display=False": "handheld=False",
    "English_launcher_fields=5, original_Japanese_title_retained=True":
        "capacity_voices_revised=7, dialogue_retained=5, separate_shortfall_leads=2",
    '"cartridge_title_20261123"': '"recruitment_capacity_20261123"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Recruit Crew capacity testing candidate

All seven spare-capacity replies keep the count legible and the follow-up question together. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(seal, {
    "Preserve the registered cartridge-title candidate": "Preserve the registered Recruit Crew capacity candidate",
    "1,103 entries and 438 passing checks": "1,109 entries and 444 passing checks",
    doc: '''    DOC.write_text(f"""# Recruit Crew capacity dialogue

All seven officers' spare-capacity prompts read naturally in two lines. Each still gives the amount of space aboard before asking whether to recruit again. The source and formatting ledger records 14 compared lines, seven revisions, five justified retentions, and two separate shortfall wrap findings. The original numeric substitution and selectors carry forward. [Exact source, previous and installed records](../{REVIEW.as_posix()})

Ordinary Azores and Istanbul Tavern replays verified Manuel's 67 and Charles's 51, the complete text and nameplates, and the transition to Assign Sailors after declining another round. The Istanbul replay continued to the Tavern entrance. The quoted costs and balances match the established replay. All seven revised variants passed native offline formatting at 12 supplied counts each. The five voices outside these two ordinary replays have offline coverage. [Paired and ordinary gameplay](../{VERIFY.as_posix()}/{played.SHEET.name})

The registered ROM passed six startup frame comparisons, 24 protected name getters, eight ASCII right-bound spans and all 17 focused tests. Its clean-input patch reconstructs the exact candidate. [Clean-input patch](../{PACKAGE.as_posix()}/translation.xdelta)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    cli = template.ArgumentParser(description=__doc__)
    cli.add_argument("--visual-sha256")
    cli.add_argument("--finish-only", action="store_true")
    args = cli.parse_args()
    assert args.finish_only or args.visual_sha256
    scope = vars(template) | globals()
    exec(compile(prepare + "\n" + finish, __file__ + "::registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
