"""Register the Alexandria Square revisions and exact clean-input patch."""
from pathlib import Path

from scripts import register_rafael_mediterranean_dialogue_20261121 as parent
from scripts import verify_alexandria_dialogue_20261121 as display
from scripts import verify_alexandria_voyage_20261121 as live
from scripts.source_locked_derivation_v5118 import checked_text


template = parent.template
stage = display.build
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-alexandria-square-v1-20261121"
ROOT = Path("out/alexandria_dialogue_registered_20261121")
ROM = ROOT / "Translation_DS_Alexandria_Square_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_alexandria_dialogue_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_alexandria_square_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
CHECKPOINT = ("Reviewed the four Alexandria cooking exchanges and forecasts, with ten wording or layout revisions "
              "and 38 justified retentions. Hodram reached the Square and triggered the full scene during an ordinary voyage.")


verification = checked_text(parent.verification, {
    'draft["decisions"] == {"revision": 40, "retention": 155}': 'draft["decisions"] == {"revision": 10, "retention": 38}',
    'playback["initialized_excerpts"] and playback["exact_native_glyph_matches"]':
        'playback["natural_activation"] and playback["exact_native_glyph_matches"]',
    'not playback["natural_activation"] and len(playback["cases"]) == 4':
        'playback["original_notice_dismissal_and_Square_return"]',
    'rendered["newly_rendered_pages"] == 40': 'rendered["newly_rendered_pages"] == 10',
    'len(playback["holds"]) + len(playback["offline_only"]) == 40 and {r["block"] for r in playback["holds"]} == {47, 48, 49, 50}':
        'len(playback["holds"]) == 2 and playback["full_scene_panels"] == 12',
    'assert changed_paths == {"/data/SC0.DK4"}': 'assert changed_paths == {f"/data/SC{i}.DK4" for i in range(4)}',
    'len(checked) == len(draft["records"]) == 195': 'len(checked) == len(draft["records"]) == 48',
    'assert result["native_pages"] == 1 and (((path, ident) not in seen) == (ident in playback["offline_only"]))':
        'assert result["native_pages"] == 1 and ((path, ident) in seen) == (row["route"] == 1)',
    'row["observed_in_initialized_excerpt"] = (path, ident) in seen':
        'row["observed_in_ordinary_gameplay"] = row["route"] == 1',
    'initialized_replay_evidence=str(live.PROOF)': 'ordinary_town_replay_evidence=str(live.PROOF)',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_market_lesson_predecessor": "verified_mediterranean_dialogue_predecessor",
    "len(batches) == 987 and len(checks) == 322": "len(batches) == 988 and len(checks) == 323",
    "four_original_exchange_command_maps_preserved=True": "four_original_town_event_and_command_maps_preserved=True",
    "changed_components=1, repository_tests": "changed_components=4, repository_tests",
    "previously_localized_records=195, new_contextual_records=0, prose_revisions=26":
        "previously_localized_records=48, new_contextual_records=0, prose_revisions=10",
    "wrap_only_revisions=14, justified_retentions=155": "wrap_only_revisions=0, justified_retentions=38",
    "four_initialized_Rafael_excerpts=True": "ordinary_Hodram_Alexandria_Square=True",
    'native_revised_pages=40, observed_holds=len(base.load(live.PROOF)["holds"]), natural_activation=False':
        'native_revised_pages=10, observed_holds=12, natural_activation=True',
    'prior_records_reviewed=195, observed_Rafael_panels=len(base.load(live.PROOF)["holds"]), offline_pages=40':
        'prior_records_reviewed=48, observed_Alexandria_panels=12, offline_pages=10',
    "prose_revisions=26, justified_retentions=155, wrap_only_revisions=14":
        "prose_revisions=10, justified_retentions=38, wrap_only_revisions=0",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Alexandria Square dialogue testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the revised Alexandria owner and cook exchanges and their forecast. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_mediterranean_dialogue", "alexandria_dialogue")

notes = parent.commit_candidate[parent.commit_candidate.index("    playback = base.load(live.PROOF)"):parent.commit_candidate.index("    prefix =")]
commit_candidate = checked_text(parent.commit_candidate, {
    "Preserve the Mediterranean dialogue candidate and the staging ROM": "Preserve the Alexandria Square candidate and the staging ROM",
    notes: '''    DOC.write_text(f"""# Alexandria Square's cooking exchange and sweets forecast

Reviewed 48 records across all four routes. Ten revisions preserve the owner's exaggerated “sweeet,” the cook's dry responses and the difference between the owner's certainty and the game's tentative forecast. The forecast now fits on one line where the longer variants previously wrapped. The other 38 records have individual reasons for retention. [Exact source, current and registered references](../{REVIEW.as_posix()})

Hodram sailed from Athens to Alexandria on a copy of an existing battery save, stayed at the Inn for the original date gate and opened the Square. Both paired runs completed the original event. The candidate matched all 12 complete text masks, including the new punch line and speakerless forecast, then returned to the Square. The other routes were checked offline. Hardware remains unverified. [Gameplay comparisons](../{(VERIFY / 'alexandria_gameplay_1.png').as_posix()}) · [Event and glyph evidence](../{(VERIFY / live.PROOF.name).as_posix()})

The voyage also captured a storm warning, all five port-warning speeches and 39 speeches from Cesare's recruitment and ship-buying lesson. Both tutorial captions were visible. The replay followed Listen, and two Skip responses remain unvisited. Five wrap or page-boundary leads are recorded with exact source bytes and actual frames for the next pass. [Arrival and tutorial coverage](../work/hodram_alexandria_arrival_20261121/ordinary_arrival_coverage.json)

The clean-input patch reconstructs the ROM exactly. Six startup holds, 24 protected name getters and 17 focused tests passed. Existing editorial credit carries forward. [Cumulative testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_mediterranean_dialogue", "alexandria_dialogue")

scope = vars(template) | globals()
for source in (verification, build, commit_candidate):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
