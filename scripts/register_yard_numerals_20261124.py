"""Register the posted Yard numeral correction after native and gameplay proof."""

import json
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_nagasaki_shipyard_20261124 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_yard_numerals_20261124 as build
from scripts import verify_yard_numerals_native_20261124 as native
from scripts.source_locked_derivation_v5118 import checked_text


template, yard, patch = parent.template, build.yard, build.patch
PROFILE = "all-routes-yard-numerals-v1-20261124"
CHECK = "registered_yard_numerals_and_complete_parent_inverse"
ARM, COMMON, ROM = build.ARM, build.COMMON, build.ROM
PATCH, PATCH_PROOF, REBUILT, STARTUP_CAPTURE = build.PATCH, build.PATCH_PROOF, build.REBUILT, build.STARTUP_CAPTURE
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_yard_numerals_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_yard_numerals.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_yard_numerals_registered_20261124.md")
CHECKPOINT = "Registered consistent Yard dialogue digits for prices, counts, discounts, durations, and refunds."
SHEET, PREVIEW = build.SHEET, build.ROOT / "portrait_sheet_01.png"
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.STORED)))


def verify(previous, visual_sha):
    stored, live, reconstructed, native_review = map(files.read, (build.STORED, build.PAIRED, PATCH_PROOF, native.OUT))
    candidate = files.digest(ROM)
    assert candidate == stored["candidate"]["sha256"] == live["candidate_sha256"] == native_review["candidate_sha256"] == files.digest(REBUILT)
    assert reconstructed["byte_exact"] and reconstructed["candidate"]["sha256"] == candidate and files.reference(PATCH) == reconstructed["patch"]
    assert reconstructed["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    assert previous["candidate_sha256"] == stored["previous"]["sha256"] == live["previous_sha256"] == native_review["predecessor_sha256"]
    assert stored["whole_parent_inverse"] and files.reference(build.STORED) == live["stored"] == native_review["patch_input"]
    assert live["ordinary_saved_game"] and not live["research_fixtures"] and not native_review["ordinary_gameplay"]
    assert [(r["frame"], r["message_ID"], r["line"]) for r in live["revised"]] == [(frame, *data) for frame, data in build.LIVE.items()]
    assert len(live["unchanged_frames"]) == 53 and not live["menu_highlight_only"]
    assert files.reference(build.BEFORE) == live["before"] and files.reference(build.REPLAY) == live["after"]
    visuals = list(map(files.reference, (SHEET, PREVIEW)))
    assert live["sheet"] == visuals[0] and len(native_review["sheets"]) == 1
    assert files.reference(native_review["sheets"][0]["path"]) == visuals[1] and native_review["sheets"][0]["sha256"] == visuals[1]["sha256"]
    assert files.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha
    assert native_review["unique_number_cases"] == 1058 and native_review["layout_cases"] == 204
    assert len(native_review["number_callers"]) == 16 and len(native_review["records"]) == 13

    clean, old, new = map(files.NdsImage.open, (files.CLEAN, previous["candidate"], ROM))
    original_arm, before, target = clean.read_file(ARM), old.read_file(ARM), new.read_file(ARM)
    assert files.sha256(before).hexdigest() == previous["target_ARM9_sha256"]
    assert files.sha256(target).hexdigest() == stored["target_ARM9_sha256"]
    shared_bytes = new.read_file(COMMON)
    assert shared_bytes == old.read_file(COMMON) and files.sha256(shared_bytes).hexdigest() == previous["target_COMMON_sha256"]
    expected, changes, suffix = patch.propose(before, original_arm)
    assert expected == target and changes == stored["instruction_changes"] and suffix == stored["suffix_callers"]
    assert template.right_bound(target, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    new.replace_file(ARM, before)
    assert bytes(new.rom.save()) == Path(previous["candidate"]).read_bytes()
    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "nine_Yard_number_branches_and_startup_extent_preserved",
    })
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, target)

    prior = files.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    entries = yard.common_rows(shared_bytes, target)
    assert shared["candidate_sha256"] == previous["candidate_sha256"] and len(shared["records"]) == 276
    assert all(yard.panels.text_reference(entries[row["message_ID"]]) == row["installed"] for row in shared["records"])
    archived = parent.parent.archived
    bounded = files.read(archived.OUT)
    wrappers = set(bounded["checked_wrapper_entries"])
    candidate_rom = files.NdsImage.open(ROM)
    assert archived.references(candidate_rom, wrappers, installed=True) == [tuple(r) for r in bounded["current_external_references"]]
    assert json.loads(json.dumps(archived.reader.references(ROM))) == bounded["filename_directory_and_offset_literal_readers"]
    outcome = native_review | dict(visual_review=visuals, stored_proof=files.reference(build.STORED),
        gameplay=files.reference(build.PAIRED), source_review=files.reference(native.OUT), changed_ARM9_calls=changes,
        target_ARM9_sha256=stored["target_ARM9_sha256"], target_COMMON_sha256=stored["target_COMMON_sha256"],
        source_credit_added=0, native_patch_module=files.reference(Path(patch.__file__)),
        unchanged_archived_message_reader_evidence=files.reference(archived.OUT),
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
old_record_update = parent.prepare[parent.prepare.index('        revised = [row["id"]'):parent.prepare.index('        update = dict(profile=')]
prepare = checked_text(parent.prepare, {
    "verified_nagasaki_tavern_recruitment_predecessor=predecessor, nagasaki_yard_reflow_release=str(REVIEW)":
        "verified_nagasaki_yard_reflow_predecessor=predecessor, yard_numerals_release=str(REVIEW)",
    "len(batches) == 1123 and len(checks) == 458": "len(batches) == 1124 and len(checks) == 459",
    "assert COMMON in paths and COMMON in records and CHECK not in checks": "assert ARM in paths and ARM in records and CHECK not in checks",
    old_record_update: '''        assert all(row["decision"] == "retention" for row in outcome["records"])
        revised = [f"ARM9_{row['address']:08X}_YARD_NUMERAL_BRANCH" for row in outcome["changed_ARM9_calls"]]
        assert len(revised) == 9
        records[ARM].extend(ident for ident in revised if ident not in records[ARM])
''',
    "snapshot_scope=COMMON": "snapshot_scope=ARM",
    'nagasaki_yard_reflow_release_proof=stage.reference(stage.PROOF), visual_review=outcome["visual_review"]':
        'yard_numerals_release_proof=stage.reference(stage.PROOF), native_patch=outcome["native_patch_module"], visual_review=outcome["visual_review"]',
    '"nagasaki_yard_reflow_pipeline"': '"yard_numerals_pipeline"',
    "build.PAIRED, SAIL_PREVIEW, RENAME_PREVIEW, yard.OUT, build.preflight.OUT, NATIVE_FONT": "build.PAIRED, PREVIEW, native.OUT",
    "registered_manifest_entries=1124, passing_release_checks=459, changed_components=1, changed_internal_files=[COMMON]":
        "registered_manifest_entries=1125, passing_release_checks=460, changed_components=1, changed_internal_files=[ARM]",
    'target_COMMON_sha256=outcome["target_COMMON_sha256"]': 'target_COMMON_sha256=outcome["target_COMMON_sha256"], target_ARM9_sha256=outcome["target_ARM9_sha256"]',
    "contextual_records_revisited=13, contextual_decisions_reused=10, previously_localized_records=13":
        "contextual_records_revisited=13, contextual_decisions_reused=13, previously_localized_records=13",
    "prose_revisions=3, justified_retentions=10, text_display_revisions=3": "prose_revisions=0, justified_retentions=13, text_display_revisions=13",
    "ordinary_Nagasaki_Yard=True, revised_gameplay_holds=4, native_pages=3, unchanged_gameplay_holds=47, background_highlight_only_holds=4":
        "ordinary_Nagasaki_Yard=True, revised_gameplay_holds=2, native_pages=15, unchanged_gameplay_holds=53",
    "prose_revisions=3, wrap_only_revisions=0, texts_retained=10": "prose_revisions=0, wrap_only_revisions=0, texts_retained=13",
    '"nagasaki_yard_reflow_20261124"': '"yard_numerals_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Yard numeral testing candidate

The Shipwright uses regular dialogue digits in Yard offers, counts, durations, and discounts. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Nagasaki Yard reflow candidate": "Preserve the registered Yard numeral candidate",
    "1,124 entries and 459 passing checks": "1,125 entries and 460 passing checks",
    doc: '''    DOC.write_text(f"""# Consistent Yard numerals

The Shipwright's mast count, durability, and 7,500-gold offer now use the regular dialogue digits. The ordinary Nagasaki replay verified both corrected panels, their controls, and the return to town. All 53 comparison frames match pixel for pixel. [Actual before and after](../{VERIFY.as_posix()}/{SHEET.name})

The Yard reuses the registered Inn digit helper on 16 verified numeric call sites. Counts, currencies, singular and plural units, duration values, and template bytes retain their meaning and structure. The 13 wording retentions have exact source and installed references. Offline proof covers 1,058 number executions and 204 bounded layouts. The 15 native pages include both amounts seen in gameplay. [Exact source, formatting, and tests](../{REVIEW.as_posix()}) · [Native previews](../{VERIFY.as_posix()}/{PREVIEW.name})

The cumulative candidate passed startup, 460 release checks, and 17 focused tests. Applying the patch to the clean ROM reconstructs the candidate byte for byte. The discount, refund, preparation, and paid repair outcomes have offline coverage in this batch. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    cli = template.ArgumentParser(description=__doc__)
    cli.add_argument("--visual-sha256")
    cli.add_argument("--finish-only", action="store_true")
    args = cli.parse_args()
    assert args.finish_only or args.visual_sha256
    scope = vars(template) | vars(parent.parent.parent.parent) | vars(parent.parent.parent) | vars(parent.parent) | vars(parent) | globals()
    exec(compile(prepare + "\n" + finish, __file__ + "::yard-numeral-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
