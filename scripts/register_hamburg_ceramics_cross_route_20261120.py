"""Register the reviewed four-route Hamburg exchange and clean-input patch."""

from collections import Counter
from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_amsterdam_tavern_followup_20261120 as tavern
from scripts import check_hamburg_ceramics_replay_20261120 as game
from scripts import register_amsterdam_tavern_editorial_20261120 as boot
from scripts import stage_hamburg_ceramics_cross_route_20261120 as stage
from scripts import verify_hamburg_ceramics_cross_route_20261120 as offline
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = stage.base, stage.native, stage.parent
PROFILE = "all-routes-hamburg-ceramics-v1-20261120"
ROOT = Path("out/hamburg_ceramics_registered_20261120_v1")
ROM = ROOT / "Translation_DS_Hamburg_Ceramics_20261120_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261120_hamburg_ceramics_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_hamburg_ceramics_registered_20261120.md")
STARTUP, QA = (stage.ROOT / name for name in ("own_startup_verification.json", "qa.xml"))
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
CHECKPOINT = "Registered the Hamburg ceramics exchange across all four story routes."


def visual_files(display, live):
    return {entry["path"]: entry["sha256"] for entry in display["contact_sheets"]} | live["sheet"]


def verify(registry, previous, viewed):
    stored, display, live = map(base.load, (stage.PROOF, offline.PROOF, game.PROOF))
    draft, source = map(base.load, (stage.review.OUTPUT, stage.review.SOURCE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == display["candidate_sha256"] == live["candidate_sha256"]
    assert stored["predecessor_sha256"] == live["parent_sha256"] == base.digest(parent.ROM) == previous["candidate_sha256"]
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"] == stored["clean_sha256"]
    assert base.digest(stage.review.OUTPUT) == stored["manuscript_sha256"]
    assert base.digest(stage.review.SOURCE) == draft["source_packet_sha256"]
    assert base.digest(stage.PROOF) == display["stage_proof_sha256"]
    assert len(viewed) == 8 and viewed == visual_files(display, live)
    assert all(base.digest(p) == sha for p, sha in (viewed | live["evidence"]).items())
    assert stored["whole_parent_inverse"] and (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    assert live["initialized_scene"] and not live["natural_Hamburg_activation"]
    assert len(live["matched"]) == 17 and live["observed_revisions"] == 11
    assert live["exact_early_and_return_frames"] == [2100, 7030, 7270, 7520]
    assert display["displayed_native_plans"] == 54 and display["exact_retentions"] == 14
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [32, 0, 0, 2]

    clean, prior, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    before, after = map(native.files, (prior, target))
    assert before.keys() == after.keys()
    archives = {f"/data/SC{i}.DK4": native.digest(after[f"/data/SC{i}.DK4"]) for i in range(4)}
    assert archives.keys() == {name for name in before if before[name] != after[name]}
    assert native.digest(after[native.ARM]) == previous["target_ARM9_sha256"]
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls == stored["source25"]
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())

    rows = {(r["file_path"], r["id"]): r for r in draft["records"]}
    verified = {(r["file_path"], r["id"]): r for r in display["receipts"]}
    observed = {r["id"] for r in live["matched"]}
    for group, indexed in zip(stored["groups"], source["groups"], strict=True):
        path, n = group["file_path"], group["block"]
        original, previous_bank, new = [native.IlnkContainer.parse(b).blocks for b in
                                       (clean.read_file(path), before[path], after[path])]
        assert native.digest(original[n]) == group["source"] == indexed["source_block_sha256"]
        assert native.digest(previous_bank[n]) == group["before"] == indexed["current_block_sha256"]
        assert native.digest(new[n]) == group["after"]
        assert [i for i, (a, b) in enumerate(zip(previous_bank, new, strict=True)) if a != b] == [n]
        for cmd in group["commands"]:
            offset = cmd["stored_offset"]
            raw = bytes.fromhex(cmd["stored"])
            assert new[n][offset:offset + len(raw)] == raw
            if not cmd["record_ids"]:
                continue
            ident, = cmd["record_ids"]
            row, receipt = rows[path, ident], verified[path, ident]
            body = raw[5:raw.index(0, 6)]
            assert body[0] == row["source_selector"]
            if row["decision"] == "revision":
                assert receipt["target_hex"] == body.hex() and len(receipt["pages"]) == 1
            else:
                assert receipt["kept_complete_command"] == cmd and body.hex() == row["current_hex"]
            row["review"]["formatting"] = True
            row["registered_reference"] = dict(candidate_sha256=candidate, file_path=path, block=n,
                command_offset=offset, offset=offset + 5, exact_stored_hex=body.hex())
            row["initialized_emulator_excerpt_observed"] = group["route"] == 2 and ident in observed
        target.replace_file(path, before[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    assert len(rows) == len(verified) == 68 and rows.keys() == verified.keys()
    assert Counter(r["finding"] for r in rows.values()) == {"prose": 53, "wrap": 1, "retention": 14}
    assert all(r["review"]["formatting"] for r in rows.values())
    validate_natural_dialogue_batch(draft)
    startup_proof = FunctionType(boot.startup_proof.__code__, boot.startup_proof.__globals__ |
                                 {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE})
    startup_proof(previous, candidate, after[native.ARM])
    draft.update(candidate_sha256=candidate, checked_story_format_guard=controls,
        formatting_and_registration_pending=False, shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"],
        new_contextual_credit=0, paired_coverage=live, native_proof_sha256=base.digest(offline.PROOF),
        amsterdam_round_scope=dict(path=str(tavern.OUTPUT), sha256=base.digest(tavern.OUTPUT), separate_pending_price_glyph=True))
    return stored, draft, archives


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 945 and len(manifest["checks"]) == 280':
        'len(manifest["batches"]) == 946 and len(manifest["checks"]) == 281',
    "stage.PROOF, STARTUP, QA, game.PROOF, args.visual_review,":
        "stage.PROOF, STARTUP, QA, offline.PROOF, game.PROOF, args.visual_review,",
    "release_stack_before_damaged_save_digits.json": "release_stack_before_hamburg_ceramics.json",
    "release_stack_with_damaged_save_digits.json": "release_stack_with_hamburg_ceramics.json",
    "verified_market_bargaining_predecessor=predecessor, damaged_save_digits_release=str(REVIEW)":
        "verified_damaged_save_digits_predecessor=predecessor, hamburg_ceramics_release=str(REVIEW)",
    "registered_damaged_save_digits_and_complete_parent_inverse": "registered_hamburg_ceramics_and_complete_parent_inverse",
    'manifest["damaged_save_digits_pipeline"]': 'manifest["hamburg_ceramics_pipeline"]',
    '''    ids = manifest["changed_records"][stage.ARM]
    new_ids = [row['id'] for row in draft['records'] if row['decision'] == 'revision']
    assert all(key not in ids for key in new_ids)
    ids.extend(new_ids)''': '''    for row in draft["records"]:
        key, file = row["id"], row["file_path"]
        assert (file, key) in credited
        ids = manifest["changed_records"][file]
        if row["decision"] == "revision" and key not in ids:
            ids.append(key)''',
    'owned_number_call=stored["changed_call"], target_ARM9_sha256=archives[stage.ARM]':
        'owned_story_blocks=stored["changed_blocks"], target_story_archive_sha256=archives',
    "changed_components=1, target_ARM9_sha256=archives[stage.ARM]": "changed_components=4",
    'ARM9_sha256=archives[stage.ARM], MESFILE_sha256=previous["target_COMMON_sha256"]':
        'ARM9_sha256=previous["target_ARM9_sha256"], MESFILE_sha256=previous["target_COMMON_sha256"]',
    "reviewed_UI_labels=0, previously_localized_records=1, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1":
        "reviewed_UI_labels=0, previously_localized_records=68, new_contextual_records=0, prose_revisions=53, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=14",
    "text_display_revisions=1, pagination_fixes=0": "text_display_revisions=0, pagination_fixes=0",
    "Continue_checksum_warning_scripted_inputs=True, copied_save_checksum_fixture=True,\n                                       ordinary_live_menu_transitions=True, retail_hardware_tested=False":
        "initialized_Lil_Hamburg_scene=True, native_offline_other_three_routes=True,\n                                       natural_Hamburg_activation=False",
    'ledger["damaged_save_digits_20261120"]': 'ledger["hamburg_ceramics_20261120"]',
    "prior_records_reviewed=1, actual_paired_states=2, new_contextual_credit=0,\n        prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1, text_display_revisions=1":
        "prior_records_reviewed=68, actual_paired_states=17, new_contextual_credit=0,\n        prose_revisions=53, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=14",
    '    pending["latest_unchanged_record_binding"] = str(REVIEW)':
        '    ledger["amsterdam_tavern_round_20261120"] = draft["amsterdam_round_scope"]',
    "Preserve the Continue checksum-warning ROM or reconstruction": "Preserve the Hamburg ceramics ROM or reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hamburg ceramics candidate

The [testing ROM](../../{ROM.as_posix()}) includes the complete recurring Hamburg scene across all four routes. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Hamburg ceramics across all four routes

The 17-turn conversation uses the same Japanese on Rafael, Hodram, Lil and Maria’s routes. The review restores consistent use of **ceramics**, keeps the collectors' courtesy and the traders’ change in tone when they approach them, and preserves the tentative forecast. All 68 records have exact source and final references. There are 53 prose revisions, one wrap-only change and 14 justified retentions. [Exact coverage ledger](../{REVIEW.as_posix()})

All 54 revised pages passed native checks and visual review. The paired emulator replay showed all 17 Lil panels, including 11 revisions, with matching screens at the scene boundaries. Six sampled holds differed in the blinking A indicator. The scene was initialized with the original Lil opening prelude. The normal Hamburg trigger and the other routes received offline coverage in this batch. [Emulator comparison](../{(VERIFY / game.SHEET.name).as_posix()})

The ordinary Amsterdam Tavern replay verified both responses to the 268-gold round and the rumor about Clifford’s fleet heading to Bristol. The original price formatter still displays wide digits. The linked receipt identifies the source caller for the next display batch. [Amsterdam coverage](../{tavern.OUTPUT.as_posix()})

Six startup holds, 24 protected getters and 30 focused tests passed. Two optional historical tests skipped. The clean-input patch rebuilds the candidate byte for byte. The dialogue ledger still credits 27,700 records and tracks 276 stored shared keys for display-owner review. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + "::register", "exec"), env)


if __name__ == "__main__":
    env["main"]()
