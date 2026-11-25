"""Register the verified developed-Azores docking argument over the cumulative ROM."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_cartridge_title_20261123 as template
from scripts import register_hodram_elegy_20261123 as parent
from scripts import stage_azores_return_20261123 as build
from scripts import stage_cartridge_title_20261123 as files
from scripts import verify_azores_return_20261123 as replay
from scripts.check_azores_return_release_20261123 import PATCH, PATCH_PROOF, REBUILT, STARTUP_CAPTURE
from scripts.reconcile_editorial_acceptance_20261123 import COMMON
from scripts.source_locked_derivation_v5118 import checked_text


PROFILE = "all-routes-developed-azores-return-v1-20261123"
CHECK = "registered_developed_azores_name_arguments_and_complete_parent_inverse"
EDIT = "ARM9_DEVELOPED_AZORES_DOCK_ARGUMENT"
ARM, WORK, ROM = build.ARM, build.ROOT, build.ROM
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_azores_return_candidate")
VERIFY = PACKAGE / "verification"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
MANIFEST = ROM.with_suffix(".manifest.json")
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_azores_return.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA = WORK / "own_startup_verification.json", WORK / "qa_passed.xml"
DOC = Path("docs/editorial_azores_return_registered_20261123.md")
CHECKPOINT = "Corrected the developed Azores port's docking question and verified its Market and Tavern in ordinary play."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=replay.SHEET, PROOF=build.PROOF)))


def verify(previous, visual_sha):
    stored, played, rebuilt = map(stage.read, (build.PROOF, replay.OUTPUT, PATCH_PROOF))
    sha = stage.digest(ROM)
    assert sha == stored["candidate_sha256"] == played["candidate_sha256"] == rebuilt["candidate"]["sha256"] == stage.digest(REBUILT)
    assert rebuilt["byte_exact"] and stage.reference(PATCH) == rebuilt["patch"]
    assert rebuilt["clean_input_sha256"] == previous["clean_input_sha256"] == stage.digest(stage.CLEAN)
    assert played["original_sha256"] == stored["verified_predecessor_sha256"] == previous["candidate_sha256"]
    assert previous["candidate_sha256"] == stage.digest(previous["candidate"])
    assert stored["whole_parent_inverse"] and stored["native_case_count"] == 2592
    assert played["ordinary_lisbon_to_azores_and_redocking"] and played["all_other_replayed_frames_identical"]
    assert played["stock_developed_town"]["native_development"] == 2
    visual = stage.reference(replay.SHEET)
    assert visual == played["screenshot"] and visual["sha256"] == visual_sha

    clean, old, candidate = map(stage.NdsImage.open, (stage.CLEAN, previous["candidate"], ROM))
    clean_arm, old_arm, arm = (image.read_file(ARM) for image in (clean, old, candidate))
    assert arm == build.patch(old_arm, clean_arm)
    assert stage.sha256(arm).hexdigest() == stored["target_ARM9_sha256"]
    candidate.replace_file(ARM, old_arm)
    assert bytes(candidate.rom.save()) == Path(previous["candidate"]).read_bytes()
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    assert stage.sha256(candidate.read_file(COMMON)).hexdigest() == previous["target_COMMON_sha256"]
    for route in range(4):
        assert stage.sha256(candidate.read_file(f"/data/SC{route}.DK4")).hexdigest() == previous[f"target_SC{route}_sha256"]

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(f, "0")) for f in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "azores_return_owned_caller_and_same_extent_wrapper",
    })
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, sha, arm)

    earlier = stage.read(parent.REVIEW)
    shared = earlier["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    row, = (item for item in played["records"] if item["decision"] == "runtime revision")
    record = row | dict(id=EDIT, decision="revision", file_path=ARM,
        context="Manuel asks whether to dock after Hodram sails out of the Azores village and returns to its developed port.",
        source_meaning="Would you like to make a port call at the named location?",
        english="Shall we stop at the Azores?", localization_note=row["reason"],
        source_call=dict(address=build.TOWN_NAME_CALL, exact_hex=clean_arm[build.SITE:build.SITE+4].hex()),
        installed_call=dict(address=build.TOWN_NAME_CALL, exact_hex=arm[build.SITE:build.SITE+4].hex()),
        runtime_alias_address=stored["alias_address"], COMMON_template_id=70)
    assert record["english"] == played["records"][0]["observed_after"][0]
    result = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(record["review"]), records=[record], candidate_sha256=sha,
        target_ARM9_sha256=stored["target_ARM9_sha256"], source_credit_added=0,
        stored_proof=stage.reference(build.PROOF), visual_review=visual, gameplay=stage.reference(replay.OUTPUT),
        shared_consumer_binding=shared | dict(candidate_sha256=sha),
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
        "verified_hodram_elegy_predecessor=predecessor, developed_azores_return_release=str(REVIEW)",
    "len(batches) == 1102 and len(checks) == 437": "len(batches) == 1107 and len(checks) == 442",
    'assert stage.BANNER not in paths and stage.BANNER not in records and CHECK not in checks':
        'assert ARM in paths and EDIT not in records[ARM] and CHECK not in checks',
    'records[stage.BANNER] = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]':
        'records[ARM].append(EDIT)',
    'assert len(records[stage.BANNER]) == 5': 'assert [row["id"] for row in outcome["records"]] == [EDIT]',
    "changed_paths=sorted([*paths, stage.BANNER])": "changed_paths=paths",
    "Path(stage.__file__)": "Path(build.__file__)",
    "snapshot_scope=stage.BANNER": "snapshot_scope=ARM",
    "banner_release_proof": "azores_return_release_proof",
    '"cartridge_title_pipeline"': '"azores_return_pipeline"',
    "stage.SHEET, stage.PROOF": "stage.SHEET, stage.PROOF, replay.OUTPUT",
    "registered_manifest_entries=1103, passing_release_checks=438, changed_components=1, changed_internal_files=[stage.BANNER]":
        'registered_manifest_entries=1108, passing_release_checks=443, changed_components=1, changed_internal_files=[ARM],\n'
        '        target_ARM9_sha256=outcome["target_ARM9_sha256"]',
    "reviewed_UI_labels=5, contextual_records_revisited=0, contextual_decisions_reused=0, previously_localized_records=0":
        "reviewed_UI_labels=0, contextual_records_revisited=8, contextual_decisions_reused=6, previously_localized_records=8",
    "new_contextual_records=0, prose_revisions=0, justified_retentions=1, text_display_revisions=5":
        "new_contextual_records=0, prose_revisions=0, justified_retentions=6, text_display_revisions=1, wrap_only_revisions=0",
    "host_preview_of_all_six_banner_fields=True": "ordinary_redocking_market_and_tavern=True",
    "handheld_firmware_display=False, launcher_GUI_display=False": "handheld=False",
    "English_launcher_fields=5, original_Japanese_title_retained=True":
        "docking_article_consumer_fixed=True, bare_town_name_and_shared_template_retained=True",
    '"cartridge_title_20261123"': '"azores_return_20261123"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Developed Azores testing candidate

Docking at the developed Azores port now asks “Shall we stop at the Azores?” The town heading still reads **Azores**. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(seal, {
    "Preserve the registered cartridge-title candidate": "Preserve the registered developed-Azores candidate",
    "1,103 entries and 438 passing checks": "1,108 entries and 443 passing checks",
    doc: '''    DOC.write_text(f"""# Returning to the developed Azores

Hodram sailed from Lisbon, discovered the Azores, entered the promised words, and returned through the original docking prompt. Manuel now asks **Shall we stop at the Azores?** on both visits. The clean Japanese asks whether to call at the selected port. The original template, portrait, choices, and selected town remain intact. The town heading stays **Azores** and Trade shows **Azores Wine**. [Exact source and installation evidence](../{REVIEW.as_posix()}) · [Paired gameplay](../{VERIFY.as_posix()}/{replay.SHEET.name})

Ordinary play opened the Market and Tavern and exercised both initial recruitment choices. Cancelling returned to Recruit Crew. Accepting brought Manuel's call, the patron's reply, and the count of 18 volunteers. COMMON 1048 still splits **try recruiting more** across lines and has an open source-bound wrap finding. Six other dialogue holds passed their complete glyph and nameplate checks. [Recruitment and exact source references](../{replay.OUTPUT.as_posix()})

The candidate passed 2,592 native address and flag cases, six startup frame comparisons, 24 protected name getters, eight right-bound spans, and 17 focused regressions. The clean-input patch reconstructs the entire ROM exactly. Other docking voices retain offline coverage. Physical hardware remains unvisited. [Clean-input patch](../{PACKAGE.as_posix()}/translation.xdelta)
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
