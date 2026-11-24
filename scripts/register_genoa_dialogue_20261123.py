"""Register the verified Genoa dialogue and the exact clean-input patch."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from scripts import register_cartridge_title_20261123 as template
from scripts import register_price_info_descriptions_20261123 as parent
from scripts import replay_genoa_dialogue_20261123 as played
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_genoa_dialogue_20261123 as build
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_moonlit_violin_20261121 import bytes_for


PROFILE = "all-routes-genoa-dialogue-v1-20261123"
CHECK = "registered_genoa_dialogue_fixed_allocations_and_complete_parent_inverse"
STORY, COMMON, ARM = build.STORY, build.COMMON, build.ARM
WORK, ROM = build.ROOT, build.ROM
PATCH, PATCH_PROOF, REBUILT, STARTUP_CAPTURE = build.PATCH, build.PATCH_PROOF, build.REBUILT, build.STARTUP_CAPTURE
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_genoa_dialogue_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_genoa_dialogue.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA = WORK / "own_startup_verification.json", WORK / "qa_passed.xml"
DOC = Path("docs/editorial_genoa_dialogue_registered_20261123.md")
CHECKPOINT = "Registered two dialogue revisions and one wrap fix from the ordinary Genoa replay."
PREVIEW = build.gameplay.OUT.parent / "genoa_proposed_text_20261123/before_after_1.png"
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=played.SHEET, PROOF=build.STORED)))


def verified_records(packet, stored, bank, live):
    changed = {row["id"]: row for row in stored["changed"]}
    pages = {row["id"]: row for row in live["changed_pages"]}
    assert set(changed) == set(pages) == set(build.IDS)
    candidate, archive = stored["staged"]["sha256"], stored["target_SC1_sha256"]
    previous = stored["predecessor"]["sha256"]
    genoa = packet["ordinary_gameplay"]["genoa"]
    records = []
    for row in genoa["story"]:
        ident, block = row["id"], row["block"]
        before, change = row["installed_reference"], changed.get(ident)
        offset = before["command_offset"]
        command = bytes.fromhex(change["after_hex"] if change else before["exact_command_hex"])
        assert bank.blocks[block][offset:offset + len(command)] == command
        raw = bytes_for(command)
        english = " ".join(raw.decode("ascii").split())
        if change:
            assert row["proposed_English"] == english and pages[ident]["stored_command_hex"] == command.hex()
            assert change["allocation_and_termination_preserved"] and change["native_inputs_preserved"]
            assert change["single_page"] and row["offline_preflight"]["native_plane_sha256"] == pages[ident]["complete_native_mask"]
        else:
            assert row["decision"] == "retention" and row["installed_English"].encode() == raw
        gameplay = None
        if change:
            gameplay = pages[ident] | {"evidence_ROM_sha256": candidate}
        elif row["gameplay_observed"]:
            gameplay = row["display"] | {"evidence_ROM_sha256": previous}
        records.append(dict(id=ident, file_path=STORY, block=block, speaker=row["speaker"], context=row["context"],
            Japanese=row["clean_Japanese"], source_meaning=row["source_gloss"], source_reference=row["source_reference"],
            current_reference=before, english=english, localization_note=row["rationale"],
            decision="revision" if change else "retention",
            change_class="wrap-only" if ident == build.IDS[-1] else "wording" if change else "retention",
            registered_reference=before | dict(candidate_sha256=candidate, archive_sha256=archive,
                block_sha256=stage.sha256(bank.blocks[block]).hexdigest(), exact_command_hex=command.hex(),
                exact_body_hex=raw.hex()), review=row["review"] | {"formatting": True},
            gameplay=gameplay))

    choice_book = {row["id"]: row for row in stage.read(build.gameplay.CHOICES)["records"]}
    for row in genoa["choices"]:
        earlier = choice_book[row["id"]]
        before = row["installed_reference"]
        command = bytes.fromhex(before["exact_command_hex"])
        offset = before["command_offset"]
        assert bank.blocks[170][offset:offset + len(command)] == command
        records.append(dict(id=row["id"], file_path=STORY, block=170, speaker=earlier["speaker"],
            context=earlier["context"], Japanese=row["clean_Japanese"], source_meaning=earlier["source_meaning"],
            localization_note=row["rationale"], source_reference=row["source_reference"], current_reference=before,
            registered_reference=before | dict(candidate_sha256=candidate, archive_sha256=archive,
                block_sha256=stage.sha256(bank.blocks[170]).hexdigest()), english=row["installed_English"],
            decision="retention", change_class="retention", review=row["review"],
            original_gameplay=dict(capture=row["capture"], evidence_ROM_sha256=previous)))
    assert len(records) == 62 and sum(row["decision"] == "revision" for row in records) == 3
    return records


def verify(previous, visual_sha):
    stored, live, patch, packet = map(stage.read, (build.STORED, played.REPORT, PATCH_PROOF, build.gameplay.OUT))
    candidate = stage.digest(ROM)
    assert candidate == stored["staged"]["sha256"] == live["candidate_sha256"] == patch["candidate"]["sha256"] == stage.digest(REBUILT)
    assert patch["byte_exact"] and stage.reference(PATCH) == patch["patch"]
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == stored["clean"]["sha256"] == stage.digest(stage.CLEAN)
    assert previous["candidate_sha256"] == stored["predecessor"]["sha256"] == live["predecessor_sha256"] == packet["candidate_sha256"]
    assert stored["editorial_and_preflight"] == stage.reference(build.gameplay.OUT) and stored["whole_parent_inverse"]
    assert stored["unchanged_archive_directory"] and stored["stored_rendering_matches_reviewed_previews"]
    assert live["ordinary_controller_and_stylus_inputs"] and live["observed_tavern_return"]
    assert len(live["unchanged_control_frames"]) == 16
    assert live["observed_choices"] == ["Yes...", "Ask what you don't know"]
    visuals = [stage.reference(played.SHEET), stage.reference(PREVIEW)]
    assert visuals == [live["visual"], *packet["ordinary_gameplay"]["genoa"]["proposed_native_sheets"]]
    assert stage.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    old, new = map(stage.NdsImage.open, (previous["candidate"], ROM))
    before, after = map(build.native.files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {STORY}
    for path, key in ((ARM, "target_ARM9_sha256"), (COMMON, "target_COMMON_sha256")):
        assert stage.sha256(after[path]).hexdigest() == stored[key] == previous[key]
    assert stage.sha256(after[STORY]).hexdigest() == stored["target_SC1_sha256"]
    assert template.right_bound(after[ARM], previous["right_bound_configuration"])["matched_repair_spans"] == 8
    bank = IlnkContainer.parse(after[STORY])
    records = verified_records(packet, stored, bank, live)
    new.replace_file(STORY, before[STORY])
    assert bytes(new.rom.save()) == Path(previous["candidate"]).read_bytes()

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    code = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "genoa_fixed_allocations_and_startup_arm9_unchanged",
    })
    exec(compile(code, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, after[ARM])

    prior = stage.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    report = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(next(iter(records))["review"]), records=records, candidate_sha256=candidate,
        target_SC1_sha256=stored["target_SC1_sha256"], changed_ids=list(build.IDS),
        source_credit_added=0, stored_proof=stage.reference(build.STORED), visual_review=visuals,
        gameplay=stage.reference(played.REPORT), localized_story_delta=dict(file=STORY, blocks=[170, 181]),
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(report)
    return report


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_recruitment_shortfall_predecessor=predecessor, price_info_descriptions_release=str(REVIEW)":
        "verified_price_info_predecessor=predecessor, genoa_dialogue_release=str(REVIEW)",
    "len(batches) == 1110 and len(checks) == 445": "len(batches) == 1111 and len(checks) == 446",
    'assert COMMON in paths and COMMON in records and CHECK not in checks':
        'assert STORY in paths and STORY in records and CHECK not in checks',
    'if row["decision"] in {"revision", "wrap revision"}': 'if row["decision"] == "revision"',
    'assert all(item in records[COMMON] for item in revised)': 'assert all(item in records[STORY] for item in revised)',
    'assert revised == [f"COMMON_MESSAGE_{key}" for key in REVISED]': 'assert sorted(revised) == list(build.IDS)',
    "snapshot_scope=COMMON, revised_records=revised": "snapshot_scope=STORY, revised_records=revised",
    "price_info_descriptions_release_proof": "genoa_dialogue_release_proof",
    '"price_info_descriptions_pipeline"': '"genoa_dialogue_pipeline"',
    "stage.SHEET, stage.PROOF, played.REPORT, *(Path(row['path']) for row in outcome['visual_review'][1:])":
        'stage.SHEET, stage.PROOF, played.REPORT, PREVIEW',
    'registered_manifest_entries=1111, passing_release_checks=446, changed_components=1, changed_internal_files=[COMMON],\n'
    '        target_COMMON_sha256=outcome["target_COMMON_sha256"]':
        'registered_manifest_entries=1112, passing_release_checks=447, changed_components=1, changed_internal_files=[STORY],\n'
        '        target_SC1_sha256=outcome["target_SC1_sha256"]',
    "contextual_records_revisited=18, contextual_decisions_reused=6, previously_localized_records=18":
        "contextual_records_revisited=62, contextual_decisions_reused=59, previously_localized_records=62",
    "prose_revisions=10, justified_retentions=6, text_display_revisions=12, wrap_only_revisions=2":
        "prose_revisions=2, justified_retentions=59, text_display_revisions=3, wrap_only_revisions=1",
    "ordinary_Lisbon_Price_Info=True": "ordinary_genoa_recruitment_and_trend=True",
    "commodity_descriptions_revised=12, descriptions_retained=6": "genoa_dialogue_revised=3, texts_retained=59",
    '"price_info_descriptions_20261123"': '"genoa_dialogue_20261123"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Genoa dialogue testing candidate

Hodram and Julio's recruitment exchange has two wording revisions. The tomato scene keeps the Owner's interjection and recollection on the same line. Apply the [clean-input patch](translation.xdelta) to reconstruct SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Price Info descriptions candidate": "Preserve the registered Genoa dialogue candidate",
    "1,111 entries and 446 passing checks": "1,112 entries and 447 passing checks",
    doc: '''    DOC.write_text(f"""# Genoa dialogue and the tomato trend

Hodram's answer about knowing the price of liquor now takes two lines. Julio's approval of Hodram's frank approach reads “Straight to the point. I like that.” In the tomato scene, “Ah” stays with the Owner's recollection. Fifty-nine nearby texts and choice labels retain their wording. [Exact Japanese, prior and installed records](../{REVIEW.as_posix()})

Ordinary Genoa gameplay verified all three complete pages and nameplates, both original choices, Julio's join notice and the return to the Tavern. Sixteen control frames match the predecessor pixel for pixel. The original command extents and relative branch bytes carry forward. [Paired gameplay](../{VERIFY.as_posix()}/{played.SHEET.name}) · [Native previews](../{VERIFY.as_posix()}/{PREVIEW.name})

The candidate passed 447 release checks, including the clean-input patch reconstruction, six startup comparisons, 24 protected name getters and eight ASCII right-bound spans. Seventeen focused tests passed. The ledger preserves 27,700 historical credits. The alternate recruitment outcomes remain outside this gameplay sample. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::registered", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
