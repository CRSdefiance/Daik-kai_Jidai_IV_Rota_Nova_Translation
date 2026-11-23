"""Register the native-verified question-tag and phrase-wrap revisions."""

from inspect import getsource
from pathlib import Path

from scripts import register_london_guild_assignments_20261118 as precedent
from scripts import replay_story_tag_wraps_20261118 as replay
from scripts import stage_story_tag_wraps_20261118 as stage
from scripts import verify_story_tag_wraps_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent = stage.base, stage.native, stage.parent
workflow = parent.workflow
PROFILE = "all-routes-story-tag-wraps-v1-20261118"
ROOT = Path("out/story_tag_wraps_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Story_Tag_Wraps_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_story_tag_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_story_tag_wraps_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
LATER_RETENTIONS = {}


CONTEXT_REASONS = {
    (49, 271): "Lil is flustered at sounding like the one asking for help. The stammer and immediate objection carry that reversal.",
    (49, 279): "Lil asks directly whether Rafael is laughing at her. The brief objection fits their teasing exchange.",
    (70, 218): "Rafael echoes the word plan with hesitation, giving Maria room to explain why he needs it.",
    (70, 227): "Rafael answers the offer politely and commits to trying. The short formal response fits the negotiation.",
    (82, 8): "Mivor's extravagant address and complaint suit his oblivious response to Cristina's anger.",
}


def retained_replay_context(stored, live):
    packet = base.load(stage.review.SOURCE)
    holds = {row["id"]: row for row in live["holds"]}
    groups = {group["block"]: group for group in stored["groups"] if group["route"] == 0}
    references = {}
    for source in packet["groups"]:
        if source["route"] != 0:
            continue
        n = source["block"]
        for row in source["records"]:
            index = row["source_record_index"]
            if (n, index) not in CONTEXT_REASONS:
                continue
            ident = f"DK4_MES_B{n}_R{index:04}"
            group = groups[n]
            command = next(c for c in group["commands"] if c["source_offset"] == row["source_command_offset"])
            assert command["stored"] == command["current"] and not command["record_ids"]
            assert holds[ident]["body_hex"] == row["current_body_hex"]
            references[ident] = dict(file_path=source["file_path"], block=n, source_index=index,
                source_offset=row["source_offset"], source_body_hex=row["source_body_hex"], Japanese=row["Japanese"],
                current_offset=row["current_offset"], current_body_hex=row["current_body_hex"],
                stored_offset=command["stored_offset"] + 5, justification=CONTEXT_REASONS[n, index],
                unchanged_stored_command=command["stored"], replay_frame=holds[ident]["frame"])
    assert len(references) == len(CONTEXT_REASONS)
    return references


bind = getsource(precedent.bind)
history = bind[bind.index("    history = {}"):bind.index("    seen, rebound =")]
bind_source = checked_text(bind, {
    history: "    history = {}\n",
    "stage.paired.text_records": "stage.paired.paired.text_records",
    "initialized Rafael replay": "initialized Rafael or Lil replay",
    "initialized_rafael=live": "initialized_wrap_excerpts=live",
})
verify_source = checked_text(getsource(precedent.verify), {
    'live["initialized_Rafael"] and live["exact_original_commands"] and live["actual_Castor_and_Rafael_macro_glyphs"]':
        'live["initialized_Rafael_and_Lil"] and live["exact_original_commands"] and live["actual_given_name_and_surname"]',
    'len(live["holds"]) == 16': 'len(live["holds"]) == 13',
    'native_proof["revision_count"] == 40 and native_proof["fresh_page_count"] == 18':
        'native_proof["revision_count"] == 17 and native_proof["fresh_page_count"] == 26',
    "== 61": "== 26",
    '    assert base.digest(native_proof["prior_proof"]["path"]) == native_proof["prior_proof"]["sha256"]\n': "",
    'native_proof["previous_sheets"] + native_proof["contact_sheets"]': 'native_proof["contact_sheets"]',
    'len(draft["records"]) == 151': 'len(draft["records"]) == 17',
    '{"revision": 40, "retention": 111}': '{"revision": 17}',
    'draft.update(approved_source25=bound, direct_visual_review=sheets)':
        'draft.update(approved_source25=bound, direct_visual_review=sheets,'
        ' replay_context_retentions=retained_replay_context(stored, live))',
})
publish = getsource(precedent.main)
pins = publish[publish.index("    for version in (1, 2, 3):"):publish.index("    for path in candidates:")]
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index("    base.save(PACKAGE / \"checksums.json\"")]
publish_source = checked_text(publish, {
    'len(manifest["batches"]) == 862 and len(manifest["checks"]) == 197':
        'len(manifest["batches"]) == 873 and len(manifest["checks"]) == 208',
    'display.PROOF, replay.LIVE, replay.SETUP, args.visual_review':
        'display.PROOF, replay.LIVE, replay.SETUP, replay.LIL_SETUP, args.visual_review',
    'draft["initialized_rafael"]': 'draft["initialized_wrap_excerpts"]',
    "release_stack_before_guild_assignments.json": "release_stack_before_story_tag_wraps.json",
    "release_stack_with_guild_assignments.json": "release_stack_with_story_tag_wraps.json",
    "verified_forest_expeditions_predecessor=predecessor, london_malacca_guild_assignments_release=str(REVIEW)":
        "verified_late_trade_exchanges_predecessor=predecessor, story_tag_wraps_release=str(REVIEW)",
    "registered_london_malacca_guild_assignments_and_complete_parent_inverse":
        "registered_story_tag_wraps_and_complete_parent_inverse",
    "london_malacca_guild_assignments_pipeline": "story_tag_wraps_pipeline",
    "prose_revisions=40, justified_retentions=111": "prose_revisions=17, justified_retentions=0",
    "name_label_revisions=0, text_display_revisions=0, final_phrase_refinements_within_revised_prose=6":
        "name_label_revisions=0, text_display_revisions=17, final_phrase_refinements_within_revised_prose=17",
    "initialized_Rafael_guild_and_riddle=True": "initialized_Rafael_and_Lil_story_excerpts=True",
    "Rafael's ruins investigation and the related London and Malacca guild assignments are reviewed.":
        "Seventeen question tags and phrase wraps are corrected across all four storylines.",
    "london_malacca_guild_assignments_20261118": "story_tag_wraps_20261118",
    "existing_credit=151": "existing_credit=17",
    pins: '''    candidates += [replay.LIL_ROM, stage.ROOT / "clean_rebuilt.nds",
                   stage.ROOT.with_name("research_v1") / stage.ROM.name]
''',
    "Preserve guild assignment ROM or replay fixture": "Preserve story wrap ROM or replay fixture",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Story question tags and phrase wraps test candidate

The [local ROM](../../{ROM.as_posix()}) includes the cumulative localization through the 17 question-tag and phrase-wrap revisions.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits user acceptance. Natural scene activation and hardware remain unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Story question tags and phrase wraps

The current candidate showed 17 wrap leads across 17 blocks in all four storylines. Each selected record was reviewed with its clean Japanese and surrounding exchange. Rafael's teasing question stays on one line, Maria keeps “Proof of Conquest” and “East Asia” together, and Gerhard's full training question precedes the original choice. Cristina's matching taunts use the same wording in Hodram's and Lil's scenes. The ledger also explains why five surrounding replies were retained verbatim. [Exact review ledger](../{REVIEW.as_posix()})

Native and visual checks cover all 17 revised one-page records and nine additional name-width renderings. Clifford's two substitutions and the guard's admiral title and surname keep their original controls. Native tests include short and maximum-length name inputs. Gerhard's revised line fits its original allocation, and the two earlier page commands, the menu and its branch targets remain byte-identical. [Native layout sheets](../{(VERIFY / 'before_after_1.png').as_posix()})

Two initialized emulator replays matched 13 complete panels, including the surrounding replies to Rafael and the actual “Lil Argot?” and “Admiral Argot?” substitutions. The original story triggers, Gerhard's choice selection and hardware remain unverified. [Rafael dialogue](../{(VERIFY / 'rafael_live_1.png').as_posix()}) · [Lil dialogue](../{(VERIFY / 'lil_live_1.png').as_posix()})

The clean Japanese patch reconstructs the full candidate byte for byte. All 114 accepted layers and the registered ASCII right-bound correction carry forward. Six startup frames, 24 protected name getters and 32 targeted tests passed. The 17 revised records had existing credit. The ledger remains at 27,700 with 276 stored shared keys open. This editorial wrap pass preserves the separate graphics work and older technical re-audit. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})

scope = vars(precedent) | globals()
for code, label in ((bind_source, "exact-records"), (verify_source, "release-gates"), (publish_source, "register")):
    exec(compile(code, __file__ + "::" + label, "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
