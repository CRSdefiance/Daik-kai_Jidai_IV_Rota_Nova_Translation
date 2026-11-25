"""Register the two source-bound Hodram elegy revisions and clean-input patch."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import replay_hodram_B16_elegy_20261123 as playback
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_hodram_B16_elegy_20261123 as build
from scripts.source_locked_derivation_v5118 import checked_text


template, parent = build.registration, build.parent
PROFILE = "all-routes-hodram-elegy-v1-20261123"
CHECK = "registered_hodram_elegy_source_controls_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_hodram_elegy_candidate")
VERIFY = PACKAGE / "verification"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
MANIFEST = build.ROM.with_suffix(".manifest.json")
PLAN = VERIFY / "registration_mutation_plan.json"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
PATCH, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_hodram_elegy.json.gz", build.ROOT / "ledger_after.json.gz"
DOC = Path("docs/editorial_hodram_elegy_registered_20261123.md")
CHECKPOINT = "Registered clearer first-stanza wording and consistent refrain wrapping in Manuel's elegy."
stage = SimpleNamespace(**(vars(files) | dict(ROM=build.ROM, PARENT_RELEASE=parent.RELEASE,
    SHEET=playback.SHEET, PROOF=build.STORED)))
STORY = build.STORY
CHANGES = ["DK4_MES_B16_R0032", "DK4_MES_B16_R0039"]


def verify(previous, visual_sha):
    stored, rebuilt, observed = map(stage.read, (build.STORED, PATCH_PROOF, playback.PLAY))
    target = stored["staged"]["sha256"]
    assert target == stage.digest(stage.ROM) == rebuilt["candidate"]["sha256"] == stage.digest(build.REBUILT)
    assert rebuilt["byte_exact"] and stage.reference(PATCH) == rebuilt["patch"]
    assert stage.digest(stage.CLEAN) == previous["clean_input_sha256"] == stored["clean"]["sha256"]
    assert stage.digest(previous["candidate"]) == previous["candidate_sha256"] == stored["predecessor"]["sha256"]
    assert observed["candidate_sha256"] == target and observed["predecessor_sha256"] == previous["candidate_sha256"]
    assert stored["whole_parent_inverse"] and stored["owned_ids"] == CHANGES
    assert [row["id"] for row in observed["changed_pages"]] == CHANGES
    assert observed["one_page_per_command"] and observed["all_14_story_pages_checked"]
    assert observed["unchanged_victory_and_return"] and len(observed["unchanged_story_frames"]) == 12
    visual = dict(offline=stage.reference(build.editorial.SHEET), gameplay=stage.reference(stage.SHEET))
    assert visual["gameplay"] == observed["visual"]
    assert visual["offline"] == stage.read(build.editorial.OUT)["preview"]
    assert stage.sha256("".join(row["sha256"] for row in visual.values()).encode("ascii")).hexdigest() == visual_sha
    old, candidate = map(stage.NdsImage.open, (previous["candidate"], stage.ROM))
    before, after = map(build.native.files, (old, candidate))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {STORY}
    assert stage.sha256(after[STORY]).hexdigest() == stored["target_SC1_sha256"]
    arm = after[build.ARM]
    assert stage.sha256(arm).hexdigest() == previous["target_ARM9_sha256"] == stored["target_ARM9_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    assert stage.sha256(after["/COMMON/MESFILE.DK4"]).hexdigest() == previous["target_COMMON_sha256"]
    for route in (0, 2, 3):
        assert stage.sha256(after[f"/data/SC{route}.DK4"]).hexdigest() == previous[f"target_SC{route}_sha256"]
    block = build.native.IlnkContainer.parse(after[STORY]).blocks[16]
    assert stage.sha256(block).hexdigest() == stored["block_sha256"]
    records = {row["id"]: row for row in stored["records"]}
    relevant = {row["id"]: row for row in observed["changed_pages"]}
    for command in stored["commands"]:
        start, raw = command["stored_offset"], bytes.fromhex(command["stored"])
        assert block[start:start+len(raw)] == raw
        if command["record_ids"]:
            key, = command["record_ids"]
            row = records[key]
            end = raw.index(0, 6)
            row["registered_reference"] = dict(candidate_sha256=target, archive_sha256=stored["target_SC1_sha256"],
                block=16, block_sha256=stored["block_sha256"], file_path=STORY,
                command_offset=start, offset=start+5, exact_command_hex=raw.hex(), exact_stored_hex=raw[5:end].hex())
            if key in relevant:
                assert raw[6:end].hex() == relevant[key]["formatted_hex"]
                row["observed_formatting"] = relevant[key]
            else:
                assert raw.hex() == command["current"] and row["decision"] == "retention"
    assert all(row["registered_reference"]["candidate_sha256"] == target for row in records.values())
    candidate.replace_file(STORY, before[STORY])
    assert bytes(candidate.rom.save()) == Path(previous["candidate"]).read_bytes()

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(f, "0")) for f in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    context = template.previous.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(template.previous.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "hodram_elegy_startup_and_ARM9_match_parent",
    })
    exec(compile(source, __file__ + "::startup", "exec"), context)
    context["startup_proof"](previous, target, arm)
    inherited = stage.read(parent.REVIEW)
    shared = inherited["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    report = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(next(iter(records.values()))["review"]), records=list(records.values()),
        candidate_sha256=target, target_SC1_sha256=stored["target_SC1_sha256"], source_credit_added=0,
        changed_ids=CHANGES, stored_proof=stage.reference(build.STORED), visual_review=visual,
        gameplay=stage.reference(playback.PLAY), localized_story_delta=dict(file=STORY, block=16, commands=CHANGES),
        shared_consumer_binding=shared | dict(candidate_sha256=target),
        retained_four_route_census_sha256=inherited["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=inherited["retained_editorial_coverage_sha256"],
        full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(report)
    return report


prep, seal = getsource(template.prepare), getsource(template.finish)
begin_readme = prep[prep.index('    (PACKAGE / "README.md")'):prep.index('    stage.write(PACKAGE / "checksums.json"')]
begin_doc = seal[seal.index("    DOC.write_text"):seal.index("    prefix =")]
prepare = checked_text(prep, {
    "with mapped(base.REGISTRY) as data:": "with mapped(REGISTRY_BEFORE) as data:",
    "with mapped(base.LEDGER) as data:": "with mapped(LEDGER_BEFORE) as data:",
    "verified_azores_wording_predecessor=predecessor, cartridge_title_release=str(REVIEW)":
        "verified_assigned_fleet_info_predecessor=predecessor, hodram_elegy_release=str(REVIEW)",
    "len(batches) == 1102 and len(checks) == 437": "len(batches) == 1106 and len(checks) == 441",
    'assert stage.BANNER not in paths and stage.BANNER not in records and CHECK not in checks':
        'assert STORY in paths and STORY in records and CHECK not in checks',
    'records[stage.BANNER] = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]':
        'revised = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]',
    'assert len(records[stage.BANNER]) == 5': 'assert revised == CHANGES and all(key in records[STORY] for key in revised)',
    "changed_paths=sorted([*paths, stage.BANNER])": "changed_paths=paths",
    "Path(stage.__file__)": "Path(build.__file__)",
    "snapshot_scope=stage.BANNER": "snapshot_scope=STORY, revised_records=CHANGES",
    "banner_release_proof": "elegy_release_proof",
    "cartridge_title_pipeline": "hodram_elegy_pipeline",
    "stage.SHEET, stage.PROOF": "stage.SHEET, stage.PROOF, playback.PLAY, build.editorial.OUT, build.editorial.SHEET",
    "registered_manifest_entries=1103, passing_release_checks=438, changed_components=1, changed_internal_files=[stage.BANNER]":
        'registered_manifest_entries=1107, passing_release_checks=442, changed_components=1, changed_internal_files=[STORY],\n'
        '        target_SC1_sha256=outcome["target_SC1_sha256"]',
    "reviewed_UI_labels=5, contextual_records_revisited=0, contextual_decisions_reused=0, previously_localized_records=0":
        "reviewed_UI_labels=0, contextual_records_revisited=14, contextual_decisions_reused=12, previously_localized_records=14",
    "new_contextual_records=0, prose_revisions=0, justified_retentions=1, text_display_revisions=5":
        "new_contextual_records=0, prose_revisions=1, justified_retentions=12, text_display_revisions=2, wrap_only_revisions=1",
    "host_preview_of_all_six_banner_fields=True":
        "focused_monster_fish_outcome=True, paired_story_pages=14, full_unchanged_frames=19",
    "handheld_firmware_display=False, launcher_GUI_display=False": "handheld=False, natural_spawn=False",
    "English_launcher_fields=5, original_Japanese_title_retained=True":
        "story_pages_checked=14, prose_and_wrap=1, wrap_only=1",
    '"cartridge_title_20261123"': '"hodram_elegy_20261123"',
    begin_readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram elegy testing candidate

Manuel's elegy restores the image of the waves bringing a mother's heartbeat to mind and gives the repeated refrain the same placement in each stanza. Apply the [clean-input patch](translation.xdelta) to the verified clean ROM to reconstruct SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(seal, {
    "Preserve the registered cartridge-title candidate": "Preserve the registered Hodram elegy candidate",
    "1,103 entries and 438 passing checks": "1,107 entries and 442 passing checks",
    begin_doc: '''    DOC.write_text(f"""# Hodram's victory scene and Manuel's elegy

