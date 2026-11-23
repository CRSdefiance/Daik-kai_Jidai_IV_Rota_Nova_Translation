"""Register the revised Lisbon fragrance scene in the cumulative testing ROM."""
from inspect import getsource
from pathlib import Path

from scripts import register_hodram_execution_20261121 as parent
from scripts import stage_lisbon_fragrance_wraps_20261121 as stage
from scripts import verify_lisbon_fragrance_replay_20261121 as live
from scripts import verify_lisbon_fragrance_wraps_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


template = parent.parent
PROFILE = "all-routes-lisbon-fragrance-wraps-v1-20261121"
ROOT = Path("out/lisbon_fragrance_wraps_registered_20261121")
ROM = ROOT / "Translation_DS_Lisbon_Fragrance_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_lisbon_fragrance_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_lisbon_fragrance_wraps_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
CHECKPOINT = "Two lines in Hodram's Lisbon fragrance scene now match Rafael's wording and keep both phrases together. Ordinary gameplay verified the full Lisbon and Seoul trend scenes."

verification = checked_text(getsource(template.verify), {
    "stage.review.OUTPUT": "stage.author.OUTPUT",
    'base.digest(draft["source_packet"])': 'base.digest(stage.author.SOURCE)',
    'draft["decisions"] == {"revision": 5, "retention": 32}':
        'draft["decisions"] == {"revision": 2, "retention": 9}',
    'playback["initialized_excerpts"] and playback["exact_native_glyph_matches"]':
        'playback["natural_activation"] and playback["exact_native_glyph_matches"]',
    'assert not playback["natural_activation"] and not playback["hardware_verified"]':
        'assert playback["original_notice_dismissal_and_Square_return"] and not playback["hardware_verified"]',
    'rendered["newly_rendered_pages"] == 5': 'rendered["newly_rendered_pages"] == 2',
    'len(playback["holds"]) == 21 and {h["route"] for h in playback["holds"]} == {0, 1}':
        'len(playback["holds"]) == 11 and {h["route"] for h in playback["holds"]} == {1}',
    'and len(viewed) == 3': 'and len(viewed) == 2',
    'groups.keys() == {"/data/SC0.DK4", "/data/SC1.DK4"}': 'groups.keys() == {"/data/SC1.DK4"}',
    'after[stage.review.shared.COMMON]': 'after["/COMMON/MESFILE.DK4"]',
    '    assert stage.review.bind_movie(clean, target, (source[native.ARM], arm))["sha256"] == draft["artwork"]["sha256"]':
        '    assert after["/data/EV1.DK4"] == before["/data/EV1.DK4"] == source["/data/EV1.DK4"]',
    'len(checked) == len(draft["records"]) == 37': 'len(checked) == len(draft["records"]) == 11',
    'row["observed_in_initialized_excerpt"]': 'row["observed_in_natural_Lisbon_replay"]',
    '    draft.update(candidate_sha256=candidate, status="registered", direct_visual_review=viewed,':
        '    draft.update(candidate_sha256=candidate, status="registered", direct_visual_review=viewed,\n'
        '        encoder="dialogue-relocatable-v1", source_packet=str(stage.author.SOURCE),',
    'excerpt_evidence=str(live.PROOF)': 'ordinary_town_replay_evidence=str(live.PROOF)',
})

main_source = getsource(template.main)
package_prose = main_source[main_source.index('    (PACKAGE / "README.md").write_text'):main_source.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(main_source, {
    "verified_search_forage_wrap_predecessor": "verified_hodram_execution_predecessor",
    "len(batches) == 979 and len(checks) == 314": "len(batches) == 981 and len(checks) == 316",
    "archive_hashes=archives, source_movie_preserved=True":
        "archive_hashes=archives, original_Lisbon_event_preserved=True",
    "changed_components=2": "changed_components=1",
    "previously_localized_records=37, new_contextual_records=0, prose_revisions=4":
        "previously_localized_records=11, new_contextual_records=0, prose_revisions=2",
    "wrap_only_revisions=0, justified_retentions=32, name_label_revisions=0, text_display_revisions=1":
        "wrap_only_revisions=0, justified_retentions=9, name_label_revisions=0, text_display_revisions=0",
    "initialized_Rafael_and_Hodram_excerpts=True": "ordinary_Hodram_Lisbon_replay=True",
    "native_revised_pages=5, observed_panels=21, natural_activation=False":
        "native_revised_pages=2, observed_panels=11, natural_activation=True",
    "prior_records_reviewed=37, actual_Rafael_and_Hodram_panels=21, offline_pages=5":
        "prior_records_reviewed=11, actual_Hodram_Lisbon_panels=11, offline_pages=2",
    "prose_revisions=4, justified_retentions=32, text_display_revisions=1":
        "prose_revisions=2, justified_retentions=9, phrases_reflowed=2",
    package_prose: '''    (PACKAGE / "README.md").write_text(f"""# Lisbon fragrance testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes two revised lines in Hodram's Lisbon Square scene. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("moonlit_violin", "lisbon_fragrance_wraps")

commit_source = getsource(template.commit)
checkpoint_prose = commit_source[commit_source.index("    DOC.write_text"):commit_source.index("    prefix =")]
commit_candidate = checked_text(commit_source, {
    "Preserve the violin candidate or replay ROM": "Preserve the verified Lisbon candidate or staging ROM",
    checkpoint_prose: '''    DOC.write_text(f"""# Lisbon fragrance and Seoul chili peppers

In Hodram's Lisbon Square scene, the women now sound more conversational and use the same wording as Rafael's version. The phrase “before everyone else does” and both clauses of the suggestion to ask about the scent stay intact. Nine other lines in the Lisbon scene have individual reasons for retention. [Clean Japanese and exact registered references](../{REVIEW.as_posix()})

Ordinary Inn stays activated the two trend scenes on the registered predecessor. The full 11-panel Lisbon and 15-panel Seoul exchanges matched native body masks and complete Lady nameplates. Seoul's Square played Yifa's recruitment first. The chili-pepper exchange then opened on the next visit. No wording or wrapping changes were needed for the Seoul exchange. [Lisbon and Seoul gameplay evidence](../translations/editorial_checkpoints/SharedText_20261110_v1/lisbon_seoul_trend_gameplay_20261121_v1.json)

The cumulative Lisbon ROM repeated the same inputs. All 11 panels, including both revisions, passed native and visual checks. The original completion flag, forecasts and returns to the Square were verified. Six startup holds, 24 protected name getters and 17 focused tests passed. [Before and after](../{(VERIFY / 'lisbon_before_after_gameplay.png').as_posix()}) · [Testing ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("moonlit_violin", "lisbon_fragrance_wraps")

scope = vars(template) | globals()
for source in (verification, build, commit_candidate):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

