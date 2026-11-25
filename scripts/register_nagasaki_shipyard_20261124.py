"""Register the three Yard revisions after current native and ordinary replay checks."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_nagasaki_tavern_recruitment_20261124 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_nagasaki_shipyard_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


template, yard = parent.template, build.yard
PROFILE = "all-routes-nagasaki-yard-reflow-v1-20261124"
CHECK = "registered_nagasaki_yard_reflow_and_complete_parent_inverse"
ARM, COMMON, ROM = build.ARM, build.COMMON, build.ROM
PATCH, PATCH_PROOF, REBUILT, STARTUP_CAPTURE = build.PATCH, build.PATCH_PROOF, build.REBUILT, build.STARTUP_CAPTURE
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_nagasaki_yard_reflow_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_nagasaki_yard_reflow.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_nagasaki_yard_reflow_registered_20261124.md")
CHECKPOINT = "Registered both Refit sail descriptions and the one-line Ship Name prompt after the Nagasaki Yard replay."
SHEET = build.SHEET
SAIL_PREVIEW = build.preflight.NATIVE_ROOT / "native_review_sheet_1.png"
RENAME_PREVIEW = build.preflight.ROOT / "portrait_sheet_01.png"
NATIVE_FONT = build.preflight.NATIVE_ROOT / "native_font_verification.json"
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.STORED)))


def verify(previous, visual_sha):
    stored, live, patch, packet, native = map(files.read, (build.STORED, build.PAIRED, PATCH_PROOF, yard.OUT, build.preflight.OUT))
    candidate = files.digest(ROM)
    assert candidate == stored["candidate"]["sha256"] == live["candidate_sha256"] == files.digest(REBUILT)
    assert patch["byte_exact"] and patch["candidate"]["sha256"] == candidate and files.reference(PATCH) == patch["patch"]
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    assert previous["candidate_sha256"] == stored["previous"]["sha256"] == live["previous_sha256"] == packet["candidate_sha256"]
    assert stored["whole_parent_inverse"] and stored["changed_messages"] == sorted(yard.PROPOSALS)
    assert stored["allocations"] == native["exact_storage_slots"] and all(not r["new_null_fields"] for r in stored["allocations"].values())
    assert files.reference(build.preflight.OUT) == stored["preflight"] and files.reference(build.STORED) == live["stored"]
    assert native["gameplay"] == files.reference(yard.OUT) and native["checked_refit_pages"] == files.reference(NATIVE_FONT)
    assert live["ordinary_saved_game"] and {r["frame"]: r["message_ID"] for r in live["revised"]} == build.REVISIONS
    assert len(live["unchanged_frames"]) == 47
    assert {row["frame"] for row in live["menu_highlight_only"] if row["background_only"]} == set(build.BLINKS)
    assert files.reference(build.BEFORE) == live["before"] and files.reference(build.REPLAY) == live["after"]
    visuals = list(map(files.reference, (SHEET, SAIL_PREVIEW, RENAME_PREVIEW)))
    assert live["sheet"] == visuals[0]
    assert all(Path(a["path"]) == Path(b["path"]) and a["sha256"] == b["sha256"]
               for a, b in zip(stored["reviewed_native_previews"], visuals[1:], strict=True))
    assert files.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    clean, old, new = map(files.NdsImage.open, (files.CLEAN, previous["candidate"], ROM))
    original_arm, arm, old_common, common = clean.read_file(ARM), new.read_file(ARM), old.read_file(COMMON), new.read_file(COMMON)
    assert arm == old.read_file(ARM) and files.sha256(arm).hexdigest() == previous["target_ARM9_sha256"]
    assert files.sha256(common).hexdigest() == stored["target_COMMON_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    before, after = (yard.common_rows(data, arm) for data in (old_common, common))
    assert [a.message_id for a, b in zip(before, after, strict=True) if a != b] == sorted(yard.PROPOSALS)
    new.replace_file(COMMON, old_common)
    assert bytes(new.rom.save()) == Path(previous["candidate"]).read_bytes()
    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "three_COMMON_yard_messages_and_startup_arm9_unchanged",
    })
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)

    jp = yard.common_message_entries(clean.read_file(COMMON), original_arm)
    ref = yard.panels.text_reference
    for label, source_rows in (("source", jp), ("predecessor", before), ("installed", after)):
        assert stored[f"exact_{label}_rows"] == {str(key): ref(source_rows[key]) for key in yard.PROPOSALS}
    proposals = {row["message_id"]: row for row in native["records"]}
    records = []
    for row in packet["records"]:
        key = row["message_ID"]
        original, prior, installed = jp[key], before[key], after[key]
        assert ref(original) == row["source"] and ref(prior) == row["installed"]
        assert original.text.count(b"%s") == prior.text.count(b"%s") == installed.text.count(b"%s")
        draft = proposals.get(key, {})
        english = " ".join(installed.text.decode("ascii").split())
        assert english == draft.get("english", " ".join(row["English"].split()))
        records.append(dict(id=f"COMMON_MESSAGE_{key}", file_path=COMMON, message_id=key,
            context=draft.get("context", "Maria visits the Nagasaki Yard for ship purchases, sales, equipment and naming."),
            speaker=row["speaker"] or ("Refit equipment help" if key in yard.REFIT.values() else "Shipyard confirmation"),
            source_meaning=draft.get("source_meaning", row["rationale"]), localization_note=row["rationale"],
            clean_Japanese=row["Japanese"], previous_English=row["English"], english=english, source_reference=ref(original),
            current_reference=ref(prior), registered_reference=ref(installed), installed_hex=installed.text.hex(),
            decision="revision" if key in proposals else "retention", review=dict.fromkeys(files.GATES, True)))
    cancel = packet["fixed_ARM9_prompt"]
    for data, spec in ((original_arm, cancel["source"]), (arm, cancel["installed"])):
        text, offset = bytes.fromhex(spec.get("source_hex", spec.get("exact_hex"))), spec["offset"]
        assert data[offset:offset + len(text)] == text
    records.append(dict(id=cancel["source"]["id"], file_path=ARM, speaker="Shipyard confirmation",
        context="Maria cancels equipment remodeling and confirms the return to the ship choice.", source_meaning="Cancel remodeling?",
        english=cancel["English"], clean_Japanese=cancel["Japanese"], localization_note=cancel["rationale"],
        source_reference=cancel["source"], current_reference=cancel["installed"], registered_reference=cancel["installed"],
        decision="retention", review=cancel["review"]))
    assert len({row["id"] for row in records}) == len(records) == 13

    previous_review = files.read(parent.REVIEW)
    shared = previous_review["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    assert all(before[r["message_ID"]] == after[r["message_ID"]] and ref(after[r["message_ID"]]) == r["installed"] for r in shared["records"])
    archived = parent.archived.OUT
    bound = files.read(archived)
    archived_receipt = files.read(parent.parent.RELEASE)
    archived_parent = files.NdsImage.open(archived_receipt["candidate"])
    assert bound["candidate_sha256"] == archived_receipt["candidate_sha256"] and archived_parent.read_file(ARM) == arm
    archived_rows = yard.common_rows(archived_parent.read_file(COMMON), arm)
    assert all(archived_rows[key] == before[key] == after[key] for key in bound["preserved_archived_messages"])
    outcome = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate,
        target_COMMON_sha256=stored["target_COMMON_sha256"], visual_review=visuals, stored_proof=files.reference(build.STORED),
        gameplay=files.reference(build.PAIRED), source_review=files.reference(yard.OUT), unchanged_archived_message_reader_evidence=files.reference(archived),
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=previous_review["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=previous_review["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_nagasaki_contract_wrap_predecessor=predecessor, nagasaki_tavern_recruitment_release=str(REVIEW)":
        "verified_nagasaki_tavern_recruitment_predecessor=predecessor, nagasaki_yard_reflow_release=str(REVIEW)",
    "len(batches) == 1122 and len(checks) == 457": "len(batches) == 1123 and len(checks) == 458",
    'assert revised == [f"COMMON_MESSAGE_{KEY}"]': 'assert sorted(revised) == sorted(f"COMMON_MESSAGE_{k}" for k in yard.PROPOSALS)',
    "nagasaki_tavern_recruitment_release_proof": "nagasaki_yard_reflow_release_proof",
    '"nagasaki_tavern_recruitment_pipeline"': '"nagasaki_yard_reflow_pipeline"',
    "build.PAIRED, PREVIEW, tavern.OUT, build.preflight.OUT":
        "build.PAIRED, SAIL_PREVIEW, RENAME_PREVIEW, yard.OUT, build.preflight.OUT, NATIVE_FONT",
    "registered_manifest_entries=1123, passing_release_checks=458": "registered_manifest_entries=1124, passing_release_checks=459",
    "contextual_records_revisited=15, contextual_decisions_reused=14, previously_localized_records=15":
        "contextual_records_revisited=13, contextual_decisions_reused=10, previously_localized_records=13",
    "prose_revisions=1, justified_retentions=14, text_display_revisions=1": "prose_revisions=3, justified_retentions=10, text_display_revisions=3",
    "ordinary_Nagasaki_Tavern_and_Recruitment=True, revised_gameplay_holds=1, native_pages=13, unchanged_gameplay_holds=32":
        "ordinary_Nagasaki_Yard=True, revised_gameplay_holds=4, native_pages=3, unchanged_gameplay_holds=47, background_highlight_only_holds=4",
    "prose_revisions=1, wrap_only_revisions=0, texts_retained=14": "prose_revisions=3, wrap_only_revisions=0, texts_retained=10",
    '"nagasaki_tavern_recruitment_20261124"': '"nagasaki_yard_reflow_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Nagasaki Yard reflow candidate

The two sail tips keep their mounting instructions together. The rename question stays on one line. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Nagasaki Tavern recruitment candidate": "Preserve the registered Nagasaki Yard reflow candidate",
    "1,123 entries and 458 passing checks": "1,124 entries and 459 passing checks",
    doc: '''    DOC.write_text(f"""# Nagasaki Yard dialogue and sail help

