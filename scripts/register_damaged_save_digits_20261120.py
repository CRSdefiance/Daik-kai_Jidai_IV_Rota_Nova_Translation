"""Register the confirmed Continue checksum-warning font correction."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.damaged_save_release import ENGLISH
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_damaged_save_digits_20261120 as game
from scripts import register_amsterdam_tavern_editorial_20261120 as boot
from scripts import register_market_bargaining_20261120 as parent
from scripts import stage_damaged_save_digits_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch = stage.base, stage.batch
PROFILE = "all-routes-damaged-save-digits-v1-20261120"
ROOT = Path("out/damaged_save_digits_registered_20261120_v1")
ROM = ROOT / "Translation_DS_Damaged_Save_Digits_20261120_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261120_damaged_save_digits_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_damaged_save_digits_registered_20261120.md")
STARTUP, QA = (stage.ROOT / name for name in ("own_startup_verification.json", "qa.xml"))
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
WORKLIST = parent.PENDING.with_name("shared_display_worklist_20261120_v1.json")
CHECKPOINT = "Registered regular-width slot numbers in the Continue checksum warning."


def verify(registry, previous, viewed):
    stored, result = map(base.load, (stage.PROOF, game.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == result["candidate_sha256"]
    assert base.digest(parent.ROM) == previous["candidate_sha256"] == stored["parent_sha256"] == result["parent_sha256"]
    assert base.digest(stage.CLEAN) == previous["clean_input_sha256"] == stored["clean_input_sha256"]
    assert stored["whole_parent_inverse"] and stored["clean_input_patch_byte_exact"]
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    assert base.digest(stage.ROOT / "translation.xdelta") == stored["clean_input_patch_sha256"]
    assert viewed == result["sheets"] == {str(p): base.digest(p) for p in (game.NATIVE_SHEET, game.GAMEPLAY_SHEET)}
    assert all(base.digest(p) == sha for p, sha in (viewed | result["evidence"]).items())
    assert [row["frame"] for row in result["emulator_holds"]] == list(game.HOLD)
    assert result["one_checksum_bit_changed_in_copied_save"] and result["original_return_frames"] == [4200, 4400, 4700, 5100]
    cases, raster = result["preparations"], result["modal_raster_cases"]
    assert [r["display_number"] for r in cases] == list(range(1, 257))
    assert all(r["original_buffer_guards"] and r["bytes_including_nul"] <= 60 for r in cases)
    assert [r["display_number"] for r in raster] == list(game.RASTER_SAMPLES)
    assert all(r["complete_glyphs_bounds_and_words"] and r["one_page"] for r in raster)
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [32, 0, 0, 2]

    clean, prior, target = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(batch.files, (prior, target))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.ARM}
    arm, common = after[stage.ARM], after[stage.COMMON]
    rebuilt, call = stage.patch(before[stage.ARM], clean.read_file(stage.ARM))
    assert rebuilt == arm and call == stored["changed_call"] and batch.digest(arm) == stored["target_ARM9_sha256"]
    assert batch.digest(common) == stored["target_COMMON_sha256"] == previous["target_COMMON_sha256"]
    target.replace_file(stage.ARM, before[stage.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()

    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(batch.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    original_table = batch.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET])
    table = batch.owned_entries(common, arm, original_table)
    pending = base.load(WORKLIST)
    assert pending["candidate_sha256"] == previous["candidate_sha256"] and len(pending["records"]) == 276
    for row in pending["records"]:
        entry = table[row["message_ID"]]
        assert batch.reference(entry) == row["current_reference"] and entry.text.hex() == row["current_hex"]

    startup_proof = FunctionType(boot.startup_proof.__code__, boot.startup_proof.__globals__ |
                                 {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE})
    startup_proof(previous, candidate, arm)
    row = dict(id="DK4_DAMAGED_SAVE_SLOT_DIGITS", file_path=stage.ARM, speaker="Load error dialog",
        decision="revision", english="{slot}" + ENGLISH,
        japanese=bytes.fromhex(call["source_suffix_hex"]).split(b"\0", 1)[0].decode("cp932"),
        source_reference=dict(caller=0x020EE090, message_copy=0x020EE67C,
            number_call=stage.CALL, suffix_offset=stage.OFFSET, suffix_capacity=stage.CAPACITY),
        current_reference=call | {"candidate_sha256": candidate, "prepared_message_capacity": 60},
        context="Continue rejects the selected save after a checksum mismatch and displays its one-based slot number.",
        source_meaning="The save data in the numbered slot is corrupted and could not be loaded.",
        localization_note="Keep the established warning because it states both the problem and the outcome in direct English. Use the registered regular-width digits for the runtime slot number. Both lines stay complete in the original window.",
        review=dict.fromkeys(batch.GATES, True))
    draft = result | dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=batch.GATES, records=[row],
        checked_story_format_guard=controls, shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"],
        shared_worklist=dict(path=str(WORKLIST), sha256=base.digest(WORKLIST), unchanged_pending_records=276),
        common_117_pending=True, new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {stage.ARM: batch.digest(arm)}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 944 and len(manifest["checks"]) == 279':
        'len(manifest["batches"]) == 945 and len(manifest["checks"]) == 280',
    "stage.STORED": "stage.PROOF",
    "release_stack_before_market_bargaining.json": "release_stack_before_damaged_save_digits.json",
    "release_stack_with_market_bargaining.json": "release_stack_with_damaged_save_digits.json",
    "verified_market_english_region_predecessor=predecessor, market_bargaining_release=str(REVIEW)":
        "verified_market_bargaining_predecessor=predecessor, damaged_save_digits_release=str(REVIEW)",
    "registered_market_bargaining_and_complete_parent_inverse": "registered_damaged_save_digits_and_complete_parent_inverse",
    'manifest["market_bargaining_pipeline"]': 'manifest["damaged_save_digits_pipeline"]',
    '    ids = manifest["changed_records"][stage.COMMON]': '    ids = manifest["changed_records"][stage.ARM]',
    '    assert all((stage.COMMON, key) in credited for key in new_ids)\n    ids.extend(key for key in new_ids if key not in ids)':
        '    assert all(key not in ids for key in new_ids)\n    ids.extend(new_ids)',
    'owned_COMMON_allocations=stored["allocations"], target_COMMON_sha256=archives[stage.COMMON]':
        'owned_number_call=stored["changed_call"], target_ARM9_sha256=archives[stage.ARM]',
    "changed_components=1, target_COMMON_sha256=archives[stage.COMMON]":
        "changed_components=1, target_ARM9_sha256=archives[stage.ARM]",
    'ARM9_sha256=previous["target_ARM9_sha256"], MESFILE_sha256=archives[stage.COMMON]':
        'ARM9_sha256=archives[stage.ARM], MESFILE_sha256=previous["target_COMMON_sha256"]',
    "reviewed_UI_labels=0, previously_localized_records=19, new_contextual_records=0, prose_revisions=2, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=17":
        "reviewed_UI_labels=0, previously_localized_records=1, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1",
    "text_display_revisions=0, pagination_fixes=0": "text_display_revisions=1, pagination_fixes=0",
    "ordinary_Lisbon_trade_no_and_yes=True, alternate_bargaining_voice_offline_only=True,\n                                       natural_activation=True":
        "Continue_checksum_warning_scripted_inputs=True, copied_save_checksum_fixture=True,\n                                       ordinary_live_menu_transitions=True, retail_hardware_tested=False",
    '    pending["physical_reference_index_updates"] = str(REVIEW)':
        '    pending["latest_unchanged_record_binding"] = str(REVIEW)',
    'ledger["market_bargaining_20261120"]': 'ledger["damaged_save_digits_20261120"]',
    "prior_records_reviewed=19, actual_paired_states=2, new_contextual_credit=0,\n        prose_revisions=2, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=17":
        "prior_records_reviewed=1, actual_paired_states=2, new_contextual_credit=0,\n        prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1, text_display_revisions=1",
    "Preserve the Market Bargaining ROM or reconstruction": "Preserve the Continue checksum-warning ROM or reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Continue checksum warning candidate

The [local ROM](../../{ROM.as_posix()}) uses the regular English font for the slot number in the damaged-save warning.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Continue checksum warning

The slot number now uses the regular English font in **“1: This save is corrupted and could not be loaded.”** The established wording conveys both the corruption and the failed load in plain English. The original checksum branch still selects the warning, and the original two-line layout remains intact. [Exact source and current decisions](../{REVIEW.as_posix()})

Paired cold-boot emulator runs used the same copy of a battery save with a single checksum-breaking bit flipped. The complete warning and the return to the save selection and title matched the expected screens. Offline tests executed 256 representable input bytes through native message preparation and independently verified all glyphs and bounds in 13 representative native renders. Hardware was outside this pass. [Emulator comparison](../{(VERIFY / game.GAMEPLAY_SHEET.name).as_posix()}) · [Native pages](../{(VERIFY / game.NATIVE_SHEET.name).as_posix()})

Six startup frames, 24 protected getters and 30 focused tests passed. Two optional historical tests skipped. The clean-input patch recreates the cumulative candidate byte for byte. The separate stored COMMON 117 entry remains in the 276-key display-owner worklist. Dialogue credit remains 27,700. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + "::register", "exec"), env)


if __name__ == "__main__":
    env["main"]()
