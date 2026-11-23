"""Register the source-bound names of both starter ships in Maria's route."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_item_gallery_wraps_20261121 as parent
from scripts import stage_maria_starter_ship_names_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_maria_starter_ship_names_20261121 import PROOF as NATIVE


base, native, workflow = parent.base, parent.native, parent.env["workflow"]
startup_release = parent.startup_release
PROFILE = "all-routes-maria-starter-ship-names-v1-20261121"
ROOT = Path("out/maria_starter_ship_names_registered_20261121_v1")
ROM = ROOT / "Translation_DS_Maria_Starter_Ship_Names_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_maria_starter_ship_names_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_maria_starter_ship_names_registered_20261121.md")
STARTUP = stage.ROOT / "own_startup_verification.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
QA = stage.ROOT / "qa_passed_v2.xml"
live = SimpleNamespace(PROOF=stage.ROOT / "shipyard_verification.json")
CHECKPOINT = "Restored both full ship names in Maria’s starting fleet."


def verify(registry, previous, viewed):
    draft, in_game, models = map(base.load, (stage.PROOF, live.PROOF, NATIVE))
    candidate = base.digest(stage.ROM)
    assert candidate == draft["candidate_sha256"] == in_game["candidate_sha256"] == models["candidate_sha256"]
    assert base.digest(stage.CLEAN) == previous["clean_input_sha256"] == draft["clean_input_sha256"]
    assert base.digest(parent.ROM) == previous["candidate_sha256"] == draft["parent_sha256"]
    assert models["changed_model_name_fields"] == [0, 4, 147, 148]
    assert models["catalogue_classes"] == 39 and models["initialized_models"] == 155
    assert in_game["checked_model_IDs"] == [147, 148] and in_game["ordinary_controls"]
    assert not in_game["hardware"] and in_game["prepared_system_unlock"]
    assert viewed == in_game["sheets"] | models["sheets"]
    for evidence in (in_game["evidence"], models["evidence"], viewed):
        assert all(base.digest(path) == digest for path, digest in evidence.items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    clean, predecessor, target = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(native.files, (predecessor, target))
    assert before.keys() == after.keys() and {k for k in before if before[k] != after[k]} == {stage.ARM}
    arm, rows = stage.transform(clean, predecessor)
    assert arm == after[stage.ARM] and rows == draft["records"]
    archives = {stage.ARM: native.digest(arm)}
    assert archives[stage.ARM] == draft["target_ARM9_sha256"]
    target.replace_file(stage.ARM, before[stage.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())

    startup = startup_release.env["startup_check"].startup_proof
    context = startup.__globals__ | {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE}
    startup_program = checked_text(getsource(startup), {
        "assert old['core_options'] == new['core_options']":
            "assert old['core_options'] | {'desmume_pointer_type': 'touch'} == new['core_options']\n"
            "    assert old['core_options']['desmume_pointer_type'] == 'mouse'\n"
            "    assert all('touch' not in action for action in new['scripted_input_schedule'])",
        "original_ARM9_and_overlay_preserved=True, hardware=False,":
            "original_ARM9_and_overlay_preserved=False, ARM9_ship_name_data_only=True, "
            "original_overlay_preserved=True, startup_used_button_only_input=True, hardware=False,",
    })
    exec(compile(startup_program, __file__ + "::startup", "exec"), context)
    context["startup_proof"](previous, candidate, arm)
    for row in rows:
        row["review"]["formatting"] = True
        row["registered_reference"] = row["staged_reference"] | {"candidate_sha256": candidate}
    review = draft | dict(records=rows, encoder="dialogue-relocatable-v1",
        status="registered", checked_story_format_guard=controls, observed_gameplay=in_game,
        original_model_getters=models, direct_visual_review=viewed, unchanged_pending_records=276,
        shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    validate_natural_dialogue_batch(review)
    return draft, review, archives


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
credit = template[template.index("    ids = manifest"):template.index('    manifest["item_gallery_wraps_pipeline"]')]
program = checked_text(template, {
    'len(manifest["batches"]) == 967 and len(manifest["checks"]) == 302':
        'len(manifest["batches"]) == 968 and len(manifest["checks"]) == 303',
    'release_stack_before_item_gallery_wraps.json': 'release_stack_before_maria_starter_ship_names.json',
    'release_stack_with_item_gallery_wraps.json': 'release_stack_with_maria_starter_ship_names.json',
    'stage.ROOT / "translation.xdelta"': 'stage.ROOT / "research.xdelta"',
    'verified_gallery_historic_sites_menu_predecessor=predecessor, item_gallery_wraps_release=str(REVIEW)':
        'verified_item_gallery_wraps_predecessor=predecessor, maria_starter_ship_names_release=str(REVIEW)',
    'registered_item_gallery_wraps_and_complete_parent_inverse': 'registered_maria_starter_ship_names_and_complete_parent_inverse',
    'manifest["item_gallery_wraps_pipeline"]': 'manifest["maria_starter_ship_names_pipeline"]',
    credit: '''    ids = manifest["changed_records"][stage.ARM]
    for row in draft["records"]:
        assert row["id"] not in ids
        ids.append(row["id"])
''',
    'original_item_description_pointers=True': 'original_ship_model_ids=True',
    'reviewed_UI_labels=0, previously_localized_records=8, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=8':
        'reviewed_UI_labels=2, previously_localized_records=2, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0',
    'name_label_revisions=0, text_display_revisions=0, pagination_fixes=0, name_consistency_revisions=0':
        'name_label_revisions=2, text_display_revisions=0, pagination_fixes=0, name_consistency_revisions=2',
    'initialized_item_collection=True, original_Gallery_cards=8, compact_offline_cases=16, carousel_and_back=True, natural_acquisition=False':
        'ordinary_Maria_opening=True, original_Shipyard=True, displayed_ship_names=2, prepared_system_unlock=True, natural_unlock=False',
    'ledger["item_gallery_wraps_20261121"]': 'ledger["maria_starter_ship_names_20261121"]',
    'prior_records_reviewed=8, actual_emulator_records=8, new_contextual_credit=0':
        'prior_records_reviewed=2, actual_emulator_records=2, new_contextual_credit=0, name_label_revisions=2',
    'wrap_only_revisions=8, justified_retentions=0, text_display_revisions=0':
        'wrap_only_revisions=0, justified_retentions=0, text_display_revisions=0',
    'Preserve the item-card wraps candidate or research ROM': 'Preserve the Maria starter ship names candidate or research ROM',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Maria’s starting fleet testing candidate

The [testing ROM](../../{ROM.as_posix()}) restores the full names Chunshen and Huachang. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Maria’s starting ship names

Maria starts with **Chunshen** (春申) and **Huachang** (華昌). The earlier labels omitted the second Chinese character from each ship name. Both use Mandarin pinyin and retain the original Junk class. [Exact source and installed references](../{REVIEW.as_posix()})

The original Hangzhou Shipyard displayed both complete names after Maria’s opening. The replay used a prepared system unlock and standard controls. Offline checks covered all 39 class and 155 initialized ship records. The two names were the only model changes. Six startup holds, 24 protected name getters and 17 focused tests passed. [Testing ROM and exact patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
environment = parent.env | globals()
exec(compile(program, __file__ + "::register", "exec"), environment)


if __name__ == "__main__":
    environment["main"]()
