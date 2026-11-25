"""Register the verified reward phrase wraps and cumulative clean-input patch."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_company_name_companion_scenes_20261121 as startup_reference
from scripts import register_victory_reward_digits_20261121 as parent
from scripts import stage_victory_reward_wrap_20261121 as stage
from scripts import verify_victory_reward_wrap_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
PROFILE = "all-routes-victory-reward-wrap-v1-20261121"
ROOT = Path("out/victory_reward_wrap_registered_20261121")
ROM = ROOT / "Translation_DS_Victory_Reward_Wrap_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_victory_reward_wrap_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_victory_reward_wrap_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP = EVIDENCE / "own_startup_verification.json"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
QA = EVIDENCE / "qa_passed.xml"
live = SimpleNamespace(PROOF=display.PROOF)
CHECKPOINT = "Captured-gold and national-award notices now keep their phrases together. The original victory replay verified the captured-gold wrap."


def verify(registry, previous, viewed):
    draft, actual = map(base.load, (stage.PROOF, display.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == draft["candidate_sha256"] == actual["candidate_sha256"]
    assert draft["parent_sha256"] == actual["parent_sha256"] == previous["candidate_sha256"]
    assert draft["exact_parent_inverse"] and draft["runtime"]["scoped_message_IDs"] == [301, 305]
    assert len(draft["native_display_cases"]) == 44 and len(draft["unchanged_native_controls"]) == 7
    assert actual["original_victory_amounts"] == [109, 103, 6055] and not actual["hardware_verified"]
    assert actual["supplies_screen_unchanged"] and len(actual["held_notices"]) == 2
    assert len(actual["exact_unchanged_framebuffers"]) == 20
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
    arm, binding = stage.selector.transform(before[stage.shared.ARM], previous["target_ARM9_sha256"])
    assert arm == after[stage.shared.ARM] and binding == draft["runtime"]
    assert native.digest(arm) == draft["target_ARM9_sha256"]
    assert native.digest(after[stage.shared.COMMON]) == previous["target_COMMON_sha256"] == draft["target_COMMON_sha256"]
    target.replace_file(stage.shared.ARM, before[stage.shared.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(original, after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())

    startup = startup_reference.startup_check.startup_proof
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
    'len(manifest["batches"]) == 974 and len(manifest["checks"]) == 309':
        'len(manifest["batches"]) == 975 and len(manifest["checks"]) == 310',
    'release_stack_before_victory_reward_digits.json': 'release_stack_before_victory_reward_wrap.json',
    'release_stack_with_victory_reward_digits.json': 'release_stack_with_victory_reward_wrap.json',
    'verified_clifford_declaration_wrap_predecessor=predecessor, victory_reward_digits_release=str(REVIEW)':
        'verified_victory_reward_digits_predecessor=predecessor, victory_reward_wrap_release=str(REVIEW)',
    'registered_victory_reward_digits_and_complete_parent_inverse':
        'registered_victory_reward_wrap_and_complete_parent_inverse',
    'manifest["victory_reward_digits_pipeline"]': 'manifest["victory_reward_wrap_pipeline"]',
    'previously_localized_records=3': 'previously_localized_records=2',
    'wrap_only_revisions=0, justified_retentions=3': 'wrap_only_revisions=2, justified_retentions=0',
    'text_display_revisions=3': 'text_display_revisions=0',
    'observed_food_water_and_gold=True, national_reward_offline=True, native_pages=11':
        'observed_captured_gold=True, national_reward_offline=True, native_pages=44',
    'ledger["victory_reward_digits_20261121"]': 'ledger["victory_reward_wrap_20261121"]',
    'prior_records_reviewed=3, actual_reward_notices=2, native_pages=11':
        'prior_records_reviewed=2, actual_reward_notices=1, native_pages=44',
    'Preserve the victory reward candidate and source ROMs': 'Preserve the victory wrap candidate and source ROMs',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Victory reward wrap testing candidate

The [testing ROM](../../{ROM.as_posix()}) keeps captured-gold and national-award phrases intact. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Captured gold and national awards

The captured-gold notice keeps “from captured ships” on one row. Short national awards still fit on one row, and longer amounts move together with “gold.” Both English paragraphs retain their wording, substitutions, and original reward calculations. [Exact source and release decisions](../{REVIEW.as_posix()})

All 44 native previews passed from one to ten decimal digits. Seven unrelated notices retained their exact display bytes. The paired emulator replay verified the revised 6055 gold notice and matched 20 other frames, including the food and water notice. The national award received offline checks. [Gameplay comparison](../{(VERIFY / display.SHEET.name).as_posix()})

Startup and 17 focused tests passed. The clean-input patch reconstructs the ROM byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
environment = parent.environment | globals()
exec(compile(program, __file__ + "::register", "exec"), environment)


if __name__ == "__main__":
    environment["main"]()
