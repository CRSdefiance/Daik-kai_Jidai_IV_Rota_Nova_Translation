"""Register the refreshed story trade terminology and its verified Lisbon lesson."""
from inspect import getsource
from pathlib import Path
import re
from types import SimpleNamespace

from scripts import audit_story_market_terms_20261119 as game
from scripts import register_help_market_terms_20261119 as parent
from scripts import register_story_short_phrase_wraps_20261119 as template
from scripts import stage_story_market_terms_20261119 as stage
from scripts import verify_story_market_terms_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-story-market-terms-v1-20261119"
ROOT = Path("out/story_market_terms_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Story_Market_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_story_market_terms_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_story_market_terms_20261119.md")
STARTUP, QA = game.play.STARTUP_PROOF, stage.ROOT / "supported_qa.xml"
VISUAL_REVIEW = stage.ROOT / "direct_visual_review.json"
CHECKPOINT = "Rafael’s village trading post and the Market dialogue now use the terminology appropriate to each location."
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=game.PROOF)

verification = checked_text(getsource(template.verify), {
    'path["result"] == [0, 1] and len(path["speeches"]) == 16':
        'path["result"] == [0, 0] and len(path["speeches"]) == 12',
    'len(path["checked_revisions"]) == playback["revised_pages_verified"] == 6':
        'len(path["checked_revisions"]) == playback["revised_pages_verified"] == 3',
    '    assert len(sheets) == 5 and viewed == {s["path"]: s["sha256"] for s in sheets}':
        '    assert viewed == {s["path"]: s["sha256"] for s in sheets}',
    '[34, 0, 0, 0]': '[22, 0, 0, 0]',
    '    archives = {f"/data/SC{i}.DK4": native.digest(after[f"/data/SC{i}.DK4"]) for i in range(4)}':
        '    archives = {path: native.digest(after[path]) for path in stored["changed_blocks"]}',
    '    assert prior["shared_storage_scope"]["exact_payloads_and_locations"]\n'
    '    assert prior["shared_storage_scope"]["pending_records"] == 276':
        '    shared = base.load(parent.parent.REVIEW)["shared_storage_scope"]\n'
        '    assert prior["preserved_ARM9_and_COMMON"] and shared["exact_payloads_and_locations"]\n'
        '    assert shared["pending_records"] == 276\n'
        '    assert native.digest(after[parent.HELP]) == previous["target_HELP_sha256"]\n'
        '    assert all(not re.search(rb"\\btrade[ \\n]+house\\b", after[f"/data/SC{i}.DK4"], re.I) for i in range(4))',
    'len(stored["groups"]) == 11 and len(commands) == len(draft["records"]) == 195':
        'len(stored["groups"]) == 6 and len(commands) == len(draft["records"]) == 202',
    'len(revisions) == 19 and len(retentions) == 176': 'len(revisions) == 34 and len(retentions) == 168',
    'block == 127': 'block == 137',
    'shared_storage_scope=prior["shared_storage_scope"]': 'shared_storage_scope=shared',
})

publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 909 and len(manifest["checks"]) == 244':
        'len(manifest["batches"]) == 910 and len(manifest["checks"]) == 245',
    "verified_square_shop_followup_predecessor": "verified_help_market_terms_predecessor",
    "help_market_terms": "story_market_terms",
    "stage.PROOF, stage.PLAN, STARTUP, QA, verified.LIVE, args.visual_review":
        "stage.PROOF, stage.review.SOURCE, stage.review.OUTPUT, stage.review.ROOT / \"city_alias_storage_recheck.json\", STARTUP, QA, verified.PROOF, verified.LIVE, args.visual_review",
    "native_display_sha256=base.digest(stage.PROOF)": "native_display_sha256=base.digest(verified.PROOF)",
    'owned_help_topics=[row["registered_reference"] for row in draft["records"] if row["decision"] == "revision"], target_HELP_sha256=archives[HELP]':
        'owned_story_records=[row["registered_reference"] for row in draft["records"] if row["decision"] == "revision"], story_archives_sha256=archives',
    "target_HELP_sha256=archives[HELP], changed_components=1": "changed_components=3",
    "HELP_sha256=archives[HELP],": 'HELP_sha256=release["target_HELP_sha256"],',
    'repository_tests=draft["repository_tests"]': "repository_tests=22",
    "prose_revisions=5, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=3":
        "prose_revisions=34, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=168",
    "text_display_revisions=5": "text_display_revisions=34",
    "ordinary_Help_pages_child_targets_and_history_return=True": "initialized_Lisbon_trade_lesson_and_market_share_choice=True",
    "natural_activation=True": "natural_activation=False",
    "previously_localized_records=8": "previously_localized_records=202",
    'stage.ROOT.parent.glob("research_v*")': 'stage.ROOT.parent.glob("staged_v*")',
    "Preserve Market Help ROM or reconstruction": "Preserve story Market ROM or reconstruction",
    '    for path in candidates:': '    candidates.append(game.play.FIXTURE)\n    for path in candidates:',
    readme: """    (PACKAGE / "README.md").write_text(f\"\"\"# Story Market terminology candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised trading-post and Market dialogue and the earlier Help fixes.
The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
\"\"\", encoding="utf-8", newline="\\n")
""",
    doc: """    DOC.write_text(f\"\"\"# Trading post and Market dialogue

Reviewed 202 records from six complete story exchanges against the clean Japanese, with 34 revisions and 168 justified retentions. Rafael and Charlotte discuss building a trading post. The Lisbon trade lesson and the other exchanges refer to the Market players can visit. Carlo makes the same tentative offer to meet there in Rafael’s and Maria’s routes, and each captain retains their own response. Rafael’s version of Carlo’s disclosure restores that the illness was going around. [Exact review ledger](../{REVIEW.as_posix()})

Every revised page passed native glyph, wrapping, bounds and visual checks. The final wrap pass kept “go out of their way” and “cargo holds” together and reused 32 exact page proofs. Charlotte’s live name token was also checked with the default and supported name lengths. The initialized Lisbon replay verified the three revised panels, both choice captions, the Market share branch and the original return. The five other blocks received offline checks. Natural scene activation and hardware remain unverified. [Native and emulator evidence](../{VERIFY.as_posix()})

The clean-input patch reconstructs the ROM byte for byte. Only SC0, SC1 and SC3 change. Help, shared text, native ARM9, the ASCII right-bound correction and all 114 accepted layers carry forward. Six startup holds, 24 protected name getters and 22 focused tests passed. Review credit remains 27,700 with 276 shared entries still open for display classification. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
""",
})
env = template.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
