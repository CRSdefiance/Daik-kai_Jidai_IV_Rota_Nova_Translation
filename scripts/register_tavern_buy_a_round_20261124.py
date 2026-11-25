"""Register the source-reviewed Tavern command and Help repairs after gameplay."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import check_tavern_buy_a_round_20261124 as played
from scripts import reconcile_elegy_acceptance_20261123 as acceptance
from scripts import register_cartridge_title_20261123 as template
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_tavern_buy_a_round_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


parent = build.parent
PROFILE = "all-routes-tavern-buy-a-round-v1-20261124"
CHECK = "registered_tavern_round_caption_help_widgets_and_complete_parent_inverse"
ARM, COMMON, HELP = build.ARM, build.COMMON, build.HELP
WORK, ROM = build.ROOT, build.ROM
PATCH, PATCH_PROOF, REBUILT, STARTUP_CAPTURE = build.PATCH, build.PATCH_PROOF, build.REBUILT, build.STARTUP_CAPTURE
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_tavern_buy_a_round_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_tavern_buy_a_round.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA = WORK / "own_startup_verification.json", WORK / "qa_passed.xml"
DOC = Path("docs/editorial_tavern_buy_a_round_registered_20261124.md")
CHECKPOINT = "Registered Buy a Round in the Tavern menu and its linked Help pages."
SHEET, PREVIEW = played.MENU_SHEET, build.PREVIEW
HELP_SHEET = played.HELP_PROOF.with_name("readable_actual_sheet_1.png")
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.STORED)))


def verify(previous, visual_sha):
    stored, tavern, help_live, patch, plan = map(stage.read, (build.STORED, played.TAVERN_PROOF, played.HELP_PROOF, PATCH_PROOF, build.PLAN))
    candidate = stage.digest(ROM)
    assert candidate == stored["candidate"]["sha256"] == tavern["candidate_sha256"] == help_live["research_ROM_sha256"] == stage.digest(REBUILT)
    assert patch["byte_exact"] and patch["candidate"]["sha256"] == candidate and stage.reference(PATCH) == patch["patch"]
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == stored["clean"]["sha256"] == stage.digest(stage.CLEAN)
    assert previous["candidate_sha256"] == stored["previous"]["sha256"] and stored["exact_complete_parent_inverse"]
    assert stored["help_plan"] == stage.reference(build.PLAN)
    assert tavern["ordinary_battery_save"] and tavern["observed_purchase_announcement_and_rumor"] and tavern["ordinary_town_return"]
    assert tavern["funds_before"] - tavern["funds_after"] == tavern["price"] == 236 and len(tavern["stable_frames"]) == 9
    assert [r["text"] for r in tavern["complete_menu_captions"]] == ["Order Drink", build.LABEL, "Recruit Crew"]
    assert help_live["actual_ordinary_controls_no_state_injection"] and help_live["all_selected_complete_actual_pages_andnative_child_targets_pass"]
    assert [r["topic_id"] for r in help_live["actual_HELP_cases"]] == sorted(build.ARTICLES)
    assert len(help_live["original_forward_back_andL_R_history_returns"]) == 3 and not help_live["offline_only_pages"]
    visuals = [stage.reference(p) for p in (SHEET, PREVIEW, HELP_SHEET)]
    assert visuals[:2] == [tavern["sheet"], stored["visual"]]
    assert visuals[2]["sha256"] == help_live["readable_actual_sheets"][0]["sha256"]
    assert stage.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    old, target = map(stage.NdsImage.open, (previous["candidate"], ROM))
    before, after = map(parent.build.native.files, (old, target))
    assert before.keys() == after.keys() and {p for p in after if after[p] != before[p]} == {ARM, HELP}
    arm, help_data = after[ARM], after[HELP]
    assert stage.sha256(arm).hexdigest() == stored["target_ARM9_sha256"]
    assert stage.sha256(help_data).hexdigest() == stored["target_HELP_sha256"] == plan["target_HELP_sha256"]
    assert stage.sha256(after[COMMON]).hexdigest() == previous["target_COMMON_sha256"]
    slot = stored["changed_ARM9_slot"]
    at, size = slot["offset"], slot["length"]
    assert at == build.SLOT and size == 16 and arm[at:at + size].hex() == slot["target_hex"]
    assert arm[:at] + bytes.fromhex(slot["prior_hex"]) + arm[at + size:] == before[ARM]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    old_blocks, new_blocks = (build.IlnkContainer.parse(data).blocks for data in (before[HELP], help_data))
    assert [i for i, (a, b) in enumerate(zip(old_blocks, new_blocks, strict=True)) if a != b] == sorted(build.ARTICLES)
    target.replace_file(ARM, before[ARM])
    target.replace_file(HELP, before[HELP])
    assert bytes(target.rom.save()) == Path(previous["candidate"]).read_bytes()

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "tavern_label_slot_and_help_only_startup_equivalent",
    })
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)

    records = stored["records"]
    for row in records:
        if row["file_path"] == HELP:
            topic = row["topic_id"]
            assert row["registered_reference"]["exact_block_hex"] == new_blocks[topic].hex()
            assert row["original_link_IDs"] == [r["topic_id"] for r in build.source_links(new_blocks[topic])]
        else:
            assert row["registered_reference"] == build.source_ref(arm, row["registered_reference"]["pointer_field"] - build.BASE)
    assert len(records) == 10 and sum(r["decision"] == "revision" for r in records) == 4
    previous_review = stage.read(parent.REVIEW)
    shared = previous_review["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    common = acceptance.common_rows(after[COMMON], arm)
    assert all(played.panels.text_reference(common[r["message_ID"]]) == r["installed"] for r in shared["records"])
    outcome = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate,
        target_ARM9_sha256=stored["target_ARM9_sha256"], target_HELP_sha256=stored["target_HELP_sha256"],
        visual_review=visuals, stored_proof=stage.reference(build.STORED), tavern_gameplay=stage.reference(played.TAVERN_PROOF),
        help_gameplay=stage.reference(played.HELP_PROOF), shared_consumer_binding=shared | {"candidate_sha256": candidate},
        retained_four_route_census_sha256=previous_review["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=previous_review["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_athens_item_rumor_predecessor=predecessor, stockholm_recruiting_release=str(REVIEW)":
        "verified_stockholm_recruiting_predecessor=predecessor, tavern_buy_a_round_release=str(REVIEW)",
    "len(batches) == 1119 and len(checks) == 454": "len(batches) == 1120 and len(checks) == 455",
    "STORY in paths and STORY in records": "set((ARM, HELP)) <= set(paths) and set((ARM, HELP)) <= set(records)",
    'assert revised == [RESPONSE]': 'assert revised == ["TAVERN_MENU_BUY_A_ROUND", "HELP_TOPIC_12", "HELP_TOPIC_14", "HELP_TOPIC_15"]',
    "records[STORY].extend(ident for ident in revised if ident not in records[STORY])":
        '''for row in outcome["records"]:
            if row["id"] in revised and row["id"] not in records[row["file_path"]]:
                records[row["file_path"]].append(row["id"])''',
    "snapshot_scope=STORY": "snapshot_scope=[ARM, HELP]",
    "stockholm_recruiting_release_proof": "tavern_buy_a_round_release_proof",
    '"stockholm_recruiting_pipeline"': '"tavern_buy_a_round_pipeline"',
    "played.PAIRED, PREVIEW": "played.TAVERN_PROOF, played.HELP_PROOF, PREVIEW, HELP_SHEET",
    "registered_manifest_entries=1120, passing_release_checks=455, changed_components=1, changed_internal_files=[STORY]":
        "registered_manifest_entries=1121, passing_release_checks=456, changed_components=2, changed_internal_files=[ARM, HELP]",
    'target_SC1_sha256=outcome["target_SC1_sha256"]':
        'target_ARM9_sha256=outcome["target_ARM9_sha256"], target_HELP_sha256=outcome["target_HELP_sha256"]',
    "reviewed_UI_labels=0, contextual_records_revisited=7, contextual_decisions_reused=6, previously_localized_records=7":
        "reviewed_UI_labels=4, contextual_records_revisited=10, contextual_decisions_reused=6, previously_localized_records=10",
    "prose_revisions=1, justified_retentions=6, text_display_revisions=1, wrap_only_revisions=0":
        "prose_revisions=3, justified_retentions=6, text_display_revisions=4, wrap_only_revisions=1",
    "ordinary_Stockholm_Tavern=True, revised_gameplay_holds=1, native_pages=1":
        "ordinary_Copenhagen_Tavern=True, revised_gameplay_holds=4, native_help_pages=3, ordinary_help_history_returns=3",
    "prose_revisions=1, wrap_only_revisions=0, texts_retained=6": "prose_revisions=3, wrap_only_revisions=1, texts_retained=6",
    '"stockholm_recruiting_20261124"': '"tavern_buy_a_round_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Buy a Round testing candidate

The Tavern name matches the Help links and explains what the player pays for. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Stockholm recruiting candidate": "Preserve the registered Tavern Buy a Round candidate",
    "1,120 entries and 455 passing checks": "1,121 entries and 456 passing checks",
    doc: '''    DOC.write_text(f"""# Buy a Round in the Tavern

**Buy a Round** matches the Japanese command for paying for drinks for the room. The Tavern index and article use the same wording. Recruit Crew Help keeps “Buy a round first” together. The other three menu actions and three related Help articles retain their wording. [Exact source, previous and installed records](../{REVIEW.as_posix()})

Ordinary Copenhagen play showed the complete caption and highlight, the original 236-gold quote and deduction, the announcement, the gossip and return to town. Nine surrounding holds match the earlier replay pixel for pixel. All three revised Help pages passed native bounds and glyph checks, and an ordinary replay followed the original links through Assign Sailors and back. [Tavern replay](../{VERIFY.as_posix()}/{SHEET.name}) · [Help replay](../{VERIFY.as_posix()}/{HELP_SHEET.name})

The cumulative build passed startup, 456 release checks and 17 focused tests. The patch reconstructs the candidate byte for byte from the clean ROM. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::tavern-round-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
