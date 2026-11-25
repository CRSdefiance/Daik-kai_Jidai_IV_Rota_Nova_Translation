"""Register the four source-reviewed inspection reactions over the cartridge-title ROM."""

from inspect import getsource
from os import link
from types import SimpleNamespace

from scripts import register_cartridge_title_20261123 as template
from scripts import stage_sea_inspection_prose_20261123 as sea
from scripts.check_sea_inspection_release_20261123 import PATCH, PATCH_PROOF, PLAY, REBUILT, SHEET, STARTUP_CAPTURE
from scripts.source_locked_derivation_v5118 import checked_text


PROFILE = "all-routes-sea-inspection-prose-v1-20261123"
CHECK = "registered_sea_inspection_prose_and_complete_parent_inverse"
PACKAGE = template.PACKAGE.with_name("all_routes_editorial_20261123_sea_inspection_prose_candidate")
VERIFY = PACKAGE / "verification"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
ROM = sea.WORK / "Translation_DS_Sea_Inspection_Prose_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PLAN = VERIFY / "registration_mutation_plan.json"
STARTUP = sea.WORK / "own_startup_verification.json"
QA = sea.WORK / "qa_passed.xml"
DOC = template.DOC.with_name("editorial_sea_inspection_prose_registered_20261123.md")
CHECKPOINT = "Registered clearer reactions for four of the eight sea-inspection voices."
REGISTRY_BEFORE, LEDGER_BEFORE = template.REGISTRY_NEXT, template.LEDGER_NEXT
REGISTRY_NEXT = sea.WORK / "release_stack_with_sea_inspection_prose.json.gz"
LEDGER_NEXT = sea.WORK / "ledger_after.json.gz"
VISUAL = sea.WORK / "visual_review.json"
stage = SimpleNamespace(**(vars(sea) | dict(PARENT_RELEASE=sea.live.RELEASE, ROM=ROM, SHEET=SHEET)))


