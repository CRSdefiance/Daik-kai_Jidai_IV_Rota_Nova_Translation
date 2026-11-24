"""Register the verified Price Info descriptions over the cumulative Shortfall build."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_cartridge_title_20261123 as template
from scripts import register_recruitment_shortfall_20261123 as parent
from scripts import replay_price_info_descriptions_20261123 as checks
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_price_info_descriptions_20261123 as build
from scripts import verify_price_info_descriptions_20261123 as played
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.source_locked_derivation_v5118 import checked_text


PROFILE = "all-routes-price-info-descriptions-v1-20261123"
CHECK = "registered_price_info_descriptions_and_complete_parent_inverse"
ARM, COMMON = build.price.ARM, build.price.COMMON
ROM, WORK = build.ROM, build.ROOT
PATCH, PATCH_PROOF, REBUILT = checks.PATCH, checks.PATCH_PROOF, checks.REBUILT
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_price_info_descriptions_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_price_info.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA, STARTUP_CAPTURE = WORK / "own_startup_verification.json", WORK / "qa_passed.xml", checks.STARTUP_CAPTURE
DOC = Path("docs/editorial_price_info_descriptions_registered_20261123.md")
CHECKPOINT = "Corrected Price Info wording and wraps for twelve trade goods."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=played.SHEET, PROOF=build.STORED)))
REVISED = (143, 166, 203, 208, 216, 225, 226, 227, 233, 234, 236, 245)


def verify(previous, visual_sha):
    stored, draft, live, patch = map(stage.read, (build.STORED, build.MANUSCRIPT, played.REPORT, PATCH_PROOF))
    candidate = stage.digest(ROM)
    assert candidate == stored["candidate_sha256"] == live["candidate_sha256"] == patch["candidate"]["sha256"] == stage.digest(REBUILT)
    assert patch["byte_exact"] and stage.reference(PATCH) == patch["patch"]
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == stage.digest(stage.CLEAN)
    assert previous["candidate_sha256"] == draft["previous_sha256"] == live["previous_sha256"] == stored["previous_sha256"]
    assert previous["candidate_sha256"] == stage.digest(previous["candidate"]) and stored["whole_parent_inverse"]
    assert stage.digest(build.MANUSCRIPT) == stored["manuscript_sha256"]
    assert sorted(map(int, stored["allocations"])) == list(REVISED)
    assert live["ordinary_gameplay"] and not live["fixture"] and live["live_message_ID"] == 143
    assert len(live["full_frame_control_matches"]) == 10 and live["original_choice_or_page_advance"]
    assert all(stage.reference(row["path"]) == row for row in live["evidence"])
    visual = stage.reference(played.SHEET)
    assert visual == live["screenshot"]
    renders = [stage.reference(row["path"]) for row in stored["sheets"]]
    assert [row["sha256"] for row in renders] == [row["sha256"] for row in stored["sheets"]]
    combined = [visual, *renders]
    assert stage.sha256("".join(row["sha256"] for row in combined).encode("ascii")).hexdigest() == visual_sha

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
        "compact_azores_payload_exact_and_startup_extent_preserved": "price_info_common_only_verified_arm9_unchanged",
    })
    exec(compile(code, __file__ + "::startup-for-common-only", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)

    prior = stage.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    before, after = (common_rows(data, arm) for data in (old_common, common))
    for row in shared["records"]:
        key = row["message_ID"]
        assert before[key] == after[key] and row["exact_body_retained"]
        assert build.price.reference(after[key]) == row["installed"]
    records = draft["records"]
    assert len(records) == 18 and all(len(row["pages"]) == 1 for row in records)
    for row in records:
        key = row["message_id"]
        assert after[key].text.hex() == row["staged_hex"]
        row["review"]["formatting"] = True
        row["registered_reference"] = row["staged_reference"] | dict(
            exact_stored_hex=row["staged_hex"], candidate_sha256=candidate)
    result = draft | dict(candidate_sha256=candidate, target_COMMON_sha256=stored["target_COMMON_sha256"],
        source_credit_added=0, visual_review=combined, stored_proof=stage.reference(build.STORED),
        gameplay=stage.reference(played.REPORT), shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_recruitment_capacity_predecessor=predecessor, recruitment_shortfall_release=str(REVIEW)":
        "verified_recruitment_shortfall_predecessor=predecessor, price_info_descriptions_release=str(REVIEW)",
    "len(batches) == 1109 and len(checks) == 444": "len(batches) == 1110 and len(checks) == 445",
    'if row["decision"] == "revision"': 'if row["decision"] in {"revision", "wrap revision"}',
    "for key in build.DRAFTS": "for key in REVISED",
    "recruitment_shortfall_release_proof": "price_info_descriptions_release_proof",
    '"recruitment_shortfall_pipeline"': '"price_info_descriptions_pipeline"',
    "registered_manifest_entries=1110, passing_release_checks=445": "registered_manifest_entries=1111, passing_release_checks=446",
    "contextual_records_revisited=7, contextual_decisions_reused=5, previously_localized_records=7":
        "contextual_records_revisited=18, contextual_decisions_reused=6, previously_localized_records=18",
    "prose_revisions=2, justified_retentions=5, text_display_revisions=2, wrap_only_revisions=0":
        "prose_revisions=10, justified_retentions=6, text_display_revisions=12, wrap_only_revisions=2",
    "focused_azores_tavern_after_single_crew_field_setup=True": "ordinary_Lisbon_Price_Info=True",
    "shortfall_voices_revised=2, dialogue_retained=5": "commodity_descriptions_revised=12, descriptions_retained=6",
    '"recruitment_shortfall_20261123"': '"price_info_descriptions_20261123"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Price Info descriptions testing candidate

Twelve descriptions now preserve the source facts and read in complete phrases within the original Price Info pages. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Recruit Crew shortfall candidate": "Preserve the registered Price Info descriptions candidate",
    "1,110 entries and 445 passing checks": "1,111 entries and 446 passing checks",
    doc: '''    DOC.write_text(f"""# Price Info commodity descriptions

Eighteen descriptions were compared with the clean Japanese. Ten wording revisions include the parasitic relationship in Cordyceps, the three properties of leather, and the mineral definition of ruby. Blades and Armor keep their wording and put the complete wartime-demand sentence on its own line. Six other descriptions retain their wording. [Exact source and installed records](../{REVIEW.as_posix()})

All 18 descriptions fit the original one-page display. All twelve revised pages passed native glyph and bounds checks and direct visual review. A paired ordinary Lisbon replay verified the complete Beef description, its return to the goods list after one button press and ten byte-identical control frames. [Paired gameplay](../{VERIFY.as_posix()}/{played.SHEET.name}) · [Native pages](../{VERIFY.as_posix()}/portrait_sheet_01.png)

The cumulative candidate passed six startup comparisons, 24 protected name getters, eight ASCII right-bound spans and 17 focused tests. The clean-input patch reconstructs the candidate exactly. [Registered build and patch](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::price-info-registered", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
