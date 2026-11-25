"""Register the roster crop and Galley reflow with exact Lisbon replay proof."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_village_article_wraps_20261124 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_lisbon_roster_galley_20261124 as build
from scripts import verify_lisbon_roster_galley_replay_20261124 as gameplay
from scripts.source_locked_derivation_v5118 import checked_text


review, template = build, parent.template
ARM, COMMON, ROM = build.ARM, build.COMMON, build.ROM
PROFILE = "all-routes-lisbon-roster-galley-v1-20261124"
CHECK = "registered_lisbon_roster_galley_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_lisbon_roster_galley_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_lisbon_roster_galley.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_lisbon_roster_galley_registered_20261124.md")
CHECKPOINT = "Registered the complete crew roster value and the Galley phrase wrap."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=build.STORED)))


def verify(previous, visual_sha):
    packet, stored, live, patch = map(files.read, (build.OUT, build.STORED, gameplay.OUT, PATCH_PROOF))
    candidate = files.digest(ROM)
    assert candidate == files.digest(REBUILT) == stored["candidate_sha256"] == live["candidate_sha256"] == packet["candidate_sha256"]
    assert patch["byte_exact"] and patch["candidate"]["sha256"] == candidate and patch["patch"] == files.reference(PATCH)
    assert previous["candidate_sha256"] == packet["previous_sha256"] == live["predecessor_sha256"] == stored["predecessor_sha256"]
    assert files.digest(files.CLEAN) == patch["clean_input_sha256"] == previous["clean_input_sha256"]
    assert stored["source_preflight"] == files.reference(build.OUT) and stored["whole_parent_inverse"]
    assert live["ordinary_play"] and live["exact_later_clue_inverse"] and gameplay.END in live["unchanged_frames"]
    assert live["full_roster_summary"]["complete_summary"]["ink_pixels"] == 122
    assert {row["frame"] for row in live["galley"]} == gameplay.GALLEY
    assert len(packet["all_native_stat_names"]) == 55
    assert all(case["complete_4_and_16_bit"] and case["native_final_x"] <= build.WIDTH for case in packet["all_native_stat_names"])
    assert len(packet["native_galley"]["records"]) == 1
    assert packet["native_galley"]["records"][0]["complete_independent_font_plane_equal"]
    declared = live["sheets"] + packet["native_galley"]["review_sheets"]
    visible = [files.reference(row["path"]) for row in declared]
    assert [row["sha256"] for row in visible] == [row["sha256"] for row in declared]
    assert files.sha256("".join(row["sha256"] for row in visible).encode("ascii")).hexdigest() == visual_sha
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    original, old, new = map(files.NdsImage.open, (files.CLEAN, previous["candidate"], ROM))
    before, after = map(parent.parent.parent.trend.files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {ARM, COMMON}
    arm, common = after[ARM], after[COMMON]
    assert files.sha256(arm).hexdigest() == stored["target_ARM9_sha256"]
    assert files.sha256(common).hexdigest() == stored["target_COMMON_sha256"]
    at = build.WIDTH_AT
    field, galley = packet["records"]
    assert field["id"] == build.FIELD_ID and galley["message_ID"] == build.KEY
    assert arm[at:at + 4].hex() == field["installed_reference"]["exact_width_hex"]
    assert before[ARM][at:at + 4].hex() == field["current_reference"]["exact_width_hex"]
    assert original.read_file(ARM)[at:at + 4].hex() == field["source_reference"]["exact_width_hex"]
    assert arm[:at] + before[ARM][at:at + 4] + arm[at + 4:] == before[ARM]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    panels = gameplay.panels
    jp = build.common_message_entries(original.read_file(COMMON), original.read_file(ARM))
    previous_rows, current = (panels.common_rows(source, arm) for source in (before[COMMON], common))
    assert [item.message_id for ref, item in zip(previous_rows, current, strict=True) if ref != item] == [build.KEY]
    for table, key in ((jp, "source_reference"), (previous_rows, "current_reference"), (current, "installed_reference")):
        assert table[build.KEY].text.hex() == galley[key]["exact_hex"]
    for component in (ARM, COMMON):
        new.replace_file(component, before[component])
    assert files.sha256(new.rom.save()).hexdigest() == previous["candidate_sha256"]

    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    startup = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "Roster_width_keeps_registered_pool_startup_exact",
    })
    exec(compile(startup, __file__ + "::bound-startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)
    prior = files.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    assert all(panels.text_reference(current[row["message_ID"]]) == row["installed"] for row in shared["records"])
    records = [r | dict(registered_reference=r["installed_reference"] | dict(candidate_sha256=candidate)) for r in (field, galley)]
    reviewed = dict(translation_policy=packet["translation_policy"], target_locale=packet["target_locale"],
        encoder=packet["encoder"], review_gates=packet["review_gates"], records=records, candidate_sha256=candidate,
        target_ARM9_sha256=stored["target_ARM9_sha256"], target_COMMON_sha256=stored["target_COMMON_sha256"],
        visual_review=visible, stored_proof=files.reference(build.STORED), gameplay=files.reference(gameplay.OUT),
        roster_native_cases=55, galley_native_pages=1, source_credit_added=0,
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(reviewed)
    return reviewed


start = parent.prepare.index('        revised = [row["id"]')
update = parent.prepare[start:parent.prepare.index("        update = dict(profile=", start)]
readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_village_clue_punctuation_predecessor=predecessor, village_article_wraps_release=str(REVIEW)":
        "verified_village_article_wraps_predecessor=predecessor, lisbon_roster_galley_release=str(REVIEW)",
    "len(batches) == 1135 and len(checks) == 470": "len(batches) == 1136 and len(checks) == 471",
    update: '''        revised = [row["id"] for row in outcome["records"]]
        assert revised == [build.FIELD_ID, f"COMMON_MESSAGE_{build.KEY}"]
        for row in outcome["records"]:
            asset = records[row["file_path"]]
            if row["id"] not in asset:
                asset.append(row["id"])
''',
    "snapshot_scope=ARM": "snapshot_scope=[ARM, COMMON]",
    "village_article_wraps_release_proof=stage.reference(stage.PROOF)": "lisbon_roster_galley_release_proof=stage.reference(stage.PROOF)",
    '"village_article_wraps_pipeline"': '"lisbon_roster_galley_pipeline"',
    "registered_manifest_entries=1136, passing_release_checks=471, changed_components=1, changed_internal_files=[ARM]":
        "registered_manifest_entries=1137, passing_release_checks=472, changed_components=2, changed_internal_files=[ARM, COMMON]",
    "contextual_records_revisited=3, contextual_decisions_reused=0, previously_localized_records=3":
        "contextual_records_revisited=2, contextual_decisions_reused=0, previously_localized_records=2",
    "prose_revisions=0, justified_retentions=0, text_display_revisions=3, phrase_wrap_adjustments=3, punctuation_fields=0":
        "prose_revisions=0, justified_retentions=0, text_display_revisions=2, phrase_wrap_adjustments=1, punctuation_fields=0",
    "position_only_Avacha=True, revised_gameplay_holds=1, native_pages=3":
        'ordinary_Lisbon_crew_and_trade=True, revised_gameplay_holds=3, native_pages=1, roster_native_cases=55',
    "prose_revisions=0, phrase_wrap_adjustments=3, punctuation_fields=0, texts_retained=0":
        "prose_revisions=0, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=0",
    '"village_article_wraps_20261124"': '"lisbon_roster_galley_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Lisbon roster and Galley testing candidate

The crew roster displays all three Finance digits. The Galley help keeps food and water together. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered village article-wrap candidate": "Preserve the registered Lisbon roster and Galley candidate",
    "1,136 entries and 471 passing checks": "1,137 entries and 472 passing checks",
    doc: '''    DOC.write_text(f"""# Lisbon crew roster and Galley help

Julio's roster summary displays **Finance 115** in full. The native stat row now uses a 72-pixel crop. The existing label and number formats were checked for all ten skill names and the separate Level format. The Galley groups **food and water** on one line while preserving the cook's effect on supplies and fatigue. [Exact source and register bindings](../{REVIEW.as_posix()})

Ordinary gameplay replayed the Lisbon Yard, Deck assignment and Market settlement. It verified the restored digit, the Galley help at both visits, and the unchanged assignment and payment results. [Crew roster comparison](../{VERIFY.as_posix()}/lisbon_roster_paired_1_20261123.png) [Galley comparison](../{VERIFY.as_posix()}/lisbon_galley_paired_1_20261123.png)

The cumulative candidate passed its own startup, 472 release checks, 17 focused tests and byte-exact clean-input reconstruction. [Testing package](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--visual-sha256")
    cli.add_argument("--finish-only", action="store_true")
    args = cli.parse_args()
    assert args.finish_only or args.visual_sha256
    lineage = [parent]
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 16:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(prepare + "\n" + finish, __file__ + "::Lisbon-display-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
