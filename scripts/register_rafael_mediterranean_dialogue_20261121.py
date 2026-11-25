"""Register Rafael's four reviewed exchanges as a cumulative testing candidate."""
from pathlib import Path

from scripts import register_rafael_first_market_20261121 as parent
from scripts import check_rafael_mediterranean_gameplay_20261121 as live
from scripts import verify_rafael_mediterranean_dialogue_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


template = parent.template
stage = display.stage
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-rafael-mediterranean-dialogue-v1-20261121"
ROOT = Path("out/rafael_mediterranean_dialogue_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_Mediterranean_Dialogue_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_rafael_mediterranean_dialogue_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_mediterranean_dialogue_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
CHECKPOINT = ("Reviewed four Rafael exchanges, from the Mediterranean debrief to the encounters with Hans, "
              "Arcadius, Lil and Camille. The batch has 40 revisions and 155 justified retentions.")


verification = checked_text(parent.verification, {
    'draft["decisions"] == {"revision": 7, "retention": 7}': 'draft["decisions"] == {"revision": 40, "retention": 155}',
    'playback["natural_activation"] and playback["exact_native_glyph_matches"]':
        'playback["initialized_excerpts"] and playback["exact_native_glyph_matches"]',
    'playback["original_preparation_menu_market_share_choice_and_market_return"]':
        'not playback["natural_activation"] and len(playback["cases"]) == 4',
    'rendered["newly_rendered_pages"] == 7': 'rendered["newly_rendered_pages"] == 40',
    'len(playback["holds"]) == 7 and len(playback["unchanged_controls"]) == 10':
        'len(playback["holds"]) + len(playback["offline_only"]) == 40 and {r["block"] for r in playback["holds"]} == {47, 48, 49, 50}',
    ' and len(viewed) == 4': '',
    'assert len(groups) == 1 and before.keys()': 'assert len(groups) == 4 and before.keys()',
    '    observed_frames = {r["frame"] for r in playback["holds"] + playback["unchanged_controls"]}\n': '',
    'len(checked) == len(draft["records"]) == 14': 'len(checked) == len(draft["records"]) == 195',
    'assert ((path, ident) in seen) == bool(row["previous_capture"]) and result["native_pages"] == 1':
        'assert result["native_pages"] == 1 and (((path, ident) not in seen) == (ident in playback["offline_only"]))',
    'row["observed_in_ordinary_gameplay"] = bool(row["previous_capture"] and row["previous_capture"]["frame"] in observed_frames)':
        'row["observed_in_initialized_excerpt"] = (path, ident) in seen',
    'ordinary_town_replay_evidence=str(live.PROOF)': 'initialized_replay_evidence=str(live.PROOF)',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'verified_rafael_harbor_predecessor': 'verified_market_lesson_predecessor',
    'len(batches) == 986 and len(checks) == 321': 'len(batches) == 987 and len(checks) == 322',
    'original_preparation_and_market_share_choices_preserved=True': 'four_original_exchange_command_maps_preserved=True',
    'previously_localized_records=14, new_contextual_records=0, prose_revisions=3':
        'previously_localized_records=195, new_contextual_records=0, prose_revisions=26',
    'wrap_only_revisions=4, justified_retentions=7': 'wrap_only_revisions=14, justified_retentions=155',
    'ordinary_Rafael_first_market_lesson=True': 'four_initialized_Rafael_excerpts=True',
    'native_revised_pages=7, observed_holds=17, natural_activation=True':
        'native_revised_pages=40, observed_holds=len(base.load(live.PROOF)["holds"]), natural_activation=False',
    'prior_records_reviewed=14, actual_Rafael_market_holds=17, offline_pages=7':
        'prior_records_reviewed=195, observed_Rafael_panels=len(base.load(live.PROOF)["holds"]), offline_pages=40',
    'prose_revisions=3, justified_retentions=7, wrap_only_revisions=4':
        'prose_revisions=26, justified_retentions=155, wrap_only_revisions=14',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's Mediterranean and North Sea dialogue candidate

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed Mediterranean debrief, Athens recruitment and Proof of Conquest discussion, and Rafael's two North Sea encounters with Lil and Camille. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_first_market", "rafael_mediterranean_dialogue")

checkpoint = parent.commit_candidate[parent.commit_candidate.index("    DOC.write_text"):parent.commit_candidate.index("    prefix =")]
commit_candidate = checked_text(parent.commit_candidate, {
    "Preserve the Rafael first Market candidate and staging ROM": "Preserve the Mediterranean dialogue candidate and the staging ROM",
    checkpoint: '''    playback = base.load(live.PROOF)
    observed = len(playback["holds"])
    offline_only = len(playback["offline_only"])
    DOC.write_text(f"""# Rafael's Mediterranean and North Sea exchanges

Reviewed all 195 records in four complete exchanges against the clean Japanese, with 26 wording revisions, 14 wrap-only revisions and 155 reasons for retention. Julio's warning restores his uncertainty about facing Pasha's forces. In Athens, the Proof of Conquest and the rumor about southern Africa read as complete thoughts. Lil and Camille keep their distinct voices, and the gift exchange leaves Rafael as puzzled as the source does. [Per-record decisions and exact references](../{REVIEW.as_posix()})

All 40 revised pages passed native font checks and visual review. Four initialized emulator excerpts matched {observed} complete revised panels and their nameplates. The other {offline_only} revised lines received offline verification. The fixtures start from Rafael's original opening prelude and preserve all four command sequences. Natural activation and hardware remain unverified. [Native and gameplay evidence](../{VERIFY.as_posix()})

The clean-input patch reconstructs the candidate exactly. The 17 focused tests, six startup holds and 24 protected name getters passed. The 195 records already have ledger credit. [Cumulative testing ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_first_market", "rafael_mediterranean_dialogue")

scope = vars(template) | globals()
for source in (verification, build, commit_candidate):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