def verify(parent, visual_sha):
    stored, play, patch = map(sea.read, (sea.PROOF, PLAY, PATCH_PROOF))
    candidate = stored["candidate"]["sha256"]
    assert candidate == play["candidate_sha256"] == patch["candidate_sha256"] == sea.digest(sea.ROM)
    assert stored["clean"]["sha256"] == patch["clean_input_sha256"] == parent["clean_input_sha256"] == sea.digest(sea.CLEAN)
    assert stored["predecessor"]["sha256"] == parent["candidate_sha256"] == sea.digest(parent["candidate"])
    assert play["actual_fixture_coverage"] == [2209] and sorted(play["captures"]) == ["fish", "whale"]
    assert patch["byte_exact"] and sea.digest(PATCH) == patch["patch"]["sha256"] and REBUILT.samefile(sea.ROM)
    refs = [play["sheet"], *stored["sheets"], sea.read(sea.PANEL_REPORT)["visual_preview"]]
    assert all(sea.digest(row["path"]) == row["sha256"] for row in refs)
    visual = {row["path"]: row["sha256"] for row in refs}
    assert sea.digest_bytes("".join(visual.values()).encode("ascii")) == visual_sha
    sea.write(VISUAL, visual)
    clean, old, new = map(sea.NdsImage.open, (sea.CLEAN, parent["candidate"], sea.ROM))
    arm = old.read_file(sea.ARM)
    assert sea.digest_bytes(arm) == stored["target_ARM9_sha256"] == parent["target_ARM9_sha256"]
    assert new.read_file(sea.ARM) == arm
    assert template.right_bound(arm, parent["right_bound_configuration"])["matched_repair_spans"] == 8
    common, updated = (image.read_file(sea.COMMON) for image in (old, new))
    assert sea.digest_bytes(updated) == stored["target_COMMON_sha256"]
    assert all(sea.digest_bytes(new.read_file(f"/data/SC{i}.DK4")) == parent[f"target_SC{i}_sha256"] for i in range(4))
    before, after = (sea.common_rows(raw, arm) for raw in (common, updated))
    assert {a.message_id for a, b in zip(before, after, strict=True) if a != b} == set(sea.EDITS)
    japanese = sea.common_message_entries(clean.read_file(sea.COMMON), clean.read_file(sea.ARM))
    for row in stored["records"]:
        n = row["message_ID"]
        assert row["source_hex"] == japanese[n].text.hex()
        assert row["current_hex"] == before[n].text.hex() and row["staged_hex"] == after[n].text.hex()
        row["registered_reference"] = row["staged_reference"] | dict(candidate_sha256=candidate)
    new.replace_file(sea.COMMON, common)
    assert bytes(new.rom.save()) == old.source.read_bytes()
    sea.validate_natural_dialogue_batch(stored)
    historical = sea.read(template.REVIEW)
    shared = historical["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == parent["candidate_sha256"]
    assert all(before[row["message_ID"]] == after[row["message_ID"]] for row in shared["records"])
    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    scope = template.previous.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    startup = checked_text(template.previous.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "sea_reaction_startup_and_ARM9_match_parent",
    })
    exec(compile(startup, __file__ + "::bound-startup", "exec"), scope)
    scope["startup_proof"](parent, candidate, arm)
    if not ROM.exists():
        link(REBUILT, ROM)
    assert ROM.samefile(sea.ROM) and sea.digest(ROM) == candidate
    return stored | dict(candidate_sha256=candidate, actual_revised_ROM_replay_pending=False, observed=play,
        visual_review=visual, sea_target_scope=sea.reference(sea.PANEL_REPORT), retained_five_stock_models=True,
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=historical["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=historical["retained_editorial_coverage_sha256"],
        new_source_credit=0, full_editorial_goal_complete=False)


old_prepare = getsource(template.prepare)
readme = old_prepare[old_prepare.index('    (PACKAGE / "README.md").write_text'):old_prepare.index('    stage.write(PACKAGE / "checksums.json"')]
prepare = checked_text(old_prepare, {
    "verified_azores_wording_predecessor=predecessor, cartridge_title_release=str(REVIEW)":
        "verified_cartridge_title_predecessor=predecessor, sea_inspection_prose_release=str(REVIEW)",
    "1102 and len(checks) == 437": "1103 and len(checks) == 438",
    '    assert stage.BANNER not in paths and stage.BANNER not in records and CHECK not in checks\n'
        '        records[stage.BANNER] = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]\n'
        '        assert len(records[stage.BANNER]) == 5':
        '    assert stage.COMMON in paths and CHECK not in checks\n'
        '        revised = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]\n'
        '        assert len(revised) == 4\n'
        '        records[stage.COMMON] = list(dict.fromkeys([*records[stage.COMMON], *revised]))',
    "changed_paths=sorted([*paths, stage.BANNER])": "changed_paths=paths",
    "edit_driver=stage.reference(Path(stage.__file__))": "edit_driver=stage.reference(Path(sea.__file__))",
    "snapshot_scope=stage.BANNER": "snapshot_scope=stage.COMMON",
    "banner_release_proof=": "stored_prose_proof=",
    '"cartridge_title_pipeline"': '"sea_inspection_prose_pipeline"',
    "PATCH_PROOF, stage.SHEET, stage.PROOF": 'PATCH_PROOF, PLAY, stage.SHEET, stage.PROOF, VISUAL, sea.PANEL_REPORT, sea.SHEET, sea.WORK / "portrait_sheet_01.png"',
    "registered_manifest_entries=1103, passing_release_checks=438, changed_components=1, changed_internal_files=[stage.BANNER]":
        "registered_manifest_entries=1104, passing_release_checks=439, changed_components=1, changed_internal_files=[stage.COMMON],\n"
        '        target_COMMON_sha256=outcome["target_COMMON_sha256"]',
    "reviewed_UI_labels=5, contextual_records_revisited=0, contextual_decisions_reused=0, previously_localized_records=0":
        "reviewed_UI_labels=0, contextual_records_revisited=9, contextual_decisions_reused=9, previously_localized_records=9",
    "new_contextual_records=0, prose_revisions=0, justified_retentions=1, text_display_revisions=5":
        "new_contextual_records=0, prose_revisions=4, justified_retentions=5, text_display_revisions=4",
    "host_preview_of_all_six_banner_fields=True": "focused_emulator_replays=2, offline_original_voice_cases=8",
    "handheld_firmware_display=False, launcher_GUI_display=False": "naturally_spawned_encounter=False, handheld=False",
    'registered_release_verification=str(RELEASE))': 'registered_release_verification=str(RELEASE), MESFILE_sha256=outcome["target_COMMON_sha256"])',
    "English_launcher_fields=5, original_Japanese_title_retained=True, new_contextual_credit=0":
        "revisited_reactions=8, contextual_notice_retained=True, prose_revisions=4, new_contextual_credit=0",
    '"cartridge_title_20261123"': '"sea_inspection_prose_20261123"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Sea-inspection prose testing candidate

This registered build revises four lookout reactions. The [clean-input patch](translation.xdelta) reconstructs the ROM with SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})

old_finish = getsource(template.finish)
checkpoint_doc = old_finish[old_finish.index("    DOC.write_text"):old_finish.index("    prefix =")]
finish = checked_text(old_finish, {
    "Preserve the registered cartridge-title candidate": "Preserve the registered sea-inspection prose candidate",
    "1,103 entries and 438 passing checks": "1,104 entries and 439 passing checks",
    checkpoint_doc: '''    DOC.write_text(f"""# Sea-inspection reactions

Five focused encounter replays verified all five tooltip classes on the cartridge-title ROM. They also showed Charles's reaction splitting “make it home alive.” The new build gives Charles a direct question on one row and revises the next three voice alternatives from the clean Japanese. Four other reactions and the unavailable information notice retain their wording. [Source decisions and evidence](../{REVIEW.as_posix()})

The Monster Fish and White Whale runs verify Charles's new line, his portrait and nameplate, and the original return to Info Mode. Seven voice alternatives have offline original-pipeline checks. Natural spawns and a played special-target victory remain unobserved in this pass. The clean-input patch, six startup comparisons, 24 protected getters and 17 tests passed. [Focused emulator comparison](../{VERIFY.as_posix()}/focused_replay.png) · [Clean-input patch](../{PACKAGE.as_posix()}/translation.xdelta)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    scope = vars(template) | globals()
    exec(compile(prepare + "\n" + finish, __file__ + "::release-transaction", "exec"), scope)
    parser = template.ArgumentParser(description=__doc__)
    parser.add_argument("--visual-sha256")
    parser.add_argument("--finish-only", action="store_true")
    args = parser.parse_args()
    if not args.finish_only:
        assert args.visual_sha256
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
