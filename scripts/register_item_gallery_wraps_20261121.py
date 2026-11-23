"""Register the verified reflow of eight item descriptions."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_gallery_historic_sites_menu_20261121 as parent
from scripts import register_sailing_help_20261120 as startup_release
from scripts import stage_item_gallery_wraps_20261121 as stage
from scripts.reconcile_shared_display_20261121 import OUTPUT as PENDING
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_item_gallery_wraps_native_20261121 import PROOF as NATIVE


base, native, shared = stage.base, parent.native, parent.shared
PROFILE = "all-routes-item-gallery-wraps-v1-20261121"
ROOT = Path("out/item_gallery_wraps_registered_20261121_v1")
ROM = ROOT / "Translation_DS_Item_Gallery_Wraps_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_item_gallery_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_item_gallery_wraps_registered_20261121.md")
STARTUP = stage.ROOT / "own_startup_verification.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
QA = stage.ROOT / "qa_passed.xml"
live = SimpleNamespace(PROOF=stage.LIVE)
CHECKPOINT = "Registered eight item-card wrap fixes with the original wording intact."


def verify(registry, previous, viewed):
    draft, observed, isolated, coverage = map(base.load, (stage.PROOF, stage.LIVE, NATIVE, stage.audit.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == draft["candidate_sha256"] == observed["candidate_sha256"] == isolated["candidate_sha256"]
    assert base.digest(stage.CLEAN) == previous["clean_input_sha256"] == draft["clean_input_sha256"]
    assert base.digest(parent.ROM) == previous["candidate_sha256"] == coverage["candidate_sha256"] == draft["parent_sha256"]
    assert base.digest(stage.audit.OUTPUT) == draft["coverage_sha256"]
    assert observed["original_gallery_controls"] and observed["full_original_carousel_return"] and observed["initialized_collection"]
    assert not observed["natural_acquisition"] and not observed["hardware"]
    assert len(viewed) == 3 and viewed == observed["sheets"] | isolated["sheets"]
    for evidence in (observed["evidence"], viewed):
        assert all(base.digest(path) == digest for path, digest in evidence.items())
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    clean, predecessor, target = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(native.files, (predecessor, target))
    assert before.keys() == after.keys() and {k for k in before if before[k] != after[k]} == {stage.ARM}
    arm, records = stage.transform(before[stage.ARM], coverage)
    common = after[stage.COMMON]
    assert after[stage.ARM] == arm and records == draft["records"] and len(records) == 8
    archives = {stage.ARM: native.digest(arm)}
    assert archives[stage.ARM] == draft["target_ARM9_sha256"]
    assert native.digest(common) == previous["target_COMMON_sha256"]
    target.replace_file(stage.ARM, before[stage.ARM])
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
            "original_ARM9_and_overlay_preserved=False, ARM9_item_wrapping_bytes_only=True, "
            "original_overlay_preserved=True, hardware=False,",
    })
    exec(compile(startup_program, __file__ + "::startup", "exec"), env)
    env["startup_proof"](previous, candidate, arm)
    gameplay = {r["item_id"]: r for r in observed["cards"]}
    official, _ = stage.audit.review_sources()
    cases = {(r["item_ID"], r["page"], r["bitmap_mode"]): r for r in isolated["cases"]}
    assert len(cases) == 32
    for row in records:
        ident, number = row["item_ID"], row["message_ID"]
        assert entries[number].text.hex() == row["related_common_hex"]
        assert row["english"] == official[number][1]["english"]
        row["source_meaning"] = official[number][1]["source_meaning"]
        for page in ("main", "standalone"):
            for mode in (4, 16):
                case = cases[ident, page, mode]
                assert case["exact_ink_and_bounds"]
                assert [d["text"] for d in case["descriptions"]] == row["staged_reference"]["lines"]
        row["review"]["formatting"] = True
        row["registered_reference"] = row["staged_reference"] | {"candidate_sha256": candidate}
        row["gameplay_frame"] = gameplay[ident]["frame"]
        row["item_name"] = gameplay[ident]["name"]
    review = draft | dict(records=records, checked_story_format_guard=controls, observed_gameplay=observed,
                         original_renderer_checks=isolated, direct_visual_review=viewed, new_contextual_credit=0,
                         unchanged_pending_records=276, shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    validate_natural_dialogue_batch(review)
    return draft, review, archives


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
credit_rows = template[template.index('    assert (stage.COMMON, "COMMON_MESSAGE_99")'):template.index('    manifest["gallery_historic_sites_menu_pipeline"]')]
program = checked_text(template, {
    'len(manifest["batches"]) == 966 and len(manifest["checks"]) == 301':
        'len(manifest["batches"]) == 967 and len(manifest["checks"]) == 302',
    'release_stack_before_gallery_historic_sites_menu.json': 'release_stack_before_item_gallery_wraps.json',
    'release_stack_with_gallery_historic_sites_menu.json': 'release_stack_with_item_gallery_wraps.json',
    'live.PROOF, FULL, args.visual_review': 'live.PROOF, NATIVE, args.visual_review',
    'verified_historic_sites_predecessor=predecessor, gallery_historic_sites_menu_release=str(REVIEW)':
        'verified_gallery_historic_sites_menu_predecessor=predecessor, item_gallery_wraps_release=str(REVIEW)',
    'registered_gallery_historic_sites_menu_and_complete_parent_inverse': 'registered_item_gallery_wraps_and_complete_parent_inverse',
    'manifest["gallery_historic_sites_menu_pipeline"]': 'manifest["item_gallery_wraps_pipeline"]',
    credit_rows: '''    ids = manifest["changed_records"][stage.ARM]
    for row in draft["records"]:
        assert (stage.COMMON, f"COMMON_MESSAGE_{row['message_ID']}") in credited
        assert row["id"] not in ids
        ids.append(row["id"])
''',
    'existing_Gallery_heading_pointer=True, changed_archive_hashes=archives':
        'original_item_description_pointers=True, target_ARM9_sha256=archives[stage.ARM]',
    'changed_components=2, target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON],':
        'changed_components=1, target_ARM9_sha256=archives[stage.ARM],',
    'reviewed_UI_labels=1, previously_localized_records=2, new_contextual_records=0, prose_revisions=2, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0':
        'reviewed_UI_labels=0, previously_localized_records=8, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=8, justified_retentions=0',
    'ordinary_empty_Gallery=True, initialized_populated_Gallery=True, modal_and_title_returns=True, natural_discovery=False':
        'initialized_item_collection=True, original_Gallery_cards=8, compact_offline_cases=16, carousel_and_back=True, natural_acquisition=False',
    'ledger["gallery_historic_sites_menu_20261121"]': 'ledger["item_gallery_wraps_20261121"]',
    'prior_records_reviewed=2, actual_emulator_records=2, new_contextual_credit=0,\n        prose_revisions=2, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0':
        'prior_records_reviewed=8, actual_emulator_records=8, new_contextual_credit=0,\n        prose_revisions=0, spacing_revisions=0, wrap_only_revisions=8, justified_retentions=0',
    'Preserve the Historic Sites menu candidate or research ROM': 'Preserve the item-card wraps candidate or research ROM',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Item description wrap testing candidate

The [testing ROM](../../{ROM.as_posix()}) improves eight item description layouts. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Item description wrap fixes

Eight item descriptions keep their reviewed wording with improved wraps. The medical text keeps its two ingredients together, the cross keeps its full period underground on one row, and the parchment ends with a complete sentence. All eight keep their original pointers and allocated lengths. [Exact wording and layout references](../{REVIEW.as_posix()})

The original Items Gallery displayed all eight revised cards and one unchanged control, then wrapped and returned using a prepared collection save. The compact item panel and both bitmap modes were also checked through the original renderer offline. Six startup holds, 24 protected name getters and 17 focused tests passed. The patch reconstructs the exact ROM from the clean input. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + "::register", "exec"), env)


if __name__ == "__main__":
    env["main"]()
