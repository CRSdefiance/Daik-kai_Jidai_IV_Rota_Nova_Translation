"""Register the source-reviewed Tunis Palace reply with cumulative proofs."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_tunis_shop_advice_20261124 as parent
from scripts import stage_tunis_palace_refusal_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


template, files = parent.template, parent.files
review, trend = build.review, build.trend
ARM, COMMON, ROM = trend.ARM, trend.COMMON, build.ROM
PROFILE = "all-routes-tunis-palace-refusal-v1-20261124"
CHECK = "registered_tunis_palace_refusal_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_tunis_palace_refusal_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_tunis_palace_refusal.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_tunis_palace_refusal_registered_20261124.md")
CHECKPOINT = "Registered the Tunis Palace guard's two-line refusal to grant a trade contract."
SHEET = build.SHEET
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.STORED)))


def visuals(preflight):
    return [files.reference(SHEET), *(files.reference(row["path"]) for row in preflight["proposed_sheets"])]


verify_source = checked_text(getsource(parent.verify), {
    "[5800, 7800, 8600, 9400]": "list(review.REVISED_HOLDS)",
    '    assert {row["frame"] for row in live["shop_selection_blinks"]} == build.MENU_BLINKS.keys()\n': "",
    'assert len(preflight["native_proposed_cases"]) == 124': 'assert [case["label"] for case in preflight["native_cases"]] == ["Current", "Proposed"]',
    "tunis_advice_keeps_ARM9_and_startup_extent_exact": "tunis_palace_refusal_keeps_ARM9_and_startup_extent_exact",
    "native_goods_cases=124": "native_pages=1",
})
readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_guild_trade_numerals_predecessor=predecessor, tunis_shop_advice_release=str(REVIEW)":
        "verified_tunis_shop_advice_predecessor=predecessor, tunis_palace_refusal_release=str(REVIEW)",
    "len(batches) == 1127 and len(checks) == 462": "len(batches) == 1128 and len(checks) == 463",
    'len(outcome["records"]) == 4': 'len(outcome["records"]) == 8',
    "tunis_shop_advice_release_proof=stage.reference(stage.PROOF)": "tunis_palace_refusal_release_proof=stage.reference(stage.PROOF)",
    '"tunis_shop_advice_pipeline"': '"tunis_palace_refusal_pipeline"',
    "registered_manifest_entries=1128, passing_release_checks=463": "registered_manifest_entries=1129, passing_release_checks=464",
    "contextual_records_revisited=4, contextual_decisions_reused=3, previously_localized_records=4":
        "contextual_records_revisited=8, contextual_decisions_reused=7, previously_localized_records=8",
    "prose_revisions=1, justified_retentions=3, text_display_revisions=1": "prose_revisions=1, justified_retentions=7, text_display_revisions=1",
    "ordinary_Tunis_Square=True, revised_gameplay_holds=4, native_pages=124":
        "ordinary_Tunis_Market_and_Palace=True, revised_gameplay_holds=2, native_pages=1",
    "prose_revisions=1, wrap_only_revisions=0, texts_retained=3": "prose_revisions=1, wrap_only_revisions=0, texts_retained=7",
    '"tunis_shop_advice_20261124"': '"tunis_palace_refusal_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Tunis Palace refusal testing candidate

The guard gives a blunt, two-line reply when the city has no room for another faction. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Tunis shop advice candidate": "Preserve the registered Tunis Palace refusal candidate",
    "1,128 entries and 463 passing checks": "1,129 entries and 464 passing checks",
    doc: '''    DOC.write_text(f"""# Tunis Palace contract refusal

The guard now says **Too bad. This city has no room for another faction.** The shorter opening preserves his blunt tone and the original reason for refusing the contract. The reply fits on two lines at native width. Seven other records retain their wording, including two alternate refusals reviewed offline. [Exact references and five review gates](../{REVIEW.as_posix()})

Ordinary Tunis gameplay showed the refusal before and after a 1,350-gold military investment. Both holds preserve the complete text and the Guard nameplate. The Market's free local Price Info, Egypt Region and Carpets labels, the ruler's investment replies, and the return to town match the predecessor. [Paired gameplay](../{VERIFY.as_posix()}/{SHEET.name})

The candidate passed 464 release checks, its own startup, 17 focused regression tests and byte-exact clean-input reconstruction. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
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
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 8:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(verify_source + "\n" + prepare + "\n" + finish, __file__ + "::Tunis-Palace-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
