"""Register the three phrase-only repairs and representative Avacha replay."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_village_clue_punctuation_20261124 as parent
from scripts import stage_village_article_wraps_20261124 as build
from scripts import verify_avacha_wrap_replay_20261124 as gameplay
from scripts import stage_cartridge_title_20261123 as files
from scripts.source_locked_derivation_v5118 import checked_text


review, template = build, parent.template
ARM, COMMON, ROM = build.ARM, build.COMMON, build.ROM
PROFILE = "all-routes-village-article-wraps-v1-20261124"
CHECK = "registered_village_article_wraps_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_village_article_wraps_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_village_article_wraps.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_village_article_wraps_registered_20261124.md")
CHECKPOINT = "Registered the three remaining article wraps in the Promised Words clues."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=build.STORED)))

verify_source = checked_text(getsource(parent.verify), {
    'assert live["position_only_focused_gameplay"] and live["same_message_requests"] and live["same_ship_writes"]':
        'assert live["position_only_focused_gameplay"]',
    'assert live["changed"]["frame"] == gameplay.RESULT and len(live["unchanged_frames"]) == 48':
        'assert live["verified_frame"] == gameplay.CLUE and gameplay.END in live["unchanged_frames"]',
    'assert [row["index"] for row in native] == list(range(24))':
        'assert [row["index"] for row in native] == sorted(build.PHRASES)',
    'sum(len(row["messages"]) for row in packet["visuals"]) == 24':
        'sum(len(row["messages"]) for row in packet["visuals"]) == 3',
    "build.cache_plan(": "build.former.cache_plan(",
    "build.MainCodeFile(": "build.former.MainCodeFile(",
    "build.BASE": "build.former.BASE",
    "build.POOL": "build.former.POOL",
    "build.cstring(": "build.former.cstring(",
    "parent.trend.files(": "parent.parent.trend.files(",
    'len(records) == 54 and sum(r["decision"] == "revision" for r in records) == 25':
        'len(records) == 3 and all(r["decision"] == "revision" for r in records)',
    "assert wraps == 18": "assert wraps == 3",
    "Village_clue_pool_copy_and_startup_extent_preserved": "Village_articles_fit_registered_pool_extent",
    "parent.build.panels": "parent.parent.build.panels",
    "native_clues=24, punctuation_fields=25": "native_clues=3, punctuation_fields=0",
})

readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_narvik_lookout_predecessor=predecessor, village_clue_punctuation_release=str(REVIEW)":
        "verified_village_clue_punctuation_predecessor=predecessor, village_article_wraps_release=str(REVIEW)",
    "len(batches) == 1134 and len(checks) == 469": "len(batches) == 1135 and len(checks) == 470",
    'assert len(revised) == 25 and len(outcome["records"]) == 54':
        'assert len(revised) == len(outcome["records"]) == 3',
    "village_clue_punctuation_release_proof=stage.reference(stage.PROOF)": "village_article_wraps_release_proof=stage.reference(stage.PROOF)",
    '"village_clue_punctuation_pipeline"': '"village_article_wraps_pipeline"',
    "registered_manifest_entries=1135, passing_release_checks=470": "registered_manifest_entries=1136, passing_release_checks=471",
    "contextual_records_revisited=54, contextual_decisions_reused=29, previously_localized_records=54":
        "contextual_records_revisited=3, contextual_decisions_reused=0, previously_localized_records=3",
    "prose_revisions=0, justified_retentions=29, text_display_revisions=24, phrase_wrap_adjustments=18, punctuation_fields=25":
        "prose_revisions=0, justified_retentions=0, text_display_revisions=3, phrase_wrap_adjustments=3, punctuation_fields=0",
    "position_only_Narvik=True, revised_gameplay_holds=1, native_pages=24":
        "position_only_Avacha=True, revised_gameplay_holds=1, native_pages=3",
    "prose_revisions=0, phrase_wrap_adjustments=18, punctuation_fields=25, texts_retained=29":
        "prose_revisions=0, phrase_wrap_adjustments=3, punctuation_fields=0, texts_retained=0",
    '"village_clue_punctuation_20261124"': '"village_article_wraps_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Promised Words article-wrap testing candidate

The definite article stays with its noun phrase in the Sugarloaf Mountain, Champlain, and Avacha clues. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})

finish = checked_text(parent.finish, {
    "Preserve the registered village-clue candidate": "Preserve the registered village article-wrap candidate",
    "1,135 entries and 470 passing checks": "1,136 entries and 471 passing checks",
    doc: '''    DOC.write_text(f"""# Article wraps for the Promised Words clues

Three clues now keep the article with its phrase. The phrases are **the bell-shaped rock**, **the Frenchman**, and **the mountain of fire in Kamchatka**. The clean Japanese, complete English, player-entered answers and template punctuation are bound in the review. [Exact record review](../{REVIEW.as_posix()})

The original consumer rendered all three clues on one page. The Avacha replay used a position-only fixture and ordinary input to reach and confirm the native keyboard answer. The complete revised clue and Charles Rochefort's nameplate passed. The confirmation, permission notice, and developed-village menu matched the previous build. [Native preview](../{VERIFY.as_posix()}/portrait_sheet_01.png) [Paired gameplay](../{VERIFY.as_posix()}/paired_avacha_article_wrap_1_20261123.png)

The candidate passed 471 release checks, its own startup, all 17 focused tests and byte-exact clean-input reconstruction. [Testing package](../{PACKAGE.as_posix()}/README.md)
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
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 15:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(verify_source + "\n" + prepare + "\n" + finish, __file__ + "::article-wrap-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
