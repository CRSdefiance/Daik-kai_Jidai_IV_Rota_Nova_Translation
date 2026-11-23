"""Register the verified World Map cluster suffix over the current release."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_company_name_companion_scenes_20261121 as parent
from scripts import stage_map_cluster_suffix_20261121 as stage
from scripts import verify_map_cluster_suffix_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
PROFILE = "all-routes-map-cluster-suffix-v1-20261121"
ROOT = Path("out/map_cluster_suffix_registered_20261121_v1")
ROM = ROOT / "Translation_DS_World_Map_Cluster_Suffix_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_map_cluster_suffix_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_map_cluster_suffix_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP = EVIDENCE / "own_startup_verification.json"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
QA = EVIDENCE / "qa_passed.xml"
live = SimpleNamespace(PROOF=display.PROOF)
CHECKPOINT = "Clustered World Map markers now say “+ more.” The town and fleet markers passed paired emulator checks."


def verify(registry, previous, viewed):
    draft, gameplay = map(base.load, (stage.PROOF, display.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == draft["candidate_sha256"] == gameplay["candidate_sha256"]
    assert draft["predecessor_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    assert draft["inverse_verified"] and len(draft["native_cases"]) == 20
    assert gameplay["ordinary_world_map_controls"] and not gameplay["hardware"]
    assert len(gameplay["unchanged_frames"]) == 10 and len(gameplay["complete_live_masks"]) == 4
    assert len(gameplay["offline_width_examples"]) == 5
    assert viewed == {str(display.SHEET): gameplay["sheet"]["sha256"]}
    for p, sha in (viewed | gameplay["evidence"]).items():
        assert base.digest(p) == sha
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    assert (EVIDENCE / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    clean, prior, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    original, before, after = map(native.files, (clean, prior, target))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {native.ARM}
    arm = after[native.ARM]
    lo, hi = stage.OFFSET, stage.OFFSET + stage.CAPACITY
    assert arm == before[native.ARM][:lo] + stage.SUFFIX + b"\0" + before[native.ARM][hi:]
    assert draft["ARM9_sha256"] == native.digest(arm)
    target.replace_file(native.ARM, before[native.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(original, after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())

    startup = parent.startup_check.startup_proof
    context = startup.__globals__ | {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE}
    source = checked_text(getsource(startup), {
        "original_ARM9_and_overlay_preserved=True, hardware=False,":
            "original_ARM9_and_overlay_preserved=False, original_overlay_preserved=True, "
            "ARM9_map_suffix_data_only=True, hardware=False,",
    })
    exec(compile(source, __file__ + "::startup", "exec"), context)
    context["startup_proof"](previous, candidate, arm)

    row, = draft["records"]
    assert row["source_reference"]["exact_hex"] == original[native.ARM][lo:hi].hex()
    assert row["current_reference"]["exact_hex"] == before[native.ARM][lo:hi].hex()
    assert row["staged_reference"]["exact_hex"] == arm[lo:hi].hex()
    row["decision"] = "revision"
    row["review"]["formatting"] = True
    row["registered_reference"] = row["staged_reference"] | {"candidate_sha256": candidate}
    draft.pop("native_raster_and_revised_gameplay_pending")
    draft.update(status="registered", checked_story_format_guard=controls, direct_visual_review=viewed,
        native_and_replay_evidence=str(display.PROOF), shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    validate_natural_dialogue_batch(draft)
    return draft, draft, {native.ARM: native.digest(arm)}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 971 and len(manifest["checks"]) == 306':
        'len(manifest["batches"]) == 972 and len(manifest["checks"]) == 307',
    'release_stack_before_company_companion_scenes.json': 'release_stack_before_map_cluster_suffix.json',
    'release_stack_with_company_companion_scenes.json': 'release_stack_with_map_cluster_suffix.json',
    'live.PROOF, display.OFFLINE, args.visual_review,': 'live.PROOF, stage.context.CHECKPOINT, args.visual_review,',
    'verified_company_name_dialogue_predecessor=predecessor, company_companion_scenes_release=str(REVIEW)':
        'verified_company_companion_scenes_predecessor=predecessor, map_cluster_suffix_release=str(REVIEW)',
    'registered_company_companion_scenes_and_complete_parent_inverse': 'registered_map_cluster_suffix_and_complete_parent_inverse',
    '        assert (path, ident) in credited\n': '',
    'manifest["company_companion_scenes_pipeline"]': 'manifest["map_cluster_suffix_pipeline"]',
    'original_company_substitution_order=True, archive_hashes=archives, exact_unchanged_FE_continuations=4, target_ARM9_sha256=previous["target_ARM9_sha256"]':
        'original_map_name_and_coordinate_arguments=True, target_ARM9_sha256=archives[native.ARM]',
    'changed_components=2, target_ARM9_sha256=previous["target_ARM9_sha256"]':
        'changed_components=1, target_ARM9_sha256=archives[native.ARM]',
    'reviewed_UI_labels=0, previously_localized_records=74': 'reviewed_UI_labels=1, previously_localized_records=1',
    'prose_revisions=3, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=71':
        'prose_revisions=1, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0',
    'pagination_fixes=1': 'pagination_fixes=0',
    'initialized_Rafael_and_Maria_excerpts=True, native_default_and_stress_pages=6, observed_panels=12, natural_activation=False':
        'original_World_Map=True, observed_clustered_town_and_fleet=True, offline_width_examples=5, copied_existing_save=True',
    'ledger["company_companion_scenes_20261121"]': 'ledger["map_cluster_suffix_20261121"]',
    'prior_records_reviewed=74, actual_Rafael_and_Maria_panels=12, offline_pages=6':
        'prior_records_reviewed=1, actual_cluster_marker_modes=2, offline_pages=5',
    '''    candidates = [ROM, stage.ROM, parent.ROM, *(
        Path(p) for p in base.load(display.LIVE)["evidence"] if p.endswith(".nds"))]''':
        '    candidates = [ROM, stage.ROM, parent.ROM]',
    'Preserve the companion-scene candidate or replay ROM': 'Preserve the map-cluster suffix candidate and source ROMs',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# World Map cluster label testing candidate

The [testing ROM](../../{ROM.as_posix()}) uses “+ more” on clustered World Map markers. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# World Map cluster labels and regional finance

The World Map now shows **Syracuse + more** and **Manuel Fleet + more** when entities share a marker. The eight-byte field preserves the original name and suffix substitutions and gives a plain marker just its name. [Source and installed references](../{REVIEW.as_posix()})

The paired replay verified complete glyphs on the two-row town marker and one-row fleet marker. The Syracuse coordinates remained complete, and the single Stockholm marker was identical. Native formatting passed 20 cases and five stress examples fit the measured layout. The replay used a copy of an established regional fleet save. [Map marker comparison](../{(VERIFY / display.SHEET.name).as_posix()})

The regional fleet panel displayed its English finance fields independently of the stored Japanese finance format. All 276 shared references were rebound to the current review input, and the 35 priority strings had no verbatim duplicate outside COMMON in the clean ROM file inventory. Other display callers remain open. [Shared references and regional trace](../{stage.context.CHECKPOINT.as_posix()})

Six startup holds, 24 protected getters and 17 focused tests passed. The clean-input patch reproduces the registered ROM byte for byte. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
environment = parent.environment | globals()
exec(compile(program, __file__ + "::register", "exec"), environment)


if __name__ == "__main__":
    environment["main"]()
