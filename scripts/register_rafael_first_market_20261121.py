"""Register the verified first Market lesson with its exact clean-input patch."""
from pathlib import Path
from types import SimpleNamespace

from scripts import register_rafael_harbor_exchange_20261121 as parent
from scripts import verify_rafael_first_market_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


template = parent.template
stage, live = display.stage, SimpleNamespace(PROOF=display.LIVE)
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-rafael-first-market-v1-20261121"
ROOT = Path("out/rafael_first_market_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_First_Market_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_rafael_first_market_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_first_market_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = display.run.STARTUP_CAPTURE
CHECKPOINT = ("Rafael's New Game replay verified Julio's loan and preparation choice. "
              "The first Market lesson has seven revisions for clearer wording and phrase continuity.")


verification = checked_text(parent.verification, {
    'draft["decisions"] == {"revision": 30, "retention": 87}': 'draft["decisions"] == {"revision": 7, "retention": 7}',
    'len(playback["movie_transition_holds"]) == 4': 'playback["original_preparation_menu_market_share_choice_and_market_return"]',
    'rendered["newly_rendered_pages"] == 45': 'rendered["newly_rendered_pages"] == 7',
    'len(playback["unchanged_controls"]) == 11': 'len(playback["unchanged_controls"]) == 10',
    'and len(viewed) == 9': 'and len(viewed) == 4',
    'len(checked) == len(draft["records"]) == 117': 'len(checked) == len(draft["records"]) == 14',
    '    assert all(after[p] == before[p] for p in ("/FLS/M20.fls", "/FLS/m21.fls"))':
        '    scene = "/data/SC0.DK4"\n'
        '    assert native.IlnkContainer.parse(before[scene]).blocks[44] == native.IlnkContainer.parse(after[scene]).blocks[44]',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_stockholm_dialogue_predecessor": "verified_rafael_harbor_predecessor",
    "len(batches) == 985 and len(checks) == 320": "len(batches) == 986 and len(checks) == 321",
    "original_harbor_and_ship_movies_preserved=True": "original_preparation_and_market_share_choices_preserved=True",
    "previously_localized_records=117, new_contextual_records=0, prose_revisions=17":
        "previously_localized_records=14, new_contextual_records=0, prose_revisions=3",
    "wrap_only_revisions=13, justified_retentions=87": "wrap_only_revisions=4, justified_retentions=7",
    "ordinary_Rafael_harbor_opening=True": "ordinary_Rafael_first_market_lesson=True",
    "native_revised_pages=30, native_name_stress_pages=15, observed_holds=22":
        "native_revised_pages=7, observed_holds=17",
    "prior_records_reviewed=117, actual_Rafael_harbor_holds=22, offline_pages=45":
        "prior_records_reviewed=14, actual_Rafael_market_holds=17, offline_pages=7",
    "prose_revisions=17, justified_retentions=87, wrap_only_revisions=13":
        "prose_revisions=3, justified_retentions=7, wrap_only_revisions=4",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's first Market lesson testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the revised first Market lesson. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_harbor", "rafael_first_market").replace("verified_rafael_first_market_predecessor", "verified_rafael_harbor_predecessor")

checkpoint = parent.commit_candidate[parent.commit_candidate.index("    DOC.write_text"):parent.commit_candidate.index("    prefix =")]
commit_candidate = checked_text(parent.commit_candidate, {
    "Preserve the Rafael harbor candidate and staging ROM": "Preserve the Rafael first Market candidate and staging ROM",
    checkpoint: '''    DOC.write_text(f"""# Rafael's New Game preparation and first Market lesson

The ordinary New Game replay matched 29 complete native glyph masks in the later harbor and preparation scene, including 22 previously revised panels. It displayed both preparation captions and followed **Ask him.** The separate **Prepare alone.** dialogue carries forward with offline evidence. [Preparation replay and exact references](../{stage.review.replay.PROOF.as_posix()})

Reviewed all 14 records in Julio's first Market lesson against clean Japanese, including both market-share choices. Three lines have revised wording, four were reflowed and seven have individual reasons for retention. The Lisbon example keeps “saffron or almonds” together. The lesson keeps “cargo hold,” “unclaimed market share,” and the two halves of Julio's comparison intact. The Palace, Market and Finish labels retain their game meanings. [Exact review](../{REVIEW.as_posix()})

The candidate replay followed **Market share?** and returned to the Trader's greeting. Seven revised panels matched the native glyph masks and ten unchanged holds matched their predecessor images. **Got it.** retains its original stored branch and earlier focused evidence. Six startup holds, 24 protected name getters, 17 focused tests and the exact clean-input patch passed. [Before and after](../{(VERIFY / 'market_before_after_2.png').as_posix()}) · [Cumulative candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_harbor", "rafael_first_market")

scope = vars(template) | globals()
for source in (verification, build, commit_candidate):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
