"""Register the verified numbered-fleet separator in the cumulative candidate."""
from inspect import getsource
from pathlib import Path

from scripts import register_athens_london_trends_20261121 as parent
from scripts import stage_numbered_fleet_spacing_20261121 as stage
from scripts import verify_numbered_fleet_spacing_20261121 as live
from scripts.source_locked_derivation_v5118 import checked_text


template = parent.template
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-numbered-fleet-spacing-v1-20261121"
ROOT = Path("out/numbered_fleet_spacing_registered_20261121")
ROM = ROOT / "Translation_DS_Numbered_Fleet_Spacing_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_numbered_fleet_spacing_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_numbered_fleet_spacing_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
CHECKPOINT = "The Route Map now separates faction names and numbered fleet labels. Both live surfaces passed glyph and bounds checks."


def checked_predecessor_startup(path, previous, retained):
    assert base.digest(path) == retained["evidence"][str(path)]
    report = base.load(path)
    assert report["ROM_sha256"] == retained["candidate_sha256"] == previous["candidate_sha256"]
    assert report["frames"] == 31000 and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and not report["hardware_device_verification"]
    assert set(shot["frame"] for shot in retained["exact_matching_frames"]) == {1600,2200,3340,4000,16000,31000}
    for shot in retained["exact_matching_frames"]:
        assert shot in report["frames_captured"] and base.digest(shot["path"]) == shot["PNG_sha256"]
    snapshot = retained["read_only_snapshot"]
    assert snapshot == report["read_only_RAM_snapshot"] and base.digest(snapshot["path"]) == snapshot["sha256"]
    return report | {"frames_captured":retained["exact_matching_frames"]}


