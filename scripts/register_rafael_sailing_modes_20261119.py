"""Register both verified sailing tutorial paths in the cumulative release."""

from pathlib import Path
from struct import unpack_from
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import count_and_base, labels
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import audit_rafael_sailing_modes_playback_20261119 as game
from scripts import register_rafael_first_voyage_20261119 as parent
from scripts import register_save_location_labels_20261119 as storage_origin
from scripts import stage_rafael_sailing_modes_20261119 as stage
from scripts import verify_rafael_sailing_modes_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-rafael-sailing-modes-v1-20261119"
ROOT = Path("out/rafael_sailing_modes_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Rafael_Sailing_Modes_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_rafael_sailing_modes_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_sailing_modes_registered_20261119.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
VERIFIED_PRIOR = Path("translations/rafael_B46_contextual_final_review_v1.json")
STORAGE = storage_origin.stage.ROOT / "shared_text_current_binding.json"
WRAPS = storage_origin.stage.ROOT / "followup_wrap_queue.json"
SC0 = "/data/SC0.DK4"
CHECKPOINT = "Rafael's sailing-mode tutorial is registered with 12 revised pages and verified accept and decline paths."
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=game.PROOF, SETUP=game.play.FIXTURES, ROM=game.play.FIXTURE)


def verify(registry, previous, viewed):
    stored, painter, playback, boot, draft = map(base.load, (stage.PROOF, offline.PROOF, game.PROOF, STARTUP, stage.review.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert all(p["candidate_sha256"] == candidate for p in (stored, painter, playback, boot))
    assert stored["predecessor_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and stored["manuscript_sha256"] == base.digest(stage.review.OUTPUT)
    assert painter["stage_proof_sha256"] == base.digest(stage.PROOF) and playback["revised_pages_verified"] == 12
    assert not playback["natural_activation"] and not playback["hardware"]
    assert [p["result"] for p in playback["paths"]] == [[0, 0], [0, 1]]
    assert [len(p["speeches"]) for p in playback["paths"]] == [22, 7]
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"]) == 6 and len(boot["original_protected_name_getters"]) == 24
    assert all(base.digest(p) == sha for receipt in (playback, boot) for p, sha in receipt["evidence"].items())
    sheets = painter["contact_sheets"] + [s for p in playback["paths"] for s in p["sheets"]]
    assert viewed == {s["path"]: s["sha256"] for s in sheets} and all(base.digest(p) == sha for p, sha in viewed.items())
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [34, 0, 0, 0]

    clean, earlier, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    before, after = map(native.files, (earlier, target))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {SC0}
    assert stored["changed_blocks"] == {SC0: [46]}
    banks = [native.IlnkContainer.parse(f[SC0]).blocks for f in (before, after)]
    assert [i for i, (a, b) in enumerate(zip(*banks, strict=True)) if a != b] == [46]
    target.replace_file(SC0, before[SC0])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    arm = after[native.ARM]
    assert native.digest(arm) == previous["target_ARM9_sha256"]
    assert native.digest(after["/COMMON/MESFILE.DK4"]) == previous["target_COMMON_sha256"]
    storage_origin.verify_runtime(arm, previous)
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    shared, queue = map(base.load, (STORAGE, WRAPS))
    prior = base.load(parent.REVIEW)
    assert prior["candidate_sha256"] == previous["candidate_sha256"]
    assert prior["verified_shared_text_storage"]["sha256"] == base.digest(STORAGE)
    assert prior["verified_prior_wrap_queue"]["sha256"] == base.digest(WRAPS)
    assert shared["arm9_sha256"] == previous["target_ARM9_sha256"]
    assert shared["common_sha256"] == previous["target_COMMON_sha256"] and len(shared["records"]) == 276
    assert queue["counts"]["open editorial lead"] == 0
    assert not any(r["file_path"] == SC0 and r["block"] == 46 for r in queue["records"])

    coverage = {(r["file_path"], r["id"]) for r in base.load(base.LEDGER)[base.CONTEXT]["integrated_record_keys"]}
    historical = {r["id"]: r for r in base.load(VERIFIED_PRIOR)["records"]}
    group, = stored["groups"]
    commands = {i: cmd for cmd in group["commands"] for i in cmd["record_ids"]}
    revisions = {r["id"]: r for r in painter["revisions"]}
    seen = {i for p in playback["paths"] for i in p["speeches"]}
    sha = native.digest(after[SC0])
    assert len(commands) == len(draft["records"]) == len(historical) == 26
    assert len(group["commands"]) == 37 and len(seen) == 24
    assert len([c for c in group["commands"] if c["word"] in stage.stage.RELATIVE]) == 4
    for row in draft["records"]:
        ident = row["id"]
        command = commands[ident]
        at, raw = command["stored_offset"], bytes.fromhex(command["stored"])
        assert banks[1][46][at:at+len(raw)] == raw
        if row["kind"] == "typed-choice-label":
            (index,) = row["native_slots"]
            count, header = count_and_base(raw)
            assert count == 2 and row["source_reference"]["command_offset"] == 256
            row["staged_inventory_id"] = ident
            row["id"] = f"DK4_CHOICE_B46_C256_O{index}"
            offset = at + header + unpack_from("<H", raw, 2 + 2*index)[0]
            value = labels(raw)[index]
        else:
            assert command["word"] == 0x4000 and raw[5] == row["source_selector"]
            offset, value = at + 5, raw[5:raw.index(0, 6)]
        assert (SC0, row["id"]) in coverage
        older = historical[row["id"]]
        assert row["source_hex"] == older["source_hex"] and all(older["review"].values())
        row["registered_reference"] = dict(candidate_sha256=candidate, file_path=SC0, block=46,
            command_offset=at, offset=offset, exact_stored_hex=value.hex(), archive_sha256=sha)
        row["initialized_emulator_excerpt_observed"] = ident in seen or row["kind"] == "typed-choice-label"
        row["review"]["formatting"] = True
        # The source branch proof and both new replays distinguish the shared thought
        # from the spoken caution, which occurs when Rafael declines the lesson.
        row["context"] = ("After Hayreddin's rescue, Julio warns Rafael that an enemy fleet may pick a fight. "
            "Accepting his offer plays the explanation and Rafael's thanks. Declining skips the panels and plays "
            "Julio's caution. Both paths end with Rafael's unfinished private thought.")
        if row["decision"] == "retention":
            assert command["stored"] == command["current"]
            assert value.hex() == row["current_hex"] == older["integrated_reference"]["stored_hex"]
            row["retained_display_review"] = dict(path=VERIFIED_PRIOR.as_posix(), sha256=base.digest(VERIFIED_PRIOR), id=row["id"])
        else:
            assert ident in seen and revisions[ident]["target_hex"] == value.hex()
            row["native_formatting_evidence"] = revisions[ident]
    draft.update(candidate_sha256=candidate, formatting_and_registration_pending=False,
        reviewed_native_and_live_sheets=viewed, checked_story_format_guard=controls, initialized_gameplay=playback,
        verified_shared_text_storage=dict(path=STORAGE.as_posix(), sha256=base.digest(STORAGE),
            unchanged_ARM9_and_COMMON=True, pending_records=276),
        verified_prior_wrap_queue=dict(path=WRAPS.as_posix(), sha256=base.digest(WRAPS),
            original_queue_records_outside_SC0_B42_B43_B46=True, open_editorial_leads=0))
    validate_natural_dialogue_batch(draft)
    return stored, draft, {SC0: sha}


publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 892 and len(manifest["checks"]) == 227':
        'len(manifest["batches"]) == 893 and len(manifest["checks"]) == 228',
    "release_stack_before_rafael_first_voyage.json": "release_stack_before_rafael_sailing_modes.json",
    "release_stack_with_rafael_first_voyage.json": "release_stack_with_rafael_sailing_modes.json",
    "verified_rafael_deck_lesson_predecessor": "verified_rafael_first_voyage_predecessor",
    "rafael_first_voyage_release": "rafael_sailing_modes_release",
    "registered_rafael_first_voyage_and_complete_parent_inverse": "registered_rafael_sailing_modes_and_complete_parent_inverse",
    "rafael_first_voyage_pipeline": "rafael_sailing_modes_pipeline",
    "prose_revisions=21, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=7":
        "prose_revisions=12, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=14",
    "text_display_revisions=21, pagination_fixes=1": "text_display_revisions=12, pagination_fixes=0",
    "initialized_Rafael_first_voyage_excerpt=True": "initialized_Rafael_sailing_tutorial_both_choices=True",
    "previously_localized_records=28": "previously_localized_records=26",
    'ledger["rafael_first_voyage_20261119"]': 'ledger["rafael_sailing_modes_20261119"]',
    "Preserve Rafael first-voyage ROM, excerpt or clean reconstruction":
        "Preserve Rafael sailing modes ROM, replay fixture or clean reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael sailing tutorial test candidate

The [local ROM](../../{ROM.as_posix()}) uses the actual sailing mode names and carries the preceding cumulative fixes.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael's sailing-mode tutorial registered

The tutorial now calls the modes **Info**, **Declare War**, and **Search** so the instructions match the on-screen headings. The 26-record review records 12 revisions and 14 exact retentions, including both choice labels. The original buttons, cycle order and targets carry forward. [Exact review](../{REVIEW.as_posix()})

Two initialized Rafael emulator runs exercised both choices with ordinary controller input. **Please do.** displayed all 12 revised pages with complete glyphs and the intended speaker or speakerless layout. **No, thanks.** skipped the instructional panels and took the original caution path. Both returned to port. All 37 original commands were observed across the two runs. Natural scene activation and hardware remain unverified. [Accept replay](../{(VERIFY / 'accept_playback_1.png').as_posix()}) · [Decline replay](../{(VERIFY / 'decline_playback_1.png').as_posix()})

Only Rafael's sailing-mode tutorial block changes. The byte-exact clean-input patch, six startup holds, 24 protected getters and 34 focused tests passed. All 114 accepted layers and the ASCII right-bound correction carry forward. The ledger stands at 27,700 with 276 stored shared entries open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
