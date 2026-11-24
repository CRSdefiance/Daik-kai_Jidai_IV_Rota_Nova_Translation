"""Register the Stockholm recruiting edit after the source, gameplay and patch checks."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import check_stockholm_recruiting_20261124 as played
from scripts import reconcile_elegy_acceptance_20261123 as acceptance
from scripts import register_cartridge_title_20261123 as template
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_stockholm_recruiting_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


parent = build.parent
PROFILE = "all-routes-stockholm-recruiting-v1-20261124"
CHECK = "registered_stockholm_recruiting_native_page_and_complete_parent_inverse"
ARM, COMMON, STORY = build.ARM, build.COMMON, build.STORY
WORK, ROM = build.ROOT, build.ROM
PATCH, PATCH_PROOF, REBUILT, STARTUP_CAPTURE = build.PATCH, build.PATCH_PROOF, build.REBUILT, build.STARTUP_CAPTURE
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_stockholm_recruiting_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_stockholm_recruiting.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA = WORK / "own_startup_verification.json", WORK / "qa_passed.xml"
DOC = Path("docs/editorial_stockholm_recruiting_registered_20261124.md")
CHECKPOINT = "Registered Gerhard's recruiting advice after both ordinary Stockholm Tavern choices."
SHEET = played.SHEET
PREVIEW = build.review.OUT.with_name("stockholm_recruiting_proposal_1_20261123.png")
RESPONSE = "DK4_MES_B134_R0025"
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.STORED)))


def verify(previous, visual_sha):
    packet, stored, live, patch = map(stage.read, (build.review.OUT, build.STORED, played.PAIRED, PATCH_PROOF))
    candidate = stage.digest(ROM)
    assert candidate == stored["candidate"]["sha256"] == live["candidate_sha256"] == stage.digest(REBUILT)
    assert patch["byte_exact"] and patch["candidate"]["sha256"] == candidate and stage.reference(PATCH) == patch["patch"]
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == stored["clean"]["sha256"] == stage.digest(stage.CLEAN)
    assert previous["candidate_sha256"] == stored["previous"]["sha256"] == live["previous_sha256"] == packet["candidate_sha256"]
    assert stored["whole_parent_inverse"] and stored["unchanged_archive_directory"]
    assert stage.reference(build.review.OUT) == stored["source_review"] and stage.reference(build.STORED) == live["stored"]
    assert live["ordinary_saved_game"] and live["same_choice_and_tavern_return"] and packet["ordinary_existing_battery_save"]
    assert live["revised"]["frame"] == played.CHANGED and len(live["unchanged_frames"]) == 8
    for ref in live["after"].values():
        assert stage.reference(ref["path"]) == ref
    visuals = [stage.reference(SHEET), stage.reference(PREVIEW)]
    assert visuals == [live["visual"], stored["visual"]]
    assert stage.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    original, old, new = map(stage.NdsImage.open, (stage.CLEAN, previous["candidate"], ROM))
    before, after = map(build.native.files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {STORY}
    assert stage.sha256(after[ARM]).hexdigest() == previous["target_ARM9_sha256"]
    assert stage.sha256(after[COMMON]).hexdigest() == previous["target_COMMON_sha256"]
    assert stage.sha256(after[STORY]).hexdigest() == stored["target_SC1_sha256"]
    assert template.right_bound(after[ARM], previous["right_bound_configuration"])["matched_repair_spans"] == 8
    archives = [build.panels.IlnkContainer.parse(data[STORY]).blocks for data in (before, after)]
    assert [i for i, (a, b) in enumerate(zip(*archives, strict=True)) if a != b] == [build.BLOCK]
    clean_block = build.panels.IlnkContainer.parse(original.read_file(STORY)).blocks[build.BLOCK]
    previous_block, block = (archive[build.BLOCK] for archive in archives)
    assert stage.sha256(block).hexdigest() == stored["target_block_sha256"]
    new.replace_file(STORY, before[STORY])
    assert bytes(new.rom.save()) == Path(previous["candidate"]).read_bytes()

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "one_Hodram_dialogue_command_and_startup_arm9_unchanged",
    })
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, after[ARM])

    edit, proposal = stored["edit"], packet["open_revision"]
    records = []
    for row in packet["recruiting"]:
        src, ref = row["source_reference"], row["installed_reference"]
        assert src["block_sha256"] == stage.sha256(clean_block).hexdigest()
        prior = build.panels.exact_command(previous_block, ref)
        at = ref["command_offset"]
        changed = row["id"] == RESPONSE
        data = bytes.fromhex(edit["after_hex"]) if changed else prior
        assert block[at:at + len(data)] == data and len(data) == len(prior)
        if changed:
            assert edit["source_reference"]["exact_body_hex"] == src["exact_body_hex"]
            assert prior.hex() == edit["before_hex"] and at == edit["command_offset"]
            assert data[:6] == prior[:6] and edit["allocation_and_termination_preserved"]
            assert edit["page_sha256"] == live["complete_page_sha256"]
            assert " ".join(build.panels.bytes_for(data).decode("ascii").split()) == proposal["english"]
        records.append(row | dict(previous_English=row["english"], english=proposal["english"] if changed else row["english"],
            localization_note=proposal["rationale"] if changed else row["localization_note"],
            current_reference=ref, decision="revision" if changed else "retention",
            registered_reference=ref | dict(exact_command_hex=data.hex(), candidate_sha256=candidate,
                exact_stored_hex=data[5:data.index(0, 6)].hex() if changed else ref["exact_stored_hex"],
                archive_sha256=stored["target_SC1_sha256"], block_sha256=stored["target_block_sha256"]),
            installed_paired_gameplay=live["revised"] if changed else None))
    assert len(records) == 7 and sum(r["decision"] == "revision" for r in records) == 1
    previous_review = stage.read(parent.REVIEW)
    shared = previous_review["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    common = acceptance.common_rows(after[COMMON], after[ARM])
    assert all(build.panels.text_reference(common[r["message_ID"]]) == r["installed"] for r in shared["records"])
    outcome = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate,
        target_SC1_sha256=stored["target_SC1_sha256"], source_review=stage.reference(build.review.OUT),
        visual_review=visuals, stored_proof=stage.reference(build.STORED), gameplay=stage.reference(played.PAIRED),
        shared_consumer_binding=shared | {"candidate_sha256": candidate},
        retained_four_route_census_sha256=previous_review["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=previous_review["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_rafael_prepare_alone_predecessor=predecessor, athens_item_rumor_release=str(REVIEW)":
        "verified_athens_item_rumor_predecessor=predecessor, stockholm_recruiting_release=str(REVIEW)",
    "len(batches) == 1118 and len(checks) == 453": "len(batches) == 1119 and len(checks) == 454",
    "COMMON in paths and COMMON in records": "STORY in paths and STORY in records",
    "records[COMMON]": "records[STORY]",
    'assert revised == [f"COMMON_MESSAGE_{KEY}"]': "assert revised == [RESPONSE]",
    "snapshot_scope=COMMON": "snapshot_scope=STORY",
    "athens_item_rumor_release_proof": "stockholm_recruiting_release_proof",
    '"athens_item_rumor_pipeline"': '"stockholm_recruiting_pipeline"',
    "build.PAIRED, PREVIEW": "played.PAIRED, PREVIEW",
    "registered_manifest_entries=1119, passing_release_checks=454": "registered_manifest_entries=1120, passing_release_checks=455",
    "changed_internal_files=[COMMON]": "changed_internal_files=[STORY]",
    'target_COMMON_sha256=outcome["target_COMMON_sha256"]': 'target_SC1_sha256=outcome["target_SC1_sha256"]',
    "contextual_records_revisited=15, contextual_decisions_reused=14, previously_localized_records=15":
        "contextual_records_revisited=7, contextual_decisions_reused=6, previously_localized_records=7",
    "justified_retentions=14": "justified_retentions=6",
    "ordinary_Athens_Tavern=True, revised_gameplay_holds=1, native_item_name_layouts=218":
        "ordinary_Stockholm_Tavern=True, revised_gameplay_holds=1, native_pages=1",
    "texts_retained=14": "texts_retained=6",
    '"athens_item_rumor_20261124"': '"stockholm_recruiting_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Stockholm recruiting candidate

Gerhard's advice fits on three readable rows and preserves the source's emphasis on recruiting quickly. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Athens item rumor candidate": "Preserve the registered Stockholm recruiting candidate",
    "1,119 entries and 454 passing checks": "1,120 entries and 455 passing checks",
    doc: '''    DOC.write_text(f"""# Gerhard's Stockholm recruiting advice

Ordinary play from a Riga save verified the sailing estimate, Gerhard's named docking prompt, arrival in Stockholm, and both recruiting choices. The original docking getter returned Stockholm's slot 7 in the read-only arrival snapshot. The five observed port notices and six other parts of the recruiting exchange retain their wording for the reasons recorded in the review. [Ordinary play and exact holdings](../{build.review.OUT.as_posix()})

Gerhard's advice now keeps “will come over” together and makes the original point about recruiting quickly. The revised dialogue occupies three rows. The native page and his nameplate match the ordinary replay. Eight other game frames match pixel for pixel, including the choice, the boarding lesson and return to the Tavern menu. [Exact Japanese and installed records](../{REVIEW.as_posix()}) · [Paired replay](../{VERIFY.as_posix()}/{SHEET.name})

The cumulative build passed 455 release checks, startup and 17 focused tests. Its clean-input patch reconstructs the ROM byte for byte. The wider archived COMMON ownership and unrelated Fleet Info writer paths remain open. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::stockholm-recruiting-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
