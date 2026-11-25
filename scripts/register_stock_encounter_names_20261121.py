"""Register the five model names and preserve the original result and inspection consumers."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_maria_starter_ship_names_20261121 as parent
from scripts import stage_stock_encounter_names_20261121 as stage
from scripts import verify_stock_encounter_names_20261121 as checked
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
PROFILE = "all-routes-stock-encounter-names-v1-20261121"
ROOT = Path("out/stock_encounter_names_registered_20261121_v1")
ROM = ROOT / "Translation_DS_Stock_Encounter_Names_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_stock_encounter_names_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_stock_encounter_names_registered_20261121.md")
STARTUP = stage.ROOT / "own_startup_verification.json"
STARTUP_CAPTURE = checked.STARTUP_CAPTURE
QA = stage.ROOT / "qa_passed.xml"
live = SimpleNamespace(PROOF=checked.PROOF)
CHECKPOINT = "Localized the five stock encounter model names and verified their victory and inspection paths."


def verify(registry, previous, viewed):
    draft, verified = map(base.load, (stage.PROOF, checked.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == draft["candidate_sha256"] == verified["candidate_sha256"]
    assert base.digest(stage.CLEAN) == previous["clean_input_sha256"] == draft["clean_input_sha256"]
    assert base.digest(parent.ROM) == previous["candidate_sha256"] == draft["parent_sha256"]
    assert verified["catalogue"] == dict(classes_checked=39, models_checked=155,
        exclusively_changed_model_name_fields=[149, 150, 151, 152, 153])
    assert len(verified["native_victory_portraits"]) == 25
    assert verified["actual_inspection"]["returned_to_Info_Mode"] and not verified["actual_inspection"]["natural_victory"]
    assert viewed == verified["sheets"] and len(viewed) == 3
    for evidence in (verified["evidence"], viewed):
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

    startup = parent.startup_release.env["startup_check"].startup_proof
    context = startup.__globals__ | {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE}
    source = checked_text(getsource(startup), {
        "original_ARM9_and_overlay_preserved=True, hardware=False,":
            "original_ARM9_and_overlay_preserved=False, ARM9_stock_model_pointers_only=True, "
            "original_overlay_preserved=True, hardware=False,",
    })
    exec(compile(source, __file__ + "::startup", "exec"), context)
    context["startup_proof"](previous, candidate, arm)

    for row in rows:
        row["review"]["formatting"] = True
        model = row["model_ID"]
        row["registered_reference"] = row["staged_reference"] | {"candidate_sha256": candidate}
        row["original_native_provider"] = verified["original_victory_provider"][str(model)]
    review = draft | dict(records=rows, encoder="dialogue-relocatable-v1", status="registered",
        checked_story_format_guard=controls, actual_inspection=verified["actual_inspection"],
        native_victory_portraits=verified["native_victory_portraits"], direct_visual_review=viewed,
        unchanged_pending_records=276, shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    validate_natural_dialogue_batch(review)
    return draft, review, archives


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 968 and len(manifest["checks"]) == 303':
        'len(manifest["batches"]) == 969 and len(manifest["checks"]) == 304',
    'release_stack_before_maria_starter_ship_names.json': 'release_stack_before_stock_encounter_names.json',
    'release_stack_with_maria_starter_ship_names.json': 'release_stack_with_stock_encounter_names.json',
    'live.PROOF, NATIVE, args.visual_review': 'live.PROOF, args.visual_review',
    'verified_item_gallery_wraps_predecessor=predecessor, maria_starter_ship_names_release=str(REVIEW)':
        'verified_maria_starter_ship_names_predecessor=predecessor, stock_encounter_names_release=str(REVIEW)',
    'registered_maria_starter_ship_names_and_complete_parent_inverse': 'registered_stock_encounter_names_and_complete_parent_inverse',
    'manifest["maria_starter_ship_names_pipeline"]': 'manifest["stock_encounter_names_pipeline"]',
    'reviewed_UI_labels=2, previously_localized_records=2, new_contextual_records=0':
        'reviewed_UI_labels=5, previously_localized_records=5, new_contextual_records=0',
    'name_label_revisions=2': 'name_label_revisions=5',
    'name_consistency_revisions=2': 'name_consistency_revisions=5',
    'ordinary_Maria_opening=True, original_Shipyard=True, displayed_ship_names=2, prepared_system_unlock=True, natural_unlock=False':
        'initialized_Ghost_Ship_inspection=True, native_victory_portraits=25, natural_victory=False',
    'ledger["maria_starter_ship_names_20261121"]': 'ledger["stock_encounter_names_20261121"]',
    'prior_records_reviewed=2, actual_emulator_records=2, new_contextual_credit=0':
        'prior_records_reviewed=5, actual_inspection_control=1, offline_victory_portraits=25, new_contextual_credit=0',
    'Preserve the Maria starter ship names candidate or research ROM': 'Preserve the stock encounter names candidate or research ROM',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Stock encounter names testing candidate

The [testing ROM](../../{ROM.as_posix()}) initializes all five stock encounter models with the existing English victory names. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Stock encounter model names

The original victory announcer reads the name of the model attached to the encounter fleet. The five models now initialize with the full English names **Monster Fish**, **Giant Squid**, **Shark**, **White Whale** and **Ghost Ship**. The separate inspection class still reads **Whale** for the White Whale model. [Exact source and installed references](../{REVIEW.as_posix()})

An initialized Ghost Ship replay verified the inspection tooltip, information notice and return to Info Mode. Offline runs checked all five model arguments through the original victory handler and rendered each with the five victory voice alternatives. All 25 portraits match the previously reviewed English display. Natural spawns, a complete special-target victory and hardware remain unvisited.

The candidate passed six startup holds, 24 protected name getters and 17 focused tests. The patch reconstructs the exact ROM from clean input. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
environment = parent.environment | globals()
exec(compile(program, __file__ + "::register", "exec"), environment)


if __name__ == "__main__":
    environment["main"]()
