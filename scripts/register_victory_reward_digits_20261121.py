"""Register the verified victory-number glyph correction and cumulative patch."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_clifford_declaration_wrap_20261121 as parent
from scripts import stage_victory_reward_digits_20261121 as stage
from scripts import verify_victory_reward_digits_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
PROFILE = "all-routes-victory-reward-digits-v1-20261121"
ROOT = Path("out/victory_reward_digits_registered_20261121")
ROM = ROOT / "Translation_DS_Victory_Reward_Digits_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_victory_reward_digits_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_victory_reward_digits_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP = EVIDENCE / "own_startup_verification.json"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
QA = EVIDENCE / "qa_passed.xml"
live = SimpleNamespace(PROOF=display.PROOF)
CHECKPOINT = "Battle rewards now use regular-width digits. Paired gameplay verified the captured gold, food, and water amounts."


def verify(registry, previous, viewed):
    draft, actual = map(base.load, (stage.PROOF, display.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == draft["candidate_sha256"] == actual["candidate_sha256"]
    assert draft["parent_sha256"] == actual["parent_sha256"] == previous["candidate_sha256"]
    assert draft["exact_parent_inverse"] and len(draft["native_number_checks"]) == 1792
    assert len(draft["native_display_cases"]) == 11 and len(draft["original_call_bindings"]) == 4
    assert actual["original_victory_amounts"] == [109, 103, 6055] and not actual["hardware_verified"]
    assert len(actual["held_notices"]) == 3 and len(actual["exact_unchanged_framebuffers"]) == 19
    assert viewed == {r["path"]: r["sha256"] for r in (*draft["sheets"], actual["sheet"])}
    for path, digest in (viewed | actual["source_evidence"]).items():
        assert base.digest(path) == digest
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    assert (EVIDENCE / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    clean, prior, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    original, before, after = map(native.files, (clean, prior, target))
    assert before.keys() == after.keys()
    assert {path for path in before if before[path] != after[path]} == {stage.shared.ARM}
    arm, changed = stage.patch(before[stage.shared.ARM], original[stage.shared.ARM])
    assert arm == after[stage.shared.ARM] and changed == draft["original_call_bindings"]
    assert native.digest(arm) == draft["target_ARM9_sha256"]
    assert native.digest(after[stage.shared.COMMON]) == previous["target_COMMON_sha256"] == draft["target_COMMON_sha256"]
    target.replace_file(stage.shared.ARM, before[stage.shared.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(original, after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())

    startup = parent.parent.parent.startup_check.startup_proof
    context = startup.__globals__ | {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE}
    source = checked_text(getsource(startup), {
        "original_ARM9_and_overlay_preserved=True, hardware=False,":
            "original_ARM9_and_overlay_preserved=False, original_overlay_preserved=True, hardware=False,",
    })
    exec(compile(source, __file__ + "::startup", "exec"), context)
    context["startup_proof"](previous, candidate, arm)
    for row in draft["records"]:
        row["registered_reference"] = row["current_reference"] | {"candidate_sha256": candidate}
    draft.pop("emulator_and_visual_gate_pending")
    draft.update(status="registered", direct_visual_review=viewed, original_dialogue_runtime=True,
                 native_and_replay_evidence=str(display.PROOF), checked_story_format_guard=controls,
                 shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    validate_natural_dialogue_batch(draft)
    return draft, draft, {stage.shared.ARM: native.digest(arm)}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 973 and len(manifest["checks"]) == 308':
        'len(manifest["batches"]) == 974 and len(manifest["checks"]) == 309',
    'release_stack_before_clifford_declaration_wrap.json': 'release_stack_before_victory_reward_digits.json',
    'release_stack_with_clifford_declaration_wrap.json': 'release_stack_with_victory_reward_digits.json',
    'live.PROOF, stage.gameplay.OUTPUT, args.visual_review,': 'live.PROOF, args.visual_review,',
    'verified_map_cluster_suffix_predecessor=predecessor, clifford_declaration_wrap_release=str(REVIEW)':
        'verified_clifford_declaration_wrap_predecessor=predecessor, victory_reward_digits_release=str(REVIEW)',
    'registered_clifford_declaration_wrap_and_complete_parent_inverse':
        'registered_victory_reward_digits_and_complete_parent_inverse',
    'manifest["clifford_declaration_wrap_pipeline"]': 'manifest["victory_reward_digits_pipeline"]',
    'original_declaration_speaker_and_context=True, target_ARM9_sha256=archives[native.ARM]':
        'original_victory_reward_arithmetic_and_modal_calls=True, target_ARM9_sha256=archives[native.ARM]',
    'changed_components=2, target_ARM9_sha256=archives[native.ARM], target_COMMON_sha256=archives[stage.shared.COMMON],':
        'changed_components=1, target_ARM9_sha256=archives[native.ARM],',
    'reviewed_UI_labels=0, previously_localized_records=1': 'reviewed_UI_labels=0, previously_localized_records=3',
    'wrap_only_revisions=1, justified_retentions=0': 'wrap_only_revisions=0, justified_retentions=3',
    'text_display_revisions=0': 'text_display_revisions=3',
    'original_fleet_declaration=True, observed_clifford_page=True, native_portraits=8, position_fixture_bytes=40':
        'original_fleet_victory=True, observed_food_water_and_gold=True, national_reward_offline=True, native_pages=11, position_fixture_bytes=40',
    'ledger["clifford_declaration_wrap_20261121"]': 'ledger["victory_reward_digits_20261121"]',
    'prior_records_reviewed=1, actual_clifford_pages=1, native_portraits=8':
        'prior_records_reviewed=3, actual_reward_notices=2, native_pages=11',
    'Preserve the Clifford wrap candidate and source ROMs': 'Preserve the victory reward candidate and source ROMs',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Victory reward digits testing candidate

The [testing ROM](../../{ROM.as_posix()}) uses regular English digits for the three battle victory notices. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Victory reward numbers

The three original victory reward notices now use regular-width digits. Captured supplies keep food before water and give both quantities in barrels. Captured gold and the national reward stay separate. The wording and original reward calculations carry forward. Four number-format calls change. [Source and registered review](../{REVIEW.as_posix()})

The paired emulator replay showed 109 barrels of food, 103 barrels of water and 6055 gold. Both notices matched their complete native glyph masks, and 19 other frames matched the previous build. The national reward and uncommon amount lengths were checked offline. The replay used the established copied save and 40-byte position fixture. [Gameplay comparison](../{(VERIFY / display.SHEET.name).as_posix()})

The captured-gold paragraph still wraps after “from” at the observed amount and can split “captured ships” with a one-digit amount. The national-reward stress example can strand “gold.” These are line-break leads for the original reward formatter. [Native previews](../{(VERIFY / 'stored_panels_01.png').as_posix()})

Startup and the 17 focused tests passed. The clean-input patch reconstructs the ROM byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
environment = parent.environment | globals()
exec(compile(program, __file__ + "::register", "exec"), environment)


if __name__ == "__main__":
    environment["main"]()
