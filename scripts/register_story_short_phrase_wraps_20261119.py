"""Register the four-route phrase fixes and the verified Ceuta tutorial replay."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import audit_ceuta_lesson_20261119 as game
from scripts import register_market_followup_20261119 as parent
from scripts import register_save_location_labels_20261119 as storage_origin
from scripts import stage_story_short_phrase_wraps_20261119 as stage
from scripts import verify_story_short_phrase_wraps_20261119 as offline
from scripts.prepare_london_guild_assignments_20261118 import text_records
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-story-phrase-wraps-v1-20261119"
ROOT = Path("out/story_short_phrase_wraps_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Story_Phrase_Wraps_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_story_phrase_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_story_short_phrase_wraps_20261119.md")
STARTUP, QA = game.STARTUP, stage.ROOT / "supported_qa.xml"
VISUAL_REVIEW = stage.ROOT / "direct_visual_review.json"
CHECKPOINT = "The four-route phrase-wrap batch is registered with 19 revised pages, 176 retentions and a focused Ceuta tutorial replay."
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=game.PROOF)


def verify(registry, previous, viewed):
    stored, painter, playback, boot, draft = map(base.load, (
        stage.PROOF, offline.PROOF, game.PROOF, STARTUP, stage.review.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert all(p["candidate_sha256"] == candidate for p in (stored, painter, playback, boot))
    assert stored["predecessor_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and stored["manuscript_sha256"] == base.digest(stage.review.OUTPUT)
    assert painter["stage_proof_sha256"] == base.digest(stage.PROOF)
    assert not playback["natural_activation"] and not playback["hardware"]
    path, = playback["paths"]
    assert path["result"] == [0, 1] and len(path["speeches"]) == 16
    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 6
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"]) == 6 and len(boot["original_protected_name_getters"]) == 24
    assert all(base.digest(p) == sha for receipt in (playback, boot) for p, sha in receipt["evidence"].items())
    sheets = painter["contact_sheets"] + path["sheets"]
    assert len(sheets) == 5 and viewed == {s["path"]: s["sha256"] for s in sheets}
    assert all(base.digest(p) == sha for p, sha in viewed.items())
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [34, 0, 0, 0]

    clean, earlier, final = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    assert base.digest(native.CLEAN) == stored["clean_sha256"] == previous["clean_input_sha256"]
    before, after = map(native.files, (earlier, final))
    archives = {f"/data/SC{i}.DK4": native.digest(after[f"/data/SC{i}.DK4"]) for i in range(4)}
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == archives.keys()
    banks = {}
    for file_path in archives:
        old, new = [native.IlnkContainer.parse(files[file_path]).blocks for files in (before, after)]
        assert [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b] == stored["changed_blocks"][file_path]
        banks[file_path] = new
        final.replace_file(file_path, before[file_path])
    assert bytes(final.rom.save()) == parent.ROM.read_bytes()
    arm = after[native.ARM]
    assert native.digest(arm) == previous["target_ARM9_sha256"]
    assert native.digest(after["/COMMON/MESFILE.DK4"]) == previous["target_COMMON_sha256"]
    storage_origin.verify_runtime(arm, previous)
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls == stored["source25"]
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    prior = base.load(parent.REVIEW)
    assert prior["candidate_sha256"] == previous["candidate_sha256"]
    assert prior["shared_storage_scope"]["exact_payloads_and_locations"]
    assert prior["shared_storage_scope"]["pending_records"] == 276

    coverage = {(r["file_path"], r["id"]) for r in base.load(base.LEDGER)[base.CONTEXT]["integrated_record_keys"]}
    commands = {(g["file_path"], i): (g["block"], c) for g in stored["groups"] for c in g["commands"] for i in c["record_ids"]}
    assert len(stored["groups"]) == 11 and len(commands) == len(draft["records"]) == 195
    revisions = {(r["file_path"], r["id"]): r for r in painter["revisions"]}
    retentions = {(r["file_path"], r["id"]): r["kept_complete_command"] for r in painter["exact_retentions"]}
    assert len(revisions) == 19 and len(retentions) == 176
    assert not revisions.keys() & retentions.keys() and revisions.keys() | retentions.keys() == commands.keys()
    seen = set(path["speeches"])
    for row in draft["records"]:
        ident, file_path = row["id"], row["file_path"]
        key = (file_path, ident)
        block, command = commands[key]
        assert row["block"] == block
        at, raw, word = command["stored_offset"], bytes.fromhex(command["stored"]), command["word"]
        assert banks[file_path][block][at:at + len(raw)] == raw
        offset, selector, value, slots = next(t for t in text_records(raw, word) if t[3] == row["native_slots"])
        assert selector == row["source_selector"]
        if word == 0x4000:
            value = bytes((selector,)) + value
        source = row["source_reference"]
        if key not in coverage and row["kind"] == "typed-choice-label":
            row["id"] = f"SC{row['route']}_B{block}_CHOICE_{source['command_offset']}_{slots[0]}"
        if key not in coverage and row["kind"] == "style":
            relative = source["offset"] - source["command_offset"] - 20
            row["id"] = f"SC{row['route']}_B{block}_STYLE_{source['command_offset']}_{relative}"
        if row["id"] != ident:
            row["staged_inventory_id"] = ident
        assert (file_path, row["id"]) in coverage
        row["registered_reference"] = dict(candidate_sha256=candidate, file_path=file_path, block=block,
            command_offset=at, offset=at + offset, exact_stored_hex=value.hex(), archive_sha256=archives[file_path])
        row["initialized_emulator_excerpt_observed"] = (file_path == "/data/SC0.DK4" and block == 127 and
            (ident in seen or row["kind"] == "typed-choice-label"))
        row["review"]["formatting"] = True
        if row["decision"] == "retention":
            assert retentions[key] == command and command["stored"] == command["current"]
            assert value.hex() == row["current_hex"]
            row["retained_display_review"] = dict(path=offline.PROOF.as_posix(), sha256=base.digest(offline.PROOF), id=ident)
        else:
            assert revisions[key]["target_hex"] == value.hex()
            row["native_formatting_evidence"] = revisions[key]
    draft.update(candidate_sha256=candidate, formatting_and_registration_pending=False,
        reviewed_native_and_live_sheets=viewed, checked_story_format_guard=controls, initialized_gameplay=playback,
        shared_storage_scope=prior["shared_storage_scope"])
    validate_natural_dialogue_batch(draft)
    return stored, draft, archives


publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 897 and len(manifest["checks"]) == 232':
        'len(manifest["batches"]) == 898 and len(manifest["checks"]) == 233',
    "release_stack_before_market_followup.json": "release_stack_before_story_phrase_wraps.json",
    "release_stack_with_market_followup.json": "release_stack_with_story_phrase_wraps.json",
    "verified_battle_dialogue_followup_predecessor": "verified_market_followup_predecessor",
    "market_followup_release": "story_short_phrase_wraps_release",
    '    manifest["checks"]["registered_market_followup_and_complete_parent_inverse"] = True':
        '    assert "registered_story_short_phrase_wraps_and_complete_parent_inverse" not in manifest["checks"]\n'
        '    manifest["checks"]["registered_story_short_phrase_wraps_and_complete_parent_inverse"] = True',
    "market_followup_pipeline": "story_short_phrase_wraps_pipeline",
    "owned_shared_records": "owned_story_records",
    "target_COMMON_sha256=archives[stage.COMMON])": "story_archive_sha256=archives)",
    "target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON], changed_components=2,":
        "changed_components=4,",
    "ARM9_sha256=archives[stage.ARM], COMMON_sha256=archives[stage.COMMON],":
        'ARM9_sha256=previous["target_ARM9_sha256"], COMMON_sha256=previous["target_COMMON_sha256"],',
    "prose_revisions=4, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=18":
        "prose_revisions=17, spacing_revisions=0, wrap_only_revisions=2, justified_retentions=176",
    "text_display_revisions=4": "text_display_revisions=19",
    "initialized_Market_recommendation_and_return=True": "initialized_Ceuta_wind_choice_and_return=True",
    "previously_localized_records=22": "previously_localized_records=195",
    'ledger["market_followup_20261119"]': 'ledger["story_short_phrase_wraps_20261119"]',
    'verified.LIVE, args.visual_review,': 'verified.PROOF, verified.LIVE, args.visual_review,',
    'candidates = [ROM, stage.ROM, stage.ROOT / "clean_rebuilt.nds"]':
        'candidates = [ROM, stage.ROM, stage.ROOT / "clean_rebuilt.nds", game.play.FIXTURE,\n'
        '                  *(stage.ROOT.parent / "research_v1").glob("*.nds")]',
    "Preserve Market follow-up ROM or clean reconstruction": "Preserve story phrase-wrap ROM, fixture or reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Story phrase-wrap test candidate

The [local ROM](../../{ROM.as_posix()}) carries the revised Ceuta sailing lesson and phrase-wrap fixes across all four routes.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Four-route story phrase-wrap candidate

We found 12 phrase breaks beyond the earlier nine. The clean Japanese and the surrounding exchanges guided 17 prose revisions, two wrap-only revisions and 176 justified retentions across 11 blocks. The changes keep phrases such as “New World,” “East Asia,” and “Crimson Dye” together and give Julio’s explanation of the tailwind to Ceuta a natural English rhythm. All 195 records already had coverage credit. The ledger records the original, prior and new command references and all five review gates. [Exact review ledger](../{REVIEW.as_posix()})

Native and visual checks covered all 19 revised pages, including three speakerless pages. A focused emulator run entered the complete revised Ceuta tutorial through an initialized Rafael fixture, showed both choice labels and all six revised tutorial pages, then took the wind-question branch back to Lisbon. The other branch and the other 13 revised pages received offline checks. Natural scene activation and hardware remain unverified. [Ceuta replay](../{(VERIFY / 'decline_playback_1.png').as_posix()})

The clean-input patch rebuilt the candidate byte for byte. Six startup checkpoints, 24 protected name getters and 34 focused tests passed. The four story archives account for every changed internal file. The registered release carries 114 accepted layers, the ASCII right-bound correction and 276 pending shared entries. Main awaits acceptance. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
