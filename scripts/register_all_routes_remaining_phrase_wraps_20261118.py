"""Register the 30 lead batch and the revised story pagination."""

from pathlib import Path

from scripts import register_all_routes_next_review_wraps_20261118 as parent
from scripts import replay_all_routes_remaining_phrase_wraps_20261118 as replay
from scripts import stage_all_routes_remaining_phrase_wraps_20261118 as stage
from scripts import verify_all_routes_remaining_phrase_wraps_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-ongoing-phrase-wraps-v1-20261118"
ROOT = Path("out/all_routes_ongoing_phrase_wraps_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Ongoing_Phrase_Wraps_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_ongoing_phrase_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_all_routes_ongoing_phrase_wraps_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
RECLAIMED = {"DK4_MES_B200_R0015": [2, 1], "DK4_MES_B208_R0043": [2, 1]}


def match_route_dialogue(draft):
    rows = {(r["route"], r["id"]): r for r in draft["records"]}
    for route, ident, ledger, earlier in (
        (0, "DK4_MES_B334_R0081", parent.REVIEW, "DK4_MES_B318_R0079"),
        (3, "DK4_MES_B208_R0043", stage.review.LETTER, "DK4_MES_B238_R0044"),
    ):
        now = rows[route, ident]
        prior, = [r for r in base.load(ledger)["records"] if r["route"] == 1 and r["id"] == earlier]
        assert now["source_hex"][2:] == prior["source_hex"][2:] and now["english"] == prior["english"]
        now["matched_prior_review"] = dict(path=str(ledger), sha256=base.digest(ledger),
            id=earlier, reference=prior["registered_reference"])
    for left, right in (("DK4_MES_B342_R0078", "DK4_MES_B324_R0077"), ("DK4_MES_B342_R0082", "DK4_MES_B324_R0081")):
        rafael, hodram = rows[0, left], rows[1, right]
        assert rafael["english"] == hodram["english"]
        for row, other in ((rafael, hodram), (hodram, rafael)):
            row["matched_current_exchange"] = {"id": other["id"], "reference": other["registered_reference"]}


bind = checked_text(parent.bind, {
    "len(retentions) == 107": "len(retentions) == 132",
    "    match_parallel_dialogue(draft)": "    match_route_dialogue(draft)",
})
verify = checked_text(parent.verify, {
    'live["both_FE_page_transitions_observed"]': 'live["training_and_convoy_advance_in_one_page"]',
    'len(live["holds"]) == 18': 'len(live["holds"]) == 15',
    'native_proof["revision_count"] == 25 and native_proof["fresh_page_count"] == 25 and native_proof["retention_count"] == 107':
        'native_proof["revision_count"] == 31 and native_proof["fresh_page_count"] == 31 and native_proof["retention_count"] == 132',
    'for item in r["layouts"]) == 25': 'for item in r["layouts"]) == 31',
    '    assert [(p["owner_id"], p["command_offset"]) for p in native_proof["preserved_FE_pages"]] == [\n'
    '        ("DK4_MES_B116_R0041", 630), ("DK4_MES_B116_R0051", 1026)]':
        '    assert native_proof["pagination_before_after"] == RECLAIMED',
    'len(draft["records"]) == 132': 'len(draft["records"]) == 163',
    '{"revision": 25, "retention": 107}': '{"revision": 31, "retention": 132}',
    '{"prose": 23, "wrap": 2, "retention": 107}': '{"prose": 31, "retention": 132}',
    'len(draft["resolved_wrap_leads"]) == 21': 'len(draft["resolved_wrap_leads"]) == 30',
})
publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 883 and len(manifest["checks"]) == 218':
        'len(manifest["batches"]) == 884 and len(manifest["checks"]) == 219',
    "release_stack_before_next_review_wraps.json": "release_stack_before_ongoing_phrase_wraps.json",
    "release_stack_with_next_review_wraps.json": "release_stack_with_ongoing_phrase_wraps.json",
    "verified_all_routes_continuing_phrase_wraps_predecessor": "verified_all_routes_next_review_wraps_predecessor",
    "all_routes_next_review_wraps_release": "all_routes_ongoing_phrase_wraps_release",
    "registered_all_routes_next_review_wraps_and_complete_parent_inverse":
        "registered_all_routes_ongoing_phrase_wraps_and_complete_parent_inverse",
    "all_routes_next_review_wraps_pipeline": "all_routes_ongoing_phrase_wraps_pipeline",
    "prose_revisions=23, wrap_only_revisions=2, justified_retentions=107":
        "prose_revisions=31, wrap_only_revisions=0, justified_retentions=132",
    "text_display_revisions=25, pagination_fixes=0, name_consistency_revisions=0":
        "text_display_revisions=31, pagination_fixes=len(RECLAIMED), name_consistency_revisions=0",
    "initialized_Rafael_and_Maria_FE_transition_excerpts": "initialized_Rafael_reading_and_Maria_training_and_convoy",
    "Twenty-one more wrap leads and their exchanges are resolved across the four routes.":
        "Thirty more wrap leads and their exchanges are resolved across the four routes.",
    "all_routes_next_review_wraps_20261118": "all_routes_ongoing_phrase_wraps_20261118",
    "existing_credit=132": "existing_credit=163",
    "Preserve next contextual wrap ROM or replay fixture": "Preserve ongoing story wrap ROM or replay fixture",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# All-routes ongoing story wraps test candidate

The [local ROM](../../{ROM.as_posix()}) includes the cumulative editorial review and resolves 30 more flagged wraps.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Natural scene activation and hardware remain unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# All-routes ongoing story wraps

Reviewed 163 turns across 24 blocks. The ledger records 31 wording revisions and 132 justified retentions. The batch resolves 30 tracked wrap leads. Rafael's reading retains the invocation of Allah and Scheherazade's formal address. The guide's walk and Charles's Alchemy Book explanation match the parallel route. Yifa's warning about holding back against a sword and the convoy's narrow escape each fit on one page. The latter uses the same wording as Hodram's letter. [Exact review ledger](../{REVIEW.as_posix()})

All 31 revised pages passed native and visual review. Fifteen complete panels matched in initialized Rafael and Maria excerpts. Both one-page Maria corrections advanced directly to the next turn. Maria used the established system-only unlock. The Hodram and Lil pages received offline checks. Natural scene activation, quest effects, and hardware remain unverified. [Native layout sheets](../{(VERIFY / 'before_after_1.png').as_posix()}) · [Rafael excerpt](../{(VERIFY / 'rafael_live_1.png').as_posix()}) · [Maria excerpt](../{(VERIFY / 'maria_live_1.png').as_posix()})

The patch reconstructs the candidate byte for byte from the clean input. All 114 accepted layers and the ASCII right-bound correction carry forward. Six startup holds, 24 protected name getters and 32 targeted tests passed. All 163 turns already had credit. The ledger stands at 27,700 with 276 stored shared keys open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
for source, label in ((bind, "exact-review"), (verify, "release-gates"), (main, "register")):
    exec(compile(source, __file__ + "::" + label, "exec"), env)

if __name__ == "__main__":
    env["main"]()
