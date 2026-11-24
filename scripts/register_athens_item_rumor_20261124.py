"""Register the Athens rumor after native and ordinary gameplay verification."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_cartridge_title_20261123 as template
from scripts import register_rafael_prepare_alone_20261123 as parent
from scripts import stage_athens_item_rumor_20261124 as build
from scripts import stage_cartridge_title_20261123 as files
from scripts.source_locked_derivation_v5118 import checked_text


PROFILE = "all-routes-athens-item-rumor-v1-20261124"
CHECK = "registered_athens_item_rumor_native_page_and_complete_parent_inverse"
ARM, COMMON, KEY = build.ARM, build.COMMON, build.KEY
WORK, ROM = build.ROOT, build.ROM
PATCH, PATCH_PROOF, REBUILT, STARTUP_CAPTURE = build.PATCH, build.PATCH_PROOF, build.REBUILT, build.STARTUP_CAPTURE
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_athens_item_rumor_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_athens_item_rumor.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA = WORK / "own_startup_verification.json", WORK / "qa_passed.xml"
DOC = Path("docs/editorial_athens_item_rumor_registered_20261124.md")
CHECKPOINT = "Registered the Tavern's item rumor after ordinary Athens and Valencia gameplay."
SHEET, PREVIEW = build.SHEET, build.review.PREVIEWS / "portrait_sheet_01.png"
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.STORED)))


def verify(previous, visual_sha):
    stored, live, patch, packet, native = map(stage.read, (build.STORED, build.PAIRED, PATCH_PROOF, build.review.OUT, build.review.PREFLIGHT))
    candidate = stage.digest(ROM)
    assert candidate == stored["candidate"]["sha256"] == live["candidate_sha256"] == stage.digest(REBUILT)
    assert patch["byte_exact"] and patch["candidate"]["sha256"] == candidate and stage.reference(PATCH) == patch["patch"]
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == stored["clean"]["sha256"] == stage.digest(stage.CLEAN)
    assert previous["candidate_sha256"] == stored["previous"]["sha256"] == live["previous_sha256"] == packet["candidate_sha256"]
    assert stored["whole_parent_inverse"] and stored["changed_message"] == KEY and stored["allocation"]["new_null_fields"] == 0
    assert stage.reference(build.review.OUT) == stored["source_review"] and stage.reference(build.review.PREFLIGHT) == stored["preflight"]
    assert stage.reference(build.STORED) == live["stored"] and live["ordinary_saved_game"]
    assert live["revised"]["frame"] == build.HOLD and len(live["unchanged_frames"]) == 16
    assert stage.reference(build.BEFORE) == live["before"] and stage.reference(build.REPLAY) == live["after"]
    visuals = [stage.reference(SHEET), stage.reference(PREVIEW)]
    assert live["sheet"] == visuals[0] and native["sheets"][0]["sha256"] == visuals[1]["sha256"]
    assert stage.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha
    assert stored["all_item_name_cases"] == 218 and stored["split_item_names"] == 0
    assert live["whole_page_sha256"] == stage.sha256(bytes.fromhex(stored["native_plane_hex"])).hexdigest()

    clean, old, new = map(stage.NdsImage.open, (stage.CLEAN, previous["candidate"], ROM))
    arm, common = new.read_file(ARM), new.read_file(COMMON)
    assert arm == old.read_file(ARM) and stage.sha256(arm).hexdigest() == stored["target_ARM9_sha256"] == previous["target_ARM9_sha256"]
    assert stage.sha256(common).hexdigest() == stored["target_COMMON_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    old_common = old.read_file(COMMON)
    before, after = (build.review.common_rows(data, arm) for data in (old_common, common))
    assert [a.message_id for a, b in zip(before, after, strict=True) if a != b] == [KEY]
    new.replace_file(COMMON, old_common)
    assert bytes(new.rom.save()) == Path(previous["candidate"]).read_bytes()

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "one_COMMON_rumor_and_startup_arm9_unchanged",
    })
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)

    jp = build.review.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    reference = build.panels.text_reference
    assert stored["exact_clean_source"] == reference(jp[KEY]) and stored["exact_predecessor"] == reference(before[KEY])
    assert stored["exact_installed"] == reference(after[KEY])
    records = []
    for row in packet["records"]:
        key = row["message_ID"]
        original, prior, installed = jp[key], before[key], after[key]
        changed = key == KEY
        assert original.text.hex() == row["source_hex"] and prior.text.hex() == row["installed_hex"]
        assert original.text.count(b"%s") == prior.text.count(b"%s") == installed.text.count(b"%s")
        gloss = ("Ask whether the listener knows the named object. It is somewhere in the world, and the speaker has heard it is very beautiful."
                 if changed else row["localization_note"])
        note = ("Say the runtime title on its own, then ask about it. Keep the unspecified location and the emphasis and hearsay about its beauty. This keeps every supplied title intact."
                if changed else row["localization_note"])
        records.append(row | dict(message_id=key, previous_English=row["english"], english=installed.text.decode("ascii").strip(),
            context="Ordinary Tavern orders and independently selected Square shop replies in Athens and Valencia.",
            source_meaning=gloss, localization_note=note, current_reference=reference(prior) | dict(exact_stored_hex=prior.text.hex()),
            registered_reference=reference(installed) | dict(exact_stored_hex=installed.text.hex(), candidate_sha256=candidate),
            source_reference=reference(original) | dict(exact_stored_hex=original.text.hex()), installed_hex=installed.text.hex(),
            decision="revision" if changed else "retention", review=dict.fromkeys(files.GATES, True)))
    assert len(records) == 15 and sum(row["decision"] == "revision" for row in records) == 1
    previous_review = stage.read(parent.REVIEW)
    shared = previous_review["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    assert all(before[r["message_ID"]] == after[r["message_ID"]] and reference(after[r["message_ID"]]) == r["installed"]
               for r in shared["records"])
    outcome = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate,
        target_COMMON_sha256=stored["target_COMMON_sha256"], source_review=stage.reference(build.review.OUT),
        visual_review=visuals, stored_proof=stage.reference(build.STORED), gameplay=stage.reference(build.PAIRED),
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=previous_review["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=previous_review["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_kurushima_confrontation_predecessor=predecessor, rafael_prepare_alone_release=str(REVIEW)":
        "verified_rafael_prepare_alone_predecessor=predecessor, athens_item_rumor_release=str(REVIEW)",
    "len(batches) == 1117 and len(checks) == 452": "len(batches) == 1118 and len(checks) == 453",
    "STORY in paths and STORY in records": "COMMON in paths and COMMON in records",
    "records[STORY]": "records[COMMON]",
    "assert revised == [build.review.RESPONSE]": 'assert revised == [f"COMMON_MESSAGE_{KEY}"]',
    "snapshot_scope=STORY": "snapshot_scope=COMMON",
    "rafael_prepare_alone_release_proof": "athens_item_rumor_release_proof",
    '"rafael_prepare_alone_pipeline"': '"athens_item_rumor_pipeline"',
    "played.PAIRED, PREVIEW": "build.PAIRED, PREVIEW",
    "registered_manifest_entries=1118, passing_release_checks=453": "registered_manifest_entries=1119, passing_release_checks=454",
    "changed_internal_files=[STORY]": "changed_internal_files=[COMMON]",
    'target_SC0_sha256=outcome["target_SC0_sha256"]': 'target_COMMON_sha256=outcome["target_COMMON_sha256"]',
    "contextual_records_revisited=10, contextual_decisions_reused=9, previously_localized_records=10":
        "contextual_records_revisited=15, contextual_decisions_reused=14, previously_localized_records=15",
    "justified_retentions=9": "justified_retentions=14",
    "ordinary_Rafael_preparation_choice=True, revised_gameplay_holds=1, native_pages=1":
        "ordinary_Athens_Tavern=True, revised_gameplay_holds=1, native_item_name_layouts=218",
    "texts_retained=9": "texts_retained=14",
    '"rafael_prepare_alone_20261123"': '"athens_item_rumor_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Athens Tavern item rumor candidate

The Tavern's rumor names the item naturally. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Rafael preparation candidate": "Preserve the registered Athens item rumor candidate",
    "1,118 entries and 453 passing checks": "1,119 entries and 454 passing checks",
    "# Current editorial checkpoint - 2026-11-23": "# Current editorial checkpoint - 2026-11-24",
    doc: '''    DOC.write_text(f"""# Myrine's Tavern rumor and regional shops

Ordinary Athens and Valencia play verified 24 complete dialogue holds across 15 shared messages. Fourteen lines retain their wording, including the barkeep's reports about three prominent figures, the tag question in the Delicacy Shop, and the Invincible Armada rumor. Myrine now introduces the Lamenting Jar by name before asking whether Hodram has heard of it. The original item substitution, vague whereabouts and admiration stay intact. [Context and exact references](../{REVIEW.as_posix()})

All 218 catalog names passed the original formatter. The old wording split 66 item names across rows. The new wording keeps every item name intact. The complete revised page and Myrine's nameplate matched ordinary gameplay. Sixteen earlier or later holds, including the return to Athens, match the predecessor pixel for pixel. [Paired replay](../{VERIFY.as_posix()}/{SHEET.name}) · [Native sample pages](../{VERIFY.as_posix()}/{PREVIEW.name})

The cumulative build passed 454 release checks, candidate startup, 17 focused tests, and byte-exact clean-input reconstruction. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::item-rumor-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
