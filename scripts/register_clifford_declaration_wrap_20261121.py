"""Register the verified declaration wrap over the current cumulative release."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_map_cluster_suffix_20261121 as parent
from scripts import stage_clifford_declaration_wrap_20261121 as stage
from scripts import verify_clifford_declaration_wrap_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
PROFILE = "all-routes-clifford-declaration-wrap-v1-20261121"
ROOT = Path("out/clifford_declaration_wrap_registered_20261121")
ROM = ROOT / "Translation_DS_Clifford_Declaration_Wrap_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_clifford_declaration_wrap_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_clifford_declaration_wrap_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP = EVIDENCE / "own_startup_verification.json"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
QA = EVIDENCE / "qa_passed.xml"
live = SimpleNamespace(PROOF=display.PROOF)
CHECKPOINT = "Kept Clifford’s wording and moved “they can beat me?” onto one line. Verified the portrait during the original declaration encounter."


def verify(registry, previous, viewed):
    draft, actual = map(base.load, (stage.PROOF, display.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == draft["candidate_sha256"] == actual["candidate_sha256"]
    assert draft["parent_sha256"] == actual["parent_sha256"] == previous["candidate_sha256"]
    assert draft["all_parent_bytes_restored"] and draft["allocation"]["changed_visible_templates"] == [stage.N]
    assert len(draft["native_views"]) == 8 and draft["runtime"]["complete_ARM9_inverse"]
    assert actual["original_fleet_inputs_and_40_byte_location_fixture"] and not actual["hardware_verified"]
    assert actual["changed_frame"] == display.HOLD and len(actual["exact_unchanged_framebuffers"]) == 21
    for path, digest in (viewed | actual["report_evidence"]).items():
        assert base.digest(path) == digest
    assert set(viewed) == {actual["after"]["path"], str(EVIDENCE / "portrait_sheet_01.png")}
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    rebuilt = EVIDENCE / "clean_rebuilt.nds"
    if not rebuilt.exists():
        apply_xdelta(native.CLEAN, EVIDENCE / "translation.xdelta", rebuilt)
    assert rebuilt.read_bytes() == stage.ROM.read_bytes()

    clean, prior, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    original, before, after = map(native.files, (clean, prior, target))
    assert before.keys() == after.keys()
    assert {path for path in before if before[path] != after[path]} == {stage.shared.ARM, stage.shared.COMMON}
    hashes = {path: native.digest(after[path]) for path in (stage.shared.ARM, stage.shared.COMMON)}
    assert hashes[stage.shared.ARM] == draft["target_ARM9_sha256"]
    assert hashes[stage.shared.COMMON] == draft["target_COMMON_sha256"]
    for path in hashes:
        target.replace_file(path, before[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(original, after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())

    startup = parent.parent.startup_check.startup_proof
    context = startup.__globals__ | {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE}
    source = checked_text(getsource(startup), {
        "original_ARM9_and_overlay_preserved=True, hardware=False,":
            "original_ARM9_and_overlay_preserved=False, original_overlay_preserved=True, hardware=False,",
    })
    exec(compile(source, __file__ + "::startup", "exec"), context)
    context["startup_proof"](previous, candidate, after[stage.shared.ARM])
    row, = draft["records"]
    row["registered_reference"] = row["staged_reference"] | {"candidate_sha256": candidate}
    row["decision"] = "wrap_only"
    draft.pop("emulator_and_visual_gate_pending")
    draft.update(status="registered", direct_visual_review=viewed, original_dialogue_runtime=True,
                 native_and_replay_evidence=str(display.PROOF), checked_story_format_guard=controls,
                 shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    validate_natural_dialogue_batch(draft)
    return draft, draft, hashes


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 972 and len(manifest["checks"]) == 307':
        'len(manifest["batches"]) == 973 and len(manifest["checks"]) == 308',
    'release_stack_before_map_cluster_suffix.json': 'release_stack_before_clifford_declaration_wrap.json',
    'release_stack_with_map_cluster_suffix.json': 'release_stack_with_clifford_declaration_wrap.json',
    'live.PROOF, stage.context.CHECKPOINT, args.visual_review,': 'live.PROOF, stage.gameplay.OUTPUT, args.visual_review,',
    'verified_company_companion_scenes_predecessor=predecessor, map_cluster_suffix_release=str(REVIEW)':
        'verified_map_cluster_suffix_predecessor=predecessor, clifford_declaration_wrap_release=str(REVIEW)',
    'registered_map_cluster_suffix_and_complete_parent_inverse': 'registered_clifford_declaration_wrap_and_complete_parent_inverse',
    'manifest["map_cluster_suffix_pipeline"]': 'manifest["clifford_declaration_wrap_pipeline"]',
    'row["decision"] == "revision"': 'row["decision"] == "wrap_only"',
    'original_map_name_and_coordinate_arguments=True, target_ARM9_sha256=archives[native.ARM]':
        'original_declaration_speaker_and_context=True, target_ARM9_sha256=archives[native.ARM]',
    'changed_components=1, target_ARM9_sha256=archives[native.ARM],':
        'changed_components=2, target_ARM9_sha256=archives[native.ARM], target_COMMON_sha256=archives[stage.shared.COMMON],',
    'reviewed_UI_labels=1, previously_localized_records=1': 'reviewed_UI_labels=0, previously_localized_records=1',
    'prose_revisions=1, spacing_revisions=0, wrap_only_revisions=0':
        'prose_revisions=0, spacing_revisions=0, wrap_only_revisions=1',
    'original_World_Map=True, observed_clustered_town_and_fleet=True, offline_width_examples=5, copied_existing_save=True':
        'original_fleet_declaration=True, observed_clifford_page=True, native_portraits=8, position_fixture_bytes=40',
    'ledger["map_cluster_suffix_20261121"]': 'ledger["clifford_declaration_wrap_20261121"]',
    'actual_cluster_marker_modes=2, offline_pages=5': 'actual_clifford_pages=1, native_portraits=8',
    'Preserve the map-cluster suffix candidate and source ROMs': 'Preserve the Clifford wrap candidate and source ROMs',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Clifford declaration wrap testing candidate

The [testing ROM](../../{ROM.as_posix()}) keeps “they can beat me?” together in Clifford’s response. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Clifford’s declaration response

The final question now reads “they can beat me?” on a single row. Clifford’s words, speaker, and three-row layout are preserved. The original portrait renderer passed all eight declaration responses. All seven alternatives matched their previous text and pixels. [Source and registered review](../{REVIEW.as_posix()})

The paired emulator run verified all the letters in the revised line and the two surrounding rows. The original controls, 44 text callbacks, and 21 other framebuffers matched, including the duel and victory rewards. The copied save used the documented 40-byte fleet-position setup. The archived attack prompts remain open. [Revised gameplay frame](../{(VERIFY / 'frame_006120_cold_boot.png').as_posix()})

The candidate passed the startup and text checks. The clean-input patch reconstructs it byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
environment = parent.environment | globals()
exec(compile(program, __file__ + "::register", "exec"), environment)


if __name__ == "__main__":
    environment["main"]()
