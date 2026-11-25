"""Register the four save and cartridge dialog revisions on the current release."""

from pathlib import Path
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_mutiny_dialogue_followup_20261119 as parent
from scripts import register_sailing_mode_prose_20261118 as template
from scripts import stage_save_dialogue_followup_20261119 as stage
from scripts import verify_save_dialogue_followup_20261119 as verified
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text

base, native = parent.base, parent.native
PROFILE = "all-routes-save-dialogue-followup-v1-20261119"
ROOT = Path("out/save_dialogue_followup_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Save_Dialogue_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_save_dialogue_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_save_dialogue_followup_20261119.md")
STARTUP, QA = verified.STARTUP, stage.ROOT / "supported_qa.xml"
CHECKPOINT = "Four save and cartridge dialog lines are revised. The overwrite confirmation and focused write-error path are verified."


def verify(registry, previous, viewed):
    stored, game, boot = map(base.load, (stage.PROOF, verified.GAME, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == game["candidate_sha256"] == boot["candidate_sha256"]
    assert base.digest(parent.ROM) == previous["candidate_sha256"] == stored["parent_sha256"]
    assert base.digest(stage.CLEAN) == previous["clean_input_sha256"] == stored["clean_input_sha256"]
    assert stored["entire_parent_inverse"] and base.digest(stage.SOURCE) == stored["original_source_manifest_sha256"]
    assert viewed == {str(p): base.digest(p) for p in (stage.SHEET, verified.SHEET)}
    assert stored["native_sheet_sha256"] == viewed[str(stage.SHEET)]
    assert all(base.digest(p) == sha for proof in (game, boot) for p, sha in proof["evidence"].items())
    assert game["actual_emulator"] and not game["hardware"] and game["native_write_instruction_restored"]
    assert len(game["original_failure_selector_direct_ARM_sites"]) == 10
    assert [r["id"] for r in game["observed"]] == ["DK4_SAVE_OVERWRITE_CONFIRM", "DK4_SAVE_WRITE_ERROR"]
    assert [r["supplied_write_failure"] for r in game["observed"]] == [False, True]
    assert game["offline_only_revision_ids"] == ["DK4_LOAD_READ_ERROR", "DK4_SAVE_CREATE_CONFIRM"]
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"]) == 6 and len(boot["original_protected_name_getters"]) == 24
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [25, 0, 0, 0]
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    old, new, clean = map(base.NdsImage.open, (parent.ROM, stage.ROM, stage.CLEAN))
    before, after = map(native.files, (old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.ARM}
    old_arm, arm, clean_arm = before[stage.ARM], after[stage.ARM], clean.read_file(stage.ARM)
    assert stage.digest(old_arm) == previous["target_ARM9_sha256"] and stage.digest(arm) == stored["target_ARM9_sha256"]
    assert stage.digest(after[stage.COMMON]) == previous["target_COMMON_sha256"] == stored["target_COMMON_sha256"]
    verify_runtime(arm, previous)
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7 and not any(controls["source_bound_new_command_counts"].values())
    inverse = bytearray(arm)
    assert {r["id"] for r in stored["records"]} == {t[0] for t in stage.FIXED}
    for row in stored["records"]:
        ref = row["current_reference"]
        loc, span = ref["offset"], ref["allocation"]
        assert old_arm[loc:loc+span].hex() == row["current_hex"] and arm[loc:loc+span].hex() == row["staged_hex"]
        assert row["source_hex"] == clean_arm[loc:loc+row["source_reference"]["allocation"]].hex()
        inverse[loc:loc+span] = old_arm[loc:loc+span]
        row["registered_reference"] = ref | dict(candidate_sha256=candidate, ARM9_sha256=stage.digest(arm),
            exact_stored_hex=row["staged_hex"])
        row["review"]["formatting"] = True
    assert bytes(inverse) == old_arm
    new.replace_file(stage.ARM, old_arm)
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    review = {k: stored[k] for k in ("candidate_sha256", "parent_sha256", "translation_policy", "target_locale",
        "encoder", "review_gates", "records")}
    review.update(new_contextual_credit=0, observed_gameplay=game, checked_story_format_guard=controls)
    validate_natural_dialogue_batch(review)
    return stored, review, {stage.ARM: stage.digest(arm)}


publish = template.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 886 and len(manifest["checks"]) == 221':
        'len(manifest["batches"]) == 889 and len(manifest["checks"]) == 224',
    "stage.PROOF, STARTUP, QA, replay.LIVE, replay.SHEET, attack.OUTPUT, args.visual_review":
        "stage.PROOF, STARTUP, QA, verified.GAME, verified.SHEET, stage.SHEET, args.visual_review",
    "release_stack_before_sailing_mode_prose.json": "release_stack_before_save_dialogue.json",
    "release_stack_with_sailing_mode_prose.json": "release_stack_with_save_dialogue.json",
    "verified_lil_maria_flagged_wraps_predecessor": "verified_mutiny_dialogue_predecessor",
    "sailing_mode_prose_release": "save_dialogue_followup_release",
    "registered_sailing_mode_prose_and_complete_parent_inverse":
        "registered_save_dialogue_followup_and_complete_parent_inverse",
    "sailing_mode_prose_pipeline": "save_dialogue_followup_pipeline",
    "native_display_sha256=base.digest(replay.LIVE)": "native_display_sha256=base.digest(verified.GAME)",
    "owned_ARM9_panels=": "owned_ARM9_templates=",
    "repository_tests=32": "repository_tests=25",
    "text_display_revisions=3": "text_display_revisions=4",
    "initialized_Info_Search_and_Declare_War_panels=True": "occupied_save_and_focused_write_failure=True",
    "prose_revisions=3, wrap_only_revisions=0, justified_retentions=0":
        "prose_revisions=4, wrap_only_revisions=0, justified_retentions=0",
    "previously_reviewed_panels=3": "previously_localized_templates=4",
    'checkpoint = "The three sailing guide panels are revised and both Madeira attack-text paths are documented."':
        "checkpoint = CHECKPOINT",
    "sailing_mode_prose_20261118": "save_dialogue_followup_20261119",
    "Preserve sailing guide prose ROM or clean reconstruction": "Preserve save dialogue ROM or clean reconstruction",
    "# Current editorial checkpoint - 2026-11-18": "# Current editorial checkpoint - 2026-11-19",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Save dialogue test candidate

The [local ROM](../../{ROM.as_posix()}) includes revised save confirmations and read/write error messages.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Save confirmations and game-card errors

The occupied and empty save slots ask **Overwrite this save?** and **Create a new save?** The date and identity fields still belong to the original slot UI. The separate read and write warnings preserve the original failure types and now tell the player to power off before reinserting the game card. Four fixed ARM9 strings changed within their terminated allocations, preserving code that later builds placed in the old padding. Ten direct callers of the original error selector match the clean ROM. [Exact review and caller evidence](../{REVIEW.as_posix()})

All four native pages passed complete glyph, continuation, allocation and width checks. The ordinary save controls on a copied Syracuse save displayed the new overwrite question. Supplying one failed native write return displayed the new write warning. The original instruction and source save were verified after the replay. The new-slot confirmation and read fault received offline native checks. Hardware remains unvisited. [Native pages](../{(VERIFY / stage.SHEET.name).as_posix()}) · [Emulator comparison](../{(VERIFY / verified.SHEET.name).as_posix()})

The replay also exposes a separate save-list spacing defect, **N. SeaAt Sea**, between a sea area name and its location status. The capture remains the reproduction for that UI issue.

The clean-input patch rebuilds the ROM byte for byte. Six startup holds, 24 protected name getters and 25 focused tests passed. The candidate carries forward all 114 accepted layers and the ASCII right-bound correction. The ledger stands at 27,700 with 276 stored shared entries still open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = template.env | globals()
exec(compile(main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()

