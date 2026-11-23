"""Register the verified Lil and Maria wrap batch over the cumulative candidate."""

from pathlib import Path

from scripts import register_all_routes_remaining_phrase_wraps_20261118 as parent
from scripts import replay_all_routes_final_flagged_wraps_20261118 as replay
from scripts import stage_all_routes_final_flagged_wraps_20261118 as stage
from scripts import verify_all_routes_final_flagged_wraps_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "lil-maria-flagged-wraps-v1-20261118"
ROOT = Path("out/lil_maria_flagged_wraps_registered_20261118_v1")
ROM = ROOT / "Translation_DS_Lil_Maria_Flagged_Wraps_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_lil_maria_flagged_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_lil_maria_flagged_wraps_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
RECLAIMED = {
    "DK4_MES_B213_R0107": [2, 1],
    "DK4_MES_B235_R0044": [2, 1],
    "DK4_MES_B240_R0120": [2, 1],
}


def verify_matched_dialogue(draft):
    checked = {}
    current_rows = {(r["file_path"], r["block"], r["source_reference"]["record_index"]):r
                    for r in draft["records"]}
    for row in draft["records"]:
        match = row.get("matching_dialogue")
        if not match:
            continue
        if "ledger" in match:
            ledger = match["ledger"]
            if ledger not in checked:
                assert base.digest(ledger) == match["ledger_sha256"]
                checked[ledger] = base.load(ledger)["records"]
            paired, = [earlier for earlier in checked[ledger] if earlier["registered_reference"] == match["reference"]]
            assert paired["id"] == match["id"]
        else:
            paired = current_rows[match["file_path"], match["block"], match["source_record_index"]]
            assert paired["source_reference"]["offset"] == match["source_offset"]
            assert paired["source_hex"][2:] == match["exact_source_body_hex"]
            match["registered_reference"] = paired["registered_reference"]
        assert paired["source_hex"][2:] == row["source_hex"][2:]
        assert paired["english"] == row["english"] and paired["review"]["formatting"]


bind = checked_text(parent.bind, {
    "len(retentions) == 132": "len(retentions) == 105",
    "initialized Rafael or Maria excerpt replay": "initialized Lil or Maria excerpt replay",
    "    match_route_dialogue(draft)": "    verify_matched_dialogue(draft)",
})
verify = checked_text(parent.verify, {
    'live["initialized_Maria"] and live["initialized_Rafael"] and live["exact_original_commands"]':
        'live["initialized_Lil_and_Maria"] and live["exact_original_commands"]',
    'live["training_and_convoy_advance_in_one_page"]': 'live["matched_rose_handover_and_convoy"]',
    'len(live["holds"]) == 15': 'len(live["holds"]) == 16',
    'native_proof["revision_count"] == 31 and native_proof["fresh_page_count"] == 31 and native_proof["retention_count"] == 132':
        'native_proof["revision_count"] == 70 and native_proof["fresh_page_count"] == 70 and native_proof["retention_count"] == 105',
    'for item in r["layouts"]) == 31': 'for item in r["layouts"]) == 70',
    'len(draft["records"]) == 163': 'len(draft["records"]) == 175',
    '{"revision": 31, "retention": 132}': '{"revision": 70, "retention": 105}',
    '{"prose": 31, "retention": 132}': '{"prose": 70, "retention": 105}',
    'len(draft["resolved_wrap_leads"]) == 30': 'len(draft["resolved_wrap_leads"]) == 64',
})
publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 884 and len(manifest["checks"]) == 219':
        'len(manifest["batches"]) == 885 and len(manifest["checks"]) == 220',
    "replay.LIVE, replay.SETUP, replay.MARIA_SETUP, args.visual_review":
        "replay.LIVE, replay.LIL_SETUP, replay.MARIA_SETUP, args.visual_review",
    "stage.ROM, replay.ROM, replay.MARIA_ROM": "stage.ROM, replay.LIL_ROM, replay.MARIA_ROM",
    "release_stack_before_ongoing_phrase_wraps.json": "release_stack_before_lil_maria_flagged_wraps.json",
    "release_stack_with_ongoing_phrase_wraps.json": "release_stack_with_lil_maria_flagged_wraps.json",
    "verified_all_routes_next_review_wraps_predecessor": "verified_all_routes_ongoing_phrase_wraps_predecessor",
    "all_routes_ongoing_phrase_wraps_release": "lil_maria_flagged_wraps_release",
    "registered_all_routes_ongoing_phrase_wraps_and_complete_parent_inverse":
        "registered_lil_maria_flagged_wraps_and_complete_parent_inverse",
    "all_routes_ongoing_phrase_wraps_pipeline": "lil_maria_flagged_wraps_pipeline",
    "prose_revisions=31, wrap_only_revisions=0, justified_retentions=132":
        "prose_revisions=70, wrap_only_revisions=0, justified_retentions=105",
    "text_display_revisions=31": "text_display_revisions=70",
    "initialized_Rafael_reading_and_Maria_training_and_convoy": "initialized_Lil_and_Maria_rose_and_convoy",
    "Thirty more wrap leads and their exchanges are resolved across the four routes.":
        "All 64 queued wrap leads from Lil and Maria and six nearby turns are reviewed.",
    "all_routes_ongoing_phrase_wraps_20261118": "lil_maria_flagged_wraps_20261118",
    "existing_credit=163": "existing_credit=175",
    "Preserve ongoing story wrap ROM or replay fixture": "Preserve Lil and Maria story wrap ROM or replay fixture",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Lil and Maria flagged wraps test candidate

The [local ROM](../../{ROM.as_posix()}) includes the cumulative editorial review through the final flagged Lil and Maria wrap batch.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Natural scene activation and hardware remain unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Lil and Maria flagged story wraps

Reviewed 175 turns across 57 blocks. The ledger records 70 wording revisions and 105 justified retentions. The batch resolves 64 queued wrap leads and six closely related revisions. The rose handover, convoy rescue, figurehead rule and several other repeated turns use the same English in the corresponding scenes. Charles's letter retains the uncertainty about whether the sound has a scientific explanation. Samwell's warning gives the animal as a bear, as the Japanese specifies. [Exact review ledger](../{REVIEW.as_posix()})

All 70 revised pages passed native and visual review. The two rose handovers and Lil's convoy rescue now take one page each. Sixteen complete panels matched in the initialized Lil and Maria excerpts, with both handovers and both versions of Charles's letter checked. Maria used the established system-only unlock. Natural scene activation, quest effects, and hardware remain unverified. [Native layout sheets](../{(VERIFY / 'before_after_1.png').as_posix()}) · [Lil excerpt](../{(VERIFY / 'lil_live_1.png').as_posix()}) · [Maria excerpt](../{(VERIFY / 'maria_live_1.png').as_posix()})

The clean-input patch rebuilds the candidate byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. Six startup holds and 24 protected name getters passed, as did 32 targeted tests. The 175 turns already had credit. The ledger stands at 27,700 with 276 stored shared keys open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
for source, label in ((bind, "exact-review"), (verify, "release-gates"), (main, "register")):
    exec(compile(source, __file__ + "::" + label, "exec"), env)

if __name__ == "__main__":
    env["main"]()
