"""Register the wrap, pagination and name-order corrections."""

from pathlib import Path
import re

from scripts import register_all_routes_followup_phrase_wraps_20261118 as parent
from scripts import replay_all_routes_continuing_phrase_wraps_20261118 as replay
from scripts import stage_all_routes_continuing_phrase_wraps_20261118 as stage
from scripts import verify_all_routes_continuing_phrase_wraps_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-continuing-phrase-wraps-v1-20261118"
ROOT = Path("out/all_routes_continuing_phrase_wraps_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Continuing_Phrase_Wraps_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_continuing_phrase_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_all_routes_continuing_phrase_wraps_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"


def name_order(draft, files):
    row, = [r for r in draft["records"] if r["route"] == 2 and r["id"] == "DK4_MES_B20_R0033"]
    assert row["english"] == "You! Barbarossa Hayreddin!"
    check = parent.stage.ROOT / "hayreddin_name_order_inventory.json"
    inventory = base.load(check)
    assert inventory["candidate_sha256"] == draft["previous_sha256"]
    paths = (native.ARM, "/COMMON/MESFILE.DK4", *(f"/data/SC{i}.DK4" for i in range(4)))
    assert not any(re.search(rb"Hayreddin[ \r\n]+Barbarossa", files[p]) for p in paths)
    assert sum(len(re.findall(rb"Barbarossa[ \r\n]+Hayreddin", files[p])) for p in paths) == 4
    row["name_order_consistency"] = dict(inventory=str(check), inventory_sha256=base.digest(check),
        corrected_literal_count=1, reversed_literal_matches_remaining=0, canonical_literal_matches=4)


bind = checked_text(parent.bind, {
    "len(retentions) == 151": "len(retentions) == 134",
    "initialized Hodram or Lil excerpt replay": "initialized Rafael, Lil or Maria excerpt replay",
    "    same_source_wording(draft)": "    name_order(draft, target)",
})
verify = checked_text(parent.verify, {
    "if before != after] == blocks": "if before != after] == sorted(blocks)",
    'live["initialized_Hodram_and_Lil"] and live["exact_original_commands"] and live["convoy_letter_and_camille_exchange_observed"]':
        'live["initialized_Lil_and_Maria"] and live["initialized_Rafael"] and live["exact_original_commands"]\n'
        '    assert live["actual_hayreddin_and_sphinx"] and live["tavern_return_one_complete_page"]',
    'len(live["holds"]) == 15': 'len(live["holds"]) == 20',
    'native_proof["revision_count"] == 18 and native_proof["fresh_page_count"] == 18 and native_proof["retention_count"] == 151':
        'native_proof["revision_count"] == 24 and native_proof["fresh_page_count"] == 27 and native_proof["retention_count"] == 134',
    'for item in r["layouts"]) == 18': 'for item in r["layouts"]) == 27',
    '    assert native_proof["native_runtime_assets_byte_identical"]':
        '    assert native_proof["native_runtime_assets_byte_identical"]\n'
        '    assert native_proof["pagination_before_after"] == {"DK4_MES_B252_R0116": [2, 1]}\n'
        '    assert native_proof["exact_original_sphinx_continuation"]["owner_id"] == "DK4_MES_B87_R0139"',
    'len(draft["records"]) == 169': 'len(draft["records"]) == 158',
    '{"revision": 18, "retention": 151}': '{"revision": 24, "retention": 134}',
    '{"prose": 17, "wrap": 1, "retention": 151}': '{"prose": 23, "wrap": 1, "retention": 134}',
    'len(draft["resolved_wrap_leads"]) == 17': 'len(draft["resolved_wrap_leads"]) == 23',
})
publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
pins = publish[publish.index("    candidates = ["):publish.index("    for path in candidates:")]
main = checked_text(publish, {
    'len(manifest["batches"]) == 881 and len(manifest["checks"]) == 216':
        'len(manifest["batches"]) == 882 and len(manifest["checks"]) == 217',
    "replay.LIVE, replay.HODRAM_SETUP, replay.LIL_SETUP, args.visual_review":
        "replay.LIVE, replay.SETUP, replay.LIL_SETUP, replay.MARIA_SETUP, args.visual_review",
    "release_stack_before_dialogue_followup.json": "release_stack_before_continuing_phrase_wraps.json",
    "release_stack_with_dialogue_followup.json": "release_stack_with_continuing_phrase_wraps.json",
    "verified_all_routes_contextual_phrase_review_predecessor": "verified_all_routes_dialogue_followup_predecessor",
    "all_routes_dialogue_followup_release": "all_routes_continuing_phrase_wraps_release",
    "registered_all_routes_dialogue_followup_and_complete_parent_inverse":
        "registered_all_routes_continuing_phrase_wraps_and_complete_parent_inverse",
    "all_routes_dialogue_followup_pipeline": "all_routes_continuing_phrase_wraps_pipeline",
    "prose_revisions=17, wrap_only_revisions=1, justified_retentions=151":
        "prose_revisions=23, wrap_only_revisions=1, justified_retentions=134",
    "text_display_revisions=18, pagination_fixes=0": "text_display_revisions=24, pagination_fixes=1, name_consistency_revisions=1",
    "initialized_Hodram_and_Lil_followup_excerpts": "initialized_Rafael_Lil_and_Maria_continuing_phrase_excerpts",
    "Seventeen wrap leads and their dialogue exchanges are reviewed across the four routes.":
        "Twenty-three wrap leads and the Barbarossa Hayreddin name order are resolved across the four routes.",
    "all_routes_dialogue_followup_20261118": "all_routes_continuing_phrase_wraps_20261118",
    "existing_credit=169": "existing_credit=158",
    "Preserve all-routes dialogue follow-up ROM or replay fixture": "Preserve continuing phrase-wrap ROM or replay fixture",
    pins: '''    candidates = [ROM, stage.ROM, replay.ROM, replay.LIL_ROM, replay.MARIA_ROM, stage.ROOT / "clean_rebuilt.nds"]
    candidates.extend(stage.ROOT.with_name(version) / stage.ROM.name for version in ("research_v1", "research_v2"))
''',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# All-routes continuing phrase wraps test candidate

The [local ROM](../../{ROM.as_posix()}) includes the cumulative review and fixes the latest wrap, pagination and name-order leads.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Natural scene activation and hardware remain unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# All-routes continuing phrase wraps

Reviewed 158 turns in 21 story blocks. The ledger records 23 wording revisions, one reflow and 134 exact retentions. The batch resolves 23 tracked wrap leads. Gerhard's recognition now uses Barbarossa Hayreddin, matching the Japanese order and nameplate. The tavern keeper's return of the rose fits one page, with the threat to report the swindler intact. The two Proofs of Conquest completion branches use identical wording. [Exact review ledger](../{REVIEW.as_posix()})

All 24 revised pages and three additional name-width cases passed native rendering and visual review. The Sphinx's extra riddle panel and its answer choices retain the original bytes and offsets. Xien's question keeps the given-name substitution and all its wording. Initialized Rafael, Lil and Maria excerpts matched 20 panels including the single-page tavern handover, the name correction and the transition from Xien's question to Maria's arithmetic. Maria used the established system-only unlock, and Hodram's revisions received offline checks. Natural activation, quest effects, and hardware remain unverified. [Native layout sheets](../{(VERIFY / 'before_after_1.png').as_posix()}) · [Rafael excerpt](../{(VERIFY / 'rafael_live_1.png').as_posix()}) · [Lil excerpt](../{(VERIFY / 'lil_live_1.png').as_posix()}) · [Maria excerpt](../{(VERIFY / 'maria_live_1.png').as_posix()})

The clean-input patch reconstructs the candidate byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. Six startup holds, 24 protected name getters and 32 targeted tests passed. These 158 turns already had credit. The ledger stands at 27,700 with 276 stored shared keys open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
for source, label in ((bind, "exact-records"), (verify, "release-gates"), (main, "register")):
    exec(compile(source, __file__ + "::" + label, "exec"), env)

if __name__ == "__main__":
    env["main"]()
