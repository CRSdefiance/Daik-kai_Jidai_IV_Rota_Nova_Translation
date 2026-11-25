"""Register the verified player-facing sailing guide prose and exact clean-input patch."""

from pathlib import Path
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_all_routes_final_flagged_wraps_20261118 as parent
from scripts import replay_sailing_mode_prose_20261118 as replay
from scripts import stage_sailing_mode_prose_20261118 as stage
from scripts import verify_attack_display_ownership_20261118 as attack
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text

base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-sailing-mode-prose-v1-20261118"
ROOT = Path("out/sailing_mode_prose_registered_20261118_v1")
ROM = ROOT / "Translation_DS_Sailing_Mode_Prose_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_sailing_mode_prose_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_sailing_mode_prose_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
GATES = ["source", "context", "localization", "naturalness", "formatting"]


def verify(registry, previous, viewed):
    staged, draft, game, boot, ownership = map(base.load, (stage.PROOF, stage.DRAFT, replay.LIVE, STARTUP, attack.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == staged["candidate_sha256"] == draft["candidate_sha256"] == game["candidate_sha256"] == boot["candidate_sha256"]
    assert base.digest(parent.ROM) == previous["candidate_sha256"] == ownership["candidate_sha256"] == staged["predecessor_sha256"]
    assert staged["preserved_renderer_and_same_allocations"] and staged["entire_parent_inverse"]
    assert game["actual_emulator"] and not game["hardware"] and game["requests_and_lower_screen_equal"]
    assert game["complete_first_last_glyphs_and_black_space"] and len(game["native_display_matches"]) == 4
    assert all(r["complete_ink_and_blank_pixels"] == 256 * 176 for r in game["native_display_matches"])
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"]) == 6 and len(boot["original_protected_name_getters"]) == 24
    assert all(base.digest(p) == sha for proof in (boot, game, ownership) for p, sha in proof["evidence"].items())
    assert viewed == {str(replay.SHEET): base.digest(replay.SHEET)}
    assert game["evidence"][str(replay.SHEET)] == viewed[str(replay.SHEET)]
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [32, 0, 0, 0]
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    old, new, clean = map(base.NdsImage.open, (parent.ROM, stage.ROM, native.CLEAN))
    before, after = map(native.files, (old, new))
    assert before.keys() == after.keys()
    assert {p for p in before if before[p] != after[p]} == {native.ARM}
    arm, old_arm = after[native.ARM], before[native.ARM]
    assert native.digest(arm) == staged["target_ARM9_sha256"]
    verify_runtime(arm, previous)
    assert native.digest(after["/COMMON/MESFILE.DK4"]) == previous["target_COMMON_sha256"]
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7 and not any(controls["source_bound_new_command_counts"].values())

    inverse = bytearray(arm)
    panels = stage.encoded(arm, draft)
    assert len(panels) == len(draft["records"]) == 3
    for panel, row in zip(panels, draft["records"], strict=True):
        ref = row["current_reference"]
        at, size = ref["offset"], ref["bytes"]
        assert native.digest(old_arm[at:at+size]) == ref["previous_sha256"]
        assert native.digest(arm[at:at+size]) == ref["revised_sha256"]
        assert panel["packed"].ljust(size, b"\0") == arm[at:at+size]
        inverse[at:at+size] = old_arm[at:at+size]
        row["registered_reference"] = dict(candidate_sha256=candidate, file_path=native.ARM,
            offset=at, runtime_pointer=ref["runtime_pointer"], bytes=size, packed_sha256=ref["revised_sha256"])
        row["formatting_evidence"] = dict(path=str(replay.LIVE), sha256=base.digest(replay.LIVE),
            frames=[r["frame"] for r in game["native_display_matches"] if r["id"] == row["id"]])
        row["speaker"] = "Sailing mode guide"
        row["file_path"] = native.ARM
        row["review"]["formatting"] = True
        row["consumer"] = dict(width_cells=40, body_rows=len(panel["lines"]), native_pages=1, runtime_substitutions=[])
    assert bytes(inverse) == old_arm
    new.replace_file(native.ARM, old_arm)
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    draft.update(encoder="dialogue-relocatable-v1", review_gates=GATES, formatting_pending=False,
                 registered=True, actual_mode_panels=game, checked_story_format_guard=controls)
    validate_natural_dialogue_batch(draft)
    return staged, draft, {native.ARM: native.digest(arm)}


publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
pins = publish[publish.index("    candidates = ["):publish.index("    for path in candidates:")]
main = checked_text(publish, {
    'len(manifest["batches"]) == 885 and len(manifest["checks"]) == 220':
        'len(manifest["batches"]) == 886 and len(manifest["checks"]) == 221',
    "stored, display_proof, draft, archives = verify": "stored, draft, archives = verify",
    '    assert all((r["file_path"], r["id"]) in credited for r in draft["records"])': "",
    "stage.PROOF, STARTUP, QA, display.PROOF, replay.LIVE, replay.LIL_SETUP, replay.MARIA_SETUP, args.visual_review":
        "stage.PROOF, STARTUP, QA, replay.LIVE, replay.SHEET, attack.OUTPUT, args.visual_review",
    '    for sheet in display_proof["contact_sheets"] + draft["initialized_phrase_excerpts"]["sheets"]:\n'
    '        dest = VERIFY / Path(sheet["path"]).name\n'
    '        copyfile(sheet["path"], dest)\n'
    '        assert base.digest(dest) == sheet["sha256"]\n': "",
    "release_stack_before_lil_maria_flagged_wraps.json": "release_stack_before_sailing_mode_prose.json",
    "release_stack_with_lil_maria_flagged_wraps.json": "release_stack_with_sailing_mode_prose.json",
    "verified_all_routes_ongoing_phrase_wraps_predecessor": "verified_lil_maria_flagged_wraps_predecessor",
    "lil_maria_flagged_wraps_release": "sailing_mode_prose_release",
    "registered_lil_maria_flagged_wraps_and_complete_parent_inverse":
        "registered_sailing_mode_prose_and_complete_parent_inverse",
    "lil_maria_flagged_wraps_pipeline": "sailing_mode_prose_pipeline",
    "native_display_sha256=base.digest(display.PROOF)": "native_display_sha256=base.digest(replay.LIVE)",
    'owned_story_blocks=stored["changed_blocks"]':
        'owned_ARM9_panels=[row["registered_reference"] for row in draft["records"]], target_ARM9_sha256=archives[native.ARM]',
    "text_display_revisions=70, pagination_fixes=len(RECLAIMED)": "text_display_revisions=3, pagination_fixes=0",
    "initialized_Lil_and_Maria_rose_and_convoy": "initialized_Info_Search_and_Declare_War_panels",
    "own_registered_startup_sha256=base.digest(startup), changed_internal_files=sorted(archives),":
        "own_registered_startup_sha256=base.digest(startup), changed_internal_files=sorted(archives),\n"
        "        target_ARM9_sha256=archives[native.ARM],",
    "manifest_sha256=release[\"manifest_sha256\"], registered_release_verification=str(RELEASE),":
        "manifest_sha256=release[\"manifest_sha256\"], registered_release_verification=str(RELEASE),\n"
        "        ARM9_sha256=archives[native.ARM],",
    "All 64 queued wrap leads from Lil and Maria and six nearby turns are reviewed.":
        "The three sailing guide panels are revised and both Madeira attack-text paths are documented.",
    "lil_maria_flagged_wraps_20261118": "sailing_mode_prose_20261118",
    "existing_credit=175": "previously_reviewed_panels=3",
    "prose_revisions=70, wrap_only_revisions=0, justified_retentions=105":
        "prose_revisions=3, wrap_only_revisions=0, justified_retentions=0",
    "Preserve Lil and Maria story wrap ROM or replay fixture": "Preserve sailing guide prose ROM or clean reconstruction",
    pins: '''    candidates = [ROM, stage.ROM, stage.ROOT / "clean_rebuilt.nds"]\n''',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Sailing mode prose test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised Info, Search and Declare War guide panels.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Sailing mode guide prose

Revisited the Japanese for all three on-screen sailing instructions. Info leads with how to select a town or ship. Search keeps the three-point fatigue penalty for an unsuccessful search and gives desertion and animal attacks their own sentence. Declare War identifies the target and consequence, preserves the goodwill penalty and keeps the original fleet-specific alliance wording. All three retain the existing heading, font dimensions and sprite allocations. [Exact review ledger](../{REVIEW.as_posix()})

The initialized Madeira replay shows the revised Info and Search panels and Declare War both before and after target selection. All four complete glyph masks and their black backgrounds match, and the lower screen and traced requests match the predecessor. This used the established position fixture and ordinary controller inputs. No hardware coverage is claimed. [Emulator sheet](../{(VERIFY / replay.SHEET.name).as_posix()})

The neutral comparison requested COMMON 2122 for “Shall we attack Madeira?” The allied-occupant comparison changed one relationship byte beyond the position fixture. The original selector filtered the town and showed “There are no targets to attack.” It made no request for COMMON 300 or 304. Both stored records remain open for any other display path, and the 276-key total stays open. [Attack routing evidence](../{(VERIFY / attack.OUTPUT.name).as_posix()})

The clean-input patch rebuilds the candidate byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. Six startup holds, 24 protected name getters and 32 focused tests passed. The ledger holds at 27,700. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
