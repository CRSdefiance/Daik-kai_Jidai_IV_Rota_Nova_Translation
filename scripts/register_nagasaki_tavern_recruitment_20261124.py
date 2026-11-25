"""Register the Nagasaki spare-berth revision after native and ordinary replay checks."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_nagasaki_contract_wrap_20261124 as parent
from scripts import reconcile_archived_message_reader_20261124 as archived
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_nagasaki_tavern_recruitment_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


template, tavern = parent.template, build.tavern
PROFILE = "all-routes-nagasaki-tavern-recruitment-v1-20261124"
CHECK = "registered_nagasaki_tavern_recruitment_and_complete_parent_inverse"
ARM, COMMON, KEY, ROM = build.ARM, build.COMMON, build.KEY, build.ROM
PATCH, PATCH_PROOF, REBUILT, STARTUP_CAPTURE = build.PATCH, build.PATCH_PROOF, build.REBUILT, build.STARTUP_CAPTURE
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_nagasaki_tavern_recruitment_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_nagasaki_tavern_recruitment.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_nagasaki_tavern_recruitment_registered_20261124.md")
CHECKPOINT = "Registered the Nagasaki Tavern spare-berth prompt with the count and question on separate lines."
SHEET = build.SHEET
PREVIEW = build.preflight.OUT.with_suffix("") / "portrait_sheet_01.png"
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.STORED)))


def verify(previous, visual_sha):
    stored, live, patch, packet, native = map(files.read, (build.STORED, build.PAIRED, PATCH_PROOF, tavern.OUT, build.preflight.OUT))
    candidate = files.digest(ROM)
    assert candidate == stored["candidate"]["sha256"] == live["candidate_sha256"] == files.digest(REBUILT)
    assert patch["byte_exact"] and patch["candidate"]["sha256"] == candidate and files.reference(PATCH) == patch["patch"]
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    assert previous["candidate_sha256"] == stored["previous"]["sha256"] == live["previous_sha256"] == packet["candidate_sha256"]
    assert stored["whole_parent_inverse"] and stored["changed_message"] == KEY and stored["allocation"]["new_null_fields"] == 0
    assert files.reference(build.preflight.OUT) == stored["preflight"] and files.reference(build.STORED) == live["stored"]
    assert native["source_review"] == files.reference(tavern.OUT) and len(native["native_cases"]) == 13
    assert live["ordinary_saved_game"] and live["revised"]["frame"] == build.HOLD and len(live["unchanged_frames"]) == 32
    assert files.reference(build.BEFORE) == live["before"] and files.reference(build.REPLAY) == live["after"]
    visuals = [files.reference(SHEET), files.reference(PREVIEW)]
    assert live["sheet"] == visuals[0] and native["sheets"][0]["sha256"] == visuals[1]["sha256"]
    assert files.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha
    observed, = [case["after"] for case in native["native_cases"] if case["count"] == 29]
    assert stored["candidate_layout"] == observed

    clean, old, new = map(files.NdsImage.open, (files.CLEAN, previous["candidate"], ROM))
    arm, old_common, common = new.read_file(ARM), old.read_file(COMMON), new.read_file(COMMON)
    assert arm == old.read_file(ARM) and files.sha256(arm).hexdigest() == previous["target_ARM9_sha256"]
    assert files.sha256(common).hexdigest() == stored["target_COMMON_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    before, after = (tavern.common_rows(data, arm) for data in (old_common, common))
    assert [a.message_id for a, b in zip(before, after, strict=True) if a != b] == [KEY]
    new.replace_file(COMMON, old_common)
    assert bytes(new.rom.save()) == Path(previous["candidate"]).read_bytes()
    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "one_COMMON_tavern_question_and_startup_arm9_unchanged",
    })
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)

    jp = tavern.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    ref = tavern.panels.text_reference
    assert [stored[f"exact_{kind}"] for kind in ("clean_source", "predecessor", "installed")] == [ref(rows[KEY]) for rows in (jp, before, after)]
    proposal, = native["records"]
    records = []
    for row in packet["verified_common_records"]:
        key = row["message_ID"]
        original, prior, installed = jp[key], before[key], after[key]
        assert ref(original) == row["source"] and ref(prior) == row["installed"]
        assert original.text.count(b"%s") == prior.text.count(b"%s") + (key == 872)
        assert prior.text.count(b"%s") == installed.text.count(b"%s")
        note = proposal["localization_note"] if key == KEY else row["rationale"]
        records.append(dict(id=f"COMMON_MESSAGE_{key}", file_path=COMMON, message_id=key,
            context="Maria orders drinks, hears a rumor, recruits sailors and confirms their assignment in Nagasaki.",
            speaker=row["speaker"], source_meaning=proposal["source_meaning"] if key == KEY else note,
            localization_note=note, clean_Japanese=row["Japanese"], previous_English=row["English"],
            english=installed.text.decode("ascii").strip(), source_reference=ref(original), current_reference=ref(prior),
            registered_reference=ref(installed), installed_hex=installed.text.hex(),
            decision="revision" if key == KEY else "retention", review=dict.fromkeys(files.GATES, True)))
    assert len({row["id"] for row in records}) == len(records) == 14
    even = packet["ARM9_even_notice"]
    offset = even["arm9_text_offset"]
    for data, key in ((clean.read_file(ARM), "source_hex"), (arm, "installed_hex")):
        text = bytes.fromhex(even[key])
        assert data[offset:offset + len(text) + 1] == text + b"\0"
    records.append(dict(id="ARM9_ASSIGN_SAILORS_EVEN_NOTICE", file_path=ARM, speaker="Sailor",
        context="The Sailor confirms the Even distribution before Maria finishes assigning sailors.",
        source_meaning="The crew was distributed evenly.", localization_note=even["rationale"], clean_Japanese=even["Japanese"],
        english=even["English"], source_reference=dict(offset=offset, exact_hex=even["source_hex"]),
        current_reference=dict(offset=offset, exact_hex=even["installed_hex"]),
        registered_reference=dict(offset=offset, exact_hex=even["installed_hex"]), decision="retention", review=even["review"]))

    previous_review = files.read(parent.REVIEW)
    shared = previous_review["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    assert all(before[r["message_ID"]] == after[r["message_ID"]] and ref(after[r["message_ID"]]) == r["installed"] for r in shared["records"])
    bounded = files.read(archived.OUT)
    assert bounded["candidate_sha256"] == previous["candidate_sha256"]
    assert all(before[key] == after[key] for key in bounded["preserved_archived_messages"])
    outcome = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate,
        target_COMMON_sha256=stored["target_COMMON_sha256"], visual_review=visuals, stored_proof=files.reference(build.STORED),
        gameplay=files.reference(build.PAIRED), source_review=files.reference(tavern.OUT),
        unchanged_archived_message_reader_evidence=files.reference(archived.OUT),
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=previous_review["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=previous_review["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_tavern_buy_a_round_predecessor=predecessor, nagasaki_contract_wrap_release=str(REVIEW)":
        "verified_nagasaki_contract_wrap_predecessor=predecessor, nagasaki_tavern_recruitment_release=str(REVIEW)",
    "len(batches) == 1121 and len(checks) == 456": "len(batches) == 1122 and len(checks) == 457",
    "nagasaki_contract_wrap_release_proof": "nagasaki_tavern_recruitment_release_proof",
    '"nagasaki_contract_wrap_pipeline"': '"nagasaki_tavern_recruitment_pipeline"',
    "build.PAIRED, PREVIEW, build.market.OUT, build.market.SHEET, build.preflight.OUT":
        "build.PAIRED, PREVIEW, tavern.OUT, build.preflight.OUT",
    "registered_manifest_entries=1122, passing_release_checks=457": "registered_manifest_entries=1123, passing_release_checks=458",
    "contextual_records_revisited=5, contextual_decisions_reused=4, previously_localized_records=5":
        "contextual_records_revisited=15, contextual_decisions_reused=14, previously_localized_records=15",
    "justified_retentions=4": "justified_retentions=14",
    "ordinary_Nagasaki_Palace_and_Trade=True, revised_gameplay_holds=1, native_pages=1, goods_info_selections=3":
        "ordinary_Nagasaki_Tavern_and_Recruitment=True, revised_gameplay_holds=1, native_pages=13, unchanged_gameplay_holds=32",
    "texts_retained=4": "texts_retained=14",
    '"nagasaki_contract_wrap_20261124"': '"nagasaki_tavern_recruitment_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Nagasaki Tavern recruitment candidate

The sailor's count and follow-up question each fit on a complete line. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Nagasaki contract wrap candidate": "Preserve the registered Nagasaki Tavern recruitment candidate",
    "1,122 entries and 457 passing checks": "1,123 entries and 458 passing checks",
    doc: '''    DOC.write_text(f"""# Nagasaki Tavern recruitment prompt

The sailor now says, “There's room aboard for 29 more. Should I keep looking?” The count and complete question take one line each in ordinary play and at all 13 checked counts. Fourteen other parts of the Tavern and assignment exchange retain their wording. [Source and complete decisions](../{REVIEW.as_posix()})

The edited replay followed the Naha tip, the Pink Apron rumor, both original recruitment choices, Even assignment and the return to town. Thirty-two comparison frames match pixel for pixel. [Paired gameplay](../{VERIFY.as_posix()}/{SHEET.name}) · [All native previews](../{VERIFY.as_posix()}/{PREVIEW.name})

The cumulative candidate passed startup, 458 release checks and 17 focused repository tests. The patch reconstructs the candidate byte for byte. Alternate local rumors and another recruiting attempt remain unvisited. [Testing build and clean-input patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    cli = template.ArgumentParser(description=__doc__)
    cli.add_argument("--visual-sha256")
    cli.add_argument("--finish-only", action="store_true")
    args = cli.parse_args()
    assert args.finish_only or args.visual_sha256
    scope = vars(template) | vars(parent.parent) | vars(parent) | globals()
    exec(compile(prepare + "\n" + finish, __file__ + "::nagasaki-tavern-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
