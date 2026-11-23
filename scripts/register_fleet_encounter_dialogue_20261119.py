"""Register the exact reviewed dolphin, Sirens, and mermaid dialogue."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import audit_fleet_encounter_dialogue_20261119 as game
from scripts import register_rafael_sailing_modes_20261119 as parent
from scripts import register_save_location_labels_20261119 as storage_origin
from scripts import stage_fleet_encounter_dialogue_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-fleet-encounter-dialogue-v1-20261119"
ROOT = Path("out/fleet_encounter_dialogue_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Fleet_Encounter_Dialogue_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_fleet_encounter_dialogue_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_fleet_encounter_dialogue_20261119.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
PENDING = storage_origin.stage.ROOT / "shared_text_current_binding.json"
CHECKPOINT = "The dolphin, Sirens, and mermaid encounters have 46 contextual decisions and three verified emulator replays."
verified = SimpleNamespace(PROOF=stage.PROOF, LIVE=game.PROOF)


def verify(registry, previous, viewed):
    stored, playback, boot = map(base.load, (stage.PROOF, game.PROOF, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == playback["candidate_sha256"] == boot["candidate_sha256"]
    assert stored["parent_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["clean_input_sha256"] == previous["clean_input_sha256"] == base.digest(stage.CLEAN)
    assert stored["entire_parent_inverse"] and stored["allocation"]["complete_COMMON_and_ARM9_table_inverse"]
    assert all(base.digest(p) == sha for r in (playback, boot) for p, sha in r["evidence"].items())
    assert all(base.digest(p) == sha for p, sha in stored["source_proofs"].items())
    assert playback["original_sequences_initialized"] and not playback["natural_random_selection_verified"] and not playback["hardware"]
    assert [r["event"] for r in playback["outcomes"]] == ["dolphins", "sirens", "mermaid"]
    assert [len(r["observed"]) for r in playback["outcomes"]] == [3, 2, 2]
    assert all(r["selector_restored"] for r in playback["outcomes"])
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"]) == 6 and len(boot["original_protected_name_getters"]) == 24
    sheets = stored["sheets"] + playback["sheets"]
    assert viewed == {s["path"]: s["sha256"] for s in sheets}
    assert all(base.digest(p) == sha for p, sha in viewed.items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [34, 0, 0, 0]
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(native.files, (old, new))
    arm, common = after[stage.ARM], after[stage.COMMON]
    assert before.keys() == after.keys()
    assert {p for p in before if before[p] != after[p]} == {stage.ARM, stage.COMMON}
    assert native.digest(arm) == stored["target_ARM9_sha256"] and native.digest(common) == stored["target_COMMON_sha256"]
    start, table = stage.workflow.DIRECTORY_OFFSET, stage.workflow.TABLE_OFFSET
    end = table + 3668*4
    assert arm[:start] == before[stage.ARM][:start] and arm[end:] == before[stage.ARM][end:]
    storage_origin.verify_runtime(arm, previous)
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    for p in (stage.ARM, stage.COMMON):
        new.replace_file(p, before[p])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    entries = stage.workflow.owned_entries(common, arm, native.digest(arm[start:table]))
    old_arm = before[stage.ARM]
    old_entries = stage.workflow.owned_entries(before[stage.COMMON], old_arm, native.digest(old_arm[start:table]))
    assert len(entries) == len(old_entries) == 3668
    changed = sorted(i for i, (a, b) in enumerate(zip(old_entries, entries, strict=True)) if a.text != b.text)
    assert changed == list(stage.EDITS)
    assert stored["allocation"]["all_unselected_native_copy_spans_exact"]
    assert stored["allocation"]["all_41_blocks_fit_8KiB"]
    pending = base.load(PENDING)
    assert len(pending["records"]) == 276
    prior_review = base.load(parent.REVIEW)
    assert prior_review["verified_shared_text_storage"]["sha256"] == base.digest(PENDING)
    for row in pending["records"]:
        ident = row["message_ID"]
        assert row["current_hex"] == entries[ident].text.hex() == old_entries[ident].text.hex()
        assert row["current_reference"] == stage.workflow.reference(entries[ident]) == stage.workflow.reference(old_entries[ident])

    ledger = base.load(base.LEDGER)
    coverage = {(r["file_path"], r["id"]) for r in ledger[base.CONTEXT]["integrated_record_keys"]}
    observed = {x["message_ID"] for a in playback["outcomes"] for x in a["observed"]}
    assert observed & set(changed) == {449, 2366}
    original_arm = clean.read_file(stage.ARM)
    original = stage.workflow.common_message_entries(clean.read_file(stage.COMMON), original_arm)
    records = stored["records"]
    assert len(records) == 46 and len(changed) == 10
    for row in records:
        ident = row["message_ID"]
        assert (row["file_path"], row["id"]) in coverage
        assert original[ident].text.hex() == row["source_hex"] and entries[ident].text.hex() == row["staged_hex"]
        assert (ident in changed) == (row["decision"] == "revision")
        row["registered_reference"] = stage.workflow.reference(entries[ident]) | dict(candidate_sha256=candidate)
        row["initialized_emulator_excerpt_observed"] = ident in observed
        row["review"]["formatting"] = True
    review = {key: stored[key] for key in ("translation_policy", "target_locale", "encoder", "review_gates", "records")}
    review.update(candidate_sha256=candidate, checked_story_format_guard=controls, new_contextual_credit=0,
        source_and_native_dependency_proofs=stored["source_proofs"], observed_gameplay=playback,
        shared_storage_scope=dict(pending_records=276, exact_payloads_and_locations=True, evidence_sha256=base.digest(PENDING)),
        preserved_story_archives=True, direct_visual_review=viewed, owned_common_directory_relocation=stored["allocation"])
    validate_natural_dialogue_batch(review)
    return stored, review, {stage.ARM: native.digest(arm), stage.COMMON: native.digest(common)}


publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 893 and len(manifest["checks"]) == 228':
        'len(manifest["batches"]) == 894 and len(manifest["checks"]) == 229',
    "stage.PROOF, STARTUP, QA, verified.PROOF, verified.LIVE, verified.SETUP, args.visual_review":
        "stage.PROOF, STARTUP, QA, verified.LIVE, args.visual_review",
    "release_stack_before_rafael_sailing_modes.json": "release_stack_before_fleet_encounter_dialogue.json",
    "release_stack_with_rafael_sailing_modes.json": "release_stack_with_fleet_encounter_dialogue.json",
    "verified_rafael_first_voyage_predecessor": "verified_rafael_sailing_modes_predecessor",
    "rafael_sailing_modes_release": "fleet_encounter_dialogue_release",
    "registered_rafael_sailing_modes_and_complete_parent_inverse": "registered_fleet_encounter_dialogue_and_complete_parent_inverse",
    "rafael_sailing_modes_pipeline": "fleet_encounter_dialogue_pipeline",
    'owned_story_records=[row["registered_reference"] for row in draft["records"]], target_SC0_sha256=archives[SC0]':
        'owned_shared_records=[row["registered_reference"] for row in draft["records"]], target_COMMON_sha256=archives[stage.COMMON]',
    'target_ARM9_sha256=previous["target_ARM9_sha256"]':
        'target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON], changed_components=1',
    'ARM9_sha256=previous["target_ARM9_sha256"]':
        'ARM9_sha256=archives[stage.ARM], COMMON_sha256=archives[stage.COMMON]',
    "prose_revisions=12, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=14":
        "prose_revisions=10, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=36",
    "text_display_revisions=12": "text_display_revisions=10",
    "initialized_Rafael_sailing_tutorial_both_choices=True": "initialized_dolphin_sirens_mermaid_replays=True",
    "previously_localized_records=26": "previously_localized_records=46",
    'ledger["rafael_sailing_modes_20261119"]': 'ledger["fleet_encounter_dialogue_20261119"]',
    "candidates = [ROM, stage.ROM, verified.ROM,": "candidates = [ROM, stage.ROM,",
    "Preserve Rafael sailing modes ROM, replay fixture or clean reconstruction":
        "Preserve fleet encounter ROM or clean reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Fleet encounter dialogue test candidate

The [local ROM](../../{ROM.as_posix()}) carries the revised dolphin and mermaid dialogue and the preceding cumulative fixes.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Dolphin, Sirens, and mermaid encounters

Reviewed 46 shared lines from the clean Japanese in their full exchanges. Ten revisions keep the dolphin lookout's request together and make the mermaid identification sound like a surprised question about the swimmer. Thirty-six retentions preserve the captains' distinct replies, the departure of the dolphins, and the Sirens' progression from puzzlement to distress. [Exact records](../{REVIEW.as_posix()})

All 46 original portrait calls passed offline. Every revised page received native and visual review. The three initialized emulator voyages showed seven complete panels, including the revised ship's-log question and mermaid identification. Each run continued to the original port sighting. The replays supplied the event prerequisites. The unused voice alternatives received offline checks. Natural event selection and hardware remain unverified. [Dolphins](../{(VERIFY / 'dolphins_replay.png').as_posix()}) · [Sirens](../{(VERIFY / 'sirens_replay.png').as_posix()}) · [Mermaid](../{(VERIFY / 'mermaid_replay.png').as_posix()})

The shared archive relocation preserves all code, all 276 pending text payloads and their locations, and all four story archives. The clean-input patch reproduces the exact ROM. Six startup holds, 24 protected getters and 34 focused tests passed. All 114 accepted layers and the ASCII right-bound correction carry forward. The ledger remains at 27,700. Main awaits acceptance. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
