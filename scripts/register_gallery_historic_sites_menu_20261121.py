"""Register the Historic Sites menu and notice on the cumulative testing ROM."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_historic_sites_editorial_20261121 as parent
from scripts import register_sailing_help_20261120 as startup_release
from scripts import stage_gallery_historic_sites_menu_20261121 as stage
from scripts.verify_gallery_historic_sites_menu_20261121 import FULL
from scripts.reconcile_shared_display_20261121 import OUTPUT as PENDING
from scripts.source_locked_derivation_v5118 import checked_text


base, native, shared = stage.base, stage.native, stage.workflow
PROFILE = "all-routes-gallery-historic-sites-menu-v1-20261121"
ROOT = Path("out/gallery_historic_sites_menu_registered_20261121_v1")
ROM = ROOT / "Translation_DS_Gallery_Historic_Sites_Menu_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_gallery_historic_sites_menu_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_gallery_historic_sites_menu_20261121.md")
STARTUP = stage.ROOT / "own_startup_verification.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
QA = stage.ROOT / "qa_passed.xml"
live = SimpleNamespace(PROOF=stage.LIVE)
CHECKPOINT = "The Gallery menu and empty-collection notice now match the Historic Sites heading."


def verify(registry, previous, viewed):
    draft, observed = map(base.load, (stage.PROOF, stage.LIVE))
    candidate = base.digest(stage.ROM)
    assert candidate == draft["candidate_sha256"] == observed["candidate_sha256"]
    assert base.digest(stage.CLEAN) == previous["clean_input_sha256"] == draft["clean_input_sha256"]
    assert base.digest(parent.ROM) == previous["candidate_sha256"] == draft["parent_sha256"]
    assert observed["ordinary_empty_collection"] and observed["populated_with_initialized_save"]
    assert observed["modal_dismissal_and_title_return"] and not observed["hardware"]
    full = base.load(FULL)
    assert full["candidate_sha256"] == candidate
    assert base.digest(full["capture_report"]) == full["capture_sha256"]
    assert [row["text"] for row in full["ordered_glyph_masks"]] == ["Items", stage.ENGLISH, "Characters", "Event Scenes"]
    assert viewed == observed["sheets"] | {full["frame"]["path"]: full["frame"]["PNG_sha256"]}
    assert all(base.digest(path) == digest for path, digest in observed["evidence"].items())
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    clean, predecessor, target = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(native.files, (predecessor, target))
    owned_paths = (stage.ARM, stage.COMMON)
    assert before.keys() == after.keys() and {k for k in before if before[k] != after[k]} == set(owned_paths)
    arm, common, records, allocation = stage.transform(clean, before[stage.ARM], before[stage.COMMON])
    assert after[stage.ARM] == arm and after[stage.COMMON] == common and records == draft["records"]
    assert len(records) == 2 and allocation == draft["allocation"]
    archives = {path: native.digest(after[path]) for path in owned_paths}
    assert archives == {stage.ARM: draft["target_ARM9_sha256"], stage.COMMON: draft["target_COMMON_sha256"]}
    for path in owned_paths:
        target.replace_file(path, before[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())

    directory = native.digest(arm[shared.DIRECTORY_OFFSET:shared.TABLE_OFFSET])
    entries = shared.owned_entries(common, arm, directory)
    pending = base.load(PENDING)
    assert len(pending["records"]) == 276
    assert all(shared.reference(entries[r["message_ID"]]) == r["current_reference"]
               and entries[r["message_ID"]].text.hex() == r["current_hex"] for r in pending["records"])
    startup = startup_release.env["startup_check"].startup_proof
    env = startup.__globals__ | {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE}
    startup_program = checked_text(getsource(startup), {
        "original_ARM9_and_overlay_preserved=True, hardware=False,":
            "original_ARM9_and_overlay_preserved=False, ARM9_Gallery_menu_pointer_only=True, "
            "original_overlay_preserved=True, hardware=False,",
    })
    exec(compile(startup_program, __file__ + "::startup", "exec"), env)
    env["startup_proof"](previous, candidate, arm)
    for row, frame in zip(records, (5100, 5500), strict=True):
        row["review"]["formatting"] = True
        row["registered_reference"] = row["staged_reference"] | {"candidate_sha256": candidate}
        row["gameplay_frame"] = frame
    review = draft | dict(records=records, checked_story_format_guard=controls, observed_gameplay=observed,
                         full_popup=full, direct_visual_review=viewed, new_contextual_credit=0, unchanged_pending_records=276,
                         shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    validate_natural_dialogue_batch(review)
    return draft, review, archives


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
credit_rows = template[template.index('    ids = manifest["changed_records"]'):template.index('    manifest["historic_sites_editorial_pipeline"]')]
program = checked_text(template, {
    'len(manifest["batches"]) == 965 and len(manifest["checks"]) == 300':
        'len(manifest["batches"]) == 966 and len(manifest["checks"]) == 301',
    'release_stack_before_historic_sites.json': 'release_stack_before_gallery_historic_sites_menu.json',
    'live.PROOF, args.visual_review': 'live.PROOF, FULL, args.visual_review',
    'release_stack_with_historic_sites.json': 'release_stack_with_gallery_historic_sites_menu.json',
    'verified_hangzhou_veracruz_predecessor=predecessor, historic_sites_editorial_release=str(REVIEW)':
        'verified_historic_sites_predecessor=predecessor, gallery_historic_sites_menu_release=str(REVIEW)',
    'registered_historic_sites_editorial_and_complete_parent_inverse': 'registered_gallery_historic_sites_menu_and_complete_parent_inverse',
    'manifest["historic_sites_editorial_pipeline"]': 'manifest["gallery_historic_sites_menu_pipeline"]',
    credit_rows: '''    assert (stage.COMMON, "COMMON_MESSAGE_99") in credited
    for row in draft["records"]:
        ids = manifest["changed_records"][row["file_path"]]
        if row["id"] not in ids:
            ids.append(row["id"])
''',
    'original_gallery_pool=True, target_ARM9_sha256=archives[stage.ARM]':
        'existing_Gallery_heading_pointer=True, changed_archive_hashes=archives',
    'changed_components=1, target_ARM9_sha256=archives[stage.ARM],':
        'changed_components=2, target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON],',
    'reviewed_UI_labels=0, previously_localized_records=19, new_contextual_records=0, prose_revisions=6, spacing_revisions=0, wrap_only_revisions=7, justified_retentions=6':
        'reviewed_UI_labels=1, previously_localized_records=2, new_contextual_records=0, prose_revisions=2, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0',
    'initialized_discovery_collection=True, original_Gallery_pages=19, changed_pages=13, carousel_wrap_and_back=True, natural_discovery=False':
        'ordinary_empty_Gallery=True, initialized_populated_Gallery=True, modal_and_title_returns=True, natural_discovery=False',
    'ledger["historic_sites_editorial_20261121"]': 'ledger["gallery_historic_sites_menu_20261121"]',
    'prior_records_reviewed=19, initialized_emulator_records=19, new_contextual_credit=0,\n        prose_revisions=6, spacing_revisions=0, wrap_only_revisions=7, justified_retentions=6':
        'prior_records_reviewed=2, actual_emulator_records=2, new_contextual_credit=0,\n        prose_revisions=2, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0',
    'parent.ROM, *(path for stage_root in (stage.PREVIEW, *stage.LAYOUT_TRIALS) for path in stage_root.glob("*.nds"))':
        'parent.ROM',
    'Preserve the Historic Sites candidate or its earlier stage': 'Preserve the Historic Sites menu candidate or research ROM',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Historic Sites menu testing candidate

The [testing ROM](../../{ROM.as_posix()}) uses Historic Sites throughout the Gallery selection. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Historic Sites Gallery menu and notice

**Historic Sites** replaces **Ruins** in the Gallery menu and matches the existing screen heading. The clean Japanese uses the same term in both places, and the collection includes churches. The empty collection now reads **No historic sites discovered yet.** The menu uses the existing heading string, and the notice keeps the original copy length and trailing blank. [Exact references and decisions](../{REVIEW.as_posix()})

Paired cold boots used the same ordinary save and verified both complete notices, dismissal and the title return. Prepared saves verified all four menu labels together and checked entry to Historic Sites, the viewer and the return. The 17 focused tests, six startup holds and 24 protected name getters passed. Hardware remains unvisited. [Gallery comparison](../{VERIFY.as_posix()}/gallery_menu_comparison.png) · [Testing ROM and exact patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + "::register", "exec"), env)


if __name__ == "__main__":
    env["main"]()
