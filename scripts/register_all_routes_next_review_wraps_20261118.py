"""Register the next contextual wrap batch against the cumulative Translation DS candidate."""

from pathlib import Path

from scripts import register_all_routes_continuing_phrase_wraps_20261118 as parent
from scripts import replay_all_routes_next_review_wraps_20261118 as replay
from scripts import stage_all_routes_next_review_wraps_20261118 as stage
from scripts import verify_all_routes_next_review_wraps_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-next-review-wraps-v1-20261118"
ROOT = Path("out/all_routes_next_review_wraps_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Next_Review_Wraps_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_next_review_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_all_routes_next_review_wraps_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"


def match_parallel_dialogue(draft):
    rows = {r["id"]: r for r in draft["records"] if r["route"] == 0}
    earlier = {r["id"]: r for r in base.load(parent.REVIEW)["records"] if r["route"] == 1}
    for current_id, prior_id in (("DK4_MES_B254_R0037", "DK4_MES_B243_R0036"),
                                ("DK4_MES_B264_R0010", "DK4_MES_B255_R0010")):
        now, prior = rows[current_id], earlier[prior_id]
        assert bytes.fromhex(now["source_hex"])[1:] == bytes.fromhex(prior["source_hex"])[1:]
        assert now["english"] == prior["english"] and prior["review"]["formatting"]
        now["matching_hodram_review"] = dict(path=str(parent.REVIEW), sha256=base.digest(parent.REVIEW),
                                             id=prior_id, reference=prior["registered_reference"])


bind = checked_text(parent.bind, {
    "len(retentions) == 134": "len(retentions) == 107",
    "initialized Rafael, Lil or Maria excerpt replay": "initialized Rafael or Maria excerpt replay",
    "    name_order(draft, target)": "    match_parallel_dialogue(draft)",
})
verify = checked_text(parent.verify, {
    'live["initialized_Lil_and_Maria"] and live["initialized_Rafael"]': 'live["initialized_Maria"] and live["initialized_Rafael"]',
    'live["actual_hayreddin_and_sphinx"] and live["tavern_return_one_complete_page"]': 'live["both_FE_page_transitions_observed"]',
    'len(live["holds"]) == 20': 'len(live["holds"]) == 18',
    'native_proof["revision_count"] == 24 and native_proof["fresh_page_count"] == 27 and native_proof["retention_count"] == 134':
        'native_proof["revision_count"] == 25 and native_proof["fresh_page_count"] == 25 and native_proof["retention_count"] == 107',
    'for item in r["layouts"]) == 27': 'for item in r["layouts"]) == 25',
    '    assert native_proof["pagination_before_after"] == {"DK4_MES_B252_R0116": [2, 1]}\n'
    '    assert native_proof["exact_original_sphinx_continuation"]["owner_id"] == "DK4_MES_B87_R0139"':
        '    assert [(p["owner_id"], p["command_offset"]) for p in native_proof["preserved_FE_pages"]] == [\n'
        '        ("DK4_MES_B116_R0041", 630), ("DK4_MES_B116_R0051", 1026)]',
    'len(draft["records"]) == 158': 'len(draft["records"]) == 132',
    '{"revision": 24, "retention": 134}': '{"revision": 25, "retention": 107}',
    '{"prose": 23, "wrap": 1, "retention": 134}': '{"prose": 23, "wrap": 2, "retention": 107}',
    'len(draft["resolved_wrap_leads"]) == 23': 'len(draft["resolved_wrap_leads"]) == 21',
})
publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
pins = publish[publish.index("    candidates = ["):publish.index("    for path in candidates:")]
main = checked_text(publish, {
    'len(manifest["batches"]) == 882 and len(manifest["checks"]) == 217':
        'len(manifest["batches"]) == 883 and len(manifest["checks"]) == 218',
    "replay.LIVE, replay.SETUP, replay.LIL_SETUP, replay.MARIA_SETUP, args.visual_review":
        "replay.LIVE, replay.SETUP, replay.MARIA_SETUP, args.visual_review",
    "release_stack_before_continuing_phrase_wraps.json": "release_stack_before_next_review_wraps.json",
    "release_stack_with_continuing_phrase_wraps.json": "release_stack_with_next_review_wraps.json",
    "verified_all_routes_dialogue_followup_predecessor": "verified_all_routes_continuing_phrase_wraps_predecessor",
    "all_routes_continuing_phrase_wraps_release": "all_routes_next_review_wraps_release",
    "registered_all_routes_continuing_phrase_wraps_and_complete_parent_inverse":
        "registered_all_routes_next_review_wraps_and_complete_parent_inverse",
    "all_routes_continuing_phrase_wraps_pipeline": "all_routes_next_review_wraps_pipeline",
    "prose_revisions=23, wrap_only_revisions=1, justified_retentions=134":
        "prose_revisions=23, wrap_only_revisions=2, justified_retentions=107",
    "text_display_revisions=24, pagination_fixes=1, name_consistency_revisions=1":
        "text_display_revisions=25, pagination_fixes=0, name_consistency_revisions=0",
    "initialized_Rafael_Lil_and_Maria_continuing_phrase_excerpts": "initialized_Rafael_and_Maria_FE_transition_excerpts",
    "Twenty-three wrap leads and the Barbarossa Hayreddin name order are resolved across the four routes.":
        "Twenty-one more wrap leads and their exchanges are resolved across the four routes.",
    "all_routes_continuing_phrase_wraps_20261118": "all_routes_next_review_wraps_20261118",
    "existing_credit=158": "existing_credit=132",
    "Preserve continuing phrase-wrap ROM or replay fixture": "Preserve next contextual wrap ROM or replay fixture",
    pins: '''    candidates = [ROM, stage.ROM, replay.ROM, replay.MARIA_ROM, stage.ROOT / "clean_rebuilt.nds"]\n''',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# All-routes next contextual wraps test candidate

The [local ROM](../../{ROM.as_posix()}) includes the cumulative editorial review and resolves 21 more flagged wraps.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Natural scene activation and hardware remain unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# All-routes next contextual wrap review

Reviewed 132 turns across 20 blocks. The ledger records 23 wording revisions, two reflows and 107 justified retentions. The batch resolves 21 tracked wrap leads. Rafael and Hodram now hear the same wording for two identical lines about the figurehead and famous ruins. Lil's correction keeps Emilio's cheese-tart joke and the full Proof of Conquest name together. Ian distinguishes being frightening from being strict about rewarding and punishing people. Maria tells Yifa to pull her weight aboard ship. [Exact review ledger](../{REVIEW.as_posix()})

All 25 revised pages passed native rendering and visual review. The two existing panels in Ian's account retain their exact offsets and bytes. Both panel transitions appeared in the initialized Maria excerpt. The initialized Rafael excerpt includes the Lamenting Jar question, a live name substitution and the ruins rumor. The two emulator excerpts matched 18 dialogue panels. Maria used the established system-only unlock. Hodram and Lil received offline checks. Natural activation, quest effects, and hardware remain unverified. [Native layout sheets](../{(VERIFY / 'before_after_1.png').as_posix()}) · [Rafael excerpt](../{(VERIFY / 'rafael_live_1.png').as_posix()}) · [Maria excerpt](../{(VERIFY / 'maria_live_1.png').as_posix()})

The patch reconstructs the candidate byte for byte from the clean input. All 114 accepted layers and the ASCII right-bound correction carry forward. Six startup holds, 24 protected name getters and 32 targeted tests passed. The 132 turns already had credit. The ledger stands at 27,700 with 276 stored shared keys open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
for source, label in ((bind, "exact-review"), (verify, "release-gates"), (main, "register")):
    exec(compile(source, __file__ + "::" + label, "exec"), env)

if __name__ == "__main__":
    env["main"]()