The first stanza restores the Japanese image of the repeated waves bringing a distant mother's heartbeat to mind. The final stanza keeps the refrain on its own line and keeps “Both” with its verb. The middle stanza retains Manuel's attribution and the uncertainty about other languages.

The paired cold-boot replay showed both revised pages with complete nameplates, all 12 retained story pages, the original Monster Fish victory notice and the return to Sea View. The encounter used three starting hull points and a one-bit activation fixture after combat brought the fish to zero. The native offline checks and 17 focused tests passed. Six startup frames, 24 name getters and all eight ASCII right-bound spans match. The clean-input patch reconstructs the whole ROM exactly. [Registered editorial review](../{REVIEW.as_posix()}) · [Paired gameplay](../{VERIFY.as_posix()}/elegy_paired_gameplay.png) · [Clean-input patch](../{PACKAGE.as_posix()}/translation.xdelta)

The ledger keeps 27,700 historical credits. Natural encounter spawning and physical hardware remain unobserved.
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    cli = template.ArgumentParser(description=__doc__)
    cli.add_argument("--visual-sha256")
    cli.add_argument("--finish-only", action="store_true")
    args = cli.parse_args()
    assert args.finish_only or args.visual_sha256
    scope = vars(template) | globals()
    exec(compile(prepare + "\n" + finish, __file__ + "::registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
