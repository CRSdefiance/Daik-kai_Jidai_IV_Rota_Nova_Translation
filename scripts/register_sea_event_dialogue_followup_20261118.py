"""Register the verified sea-event dialogue and its byte-exact clean-input patch."""

from pathlib import Path
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_sailing_mode_prose_20261118 as parent
from scripts import stage_sea_event_dialogue_followup_20261118 as stage
from scripts import verify_sea_event_dialogue_followup_20261118 as verified
from scripts.source_locked_derivation_v5118 import checked_text

base, native = parent.base, parent.native
PROFILE = "all-routes-sea-event-dialogue-followup-v1-20261118"
ROOT = Path("out/sea_event_dialogue_followup_registered_20261118_v1")
ROM = ROOT / "Translation_DS_Sea_Event_Dialogue_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_sea_event_dialogue_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_sea_event_dialogue_followup_20261118.md")
STARTUP, QA = verified.STARTUP, stage.ROOT / "supported_qa_replay.xml"
LAYOUT = stage.ROOT / "portrait_sheet_01.png"
CHECKPOINT = "Six shared storm and sea-foam lines are revised, and the five-part sea-foam event has a fresh emulator replay."


def verify(registry, previous, viewed):
    stored, game, boot = map(base.load, (stage.PROOF, verified.GAME, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == game["candidate_sha256"] == boot["candidate_sha256"]
    assert base.digest(parent.ROM) == previous["candidate_sha256"] == stored["parent_sha256"]
    assert base.digest(stage.CLEAN) == previous["clean_input_sha256"] == stored["clean_input_sha256"]
    assert stored["entire_parent_inverse"] and stored["preserved_entries"] == 3662
    assert sorted(map(int, stored["allocations"])) == sorted(stage.REVISIONS)
    assert viewed == {str(p): base.digest(p) for p in (LAYOUT, verified.SHEET)}
    sheet, = stored["sheets"]
    assert sheet["path"] == str(LAYOUT) and sheet["sha256"] == viewed[str(LAYOUT)] and len(sheet["messages"]) == 12
    assert all(base.digest(p) == sha for proof in (game, boot) for p, sha in proof["evidence"].items())
    assert game["actual_emulator"] and not game["hardware"] and game["selector_word_restored"]
    assert [r["message_ID"] for r in game["observed"]] == [457, 463, 469, 470, 478]
    assert game["observed_revised_records"] == [457]
    assert game["offline_only_revised_records"] == sorted(set(stage.REVISIONS) - {457})
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"]) == 6 and len(boot["original_protected_name_getters"]) == 24
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [41, 0, 0, 0]
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    old, new, clean = map(base.NdsImage.open, (parent.ROM, stage.ROM, stage.CLEAN))
    before, after = map(native.files, (old, new))
    assert before.keys() == after.keys()
    assert {p for p in before if before[p] != after[p]} == {stage.COMMON}
    assert native.digest(after[stage.ARM]) == previous["target_ARM9_sha256"] == stored["target_ARM9_sha256"]
    assert native.digest(before[stage.COMMON]) == previous["target_COMMON_sha256"]
    assert native.digest(after[stage.COMMON]) == stored["target_COMMON_sha256"]
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7 and not any(controls["source_bound_new_command_counts"].values())
    new.replace_file(stage.COMMON, before[stage.COMMON])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()

    earlier = stored["earlier_review"]
    assert base.digest(earlier["path"]) == earlier["sha256"]
    source = {r["message_ID"]: r for r in base.load(earlier["path"])["records"]}
    for row in stored["records"]:
        original = source[row["message_ID"]]
        assert row["source_reference"] == original["source_reference"] and row["source_hex"] == original["source_hex"]
        row["source_meaning"] = original["source_meaning"]
        row["registered_reference"] = row["staged_reference"] | dict(candidate_sha256=candidate,
            exact_stored_hex=row["staged_hex"])
        row["review"]["formatting"] = True
    review = {k: stored[k] for k in (
        "candidate_sha256", "parent_sha256", "clean_input_sha256", "translation_policy", "target_locale", "encoder",
        "review_gates", "records")}
    review.update(new_contextual_credit=0, observed_gameplay=game, checked_story_format_guard=controls)
    validate_natural_dialogue_batch(review)
    return stored, review, {stage.COMMON: stored["target_COMMON_sha256"]}


publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
pins = publish[publish.index("    candidates = ["):publish.index("    for path in candidates:")]
main = checked_text(publish, {
    'len(manifest["batches"]) == 886 and len(manifest["checks"]) == 221':
        'len(manifest["batches"]) == 887 and len(manifest["checks"]) == 222',
    '    pending = ledger["pending_shared_consumer_checkpoint_20261114"]':
        '    assert all((r["file_path"], r["id"]) in credited for r in draft["records"])\n'
        '    pending = ledger["pending_shared_consumer_checkpoint_20261114"]',
    "stage.PROOF, STARTUP, QA, replay.LIVE, replay.SHEET, attack.OUTPUT, args.visual_review":
        "stage.PROOF, STARTUP, QA, verified.GAME, verified.SHEET, LAYOUT, args.visual_review",
    "release_stack_before_sailing_mode_prose.json": "release_stack_before_sea_event_dialogue.json",
    "release_stack_with_sailing_mode_prose.json": "release_stack_with_sea_event_dialogue.json",
    "verified_lil_maria_flagged_wraps_predecessor": "verified_sailing_mode_prose_predecessor",
    "sailing_mode_prose_release": "sea_event_dialogue_followup_release",
    "registered_sailing_mode_prose_and_complete_parent_inverse":
        "registered_sea_event_dialogue_followup_and_complete_parent_inverse",
    "sailing_mode_prose_pipeline": "sea_event_dialogue_followup_pipeline",
    'row["decision"] == "revision"': 'row["decision"] != "retention"',
    "native_display_sha256=base.digest(replay.LIVE)": "native_display_sha256=base.digest(verified.GAME)",
    'owned_ARM9_panels=[row["registered_reference"] for row in draft["records"]], target_ARM9_sha256=archives[native.ARM]':
        'allocations=stored["allocations"], target_COMMON_sha256=archives[stage.COMMON]',
    "target_ARM9_sha256=archives[native.ARM],": "target_COMMON_sha256=archives[stage.COMMON],",
    "ARM9_sha256=archives[native.ARM],": "COMMON_sha256=archives[stage.COMMON],",
    "repository_tests=32": "repository_tests=41",
    "text_display_revisions=3": "text_display_revisions=6",
    "initialized_Info_Search_and_Declare_War_panels=True": "initialized_sea_foam_exchange=True",
    "prose_revisions=3, wrap_only_revisions=0, justified_retentions=0":
        "prose_revisions=4, wrap_only_revisions=2, justified_retentions=25",
    "previously_reviewed_panels=3": "previously_reviewed_records=31",
    'checkpoint = "The three sailing guide panels are revised and both Madeira attack-text paths are documented."':
        "checkpoint = CHECKPOINT",
    "sailing_mode_prose_20261118": "sea_event_dialogue_followup_20261118",
    "Preserve sailing guide prose ROM or clean reconstruction": "Preserve sea-event dialogue ROM or clean reconstruction",
    pins: '''    candidates = [ROM, stage.ROM, stage.ROOT / "clean_rebuilt.nds", verified.replay.LIVE / "SeaWrap.nds"]\n''',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Sea-event dialogue test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised storm warnings and lookout dialogue.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Storm warnings and sea-foam dialogue

Reviewed all seven sudden-storm voices and the complete five-part sea-foam exchange from the clean Japanese, including the alternate voices. Two storm warnings again address the admiral, and two others keep their wording with breaks at sentence boundaries. The formal and informal lookout reports preserve separate voices and turn the sighting into a complete second row. The 25 retentions keep the progression from sighting to recognition, uncertainty, explanation and the order to steer clear. [Exact review ledger](../{REVIEW.as_posix()})

All six revised pages passed complete glyph, width and original allocation checks and received visual review. The focused emulator voyage presented the revised formal warning and all four following turns, then returned to sailing. It used a copied save, the established temporary event selection fixture and ordinary controller input. The five other revisions received offline checks. Natural occurrence and hardware remain unverified. [Native pages](../{(VERIFY / LAYOUT.name).as_posix()}) · [Emulator replay](../{(VERIFY / verified.SHEET.name).as_posix()})

The cumulative candidate passes six startup comparisons, 24 protected name getters and 41 focused tests. The patch reconstructs the ROM byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. The 31 records already had credit. The ledger stands at 27,700, with 276 mapped shared keys still open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()

