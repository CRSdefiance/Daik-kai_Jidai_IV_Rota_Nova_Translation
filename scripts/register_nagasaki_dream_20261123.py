"""Register the reviewed Nagasaki dream with its ordinary replay and native checks."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from scripts import register_cartridge_title_20261123 as template
from scripts import register_missionary_destination_20261123 as parent
from scripts import replay_nagasaki_dream_20261123 as played
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_nagasaki_dream_20261123 as build
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.source_locked_derivation_v5118 import checked_text


PROFILE = "all-routes-nagasaki-dream-v1-20261123"
CHECK = "registered_nagasaki_dream_native_scene_and_complete_parent_inverse"
STORY, COMMON, ARM = build.STORY, build.COMMON, build.ARM
WORK, ROM = build.ROOT, build.ROM
PATCH, PATCH_PROOF, REBUILT, STARTUP_CAPTURE = build.PATCH, build.PATCH_PROOF, build.REBUILT, build.STARTUP_CAPTURE
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_nagasaki_dream_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_nagasaki_dream.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA = WORK / "own_startup_verification.json", WORK / "qa_passed.xml"
DOC = Path("docs/editorial_nagasaki_dream_registered_20261123.md")
CHECKPOINT = "Registered four revisions to the Nagasaki Inn dream after an ordinary replay."
SHEET = WORK / "paired_nagasaki_dream_1_20261123.png"
PREVIEW = played.review.OUT.with_name("nagasaki_dream_proposals_20261123") / "before_after_1.png"
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.STORED)))


def verify(previous, visual_sha):
    stored, live, patch, packet = map(stage.read, (build.STORED, played.REPORT, PATCH_PROOF, played.review.OUT))
    candidate = stage.digest(ROM)
    assert candidate == stored["candidate"]["sha256"] == live["candidate_sha256"] == patch["candidate"]["sha256"] == stage.digest(REBUILT)
    assert patch["byte_exact"] and stage.reference(PATCH) == patch["patch"]
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == stored["clean"]["sha256"] == stage.digest(stage.CLEAN)
    assert stored["whole_parent_inverse"] and stage.reference(played.review.OUT) == stored["source_review"]
    assert previous["candidate_sha256"] == stored["previous"]["sha256"] == live["predecessor_sha256"] == packet["candidate_sha256"]
    assert live["ordinary_controller_gameplay"] and live["cleaver_and_Inn_return"] and not live["fixture"]
    assert len(live["identical_control_frames"]) == 29 and not live["conditional_Angelo_panels_observed"]
    assert stage.reference(live["original_capture"]["path"]) == live["original_capture"]
    assert stage.reference(played.CAPTURE) == live["revised_capture"]
    visuals = [stage.reference(SHEET), stage.reference(PREVIEW)]
    assert visuals == [live["visual"], *packet["offline_proposed_pages"]]
    assert stage.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    old, new = map(stage.NdsImage.open, (previous["candidate"], ROM))
    before, after = map(build.native.files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {STORY}
    assert stage.sha256(after[ARM]).hexdigest() == previous["target_ARM9_sha256"] == stored["target_ARM9_sha256"]
    assert stage.sha256(after[COMMON]).hexdigest() == previous["target_COMMON_sha256"] == stored["target_COMMON_sha256"]
    assert stage.sha256(after[STORY]).hexdigest() == stored["target_SC3_sha256"]
    assert template.right_bound(after[ARM], previous["right_bound_configuration"])["matched_repair_spans"] == 8
    original_archive, installed_archive = map(IlnkContainer.parse, (before[STORY], after[STORY]))
    assert {i for i, (a, b) in enumerate(zip(original_archive.blocks, installed_archive.blocks, strict=True)) if a != b} == {build.BLOCK}
    block = installed_archive.blocks[build.BLOCK]
    assert stage.sha256(block).hexdigest() == stored["target_block_sha256"]
    new.replace_file(STORY, before[STORY])
    assert bytes(new.rom.save()) == Path(previous["candidate"]).read_bytes()

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    code = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "nagasaki_story_only_and_startup_arm9_unchanged",
    })
    exec(compile(code, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, after[ARM])

    commands = {ident: node for node in stored["commands"] for ident in node["record_ids"]}
    native_pages = stored["stored_native_pages"]
    witnessed = {row["id"]: row for row in live["changed_holds"]}
    assert len(commands) == 17 and len(witnessed) == 3 and len(native_pages) == 4
    assert {ident for ident in native_pages if ident not in witnessed} == {ident for ident in native_pages if ident.endswith("_R0094")}
    records = []
    for row in stored["records"]:
        ident = row["id"]
        node = commands[ident]
        at = node["stored_offset"]
        data = bytes.fromhex(node["stored"])
        assert block[at:at + len(data)] == data
        assert row["source_reference"]["exact_command_hex"] == node["source"]
        assert row["installed_reference"]["exact_command_hex"] == node["current"]
        assert " ".join(build.bytes_for(data).decode("ascii").split()) == row["english"]
        native = native_pages.get(ident)
        if native:
            assert row["decision"] == "revision" and native["page_sha256"] == row["offline_preflight"]["native_plane_sha256"]
            if ident in witnessed:
                assert native["page_sha256"] == witnessed[ident]["native_plane_sha256"]
        else:
            assert row["decision"] == "retention" and node["stored"] == node["current"]
        installed = dict(file=STORY, block=build.BLOCK, command_offset=at, exact_command_hex=data.hex(),
            candidate_sha256=candidate, archive_sha256=stored["target_SC3_sha256"], block_sha256=stored["target_block_sha256"])
        records.append(row | dict(source_meaning=row["source_gloss"], localization_note=row["rationale"],
            current_reference=row["installed_reference"], registered_reference=installed, review=dict.fromkeys(files.GATES, True),
            installed_native_page=native, revised_gameplay=witnessed.get(ident)))
    prior = stage.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    common = common_rows(after[COMMON], after[ARM])
    assert all(played.panels.text_reference(common[row["message_ID"]]) == row["installed"] for row in shared["records"])
    outcome = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate,
        target_SC3_sha256=stored["target_SC3_sha256"], award=packet["award"], source_review=stage.reference(played.review.OUT),
        visual_review=visuals, stored_proof=stage.reference(build.STORED), gameplay=stage.reference(played.REPORT),
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_london_relic_tip_predecessor=predecessor, missionary_destination_release=str(REVIEW)":
        "verified_missionary_destination_predecessor=predecessor, nagasaki_dream_release=str(REVIEW)",
    "len(batches) == 1114 and len(checks) == 449": "len(batches) == 1115 and len(checks) == 450",
    "ARM in paths and ARM in records": "STORY in paths and STORY in records",
    'assert revised == [RECORD] and RECORD not in records[ARM]\n        records[ARM] = [*records[ARM], RECORD]':
        'assert len(revised) == 4 and all(ident in records[STORY] for ident in revised)',
    "snapshot_scope=ARM": "snapshot_scope=STORY",
    "missionary_destination_release_proof": "nagasaki_dream_release_proof",
    '"missionary_destination_pipeline"': '"nagasaki_dream_pipeline"',
    "stage.PROOF, played.REPORT": "stage.PROOF, played.REPORT, PREVIEW",
    "registered_manifest_entries=1115, passing_release_checks=450": "registered_manifest_entries=1116, passing_release_checks=451",
    "changed_internal_files=[ARM]": "changed_internal_files=[STORY]",
    'target_ARM9_sha256=outcome["target_ARM9_sha256"]': 'target_SC3_sha256=outcome["target_SC3_sha256"]',
    "reviewed_UI_labels=1, contextual_records_revisited=1, contextual_decisions_reused=0, previously_localized_records=0":
        "reviewed_UI_labels=0, contextual_records_revisited=17, contextual_decisions_reused=13, previously_localized_records=17",
    "prose_revisions=0, justified_retentions=0, text_display_revisions=1": "prose_revisions=4, justified_retentions=13, text_display_revisions=4",
    "focused_Fleet_Info_destination_fixture=True": "ordinary_Nagasaki_dream=True, revised_gameplay_holds=3, conditional_Angelo_panels_observed=False",
    "display_label_revised=1": "prose_revisions=4, texts_retained=13",
    '"missionary_destination_20261123"': '"nagasaki_dream_20261123"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Nagasaki Inn dream testing candidate

The four revised lines preserve the Namahage encounter, the reward, and the return to the Inn. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Missionary destination candidate": "Preserve the registered Nagasaki dream candidate",
    "1,115 entries and 450 passing checks": "1,116 entries and 451 passing checks",
    doc: '''    DOC.write_text(f"""# Maria’s Nagasaki Inn dream

Four story lines were revised. Yukihisa's startled recognition and his question on waking now sound spoken. His aside restores the explicit **tomorrow morning**. Angelo's conditional interruption returns to his earlier question about the object. Thirteen lines retain their wording, including the dream's repeated calls. The Namahage Cleaver award retains its wording and substitution. [Exact Japanese, earlier and installed records](../{REVIEW.as_posix()})

Ordinary gameplay sailed into Nagasaki from an existing Maria save and triggered the dream through the Inn. Fifteen story panels appeared, and all three revised panels on this path matched their full native glyphs and nameplates. Twenty-nine control frames matched the earlier candidate pixel for pixel, including the cleaver award, Inn choices and return to town. Both Angelo panels stayed unvisited. The revised conditional line passed stored-command and native page checks. [Paired gameplay](../{VERIFY.as_posix()}/{SHEET.name}) · [Native previews](../{VERIFY.as_posix()}/{PREVIEW.name}) · [Initial gameplay and save provenance](../{played.review.OUT.as_posix()})

The release passed 451 checks, its own startup and 17 focused tests. The patch reconstructs the complete candidate from the clean input. The 27,700 historical editorial credits carry forward. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::nagasaki-dream-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
