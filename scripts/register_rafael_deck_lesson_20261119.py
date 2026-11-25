"""Register the revised Deck lesson and its exact cumulative clean-input patch."""

from pathlib import Path
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_save_location_labels_20261119 as parent
from scripts import stage_rafael_deck_lesson_20261119 as stage
from scripts import verify_rafael_deck_lesson_20261119 as verified
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-rafael-deck-lesson-v1-20261119"
ROOT = Path("out/rafael_deck_lesson_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Rafael_Deck_Lesson_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_rafael_deck_lesson_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_deck_lesson_20261119.md")
STARTUP, QA = verified.STARTUP, stage.ROOT / "supported_qa_v2.xml"
PRIOR = Path("translations/rafael_B42_B43_contextual_final_review_v1.json")
SHARED = parent.stage.ROOT / "shared_text_current_binding.json"
WRAP_QUEUE = parent.stage.ROOT / "followup_wrap_queue.json"
SC0 = "/data/SC0.DK4"
CHECKPOINT = "Julio's complete Deck lesson has seven revised lines and five retentions, with the First Mate explanation on one page."


def verify(registry, previous, viewed):
    stored, display, game, boot, draft = map(base.load,
        (stage.PROOF, verified.PROOF, verified.LIVE, STARTUP, stage.review.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert all(p["candidate_sha256"] == candidate for p in (stored, display, game, boot))
    assert stored["predecessor_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and stored["manuscript_sha256"] == base.digest(stage.review.OUTPUT)
    assert display["stage_proof_sha256"] == base.digest(stage.PROOF)
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"]) == 6 and len(boot["original_protected_name_getters"]) == 24
    assert all(base.digest(p) == sha for receipt in (game, boot) for p, sha in receipt["evidence"].items())
    assert game["initialized_Rafael"] and game["exact_native_panel_masks"] and game["exact_original_commands"]
    assert not game["natural_activation"] and not game["hardware"]
    assert len(game["holds"]) == 9 and all(h["page"] == 1 for h in game["holds"])
    sheets = display["contact_sheets"] + game["sheets"]
    assert viewed == {s["path"]: s["sha256"] for s in sheets}
    assert all(base.digest(p) == sha for p, sha in viewed.items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [34, 0, 0, 0]
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    clean, predecessor, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    before, after = map(native.files, (predecessor, target))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {SC0}
    assert stored["changed_blocks"] == {SC0: [43]}
    old_blocks, new_blocks = (native.IlnkContainer.parse(f[SC0]).blocks for f in (before, after))
    assert [i for i, (a, b) in enumerate(zip(old_blocks, new_blocks, strict=True)) if a != b] == [43]
    arm = after[native.ARM]
    assert native.digest(arm) == previous["target_ARM9_sha256"]
    assert native.digest(after["/COMMON/MESFILE.DK4"]) == previous["target_COMMON_sha256"]
    parent.verify_runtime(arm, previous)
    shared, queue = map(base.load, (SHARED, WRAP_QUEUE))
    assert shared["candidate_sha256"] == queue["candidate_sha256"] == previous["candidate_sha256"]
    assert shared["arm9_sha256"] == previous["target_ARM9_sha256"]
    assert shared["common_sha256"] == previous["target_COMMON_sha256"]
    assert len(shared["records"]) == sum(shared["counts"].values()) == 276
    assert queue["counts"]["open editorial lead"] == 0
    assert not any(r["file_path"] == SC0 and r["block"] == 43 for r in queue["records"])
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    target.replace_file(SC0, before[SC0])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()

    sha = native.digest(after[SC0])
    prior_rows = {r["id"]: r for r in base.load(PRIOR)["records"] if r["block"] == 43}
    checked = {r["id"]: r for r in display["records"]}
    observed = {r["id"] for r in game["holds"]}
    assert len(checked) == len(draft["records"]) == len(prior_rows) == 12
    assert [r["id"] for r in checked.values() if r.get("pagination") == [2, 1]] == ["DK4_MES_B43_R0030"]
    credited = {(r["file_path"], r["id"]) for r in base.load(base.LEDGER)[base.CONTEXT]["integrated_record_keys"]}
    for row in draft["records"]:
        ident = row["id"]
        assert (SC0, ident) in credited
        evidence = checked[ident]
        command = evidence["current_reference"]
        at = command["stored_offset"]
        raw = bytes.fromhex(command["stored"])
        assert new_blocks[43][at:at+len(raw)] == raw and raw[5] == row["source_selector"]
        row["registered_reference"] = dict(candidate_sha256=candidate, file_path=SC0, block=43,
            command_offset=at, offset=at + 5, exact_stored_hex=evidence["exact_stored_hex"], archive_sha256=sha)
        row["initialized_emulator_excerpt_observed"] = ident in observed
        row["review"]["formatting"] = True
        if row["decision"] == "retention":
            older = prior_rows[ident]
            assert older["source_hex"] == row["source_hex"] and all(older["review"].values())
            assert older["planned_integrated_reference"]["exact_stored_hex"] == row["current_hex"] == evidence["exact_stored_hex"]
            row["retained_display_review"] = dict(path=PRIOR.as_posix(), sha256=base.digest(PRIOR), id=ident)
        else:
            assert ident in observed and evidence["page"]["native_independent_plane_equal"]
            row["native_formatting_evidence"] = evidence
            if notes := evidence["source_row_count_notes"]:
                assert {n["code"] for n in notes} == {"line-break-count"}
                row["qa_waivers"] = ["line-break-count"]
                row["qa_waiver_reason"] = ("The Japanese and revised English wrap at different word boundaries. "
                    "The original painter and replay show the complete revised English on one page.")
    assert sum(r["decision"] == "revision" for r in draft["records"]) == 7
    draft.update(candidate_sha256=candidate, formatting_and_registration_pending=False,
                 earlier_source_review=PRIOR.as_posix(), reviewed_native_and_live_sheets=viewed,
                 checked_story_format_guard=controls, initialized_gameplay=game,
                 verified_shared_text_storage=dict(path=SHARED.as_posix(), sha256=base.digest(SHARED),
                     unchanged_ARM9_and_COMMON=True, pending_records=276),
                 verified_prior_wrap_queue=dict(path=WRAP_QUEUE.as_posix(), sha256=base.digest(WRAP_QUEUE),
                     original_queue_records_outside_SC0_B43=True, open_editorial_leads=0))
    validate_natural_dialogue_batch(draft)
    return stored, draft, {SC0: sha}


publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 890 and len(manifest["checks"]) == 225':
        'len(manifest["batches"]) == 891 and len(manifest["checks"]) == 226',
    "stage.PROOF, STARTUP, QA, verified.GAME, verified.SHEET, verified.OFFLINE, args.visual_review":
        "stage.PROOF, STARTUP, QA, verified.PROOF, verified.LIVE, verified.SETUP, args.visual_review,\n"
        "                   *(Path(p) for p in base.load(args.visual_review))",
    "release_stack_before_save_location_labels.json": "release_stack_before_rafael_deck_lesson.json",
    "release_stack_with_save_location_labels.json": "release_stack_with_rafael_deck_lesson.json",
    "verified_save_dialogue_predecessor": "verified_save_location_labels_predecessor",
    "save_location_labels_release": "rafael_deck_lesson_release",
    "registered_save_location_labels_and_complete_parent_inverse": "registered_rafael_deck_lesson_and_complete_parent_inverse",
    "save_location_labels_pipeline": "rafael_deck_lesson_pipeline",
    "base.digest(verified.GAME)": "base.digest(verified.PROOF)",
    "owned_ARM9_templates=[row[\"registered_reference\"] for row in draft[\"records\"]], target_ARM9_sha256=archives[native.ARM]":
        "owned_story_records=[row[\"registered_reference\"] for row in draft[\"records\"]], target_SC0_sha256=archives[SC0]",
    "archives[native.ARM]": 'previous["target_ARM9_sha256"]',
    "repository_tests=23": "repository_tests=34",
    "prose_revisions=1, spacing_revisions=3, wrap_only_revisions=0, justified_retentions=3":
        "prose_revisions=7, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=5",
    "text_display_revisions=4, pagination_fixes=0": "text_display_revisions=7, pagination_fixes=1",
    "ordinary_save_and_load_slot_lists=True": "initialized_Rafael_deck_lesson_excerpt=True",
    "previously_localized_labels=7": "previously_localized_records=12",
    'ledger["save_location_labels_20261119"]': 'ledger["rafael_deck_lesson_20261119"]',
    "candidates = [ROM, stage.ROM, stage.ROOT": "candidates = [ROM, stage.ROM, verified.ROM, stage.ROOT",
    "Preserve save location label ROM or clean reconstruction": "Preserve Rafael Deck lesson ROM, excerpt or clean reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael Deck lesson test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised Deck tutorial and the previous cumulative fixes.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael's Deck lesson

Reviewed all 12 turns of Julio's lesson from the clean Japanese. Seven revisions clarify how to assign jobs and what the First Mate, Surveyor and Lookout do. The Surveyor now uses the menu name **Auto Move**. The First Mate's negotiation and fatigue benefits fit together on one page. Five exact retentions preserve Julio's normal-font F, the live given-name substitution, and the final system instructions. [Exact review](../{REVIEW.as_posix()})

The native renderer and visual check cover every revised page. An initialized Rafael emulator excerpt displayed all seven revisions and two unchanged turns, including Julio saying Rafael's name. The First Mate page advances directly to the Surveyor. The final system panel carries its exact earlier proof. Natural tutorial activation and hardware remain unverified. [Native pages](../{(VERIFY / 'before_after_1.png').as_posix()}) · [Emulator excerpt](../{(VERIFY / 'rafael_live_1.png').as_posix()})

Only Rafael's Deck lesson block changes. The clean-input patch reproduces the candidate byte for byte. The ROM carries all 114 accepted layers and the ASCII right-bound correction. Six startup holds, 24 protected getters and 34 focused tests passed. The ledger remains at 27,700 with 276 stored shared keys open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
