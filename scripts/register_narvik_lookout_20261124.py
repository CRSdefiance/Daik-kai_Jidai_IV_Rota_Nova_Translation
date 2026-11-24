"""Register the Narvik lookout reflow after startup and a paired focused replay."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_tripoli_hodram_warning_20261124 as parent
from scripts import register_tunis_shop_advice_20261124 as common_template
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_narvik_lookout_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


review, trend = build.review, build.trend
ARM, COMMON, ROM = trend.ARM, trend.COMMON, build.ROM
PROFILE = "all-routes-narvik-lookout-v1-20261124"
CHECK = "registered_narvik_lookout_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_narvik_lookout_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_narvik_lookout.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_narvik_lookout_registered_20261124.md")
CHECKPOINT = "Registered the one-line village sighting and verified the Narvik Promised Words exchange."
template = parent.template
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=build.STORED)))


def visuals(preflight, live):
    return [files.reference(row["path"]) for row in live["sheets"] + preflight["proposed_sheets"]]


baseline = getsource(common_template.verify)
before_live = baseline[baseline.index('    assert live["before"]'):baseline.index('    assert files.sha256("".join')]
records_check = baseline[baseline.index("        key = row["):baseline.index("    prior = files.read(parent.REVIEW)")]
verify_source = checked_text(baseline, {
    before_live: '''    assert live["before"] == preflight["location_only_narvik"]
    assert live["after"]["controller"]["sha256"] == live["before"]["controller"]["sha256"]
    assert live["stored"] == files.reference(build.STORED) and live["position_only_focused_gameplay"]
    assert live["same_trace_message_requests"] and live["changed"]["frame"] == build.CHANGED
    assert 13800 in live["unchanged_frames"] and live["changed"]["full_native_ink_pixels"] > 0
    visible = visuals(preflight, live)
    assert [r["sha256"] for r in visible] == [r["sha256"] for r in live["sheets"] + preflight["proposed_sheets"]]
    assert len(preflight["native"]) == 2
    assert preflight["native"][1]["lines"] == [review.PROPOSED]
''',
    records_check: '''        if row["file_path"] == COMMON:
            key = row["message_ID"]
            assert jp[key].text.hex() == row["source_hex"] and former[key].text.hex() == row["current_hex"]
            assert current[key].text.hex() == row.get("proposed_hex", row["current_hex"])
            reference = row.get("proposed_reference", row["current_reference"])
            observed = text_ref(current[key])
            assert all(reference[k] == value for k, value in observed.items())
            registered = observed | dict(exact_stored_hex=current[key].text.hex())
        else:
            assert row["file_path"] == ARM and arm == old.read_file(ARM)
            registered = row["installed_reference"]
        records.append(row | dict(registered_reference=registered | dict(candidate_sha256=candidate)))
''',
    "tunis_advice_keeps_ARM9_and_startup_extent_exact": "Narvik_lookout_keeps_ARM9_and_startup_extent_exact",
    "native_goods_cases=124": "native_pages=1, fixture_free_Copenhagen=True, position_only_Narvik=True",
})

start = parent.prepare.index('        revised = [row["id"]')
before_update = parent.prepare[start:parent.prepare.index("        update = dict(profile=", start)]
readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_tavern_sighting_rumor_predecessor=predecessor, tripoli_hodram_warning_release=str(REVIEW)":
        "verified_tripoli_hodram_warning_predecessor=predecessor, narvik_lookout_release=str(REVIEW)",
    "len(batches) == 1132 and len(checks) == 467": "len(batches) == 1133 and len(checks) == 468",
    "assert {ARM, COMMON, STORY} <= set(paths) and {ARM, COMMON, STORY} <= records.keys()":
        "assert {ARM, COMMON} <= set(paths) and {ARM, COMMON} <= records.keys()",
    before_update: '''        revised = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]
        assert revised == [f"COMMON_MESSAGE_{review.KEY}"] and len(outcome["records"]) == 18
        records[COMMON].extend(ident for ident in revised if ident not in records[COMMON])
''',
    "snapshot_scope=STORY": "snapshot_scope=COMMON",
    "tripoli_hodram_warning_release_proof=stage.reference(stage.PROOF)": "narvik_lookout_release_proof=stage.reference(stage.PROOF)",
    '"tripoli_hodram_warning_pipeline"': '"narvik_lookout_pipeline"',
    "stage.PROOF, build.PAIRED, review.OUT, LEVEL_UPS": "stage.PROOF, build.PAIRED, review.OUT",
    ' target_SC1_sha256=outcome["target_SC1_sha256"],': "",
    "registered_manifest_entries=1133, passing_release_checks=468, changed_components=1, changed_internal_files=[STORY]":
        "registered_manifest_entries=1134, passing_release_checks=469, changed_components=1, changed_internal_files=[COMMON]",
    "contextual_records_revisited=11, contextual_decisions_reused=10, previously_localized_records=11":
        "contextual_records_revisited=18, contextual_decisions_reused=17, previously_localized_records=18",
    "prose_revisions=1, justified_retentions=10, text_display_revisions=1":
        "prose_revisions=1, justified_retentions=17, text_display_revisions=1",
    "ordinary_Syracuse_to_Tripoli=True": "ordinary_Copenhagen_departure=True, position_only_Narvik=True",
    "prose_revisions=1, wrap_only_revisions=0, texts_retained=10": "prose_revisions=1, wrap_only_revisions=0, texts_retained=17",
    '"tripoli_hodram_warning_20261124"': '"narvik_lookout_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Narvik lookout testing candidate

Manuel's full village sighting fits one line. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})

finish = checked_text(parent.finish, {
    "Preserve the registered Tripoli Hodram warning candidate": "Preserve the registered Narvik lookout candidate",
    "1,133 entries and 468 passing checks": "1,134 entries and 469 passing checks",
    doc: '''    DOC.write_text(f"""# Copenhagen departure and the Narvik village exchange

Manuel now says **Admiral, we've spotted a village!** on one line. The shorter exclamation suits the lookout, preserves his address, and leads into the separate discovery notice. The review gives individual reasons for retaining the other 17 records. [Exact source, installed text and review](../{REVIEW.as_posix()})

Ordinary Copenhagen controls verified the low-crew warning, 16-gold resupply, departure report and the option to decline stopping. A second replay started near Narvik using the original position-only fixture. The game handled discovery, resupply, repairs and acceptance of the typed Svartisen answer. The confirmed notice grants access from the next visit. The tested waypoint and ordinary portion of the northbound voyage are recorded separately. [Paired focused replay](../{VERIFY.as_posix()}/paired_narvik_lookout_20261124_1_20261123.png)

The candidate changes only COMMON 1320 and passed startup, 469 release checks, 17 focused tests and byte-exact clean-input reconstruction. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
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
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 13:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(verify_source + "\n" + prepare + "\n" + finish, __file__ + "::Narvik-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
