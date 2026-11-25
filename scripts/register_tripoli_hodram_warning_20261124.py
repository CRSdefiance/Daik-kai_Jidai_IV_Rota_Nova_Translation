"""Register the Tripoli warning and its paired ordinary story replay."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_tavern_sighting_rumor_20261124 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_tripoli_hodram_warning_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


review = build
ARM, COMMON, STORY, ROM = build.ARM, build.COMMON, build.STORY, build.ROM
PROFILE = "all-routes-tripoli-hodram-warning-v1-20261124"
CHECK = "registered_tripoli_hodram_warning_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_tripoli_hodram_warning_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_tripoli_hodram_warning.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_tripoli_hodram_warning_registered_20261124.md")
CHECKPOINT = "Registered the Port Worker's more natural warning to Hodram at Tripoli."
LEVEL_UPS = review.OUT.with_name("syracuse_level_ups_20261124.json")
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=build.STORED)))
template = parent.template


def verify(previous, visual_sha):
    packet, stored, live, patch = map(files.read, (review.OUT, build.STORED, build.PAIRED, PATCH_PROOF))
    candidate = files.digest(ROM)
    assert candidate == stored["candidate_sha256"] == live["candidate_sha256"] == files.digest(REBUILT)
    assert patch["byte_exact"] and patch["candidate"]["sha256"] == candidate and patch["patch"] == files.reference(PATCH)
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == stored["clean_input_sha256"] == files.digest(files.CLEAN)
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == live["predecessor_sha256"] == packet["candidate_sha256"]
    assert stored["whole_parent_inverse"] and stored["unchanged_archive_directory"]
    assert stored["source_preflight"] == files.reference(review.OUT) and live["stored"] == files.reference(build.STORED)
    assert live["source"] == files.reference(build.BEFORE) and live["replay"] == files.reference(build.AFTER)
    assert packet["ordinary_gameplay"] and live["ordinary_gameplay"]
    voyage = files.read(LEVEL_UPS)
    assert voyage["candidate_sha256"] == candidate and voyage["paired_parent_sha256"] == previous["candidate_sha256"]
    assert len(voyage["holds"]) == 3 and all(row["geometry"]["complete_ink_and_blank_cells_exact"] for row in voyage["holds"])
    assert live["changed_frame"]["frame"] == build.HOLD and build.END in live["unchanged_frames"]
    assert len(live["unchanged_frames"]) == len(build.panels.shots(files.read(build.BEFORE), "_navigation.png")) - 1
    visuals = [files.reference(build.SHEET), files.reference(build.PREVIEW)]
    assert visuals == [live["visual"], stored["native_preview"]] and visuals[1] == packet["native_preview"]
    assert files.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    clean, old, new = map(files.NdsImage.open, (files.CLEAN, previous["candidate"], ROM))
    before, after = map(build.fixed.previous.native.files, (old, new))
    assert before.keys() == after.keys() and {key for key in before if before[key] != after[key]} == {STORY}
    for path, field in ((ARM, "target_ARM9_sha256"), (COMMON, "target_COMMON_sha256")):
        assert files.sha256(after[path]).hexdigest() == previous[field] == stored[field]
    assert files.sha256(after[STORY]).hexdigest() == stored["target_SC1_sha256"]
    assert template.right_bound(after[ARM], previous["right_bound_configuration"])["matched_repair_spans"] == 8
    former, current = [build.IlnkContainer.parse(archive[STORY]).blocks for archive in (before, after)]
    assert [i for i, (a, b) in enumerate(zip(former, current, strict=True)) if a != b] == [build.BLOCK]
    block, old_block = current[build.BLOCK], former[build.BLOCK]
    assert files.sha256(block).hexdigest() == stored["target_block_sha256"]
    edit = stored["edit"]
    offset = edit["command_offset"]
    old_command, new_command = [bytes.fromhex(edit[key]) for key in ("before_hex", "after_hex")]
    assert len(old_command) == len(new_command) and old_command[:6] == new_command[:6]
    assert edit["allocation_and_termination_preserved"] and live["changed_frame"]["body_mask_sha256"] == edit["page_sha256"]
    assert block[offset:offset + len(new_command)] == new_command
    assert block[:offset] + old_command + block[offset + len(new_command):] == old_block
    new.replace_file(STORY, before[STORY])
    assert files.sha256(new.rom.save()).hexdigest() == previous["candidate_sha256"]
    del old, new

    source_block = build.IlnkContainer.parse(clean.read_file(STORY)).blocks[build.BLOCK]
    source_common = build.panels.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    installed_common = build.panels.common_rows(after[COMMON], after[ARM])
    del clean
    rows = []
    for row in packet["records"]:
        if "message_ID" in row:
            key = row["message_ID"]
            jp, en = source_common[key], installed_common[key]
            assert jp.text.hex() == row["source_reference"]["exact_hex"]
            assert en.text.hex() == row["current_reference"]["exact_hex"]
            registered = row["installed_reference"] | dict(candidate_sha256=candidate)
        else:
            original = build.panels.exact_command(source_block, row["source_reference"])
            ref = row["current_reference"]
            previous_command = build.panels.exact_command(old_block, ref)
            at = ref["command_offset"]
            found = new_command if row["id"] == build.KEY else previous_command
            assert found[:6] == original[:6] == previous_command[:6]
            assert block[at:at + len(found)] == found
            assert " ".join(build.bytes_for(found).decode("ascii").split()) == row["english"]
            registered = ref | dict(exact_command_hex=found.hex(), archive_sha256=stored["target_SC1_sha256"],
                                    block_sha256=stored["target_block_sha256"], candidate_sha256=candidate)
        rows.append(row | dict(registered_reference=registered))
    assert len(rows) == 11 and sum(row["decision"] == "revision" for row in rows) == 1

    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "Tripoli_story_preserves_ARM9_and_startup_extent",
    })
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, after[ARM])

    prior = files.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    assert all(build.panels.text_reference(installed_common[row["message_ID"]]) == row["installed"] for row in shared["records"])
    result = dict(translation_policy=packet["translation_policy"], target_locale=packet["target_locale"],
        encoder=packet["encoder"], review_gates=packet["review_gates"], records=rows, candidate_sha256=candidate,
        target_ARM9_sha256=stored["target_ARM9_sha256"], target_COMMON_sha256=stored["target_COMMON_sha256"],
        target_SC1_sha256=stored["target_SC1_sha256"], visual_review=visuals, stored_proof=files.reference(build.STORED),
        gameplay=files.reference(build.PAIRED), additional_voyage_holds=files.reference(LEVEL_UPS), source_credit_added=0, shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


start = parent.prepare.index('        revised = [row["id"]')
old_update = parent.prepare[start:parent.prepare.index("        update = dict(profile=", start)]
readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_istanbul_tavern_rumor_predecessor=predecessor, tavern_sighting_rumor_release=str(REVIEW)":
        "verified_tavern_sighting_rumor_predecessor=predecessor, tripoli_hodram_warning_release=str(REVIEW)",
    "len(batches) == 1131 and len(checks) == 466": "len(batches) == 1132 and len(checks) == 467",
    "assert {ARM, COMMON} <= set(paths) and {ARM, COMMON} <= records.keys()":
        "assert {ARM, COMMON, STORY} <= set(paths) and {ARM, COMMON, STORY} <= records.keys()",
    old_update: '''        revised = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]
        assert revised == [build.KEY] and len(outcome["records"]) == 11
        records[STORY].extend(ident for ident in revised if ident not in records[STORY])
''',
    "snapshot_scope=COMMON": "snapshot_scope=STORY",
    "tavern_sighting_rumor_release_proof=stage.reference(stage.PROOF)": "tripoli_hodram_warning_release_proof=stage.reference(stage.PROOF)",
    '"tavern_sighting_rumor_pipeline"': '"tripoli_hodram_warning_pipeline"',
    "stage.PROOF, build.NATIVE, review.OUT": "stage.PROOF, build.PAIRED, review.OUT, LEVEL_UPS",
    'target_COMMON_sha256=outcome["target_COMMON_sha256"], target_ARM9_sha256=outcome["target_ARM9_sha256"],':
        'target_COMMON_sha256=outcome["target_COMMON_sha256"], target_ARM9_sha256=outcome["target_ARM9_sha256"], '
        'target_SC1_sha256=outcome["target_SC1_sha256"],',
    "registered_manifest_entries=1132, passing_release_checks=467, changed_components=1, changed_internal_files=[COMMON]":
        "registered_manifest_entries=1133, passing_release_checks=468, changed_components=1, changed_internal_files=[STORY]",
    "contextual_records_revisited=2, contextual_decisions_reused=1, previously_localized_records=2":
        "contextual_records_revisited=11, contextual_decisions_reused=10, previously_localized_records=11",
    "prose_revisions=1, justified_retentions=1, text_display_revisions=1":
        "prose_revisions=1, justified_retentions=10, text_display_revisions=1",
    "representative_Tavern_gameplay_carried_forward=True, revised_gameplay_holds=0, native_pages=7, native_item_region_cases=121":
        'ordinary_Syracuse_to_Tripoli=True, revised_gameplay_holds=1, native_pages=1, '
        'unchanged_gameplay_holds=len(stage.read(build.PAIRED)["unchanged_frames"])',
    "prose_revisions=1, wrap_only_revisions=0, texts_retained=1": "prose_revisions=1, wrap_only_revisions=0, texts_retained=10",
    '"tavern_sighting_rumor_20261124"': '"tripoli_hodram_warning_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's Tripoli warning testing candidate

The Port Worker tells Hodram to head for safer waters. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Tavern sighting rumor candidate": "Preserve the registered Tripoli Hodram warning candidate",
    "1,132 entries and 467 passing checks": "1,133 entries and 468 passing checks",
    doc: '''    DOC.write_text(f"""# Hodram's warning at Tripoli

The Port Worker keeps the dangerous person unnamed and tells Hodram, **Trust me. Head for safer waters.** The advice keeps the original warning and sounds natural in the worker's voice. Four other story turns and six surrounding shared responses retain their wording. [Clean Japanese, installed references and reasons](../{REVIEW.as_posix()})

Ordinary controls sailed from Syracuse, discovered Tripoli and reached the complete warning exchange. The paired replays verify the revised page, the original Port Worker nameplate, the 282-gold resupply and the refusal to Auto Move to Lisbon. The voyage ends in Tripoli. [Paired gameplay](../{VERIFY.as_posix()}/{build.SHEET.name})

The candidate changes only Hodram's story archive and passed startup, 468 release checks, 17 focused tests and byte-exact clean-input reconstruction. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--visual-sha256")
    parser.add_argument("--finish-only", action="store_true")
    args = parser.parse_args()
    assert args.finish_only or args.visual_sha256
    lineage = [parent]
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 12:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(prepare + "\n" + finish, __file__ + "::Tripoli-warning-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
