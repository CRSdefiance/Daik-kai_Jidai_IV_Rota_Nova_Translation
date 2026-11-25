"""Register the alternate Tavern sighting rumor after native and release checks."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_istanbul_tavern_rumor_20261124 as parent
from scripts import register_tunis_shop_advice_20261124 as common_template
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_tavern_sighting_rumor_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


review, trend = build.review, build.trend
ARM, COMMON, ROM = review.ARM, review.COMMON, build.ROM
PROFILE = "all-routes-tavern-sighting-rumor-v1-20261124"
CHECK = "registered_tavern_sighting_rumor_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_tavern_sighting_rumor_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_tavern_sighting_rumor.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_tavern_sighting_rumor_registered_20261124.md")
CHECKPOINT = "Registered the alternate Tavern sighting rumor with complete item and region names."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=build.STORED)))
template = parent.template


def visuals(preflight):
    return [files.reference(row["path"]) for row in preflight["proposed_sheets"]]


baseline = getsource(common_template.verify)
old_live = baseline[baseline.index('    assert live["before"]'):baseline.index('    assert files.sha256("".join')]
verify_source = checked_text(baseline, {
    "build.PAIRED": "build.NATIVE",
    old_live: '''    assert live["ordinary_representative_consumer"] == preflight["ordinary_representative_consumer"]
    assert live["ordinary_representative_consumer"] == files.reference(parent.REVIEW)
    assert live["ordinary_representative_paired_gameplay"] == files.reference(parent.build.PAIRED)
    assert live["exact_reused_consumer_dependencies"]["ARM9_sha256"] == previous["target_ARM9_sha256"]
    assert live["exact_reused_consumer_dependencies"]["unchanged_870_archived_record"]
    assert len(live["installed_loader_and_formatter"]) == 3
    assert preflight["previous_item_names_split"] == 89 and preflight["proposed_item_names_split"] == 0
    assert len(preflight["native_cases"]) == 121
    visible = visuals(preflight)
    assert visible == [dict(path=Path(row["path"]).as_posix(), sha256=row["sha256"])
                       for row in preflight["proposed_sheets"]]
''',
    "tunis_advice_keeps_ARM9_and_startup_extent_exact": "Tavern_sighting_keeps_ARM9_and_startup_extent_exact",
    "gameplay=files.reference(build.PAIRED)": "installed_native=files.reference(build.NATIVE)",
    "native_goods_cases=124": "native_item_region_cases=121, ordinary_sighting_activation_observed=False",
})

start = parent.prepare.index('        revised = [row for row in outcome["records"]')
old_update = parent.prepare[start:parent.prepare.index("        update = dict(profile=", start)]
old_copies = 'stage.SHEET, stage.PROOF, build.PAIRED, review.OUT,\n        *(Path(row["path"]) for row in outcome["visual_review"][1:])'
readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_maria_captured_ship_predecessor=predecessor, istanbul_tavern_rumor_release=str(REVIEW)":
        "verified_istanbul_tavern_rumor_predecessor=predecessor, tavern_sighting_rumor_release=str(REVIEW)",
    "len(batches) == 1130 and len(checks) == 465": "len(batches) == 1131 and len(checks) == 466",
    old_update: '''        revised = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]
        assert revised == [f"COMMON_MESSAGE_{review.KEY}"] and len(outcome["records"]) == 2
        records[COMMON].extend(ident for ident in revised if ident not in records[COMMON])
''',
    "snapshot_scope=[ARM, COMMON]": "snapshot_scope=COMMON",
    "istanbul_tavern_rumor_release_proof=stage.reference(stage.PROOF)": "tavern_sighting_rumor_release_proof=stage.reference(stage.PROOF)",
    '"istanbul_tavern_rumor_pipeline"': '"tavern_sighting_rumor_pipeline"',
    old_copies: 'stage.PROOF, build.NATIVE, review.OUT, *(Path(row["path"]) for row in outcome["visual_review"])',
    "registered_manifest_entries=1131, passing_release_checks=466, changed_components=2, changed_internal_files=[ARM, COMMON]":
        "registered_manifest_entries=1132, passing_release_checks=467, changed_components=1, changed_internal_files=[COMMON]",
    "contextual_records_revisited=13, contextual_decisions_reused=11, previously_localized_records=13":
        "contextual_records_revisited=2, contextual_decisions_reused=1, previously_localized_records=2",
    "prose_revisions=2, justified_retentions=11, text_display_revisions=3":
        "prose_revisions=1, justified_retentions=1, text_display_revisions=1",
    'ordinary_Istanbul_Tavern_and_London_Guild=True, revised_gameplay_holds=2, native_pages=8, unchanged_gameplay_holds=sum(len(stage.read(build.PAIRED)[label]["unchanged_frames"]) for label in ("tavern", "guild"))':
        "representative_Tavern_gameplay_carried_forward=True, revised_gameplay_holds=0, native_pages=7, native_item_region_cases=121",
    "prose_revisions=2, wrap_only_revisions=0, texts_retained=11": "prose_revisions=1, wrap_only_revisions=0, texts_retained=1",
    '"istanbul_tavern_rumor_20261124"': '"tavern_sighting_rumor_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Tavern sighting rumor testing candidate

The alternate Tavern patron's rumor keeps each item and region together. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Istanbul Tavern rumor candidate": "Preserve the registered Tavern sighting rumor candidate",
    "1,131 entries and 466 passing checks": "1,132 entries and 467 passing checks",
    doc: '''    DOC.write_text(f"""# Alternate Tavern sighting rumor

The patron now asks **Heard the rumor about a rare item?** On the next line, **They say** introduces the reported sighting. All 121 stock item and region combinations keep both names intact. The previous version split 89 item names. The patron's optional follow-up retains its skepticism about the drunk's word and its respect for the listener. [Clean Japanese, exact installed bytes and review](../{REVIEW.as_posix()})

The original caller fragments resolved the item, region and Patron on all 121 cases. The staged archive passed the native loader and renderer checks for Black Rapier, Red-Haired Pirate Sword, Saladin's Silver Armor and the follow-up. The earlier ordinary Istanbul Tavern replay carries forward on the unchanged renderer and COMMON 870. Natural activation of COMMON 863 and 868 remains unobserved. [Native previews](../{VERIFY.as_posix()}/portrait_sheet_01.png) [Representative Istanbul gameplay](editorial_istanbul_tavern_rumor_registered_20261124.md)

The candidate passed 467 release checks, its own startup, 17 focused regressions and byte-exact reconstruction from the clean ROM. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
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
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 11:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(verify_source + "\n" + prepare + "\n" + finish, __file__ + "::Tavern-sighting-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