def verify(registry, previous, viewed):
    stored, observed = map(base.load,(stage.PROOF,live.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == observed["candidate_sha256"]
    assert stored["predecessor_sha256"] == observed["predecessor_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert base.digest(native.CLEAN) == stored["clean_sha256"] == previous["clean_input_sha256"]
    assert stored["complete_parent_inverse"] and stored["affected_snapshot_labels"] == 38
    assert len(stored["existing_getter_results"]) == 50
    assert observed["ordinary_route_map"] and observed["original_ordinal_and_cluster_suffix_preserved"]
    assert observed["changed_surfaces_limited_to_header_and_marker"] and not observed["hardware_verified"]
    assert len(observed["live_header"]) == len(observed["live_markers"]) == 2
    sheet = observed["visual_review"]
    assert viewed == {sheet["path"]:sheet["sha256"]}
    for p, sha in (viewed | observed["evidence"] | stored["evidence"]).items():
        assert base.digest(p) == sha
    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k,"0")) for k in ("tests","failures","errors","skipped")] == [17,0,0,0]
    assert (EVIDENCE / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    clean, predecessor, target = map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    original, before, after = map(native.files,(clean,predecessor,target))
    assert before.keys() == after.keys()
    assert {p for p in before if before[p] != after[p]} == {native.ARM}
    a, b = stage.OFFSET, stage.OFFSET+stage.CAPACITY
    arm = after[native.ARM]
    assert original[native.ARM][a:b] == before[native.ARM][a:b] == stage.SOURCE
    assert arm == before[native.ARM][:a] + stage.ENGLISH + before[native.ARM][b:]
    assert native.digest(arm) == stored["target_ARM9_sha256"]
    with template.mapped(parent.MANIFEST) as data:
        current_checks = template.value(data,"checks",2)
    assert current_checks["registered_runtime_bounds_and_complete_parent_target_inverse"]
    target.replace_file(native.ARM,before[native.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = template.bind_registered_story_percent_guard(guard)(original,after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    startup = template.startup_check.startup_proof
    verify_startup = checked_text(getsource(startup), {
        "old, _ = checked_report(old_capture, previous['candidate_sha256'], START_FRAMES[-1])":
            "old = checked_predecessor_startup(old_capture, previous, prior_proof)",
        "original_ARM9_and_overlay_preserved=True, hardware=False,":
            "original_ARM9_and_overlay_preserved=False, original_overlay_preserved=True, "
            "sole_ARM9_change_numbered_fleet_format=True, hardware=False,",
    })
    context = startup.__globals__ | {"STARTUP":STARTUP,"STARTUP_CAPTURE":STARTUP_CAPTURE,
                                     "checked_predecessor_startup":checked_predecessor_startup}
    exec(compile(verify_startup,__file__+"::startup","exec"),context)
    context["startup_proof"](previous,candidate,arm)

    row, = stored["records"]
    assert row["source_reference"]["exact_hex"] == stage.SOURCE.hex()
    assert row["current_reference"]["exact_hex"] == stage.SOURCE.hex()
    assert row["staged_reference"]["exact_hex"] == stage.ENGLISH.hex()
    row.update(decision="revision",registered_reference=row["staged_reference"] | {"candidate_sha256":candidate})
    row["review"]["formatting"] = True
    draft = stored | dict(status="registered",checked_story_format_guard=controls,direct_visual_review=viewed,
        native_and_replay_evidence=str(live.PROOF),shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    draft.pop("gameplay_of_revised_candidate_pending")
    template.validate_natural_dialogue_batch(draft)
    return stored,draft,{native.ARM:native.digest(arm)}


main_source = getsource(template.main)
readme = main_source[main_source.index('    (PACKAGE / "README.md").write_text'):main_source.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(main_source,{
    "verified_search_forage_wrap_predecessor": "verified_athens_london_trends_predecessor",
    "len(batches) == 979 and len(checks) == 314": "len(batches) == 983 and len(checks) == 318",
    "live.PROOF, display.PROOF, args.visual_review,": "live.PROOF, args.visual_review,",
    "source_movie_preserved=True": "fleet_name_and_ordinal_arguments_retained=True",
    'target_ARM9_sha256=previous["target_ARM9_sha256"]': 'target_ARM9_sha256=archives[native.ARM]',
    "changed_components=2, repository_tests": 'changed_components=1, target_ARM9_sha256=archives[native.ARM], repository_tests',
    "reviewed_UI_labels=0": "reviewed_UI_labels=1",
    "previously_localized_records=37, new_contextual_records=0, prose_revisions=4, spacing_revisions=0":
        "previously_localized_records=1, new_contextual_records=0, prose_revisions=0, spacing_revisions=1",
    "justified_retentions=32, name_label_revisions=0, text_display_revisions=1":
        "justified_retentions=0, name_label_revisions=1, text_display_revisions=0",
    "initialized_Rafael_and_Hodram_excerpts=True": "ordinary_Route_Map=True",
    "native_revised_pages=5, observed_panels=21, natural_activation=False":
        "native_formatter_outputs=50, observed_surfaces=2, natural_activation=True",
    "len(credited) == 27700 and all((r[\"file_path\"], r[\"id\"]) in credited for r in draft[\"records\"])":
        "len(credited) == 27700",
    'registered_release_verification=str(RELEASE),': 'registered_release_verification=str(RELEASE), ARM9_sha256=archives[native.ARM],',
    "prior_records_reviewed=37, actual_Rafael_and_Hodram_panels=21, offline_pages=5":
        "prior_records_reviewed=1, actual_Route_Map_surfaces=2, offline_getter_outputs=50",
    "prose_revisions=4, justified_retentions=32, text_display_revisions=1":
        "prose_revisions=0, justified_retentions=0, spacing_revisions=1",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Numbered fleet label testing candidate

The [testing ROM](../../{ROM.as_posix()}) separates the faction name and numbered fleet label. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("moonlit_violin","numbered_fleet_spacing")

commit_source = getsource(template.commit)
checkpoint_prose = commit_source[commit_source.index("    DOC.write_text"):commit_source.index("    prefix =")]
commit_candidate = checked_text(commit_source,{
    "Preserve the violin candidate or replay ROM": "Preserve the numbered-fleet candidate and staging ROM",
    checkpoint_prose: '''    DOC.write_text(f"""# Numbered fleet names on the Route Map

The Route Map now displays **Clifford Fleet 2** in the header and **Clifford Fleet 2 + more** on the clustered marker. The original formatter supplied the company and numbered fleet in the right order. A space was added inside its existing eight-byte field. Both substitutions, the native ordinal glyph and the cluster suffix remain exact. [Source and installed references](../{REVIEW.as_posix()})

Ordinary play reproduced both labels, and complete glyph masks matched each revised surface. The native getter checked 50 fleets from the original read-only snapshot. Thirty-eight numbered fleet names gained the separator, and the twelve controls kept their exact names. Six startup holds, 24 protected name getters and 17 focused tests passed. [Before and after](../{(VERIFY / live.SHEET.name).as_posix()}) · [Cumulative testing ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("moonlit_violin","numbered_fleet_spacing")

scope = vars(template) | globals()
for source in (build,commit_candidate):
    exec(compile(source,__file__,"exec"),scope)


if __name__ == "__main__":
    scope["main"]()
