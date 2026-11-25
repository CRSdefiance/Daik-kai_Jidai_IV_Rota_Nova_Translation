"""Register the ordinary-tested Claudio reflow over the Deck View release."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import check_claudio_opening_wrap_20261124 as checks
from scripts import reconcile_elegy_acceptance_20261123 as acceptance
from scripts import register_cartridge_title_20261123 as template
from scripts import register_deck_skill_guidance_20261124 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_claudio_opening_wrap_20261124 as build
from scripts import verify_claudio_opening_wrap_20261124 as gameplay
from scripts import verify_rafael_new_game_fleet_20261124 as review
from scripts.source_locked_derivation_v5118 import checked_text

PROFILE = "all-routes-claudio-opening-wrap-v1-20261124"
CHECK = "registered_claudio_opening_wrap_and_complete_parent_inverse"
WORK, ROM, STORY, BLOCK = build.ROOT, build.ROM, build.STORY, build.BLOCK
ARM, COMMON = parent.ARM, parent.COMMON
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_claudio_opening_wrap_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json",
                                                  "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF = checks.PATCH, checks.REBUILT, checks.PATCH_PROOF
STARTUP_CAPTURE, QA = checks.STARTUP_CAPTURE, checks.QA
STARTUP = WORK / "own_startup_verification.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_claudio_opening_wrap.json.gz", WORK / "ledger_after.json.gz"
DOC = Path("docs/editorial_claudio_opening_wrap_registered_20261124.md")
CHECKPOINT = "Registered Claudio's opening reflow with his full phrase intact."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=build.STORED)))


def verify(previous, visual_sha):
    stored, packet, live, native, patch = map(files.read, (build.STORED, review.OUT, gameplay.OUT, build.NATIVE, PATCH_PROOF))
    candidate = files.digest(ROM)
    assert previous["candidate_sha256"] == stored["previous"]["sha256"] == packet["candidate_sha256"]
    assert stored["candidate"] == live["candidate"] == files.reference(ROM)
    assert patch["byte_exact"] and patch["candidate"] == files.reference(ROM) and patch["patch"] == files.reference(PATCH)
    assert patch["rebuilt"] == files.reference(REBUILT) and files.digest(REBUILT) == candidate
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    assert stored["complete_parent_inverse"] and stored["unchanged_archive_directory"]
    assert native["offline_native_renderer"] and live["cold_boot_ordinary_new_game"]
    assert len(live["matching_companion_frames"]) == 10
    assert live["revised_frame"] == gameplay.HOLD and live["reviewed_record"] == review.WRAP_ID
    visuals = [files.reference(gameplay.SHEET), files.reference(build.SHEET)]
    assert visuals == [live["contact_sheet"], native["sheet"]]
    assert files.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    clean, old, new = map(files.NdsImage.open, (files.CLEAN, previous["candidate"], ROM))
    before, after = map(build.paths, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {STORY}
    assert files.sha256(after[ARM]).hexdigest() == previous["target_ARM9_sha256"]
    assert files.sha256(after[COMMON]).hexdigest() == previous["target_COMMON_sha256"]
    assert files.sha256(after[STORY]).hexdigest() == stored["target_archive_sha256"]
    assert template.right_bound(after[ARM], previous["right_bound_configuration"])["matched_repair_spans"] == 8
    old_blocks, blocks = [build.IlnkContainer.parse(data[STORY]).blocks for data in (before, after)]
    assert [n for n, (a, b) in enumerate(zip(old_blocks, blocks, strict=True)) if a != b] == [BLOCK]
    source = build.IlnkContainer.parse(clean.read_file(STORY)).blocks[BLOCK]
    new.replace_file(STORY, before[STORY])
    assert files.sha256(new.rom.save()).hexdigest() == previous["candidate_sha256"]

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    startup = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    program = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "one_Rafael_wrap_command_and_startup_arm9_unchanged",
    })
    exec(compile(program, __file__ + "::startup", "exec"), startup)
    startup["startup_proof"](previous, candidate, after[ARM])

    records = []
    for row in packet["story"]["encounter_records"].values():
        existing = row["installed_reference"]
        clean_ref = row["source_reference"]
        clean_bytes = bytes.fromhex(clean_ref["exact_command_hex"])
        source_at = clean_ref["command_offset"]
        assert source[source_at:source_at + len(clean_bytes)] == clean_bytes
        at, command = existing["command_offset"], bytes.fromhex(existing["exact_command_hex"])
        assert old_blocks[BLOCK][at:at + len(command)] == command
        revised = row["id"] == review.WRAP_ID
        data = bytes.fromhex(stored["edit"]["stored"]) if revised else command
        assert len(data) == len(command) and data[:6] == command[:6]
        assert blocks[BLOCK][at:at + len(data)] == data
        body = data[6:data.index(0, 6)]
        assert " ".join(body.decode("ascii").split()) == row["english"]
        result = row | dict(file_path=STORY, block=BLOCK, decision="revision" if revised else "retention",
            change_class="wrap_only" if revised else "retention", review=dict.fromkeys(files.GATES, True),
            registered_reference=existing | dict(exact_command_hex=data.hex(), exact_body_hex=body.hex(),
                candidate_sha256=candidate, archive_sha256=stored["target_archive_sha256"],
                block_sha256=files.sha256(blocks[BLOCK]).hexdigest()))
        if revised:
            result.update(localization_note="Claudio's boast and the captain-name substitution retain their wording. The full phrase 'at his side' now stays together.",
                          protected_phrases=["at his side."], live_revision=files.reference(gameplay.OUT))
            result.pop("staged_or_installed_revision")
        records.append(result)
    assert len(records) == 5 and sum(r["decision"] == "revision" for r in records) == 1

    previous_review = files.read(parent.REVIEW)
    shared = previous_review["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    common = acceptance.common_rows(after[COMMON], after[ARM])
    assert all(review.gameplay.panels.text_reference(common[r["message_ID"]]) == r["installed"] for r in shared["records"])
    outcome = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate,
        target_SC0_sha256=stored["target_archive_sha256"], source_review=files.reference(review.OUT),
        visual_review=visuals, stored_proof=files.reference(build.STORED), gameplay=files.reference(gameplay.OUT),
        shared_consumer_binding=shared | {"candidate_sha256": candidate},
        retained_four_route_census_sha256=previous_review["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=previous_review["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


current_prepare = parent.prepare
readme = current_prepare[current_prepare.index('    (PACKAGE / "README.md")'):current_prepare.index('    stage.write(PACKAGE / "checksums.json"')]
current_finish = parent.finish
doc = current_finish[current_finish.index("    DOC.write_text"):current_finish.index("    prefix =")]
prepare = checked_text(current_prepare, {
    "verified_cargo_storage_warning_predecessor=predecessor, deck_skill_guidance_release=str(REVIEW)":
        "verified_deck_skill_guidance_predecessor=predecessor, claudio_opening_wrap_release=str(REVIEW)",
    "len(batches) == 1141 and len(checks) == 476": "len(batches) == 1142 and len(checks) == 477",
    "{ARM, COMMON} <= set(paths) and {ARM, COMMON} <= records.keys()": "{ARM, COMMON, STORY} <= set(paths) and {ARM, COMMON, STORY} <= records.keys()",
    "assert revised == [r['id'] for r in outcome['records'] if r['field'] == build.FIELD] and len(revised) == 1":
        "assert revised == [review.WRAP_ID]",
    "snapshot_scope=[ARM]": "snapshot_scope=[STORY]",
    "deck_skill_guidance_release_proof": "claudio_opening_wrap_release_proof",
    '"deck_skill_guidance_pipeline"': '"claudio_opening_wrap_pipeline"',
    "gameplay.OUT, review.OUT, *(": "gameplay.OUT, review.OUT, build.NATIVE, *(",
    "registered_manifest_entries=1142, passing_release_checks=477, changed_components=1, changed_internal_files=[ARM]":
        "registered_manifest_entries=1143, passing_release_checks=478, changed_components=1, changed_internal_files=[STORY]",
    'target_COMMON_sha256=outcome["target_COMMON_sha256"], target_ARM9_sha256=outcome["target_ARM9_sha256"]':
        'target_SC0_sha256=outcome["target_SC0_sha256"]',
    "contextual_records_revisited=15, contextual_decisions_reused=0, previously_localized_records=15":
        "contextual_records_revisited=5, contextual_decisions_reused=4, previously_localized_records=5",
    "prose_revisions=1, justified_retentions=14, text_display_revisions=0, phrase_wrap_adjustments=0":
        "prose_revisions=0, justified_retentions=4, text_display_revisions=0, phrase_wrap_adjustments=1",
    'ordinary_Riga_Market_Deck_and_departure=True, revised_gameplay_holds=5, native_pages=1, unchanged_gameplay_holds=stage.read(gameplay.OUT)["unchanged_holds"]':
        'ordinary_Rafael_New_Game=True, revised_gameplay_holds=1, native_pages=3, unchanged_gameplay_holds=10',
    "prose_revisions=1, phrase_wrap_adjustments=0, punctuation_fields=0, texts_retained=14":
        "prose_revisions=0, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=4",
    '"deck_skill_guidance_20261124"': '"claudio_opening_wrap_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Claudio's opening reflow

Claudio's line keeps “at his side” together and retains the captain-name substitution. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate}.
""", encoding="utf-8")
''',
})
finish = checked_text(current_finish, {
    "Preserve the registered Deck View skill guidance candidate": "Preserve the registered Claudio opening reflow candidate",
    "1,142 entries and 477 passing checks": "1,143 entries and 478 passing checks",
    doc: '''    DOC.write_text(f"""# Claudio's opening reflow

Claudio's “at his side” now stays together in Rafael's opening. The original wording, portrait, speaker control, and captain-name substitution carry through. The default and one- and 16-letter variants pass the original renderer on one page. Ordinary paired New Game verified the complete revised body and Claudio's nameplate, with ten companion frames matching. [Exact review](../{REVIEW.as_posix()}) · [Ordinary before and after](../{VERIFY.as_posix()}/{gameplay.SHEET.name})

New Game also traced 234 writes across the 63 actual fleet and 20 company objects. All 146 dock, destination and headquarters fields reconcile at eight snapshots. No write supplied slot 114. The three resident COMMON function-pointer words are already known, and no request used the five archived keys. The ordinary Missionary producer and those display owners remain open. [Exact seeds, writes, and source references](../{review.OUT.as_posix()})

The testing build passed 478 release checks, independent startup, 17 focused tests and byte-for-byte clean-input patch reconstruction. [Testing package](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})


def main():
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--visual-sha256")
    cli.add_argument("--finish-only", action="store_true")
    args = cli.parse_args()
    assert args.finish_only or args.visual_sha256
    lineage = [parent]
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 16:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(prepare + "\n" + finish, __file__ + "::registered-opening-reflow", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()


if __name__ == "__main__":
    main()
