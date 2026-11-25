"""Register the four reviewed lessons and exact cumulative clean-input patch."""
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_fernando_parallel_routes_20261121 as parent
from scripts import register_rafael_refit_sailing_lessons_20261121 as ancestor
from scripts import verify_refit_sailing_parallel_gameplay_20261121 as live
from scripts import verify_refit_sailing_parallel_routes_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


template, stage = parent.template, display.stage
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-refit-sailing-parallel-lessons-v1-20261121"
ROOT = Path("out/refit_sailing_parallel_routes_registered_20261121")
ROM = ROOT / "Translation_DS_Refit_And_Sailing_All_Routes_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_refit_sailing_parallel_routes_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_refit_sailing_parallel_routes_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
CHECKPOINT = ("Reviewed 134 records across four refit and sailing lessons. The registered build has "
              "85 revisions, 49 justified retentions and three fewer page turns.")


previous_pages_source = checked_text(getsource(ancestor.previous_pages), {
    'assert len(reduced) == 7 and live.QUESTION in reduced':
        'assert set(reduced) == {"DK4_MES_B171_R0075", "DK4_MES_B171_R0095", "DK4_MES_B171_R0098"}',
})
verification = checked_text(ancestor.verification, {
    'draft["decisions"] == {"revision": 34, "retention": 28}': 'draft["decisions"] == {"revision": 85, "retention": 49}',
    'rendered["newly_rendered_pages"] == 34': 'rendered["newly_rendered_pages"] == 85',
    'len(playback["holds"]) == 19 and rendered["native_caption_count"] == 4':
        'len(playback["holds"]) == 36 and rendered["native_caption_count"] == 8',
    'assert playback["uninterrupted_wind_angle_question"]["id"] == live.QUESTION':
        'assert len(playback["unchanged_sample_panels"]) == 1 and {h["route"] for h in playback["holds"]} == {1, 2}',
    '[m["block"] for m in playback["captions"]] == [179, 180]':
        '[m["route"] for m in playback["captions"]] == [1, 2]',
    'playback["unchanged_immediate_followups"]': 'playback["unchanged_sample_panels"]',
    'len(groups) == 2 and before.keys()': 'len(groups) == 4 and before.keys()',
    'changed_paths == {"/data/SC0.DK4"}': 'changed_paths == {f"/data/SC{i}.DK4" for i in (1, 2, 3)}',
    'len(checked) == len(draft["records"]) == 62': 'len(checked) == len(draft["records"]) == 134',
    '    draft["shorter_pagination"] = previous_pages(previous_rom, draft["records"])':
        '''    draft["shorter_pagination"] = previous_pages(previous_rom, draft["records"])
    assert draft["findings"] == {"prose and wrap": 84, "wrap": 1, "retention": 49}''',
})

readme = ancestor.build[ancestor.build.index('    (PACKAGE / "README.md").write_text'):ancestor.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(ancestor.build, {
    "verified_alexandria_ship_lessons_predecessor": "verified_fernando_parallel_routes_predecessor",
    "len(batches) == 991 and len(checks) == 326": "len(batches) == 994 and len(checks) == 329",
    "changed_components=1, repository_tests": "changed_components=3, repository_tests",
    "previously_localized_records=62, new_contextual_records=0, prose_revisions=32":
        "previously_localized_records=134, new_contextual_records=0, prose_revisions=84",
    "wrap_only_revisions=2, justified_retentions=28": "wrap_only_revisions=1, justified_retentions=49",
    "pagination_fixes=7": "pagination_fixes=3",
    "focused_Rafael_refit_and_sailing_lessons=True": "focused_Hodram_sailing_and_Lil_refit=True",
    "native_revised_pages=34, observed_holds=19, native_choice_captions=4":
        "native_revised_pages=85, observed_holds=36, native_choice_captions=8",
    "prior_records_reviewed=62, observed_Rafael_panels=19, native_pages=34":
        "prior_records_reviewed=134, observed_Hodram_and_Lil_panels=36, native_pages=85",
    "prose_revisions=32, justified_retentions=28, wrap_only_revisions=2":
        "prose_revisions=84, justified_retentions=49, wrap_only_revisions=1",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Parallel refit and sailing lessons testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the four reviewed sailing and refit lessons. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_refit_sailing_lessons", "refit_sailing_parallel_routes")

notes = ancestor.commit_candidate[ancestor.commit_candidate.index("    DOC.write_text"):ancestor.commit_candidate.index("    prefix =")]
commit_candidate = checked_text(ancestor.commit_candidate, {
    "Preserve the flagship refit and sailing candidate, staging and focused emulator ROMs":
        "Preserve the parallel refit and sailing candidate, staging and focused emulator ROMs",
    notes: '''    DOC.write_text(f"""# Hodram, Lil and Maria's refit and sailing lessons

Reviewed all 134 records across four complete scenes. The batch has 84 wording revisions, one wrap-only revision and 49 justified retentions. Lil and Maria's refit advice uses the game's room and job names, including Nursery, Sickbay, Cabin and Lounge. Hodram's square-sail, spritsail and jigger-spanker speeches now fit on one page each. Manuel's distinct introductions and the player's original dialogue choices remain intact. [Exact source, predecessor and current references](../{REVIEW.as_posix()})

All 85 revised pages, 15 name-length cases and eight retained captions passed native checks and visual review. Focused emulator excerpts verified 36 revised pages, one retained speech and both choice menus in Hodram's sailing and Lil's refit scenes. The other scenes were checked offline. Natural activation and hardware remain unverified. [Native and play evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters, 17 focused tests and exact clean-input reconstruction passed. Existing editorial credit carries forward. [Cumulative testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_refit_sailing_lessons", "refit_sailing_parallel_routes")

scope = vars(template) | globals()
for source in (previous_pages_source, verification, build, commit_candidate):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
