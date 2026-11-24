"""Register the captured-ship wording with its source, replays, and exact patch."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from scripts import register_tunis_palace_refusal_20261124 as parent
from scripts import stage_maria_captured_ship_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


template, files = parent.template, parent.files
review, trend = build.review, build.trend
ARM, COMMON, ROM = trend.ARM, trend.COMMON, build.ROM
PROFILE = "all-routes-maria-captured-ship-v1-20261124"
CHECK = "registered_maria_captured_ship_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_maria_captured_ship_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_maria_captured_ship.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_maria_captured_ship_registered_20261124.md")
CHECKPOINT = "Registered Maria's captured-ship notice with the complete ship name on one line."
SHEET = build.SHEET
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.STORED)))


def visuals(preflight):
    return [files.reference(SHEET), *(files.reference(row["path"]) for row in preflight["proposed_sheets"])]


verify_source = checked_text(parent.verify_source, {
    "list(review.REVISED_HOLDS)": "[review.RESULT_FRAME]",
    'assert [case["label"] for case in preflight["native_cases"]] == ["Current", "Proposed"]':
        '''assert len(preflight["native_cases"]) == 30 and all(case["layout"]["complete_runtime_name_on_one_line"]
            for case in preflight["native_cases"][1:])''',
    "tunis_palace_refusal_keeps_ARM9_and_startup_extent_exact": "maria_captured_ship_keeps_ARM9_and_startup_extent_exact",
    "native_pages=1, source_credit_added=0": "native_name_cases=29, source_credit_added=0",
})
readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_tunis_shop_advice_predecessor=predecessor, tunis_palace_refusal_release=str(REVIEW)":
        "verified_tunis_palace_refusal_predecessor=predecessor, maria_captured_ship_release=str(REVIEW)",
    "len(batches) == 1128 and len(checks) == 463": "len(batches) == 1129 and len(checks) == 464",
    'len(outcome["records"]) == 8': 'len(outcome["records"]) == 7',
    "tunis_palace_refusal_release_proof=stage.reference(stage.PROOF)": "maria_captured_ship_release_proof=stage.reference(stage.PROOF)",
    '"tunis_palace_refusal_pipeline"': '"maria_captured_ship_pipeline"',
    "registered_manifest_entries=1129, passing_release_checks=464": "registered_manifest_entries=1130, passing_release_checks=465",
    "contextual_records_revisited=8, contextual_decisions_reused=7, previously_localized_records=8":
        "contextual_records_revisited=7, contextual_decisions_reused=6, previously_localized_records=7",
    "prose_revisions=1, justified_retentions=7, text_display_revisions=1": "prose_revisions=1, justified_retentions=6, text_display_revisions=1",
    "ordinary_Tunis_Market_and_Palace=True, revised_gameplay_holds=2, native_pages=1":
        "ordinary_Maria_Nagasaki_duel=True, revised_gameplay_holds=1, native_pages=29",
    "prose_revisions=1, wrap_only_revisions=0, texts_retained=7": "prose_revisions=1, wrap_only_revisions=0, texts_retained=6",
    '"tunis_palace_refusal_20261124"': '"maria_captured_ship_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Maria captured-ship testing candidate

The sailor names the captured ship without splitting its name between lines. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Tunis Palace refusal candidate": "Preserve the registered Maria captured-ship candidate",
    "1,129 entries and 464 passing checks": "1,130 entries and 465 passing checks",
    doc: '''    DOC.write_text(f"""# Maria's captured-ship notice

The sailor now says **We took War Ironclad from the enemy!** The Japanese identifies the one named enemy ship and reports its capture in a blunt voice. The revision keeps that source meaning, the original runtime name and the same allocation. All 29 native cases keep the ship name together, including 18-byte names, names with spaces and legacy Japanese name bytes. Six companion records retain their wording. [Source, current and installed dialogue](../{REVIEW.as_posix()})

Ordinary controls took the party from Nagasaki through the failed Osaka Auto Move, the manual departure, the eight-page Kurushima confrontation and the boarding duel. Both builds reached the captured-ship notice. The revised body and Sailor nameplate passed complete glyph checks. The duel and later flagship-capture holds matched. The replay used the preserved Maria battery save with its recorded earlier setup. Osaka docking remains unvisited. [Paired gameplay](../{VERIFY.as_posix()}/{SHEET.name})

The candidate passed 465 release checks, its own startup, 17 focused regressions and byte-exact clean-input reconstruction. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
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
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 9:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(verify_source + "\n" + prepare + "\n" + finish, __file__ + "::captured-ship-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
