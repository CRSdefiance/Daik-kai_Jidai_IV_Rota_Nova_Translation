"""Register the follow-up dialogue batch on the verified cumulative release."""

from pathlib import Path

from scripts import register_all_routes_next_phrase_wraps_20261118 as parent
from scripts import replay_all_routes_followup_phrase_wraps_20261118 as replay
from scripts import stage_all_routes_followup_phrase_wraps_20261118 as stage
from scripts import verify_all_routes_followup_phrase_wraps_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-dialogue-followup-v1-20261118"
ROOT = Path("out/all_routes_dialogue_followup_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Dialogue_Followup_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_dialogue_followup_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_all_routes_dialogue_followup_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"


def same_source_wording(draft):
    hodram = {r["id"]: r for r in draft["records"] if r["route"] == 1}
    recent, early = parent.parent, parent.parent.parent

    def no_layout(text):
        return "".join(text.split()).replace("、", "")

    for ident, earlier, earlier_id in (("DK4_MES_B17_R0229", early, "DK4_MES_B26_R0259"),
                                      ("DK4_MES_B91_R0061", recent, "DK4_MES_B91_R0062")):
        row, = [r for r in base.load(earlier.REVIEW)["records"] if r["id"] == earlier_id and r["route"] == 0]
        assert no_layout(hodram[ident]["Japanese"]) == no_layout(row["Japanese"])
        assert hodram[ident]["english"] == row["english"] and row["review"]["formatting"]
        hodram[ident]["matching_rafael_review"] = dict(path=str(earlier.REVIEW), sha256=base.digest(earlier.REVIEW),
            id=earlier_id, reference=row["registered_reference"])

    paired = recent.stage.review.SOURCE
    group, = [g for g in base.load(paired)["groups"] if g["route"] == 0 and g["block"] == 91]
    row, = [r for r in group["records"] if r["source_record_index"] == 32]
    rebuke = hodram["DK4_MES_B91_R0031"]
    assert rebuke["Japanese"] == row["Japanese"]
    assert rebuke["english"] == stage.review.logical(row["current_English"])
    rebuke["matching_rafael_text"] = dict(path=str(paired), sha256=base.digest(paired), file_path=group["file_path"],
        block=group["block"], source_record_index=32, source_offset=row["source_offset"],
        current_offset=row["current_offset"], current_body_hex=row["current_body_hex"])


bind = checked_text(parent.bind, {
    "len(retentions) == 136": "len(retentions) == 151",
    "initialized Lil or Maria excerpt replay": "initialized Hodram or Lil excerpt replay",
    "    validate_natural_dialogue_batch(draft)": """    same_source_wording(draft)
    for row in draft["records"]:
        row["source_meaning"] = row["source_meaning"].replace("; aloud", ". Aloud").replace("happened by; the", "happened by. The")
    validate_natural_dialogue_batch(draft)""",
})
reuse_checks = (
    '    reused = native_proof["dependency_exact_reuse"]\n'
    '    assert base.digest(reused["path"]) == reused["sha256"]\n'
    '    assert (reused["revised_pages"], reused["retained_records"]) == (13, 136)\n'
    '    assert len(native_proof["refreshed_punctuation_records"]) == 2\n'
)
verify = checked_text(parent.verify, {
    'live["initialized_Lil_and_Maria"] and live["exact_original_commands"] and live["actual_company_names_and_shared_accusation"]':
        'live["initialized_Hodram_and_Lil"] and live["exact_original_commands"] and live["convoy_letter_and_camille_exchange_observed"]',
    'len(live["holds"]) == 13': 'len(live["holds"]) == 15',
    'native_proof["revision_count"] == 15 and native_proof["fresh_page_count"] == 21 and native_proof["retention_count"] == 136':
        'native_proof["revision_count"] == 18 and native_proof["fresh_page_count"] == 18 and native_proof["retention_count"] == 151',
    'for item in r["layouts"]) == 21': 'for item in r["layouts"]) == 18',
    reuse_checks: "",
    'len(draft["records"]) == 151': 'len(draft["records"]) == 169',
    '{"revision": 15, "retention": 136}': '{"revision": 18, "retention": 151}',
    '{"prose": 14, "wrap": 1, "retention": 136}': '{"prose": 17, "wrap": 1, "retention": 151}',
    'len(draft["resolved_wrap_leads"]) == 13': 'len(draft["resolved_wrap_leads"]) == 17',
})
publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
pins = publish[publish.index("    candidates = ["):publish.index("    for path in candidates:")]
main = checked_text(publish, {
    'len(manifest["batches"]) == 880 and len(manifest["checks"]) == 215':
        'len(manifest["batches"]) == 881 and len(manifest["checks"]) == 216',
    "replay.LIVE, replay.LIL_SETUP, replay.MARIA_SETUP, args.visual_review":
        "replay.LIVE, replay.HODRAM_SETUP, replay.LIL_SETUP, args.visual_review",
    "release_stack_before_contextual_phrase_review.json": "release_stack_before_dialogue_followup.json",
    "release_stack_with_contextual_phrase_review.json": "release_stack_with_dialogue_followup.json",
    "verified_rafael_trade_lesson_and_scenes_predecessor": "verified_all_routes_contextual_phrase_review_predecessor",
    "all_routes_contextual_phrase_review_release": "all_routes_dialogue_followup_release",
    "registered_all_routes_contextual_phrase_review_and_complete_parent_inverse":
        "registered_all_routes_dialogue_followup_and_complete_parent_inverse",
    "all_routes_contextual_phrase_review_pipeline": "all_routes_dialogue_followup_pipeline",
    "prose_revisions=14, wrap_only_revisions=1, justified_retentions=136":
        "prose_revisions=17, wrap_only_revisions=1, justified_retentions=151",
    "text_display_revisions=15, pagination_fixes=0": "text_display_revisions=18, pagination_fixes=0",
    "initialized_Lil_and_Maria_phrase_excerpts": "initialized_Hodram_and_Lil_followup_excerpts",
    "Thirteen wrap leads and their dialogue exchanges are reviewed across all four routes.":
        "Seventeen wrap leads and their dialogue exchanges are reviewed across the four routes.",
    "all_routes_contextual_phrase_review_20261118": "all_routes_dialogue_followup_20261118",
    "existing_credit=151": "existing_credit=169",
    "Preserve all-routes phrase review ROM or replay fixture": "Preserve all-routes dialogue follow-up ROM or replay fixture",
    pins: '''    candidates = [ROM, stage.ROM, replay.HODRAM_ROM, replay.LIL_ROM, stage.ROOT / "clean_rebuilt.nds"]
''',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# All-routes dialogue follow-up test candidate

The [local ROM](../../{ROM.as_posix()}) includes the cumulative revisions through the current Rafael, Hodram, Lil and Maria exchanges.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Natural scene activation and hardware remain unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# All-routes dialogue follow-up

Reviewed 169 turns in 16 story blocks across the four routes. The ledger records 17 wording revisions, one reflow and 151 exact retentions. Seventeen tracked wrap leads are resolved. Three repeated turns carry the same wording in Rafael's and Hodram's routes. Charles's letter keeps the chance arrival of the Spanish navy and the merchant convoy's narrow escape. Kuhn's question preserves what he is willing to say before Camille calls him Dad. Xien's question about Nagarpur keeps its English and starts on a complete line. [Exact review ledger](../{REVIEW.as_posix()})

The original renderer checked all 18 revised pages and 151 exact retentions. Every revised page was viewed. Fifteen complete panels matched in initialized Hodram and Lil excerpts. They include Charles's four-row letter and the exchange with Camille and Kuhn. Rafael and Maria received offline checks. Natural activation, quest and combat effects, and hardware remain unverified. [Native layout sheets](../{(VERIFY / 'before_after_1.png').as_posix()}) · [Hodram excerpt](../{(VERIFY / 'hodram_live_1.png').as_posix()}) · [Lil excerpt](../{(VERIFY / 'lil_live_1.png').as_posix()})

The clean-input patch reconstructs the candidate byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. Six startup holds, 24 protected name getters and 32 targeted tests passed. These 169 turns already had credit. The ledger stands at 27,700 with 276 stored shared keys open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
for source, label in ((bind, "exact-records"), (verify, "release-gates"), (main, "register")):
    exec(compile(source, __file__ + "::" + label, "exec"), env)

if __name__ == "__main__":
    env["main"]()
