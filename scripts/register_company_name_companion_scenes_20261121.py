"""Register the source-bound Gerhard and Maria companion scenes."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_amsterdam_tavern_editorial_20261120 as startup_check
from scripts import register_company_name_dialogue_20261121 as parent
from scripts import stage_company_name_companion_scenes_20261121 as stage
from scripts import verify_company_name_companion_scenes_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
PROFILE = "all-routes-company-companion-scenes-v1-20261121"
ROOT = Path("out/company_companion_scenes_registered_20261121_v1")
ROM = ROOT / "Translation_DS_Company_Companion_Scenes_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_company_companion_scenes_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_company_companion_scenes_registered_20261121.md")
EVIDENCE = stage.EVIDENCE_ROOT
STARTUP = EVIDENCE / "own_startup_verification.json"
STARTUP_CAPTURE = EVIDENCE / "registered_startup/exact_capture/capture_report.json"
QA = EVIDENCE / "qa_passed.xml"
live = SimpleNamespace(PROOF=display.LIVE)
CHECKPOINT = "Reviewed Gerhard’s visit and training in Rafael’s route and Ian’s story in Maria’s route. Registered three dialogue revisions and 71 justified retentions."


def verify(registry, previous, viewed):
    stored, draft, offline, playback = map(base.load, (stage.PROOF, stage.REVIEW, display.OFFLINE, display.LIVE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == offline["candidate_sha256"] == playback["candidate_sha256"]
    assert stored["predecessor_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["manuscript_sha256"] == base.digest(stage.REVIEW)
    assert draft["source_packet_sha256"] == base.digest(draft["source_packet"])
    assert draft["decisions"] == {"retention": 71, "revision": 3}
    assert offline["newly_rendered_pages"] == 6 and not offline["actual_gameplay"]
    assert len(playback["holds"]) == 12 and playback["initialized_Rafael_and_Maria"]
    assert not playback["natural_activation"] and not playback["hardware"]
    assert viewed == {s["path"]: s["sha256"] for s in offline["sheets"] + playback["sheets"]} and len(viewed) == 3
    for path, sha in (viewed | playback["evidence"] | offline["historical_FEs"]).items():
        assert base.digest(path) == sha
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    assert (EVIDENCE / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    clean, predecessor, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    original, before, after = map(native.files, (clean, predecessor, target))
    groups = {g["path"]: g for g in stored["groups"]}
    assert before.keys() == after.keys()
    assert {path for path in before if before[path] != after[path]} == groups.keys() == {"/data/SC0.DK4", "/data/SC3.DK4"}
    assert stored["whole_parent_inverse"]
    assert sum(len(g["preceding_continuations_unchanged"]) for g in groups.values()) == 4
    archives, installed = {}, {}
    for path, group in groups.items():
        old, new = [native.IlnkContainer.parse(data).blocks for data in (before[path], after[path])]
        block = group["block"]
        assert [i for i, (x, y) in enumerate(zip(old, new, strict=True)) if x != y] == [block]
        assert native.digest(old[block]) == group["before"] and native.digest(new[block]) == group["after"]
        archives[path] = native.digest(after[path])
        installed[path] = new[block]
        target.replace_file(path, before[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(original, after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    arm = after[native.ARM]
    assert native.digest(arm) == previous["target_ARM9_sha256"]

    startup = startup_check.startup_proof
    context = startup.__globals__ | {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE}
    exec(compile(getsource(startup), __file__ + "::startup", "exec"), context)
    context["startup_proof"](previous, candidate, arm)

    checked = {(r["file_path"], r["id"]): r for r in offline["decisions"]}
    assert len(checked) == len(draft["records"]) == 74
    assert [r["id"] for r in checked.values() if r.get("old_new_page_count") == [2, 1]] == ["DK4_MES_B116_R0110"]
    seen = {(r["route"], r["id"]) for r in playback["holds"]}
    for row in draft["records"]:
        path, ident = row["file_path"], row["id"]
        result = checked[path, ident]
        assert result["decision"] == row["decision"]
        for page in row["target_pages"]:
            start = page["offset"]
            raw = bytes.fromhex(page["exact_command_hex"])
            assert installed[path][start:start + len(raw)] == raw
        row["review"]["formatting"] = True
        row["formatting_scope"] = result["scope"]
        row["observed_in_initialized_excerpt"] = (row["route"], ident) in seen
        row["registered_reference"] = dict(file_path=path, block=row["block"],
            archive_sha256=archives[path], block_sha256=groups[path]["after"],
            candidate_sha256=candidate, pages=row["target_pages"])
    draft.update(candidate_sha256=candidate, status="registered", direct_visual_review=viewed,
        checked_story_format_guard=controls, retentions=71, revisions=3,
        pagination_fixes=1, native_preview_evidence=str(display.OFFLINE), initialized_excerpt_evidence=str(display.LIVE),
        shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    validate_natural_dialogue_batch(draft)
    return stored, draft, archives


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 970 and len(manifest["checks"]) == 305':
        'len(manifest["batches"]) == 971 and len(manifest["checks"]) == 306',
    'release_stack_before_company_name_dialogue.json': 'release_stack_before_company_companion_scenes.json',
    'release_stack_with_company_name_dialogue.json': 'release_stack_with_company_companion_scenes.json',
    'stage.ROOT / "translation.xdelta"': 'EVIDENCE / "translation.xdelta"',
    'preserve_copy(stage.ROOT / "clean_rebuilt.nds", ROM)': 'preserve_copy(EVIDENCE / "clean_rebuilt.nds", ROM)',
    'live.PROOF, display.PROOF, observed.SETUP, args.visual_review,': 'live.PROOF, display.OFFLINE, args.visual_review,',
    'verified_stock_encounter_names_predecessor=predecessor, company_name_dialogue_release=str(REVIEW)':
        'verified_company_name_dialogue_predecessor=predecessor, company_companion_scenes_release=str(REVIEW)',
    'registered_company_name_dialogue_and_complete_parent_inverse': 'registered_company_companion_scenes_and_complete_parent_inverse',
    'assert credited_key(row, credited) in credited': 'assert (path, ident) in credited',
    'manifest["company_name_dialogue_pipeline"]': 'manifest["company_companion_scenes_pipeline"]',
    'original_company_substitution_order=True, archive_hashes=archives, Rafael_retention_credit_aliases=RAFAEL_RETENTION_ALIASES':
        'original_company_substitution_order=True, archive_hashes=archives, exact_unchanged_FE_continuations=4',
    'changed_components=4': 'changed_components=2',
    'previously_localized_records=73': 'previously_localized_records=74',
    'prose_revisions=12, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=61':
        'prose_revisions=3, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=71',
    'text_display_revisions=4': 'text_display_revisions=0',
    'pagination_fixes=0': 'pagination_fixes=1',
    'initialized_Lil_company_name_dialogue=True, native_default_and_stress_pages=48':
        'initialized_Rafael_and_Maria_excerpts=True, native_default_and_stress_pages=6, observed_panels=12',
    'ledger["company_name_dialogue_20261121"]': 'ledger["company_companion_scenes_20261121"]',
    'prior_records_reviewed=73, actual_Lil_panels=10, offline_pages=48':
        'prior_records_reviewed=74, actual_Rafael_and_Maria_panels=12, offline_pages=6',
    '''    candidates = [ROM, stage.ROM, stage.ROOT / "clean_rebuilt.nds",
                  parent.ROM, observed.ROM]''':
        '''    candidates = [ROM, stage.ROM, parent.ROM, *(
        Path(p) for p in base.load(display.LIVE)["evidence"] if p.endswith(".nds"))]''',
    'Preserve the company-name editorial candidate or replay ROM': 'Preserve the companion-scene candidate or replay ROM',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Company companion scenes testing candidate

The [testing ROM](../../{ROM.as_posix()}) updates three lines in Rafael’s and Maria’s routes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Gerhard’s visit and Ian’s account

Reviewed 74 previously localized records against clean Japanese. Janus now names Gerhard’s skill as a navigator before Gerhard interrupts him. Rafael invites Gerhard back to sea, and Richard’s boast now fits on one page before Samwell cuts him off. The other 71 lines have individual reasons for retention. [Exact source, installed and registered references](../{REVIEW.as_posix()})

Both scenes were aligned across four preexisting speakerless continuation commands. These commands remain byte-identical. Six fresh default and name-width preview pages passed visual and native checks. Focused emulator replays of the initialized routes showed 12 matching panels, including all three revised lines. Natural scene activation and hardware remain open.

The cumulative ROM passed six startup holds, 24 protected name getters and 17 focused tests. The release preserves the registered display runtime and reconstructs byte for byte from clean input. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
environment = parent.environment | globals()
exec(compile(program, __file__ + "::register", "exec"), environment)


if __name__ == "__main__":
    environment["main"]()