The Yard asks “Which ship do you want to rename?” on one line. The square and lateen tips preserve their wind advantages and opposing mounting restrictions. Ten neighboring records retain their wording. [Source, stored text, and review gates](../{REVIEW.as_posix()})

Ordinary play verified four changed holds and 47 pixel-identical comparison frames. Four further frames differ only in the blinking menu highlight backgrounds. Every glyph in those frames is pixel-identical. The replay covers purchase and sale cancellation, the no-damage repair response, the native rename keyboard, equipment and Dock cancellation, and return to Nagasaki with unchanged funds. [Paired gameplay](../{VERIFY.as_posix()}/{SHEET.name}) · [Sail previews](../{VERIFY.as_posix()}/{SAIL_PREVIEW.name}) · [Rename preview](../{VERIFY.as_posix()}/{RENAME_PREVIEW.name})

The cumulative candidate passed startup, 459 release checks, and 17 focused tests. The clean-input patch reconstructs the complete candidate. Completed transactions, damaged ships, and extra Dock branches remain unvisited in this replay. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    cli = template.ArgumentParser(description=__doc__)
    cli.add_argument("--visual-sha256")
    cli.add_argument("--finish-only", action="store_true")
    args = cli.parse_args()
    assert args.finish_only or args.visual_sha256
    scope = vars(template) | vars(parent.parent.parent) | vars(parent.parent) | vars(parent) | globals()
    exec(compile(prepare + "\n" + finish, __file__ + "::nagasaki-yard-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
