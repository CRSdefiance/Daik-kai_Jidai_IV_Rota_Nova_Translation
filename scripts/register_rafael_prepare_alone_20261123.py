"""Register the corrected Lisbon reply and its ordinary New Game replay."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import check_rafael_prepare_alone_20261123 as played
from scripts import reconcile_elegy_acceptance_20261123 as acceptance
from scripts import register_cartridge_title_20261123 as template
from scripts import register_kurushima_confrontation_wraps_20261123 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_rafael_prepare_alone_20261123 as build
from scripts.source_locked_derivation_v5118 import checked_text


PROFILE = "all-routes-rafael-prepare-alone-v1-20261123"
CHECK = "registered_rafael_prepare_alone_native_page_and_complete_parent_inverse"
STORY, COMMON, ARM = build.STORY, build.COMMON, build.ARM
WORK, ROM = build.ROOT, build.ROM
PATCH, PATCH_PROOF, REBUILT, STARTUP_CAPTURE = build.PATCH, build.PATCH_PROOF, build.REBUILT, build.STARTUP_CAPTURE
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_rafael_prepare_alone_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_rafael_prepare_alone.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA = WORK / "own_startup_verification.json", WORK / "qa_passed.xml"
DOC = Path("docs/editorial_rafael_prepare_alone_registered_20261123.md")
CHECKPOINT = "Registered Julio's revised reply when Rafael chooses to prepare alone in Lisbon."
SHEET, PREVIEW = played.SHEET, build.NATIVE
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.STORED)))


def verify(previous, visual_sha):
    packet, stored, live, patch = map(stage.read, (build.review.OUT, build.STORED, played.PAIRED, PATCH_PROOF))
    candidate = stage.digest(ROM)
    assert candidate == stored["candidate"]["sha256"] == live["candidate_sha256"] == stage.digest(REBUILT)
    assert patch["byte_exact"] and patch["candidate"]["sha256"] == candidate and stage.reference(PATCH) == patch["patch"]
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == stored["clean"]["sha256"] == stage.digest(stage.CLEAN)
    assert previous["candidate_sha256"] == stored["previous"]["sha256"] == live["previous_sha256"] == packet["candidate_sha256"]
    assert stored["whole_parent_inverse"] and stored["unchanged_archive_directory"]
    assert stage.reference(build.review.OUT) == stored["source_review"]
    assert stage.reference(build.STORED) == live["stored"]
    assert live["ordinary_new_game"] and live["original_choice_and_town_return_unchanged"] and packet["ordinary_new_game"]
    assert live["changed_frame"]["frame"] == build.review.RESPONSE_FRAME and len(live["unchanged_frames"]) == 11
    assert stage.reference(build.review.run.REPORT) == live["source_run"] and stage.reference(played.REPLAY) == live["replay"]
    visuals = [stage.reference(SHEET), stage.reference(PREVIEW)]
    assert visuals == [live["visual"], stored["visual"]] and live["separate_native_preview"] == visuals[1]
    assert stage.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    original, old, new = map(stage.NdsImage.open, (stage.CLEAN, previous["candidate"], ROM))
    before, after = map(build.native.files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {STORY}
    assert stage.sha256(after[ARM]).hexdigest() == previous["target_ARM9_sha256"]
    assert stage.sha256(after[COMMON]).hexdigest() == previous["target_COMMON_sha256"]
    assert stage.sha256(after[STORY]).hexdigest() == stored["target_SC0_sha256"]
    assert template.right_bound(after[ARM], previous["right_bound_configuration"])["matched_repair_spans"] == 8
    archives = [build.IlnkContainer.parse(data[STORY]).blocks for data in (before, after)]
    assert [i for i, (a, b) in enumerate(zip(*archives, strict=True)) if a != b] == [build.BLOCK]
    clean_block = build.IlnkContainer.parse(original.read_file(STORY)).blocks[build.BLOCK]
    previous_block, block = (archive[build.BLOCK] for archive in archives)
    assert stage.sha256(block).hexdigest() == stored["target_block_sha256"]
    new.replace_file(STORY, before[STORY])
    assert bytes(new.rom.save()) == Path(previous["candidate"]).read_bytes()

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "one_Rafael_block_and_startup_arm9_unchanged",
    })
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, after[ARM])

    edit = stored["edit"]
    selection = packet["selection"]
    at, menu = selection["original_menu_offset"], bytes.fromhex(selection["exact_installed_command"])
    assert selection["selected_slot"] == 1 and block[at:at + len(menu)] == menu
    records = []
    for row in packet["context_records"]:
        src, ref = row["source_reference"], row["current_reference"]
        a = played.panels.exact_command(clean_block, src)
        b = played.panels.exact_command(previous_block, ref)
        changed = row["id"] == build.review.RESPONSE
        data = bytes.fromhex(edit["after_hex"]) if changed else b
        at = ref["command_offset"]
        assert block[at:at + len(data)] == data and a[:6] == b[:6] == data[:6]
        english = build.ENGLISH if changed else row["english"]
        assert " ".join(build.bytes_for(data).decode("ascii").split()) == english
        if changed:
            assert b.hex() == edit["before_hex"] and at == edit["command_offset"]
            assert edit["page_sha256"] == live["complete_page_sha256"] and edit["allocation_and_termination_preserved"]
        records.append(row | dict(previous_English=row["english"], english=english,
            localization_note=build.RATIONALE if changed else row["localization_note"],
            decision="revision" if changed else "retention", registered_reference=ref | dict(
                exact_command_hex=data.hex(), candidate_sha256=candidate, archive_sha256=stored["target_SC0_sha256"],
                block_sha256=stored["target_block_sha256"]), installed_paired_gameplay=live["changed_frame"] if changed else None))
    assert len(records) == 10 and sum(row["decision"] == "revision" for row in records) == 1
    prior = stage.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    common = acceptance.common_rows(after[COMMON], after[ARM])
    assert all(played.panels.text_reference(common[row["message_ID"]]) == row["installed"] for row in shared["records"])
    outcome = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate,
        target_SC0_sha256=stored["target_SC0_sha256"], source_review=stage.reference(build.review.OUT),
        visual_review=visuals, stored_proof=stage.reference(build.STORED), gameplay=stage.reference(played.PAIRED),
        choice=selection, shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_nagasaki_dream_predecessor=predecessor, kurushima_confrontation_release=str(REVIEW)":
        "verified_kurushima_confrontation_predecessor=predecessor, rafael_prepare_alone_release=str(REVIEW)",
    "len(batches) == 1116 and len(checks) == 451": "len(batches) == 1117 and len(checks) == 452",
    "assert len(revised) == 3": "assert revised == [build.review.RESPONSE]",
    "kurushima_confrontation_release_proof": "rafael_prepare_alone_release_proof",
    '"kurushima_confrontation_pipeline"': '"rafael_prepare_alone_pipeline"',
    "played.PAIRED, played.NATIVE, PREVIEW": "played.PAIRED, PREVIEW",
    "registered_manifest_entries=1117, passing_release_checks=452": "registered_manifest_entries=1118, passing_release_checks=453",
    'target_SC3_sha256=outcome["target_SC3_sha256"]': 'target_SC0_sha256=outcome["target_SC0_sha256"]',
    "contextual_records_revisited=8, contextual_decisions_reused=5, previously_localized_records=8":
        "contextual_records_revisited=10, contextual_decisions_reused=9, previously_localized_records=10",
    "prose_revisions=2, justified_retentions=5, text_display_revisions=3, wrap_only_revisions=1":
        "prose_revisions=1, justified_retentions=9, text_display_revisions=1, wrap_only_revisions=0",
    "ordinary_Kurushima_confrontation=True, revised_gameplay_holds=3, native_pages=6":
        "ordinary_Rafael_preparation_choice=True, revised_gameplay_holds=1, native_pages=1",
    "prose_revisions=2, wrap_only_revisions=1, texts_retained=5": "prose_revisions=1, wrap_only_revisions=0, texts_retained=9",
    '"kurushima_confrontation_wraps_20261123"': '"rafael_prepare_alone_20261123"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's Lisbon preparation candidate

Julio gives Rafael a more natural send-off after **Prepare alone**. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Kurushima confrontation candidate": "Preserve the registered Rafael preparation candidate",
    "1,117 entries and 452 passing checks": "1,118 entries and 453 passing checks",
    doc: '''    DOC.write_text(f"""# Rafael's Lisbon preparation choice

Julio now tells Rafael, “That's the spirit! Do your best!” after **Prepare alone**. The clean Japanese conveys approval of Rafael's initiative and encouragement. The revised line fits in one row. Nine neighboring speeches retain their wording, including Julio's guidance on the alternate path. [Exact Japanese, previous and installed records](../{REVIEW.as_posix()})

An ordinary New Game replay verified the complete revised dialogue and Julio's nameplate. Eleven sampled frames match the predecessor pixel for pixel, including both menu captions, the lower highlight, and the return to Lisbon. The **Ask him** lesson uses earlier ordinary gameplay evidence. The exact replay comparison and native preview are included in the package. [Paired gameplay](../{VERIFY.as_posix()}/{SHEET.name}) · [Native preview](../{VERIFY.as_posix()}/{PREVIEW.name})

The cumulative build passed 453 release checks, its own startup and 17 focused tests. The clean-input patch reconstructs the candidate byte for byte. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::rafael-preparation-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
