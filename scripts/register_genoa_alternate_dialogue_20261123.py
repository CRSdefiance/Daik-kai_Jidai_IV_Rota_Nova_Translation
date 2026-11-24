"""Register the alternate Genoa dialogue after both ordinary branches pass."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from scripts import register_cartridge_title_20261123 as template
from scripts import register_genoa_dialogue_20261123 as parent
from scripts import replay_genoa_alternate_dialogue_release_20261123 as played
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_genoa_alternate_dialogue_20261123 as build
from scripts import verify_genoa_alternate_choices_20261123 as review
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_moonlit_violin_20261121 import bytes_for


PROFILE = "all-routes-genoa-alternate-dialogue-v1-20261123"
CHECK = "registered_genoa_alternate_dialogue_nested_allocations_and_complete_parent_inverse"
STORY, COMMON, ARM = build.STORY, build.COMMON, build.ARM
WORK, ROM = build.ROOT, build.ROM
PATCH, PATCH_PROOF, REBUILT, STARTUP_CAPTURE = build.PATCH, build.PATCH_PROOF, build.REBUILT, build.STARTUP_CAPTURE
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_genoa_alternate_dialogue_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_genoa_alternate_dialogue.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA = WORK / "own_startup_verification.json", WORK / "qa_passed.xml"
DOC = Path("docs/editorial_genoa_alternate_dialogue_registered_20261123.md")
CHECKPOINT = "Registered two wording edits and two wrap fixes in Julio's alternate Genoa choices."
PREVIEW = review.OUT.with_name("genoa_alternate_choice_previews_20261123") / "before_after_1.png"
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=played.SHEET, PROOF=build.STORED)))


def verified_records(prior, verified, stored, live, block):
    old_pages = {row["id"]: row for case in verified["choice_paths"].values() for row in case["story"]}
    live_pages = {row["id"]: row for case in live["outcomes"].values() for row in case["reviewed_pages"]}
    edits = {row["id"]: row for row in stored["changed"]}
    assert set(edits) == set(live_pages) == set(build.IDS)
    candidate = stored["staged"]["sha256"]
    block_hash = stage.sha256(block).hexdigest()
    records = []
    for old in (row for row in prior["records"] if row["block"] == 170):
        ident, now = old["id"], old["registered_reference"]
        change, observed = edits.get(ident), old_pages.get(ident)
        assert old["review"] == dict.fromkeys(files.GATES, True)
        command = bytes.fromhex(change["after_hex"] if change else now["exact_command_hex"])
        offset = now["command_offset"]
        assert block[offset:offset + len(command)] == command
        registered = now | dict(candidate_sha256=candidate, archive_sha256=stored["target_SC1_sha256"],
            block_sha256=block_hash, exact_command_hex=command.hex())
        row = old | dict(current_reference=now, registered_reference=registered, decision="retention",
                         change_class="retention", gameplay=None)
        if observed:
            assert observed["source_reference"] == old["source_reference"] and observed["installed_reference"] == now
            row["gameplay"] = dict(frame=observed["frame"], evidence_ROM_sha256=stored["predecessor"]["sha256"],
                                   full_native_page_sha256=observed["full_page_sha256"])
        if change:
            assert observed["review"]["formatting"] is False and change["single_page"]
            assert change["allocation_and_termination_preserved"] and change["native_inputs_preserved"]
            assert live_pages[ident]["exact_command_hex"] == command.hex()
            assert observed["offline_preflight"]["native_plane_sha256"] == live_pages[ident]["full_native_page_sha256"]
            raw = bytes_for(command)
            english = " ".join(raw.decode("ascii").split())
            assert english == observed["proposed_English"]
            kind = "wrap-only" if english == old["english"] else "wording"
            row.update(english=english, decision="revision", change_class=kind, localization_note=observed["rationale"],
                gameplay=live_pages[ident] | {"evidence_ROM_sha256": candidate})
            registered["exact_body_hex"] = raw.hex()
        records.append(row)
    assert len(records) == 52
    assert sum(row["change_class"] == "wording" for row in records) == 2
    assert sum(row["change_class"] == "wrap-only" for row in records) == 2
    return records


def verify(previous, visual_sha):
    stored, live, patch, packet = map(stage.read, (build.STORED, played.REPORT, PATCH_PROOF, review.OUT))
    candidate = stage.digest(ROM)
    assert candidate == stored["staged"]["sha256"] == live["candidate_sha256"] == patch["candidate"]["sha256"] == stage.digest(REBUILT)
    assert patch["byte_exact"] and stage.reference(PATCH) == patch["patch"]
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == stored["clean"]["sha256"] == stage.digest(stage.CLEAN)
    assert previous["candidate_sha256"] == stored["predecessor"]["sha256"] == live["predecessor_sha256"] == packet["candidate_sha256"]
    assert stored["editorial_and_preflight"] == stage.reference(review.OUT) and stored["whole_parent_inverse"]
    assert stored["unchanged_archive_directory"] and stored["stored_rendering_matches_reviewed_previews"]
    assert set(stored["blocks"]) == {"170"} and stored["blocks"]["170"]["exact_native_command_extents"] > 52
    assert live["ordinary_controller_inputs"] and live["matched_control_frames"] == 32 and live["changed_page_holds"] == 4
    assert set(live["outcomes"]) == set(review.PAGES)
    assert all(row["retained_join_notice_and_tavern_return"] for row in live["outcomes"].values())
    visuals = [stage.reference(played.SHEET), stage.reference(PREVIEW)]
    assert visuals == [live["visual"], *packet["offline_proposed_pages"]]
    assert stage.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    old, new = map(stage.NdsImage.open, (previous["candidate"], ROM))
    before, after = map(build.previous.native.files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {STORY}
    for path, key in ((ARM, "target_ARM9_sha256"), (COMMON, "target_COMMON_sha256")):
        assert stage.sha256(after[path]).hexdigest() == stored[key] == previous[key]
    assert stage.sha256(after[STORY]).hexdigest() == stored["target_SC1_sha256"]
    assert template.right_bound(after[ARM], previous["right_bound_configuration"])["matched_repair_spans"] == 8
    prior = stage.read(parent.REVIEW)
    records = verified_records(prior, packet, stored, live, IlnkContainer.parse(after[STORY]).blocks[170])
    new.replace_file(STORY, before[STORY])
    assert bytes(new.rom.save()) == Path(previous["candidate"]).read_bytes()

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    code = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "genoa_alternate_allocations_and_startup_arm9_unchanged",
    })
    exec(compile(code, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, after[ARM])

    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    outcome = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(records[0]["review"]), records=records, candidate_sha256=candidate,
        target_SC1_sha256=stored["target_SC1_sha256"], changed_ids=list(build.IDS),
        source_credit_added=0, stored_proof=stage.reference(build.STORED), visual_review=visuals,
        gameplay=stage.reference(played.REPORT), localized_story_delta=dict(file=STORY, blocks=[170]),
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_price_info_predecessor=predecessor, genoa_dialogue_release=str(REVIEW)":
        "verified_genoa_dialogue_predecessor=predecessor, genoa_alternate_dialogue_release=str(REVIEW)",
    "len(batches) == 1111 and len(checks) == 446": "len(batches) == 1112 and len(checks) == 447",
    "genoa_dialogue_release_proof": "genoa_alternate_dialogue_release_proof",
    '"genoa_dialogue_pipeline"': '"genoa_alternate_dialogue_pipeline"',
    "registered_manifest_entries=1112, passing_release_checks=447": "registered_manifest_entries=1113, passing_release_checks=448",
    "contextual_records_revisited=62, contextual_decisions_reused=59, previously_localized_records=62":
        "contextual_records_revisited=52, contextual_decisions_reused=48, previously_localized_records=52",
    "prose_revisions=2, justified_retentions=59, text_display_revisions=3, wrap_only_revisions=1":
        "prose_revisions=2, justified_retentions=48, text_display_revisions=4, wrap_only_revisions=2",
    "ordinary_genoa_recruitment_and_trend=True": "ordinary_genoa_alternate_choices=True",
    "genoa_dialogue_revised=3, texts_retained=59": "alternate_dialogue_revised=4, texts_retained=48",
    '"genoa_dialogue_20261123"': '"genoa_alternate_dialogue_20261123"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Genoa alternate choices testing candidate

Julio's two alternate recruitment branches include two wording changes and two wrap fixes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Genoa dialogue candidate": "Preserve the registered Genoa alternate dialogue candidate",
    "1,112 entries and 447 passing checks": "1,113 entries and 448 passing checks",
    doc: '''    DOC.write_text(f"""# Julio's alternate Genoa choices

The route where Hodram tests Julio keeps the mock lesson together in three readable lines. On the other route, Hodram says he plans to look for better liquor on the voyage. Julio's impatient demand and his greeting about sailing together each keep their full phrase on one line. Forty-eight other texts and labels retain their wording. [Exact Japanese, previous and installed records](../{REVIEW.as_posix()})

Both ordinary replays used the lower menu option. All four changed pages and nameplates passed complete glyph checks. The two join notices and Tavern returns match the preceding build, along with both menu selections and the other control frames. The 32 matching frames and native nested command checks support the three recruitment paths covered across the Genoa builds. [Paired gameplay](../{VERIFY.as_posix()}/{played.SHEET.name}) · [Native previews](../{VERIFY.as_posix()}/{PREVIEW.name})

The cumulative candidate passed 448 release checks and 17 focused tests. The patch reconstructs the complete ROM from the clean input. Six startup frames, 24 protected name getters, eight ASCII right-bound spans and the 27,700 historical editorial credits carry forward. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
