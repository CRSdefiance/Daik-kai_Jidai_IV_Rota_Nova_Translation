"""Register Fernando's reviewed exchanges across the four cumulative routes."""
from collections import Counter
from pathlib import Path

from scripts import register_rafael_fernando_coin_game_20261121 as parent
from scripts import verify_fernando_parallel_gameplay_20261121 as live
from scripts import verify_fernando_parallel_routes_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


template, stage = parent.template, display.stage
base, native, workflow = stage.base, stage.native, parent.workflow
ancestor = parent.parent
PROFILE = "all-routes-fernando-parallel-exchanges-v1-20261121"
ROOT = Path("out/fernando_parallel_routes_registered_20261121")
ROM = ROOT / "Translation_DS_Fernando_All_Routes_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_fernando_parallel_routes_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_fernando_parallel_routes_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE/"own_startup_verification.json", EVIDENCE/"qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
CHECKPOINT = ("Reviewed 120 Fernando records across Hodram, Lil and Maria and fixed Rafael's farewell wrap. "
              "The registered build has 62 revisions and 59 justified retentions.")


verification = checked_text(ancestor.verification, {
    'draft["decisions"] == {"revision": 34, "retention": 28}': 'draft["decisions"] == {"revision": 63, "retention": 58}',
    'rendered["newly_rendered_pages"] == 34': 'rendered["newly_rendered_pages"] == 63',
    'len(playback["holds"]) == 19': 'len(playback["holds"]) == 30',
    'assert playback["uninterrupted_wind_angle_question"]["id"] == live.QUESTION':
        'assert len(playback["unchanged_sample_panels"]) == 4 and {r["route"] for r in playback["holds"]} == {1, 2}',
    '[m["block"] for m in playback["captions"]] == [179, 180]':
        '[m["route"] for m in playback["captions"]] == [1]',
    'len(groups) == 2 and before.keys()': 'len(groups) == 4 and before.keys()',
    'changed_paths == {"/data/SC0.DK4"}': 'changed_paths == {f"/data/SC{i}.DK4" for i in range(4)}',
    'len(checked) == len(draft["records"]) == 62': 'len(checked) == len(draft["records"]) == 121',
    'any(ident == f["id"] for f in playback["unchanged_immediate_followups"]))':
        '''any(ident == f["id"] for f in playback["unchanged_sample_panels"]))
        if ident == display.BYTE_EXACT:
            group = groups[path, row["block"]]
            command, = [cmd for cmd in group["commands"] if ident in cmd["record_ids"]]
            assert row["finding"] == "wrap" and command["current"] == command["stored"]
            row["decision"] = row["finding"] = "retention"
            row["localization_note"] += " The native reflow reproduced the existing wrap exactly."''',
    '    draft["shorter_pagination"] = previous_pages(previous_rom, draft["records"])':
        '''    draft["decisions"] = dict(Counter(r["decision"] for r in draft["records"]))
    draft["findings"] = dict(Counter(r["finding"] for r in draft["records"]))
    assert draft["decisions"] == {"revision": 62, "retention": 59}
    assert draft["findings"] == {"prose and wrap": 60, "wrap": 2, "retention": 59}
    coin_routes = set()
    for group in groups.values():
        for command in group["commands"]:
            if command["word"] == 0xC101:
                assert command["source"] == command["current"] == command["stored"] == "01c1"
                coin_routes.add(group["route"])
    assert coin_routes == {0, 1, 3}
    draft["original_coin_command_routes"] = sorted(coin_routes)''',
})

readme = ancestor.build[ancestor.build.index('    (PACKAGE / "README.md").write_text'):ancestor.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(ancestor.build, {
    "verified_alexandria_ship_lessons_predecessor": "verified_rafael_fernando_coin_game_predecessor",
    "len(batches) == 991 and len(checks) == 326": "len(batches) == 993 and len(checks) == 328",
    "original_refit_and_sailing_command_maps_preserved=True": "original_coin_and_dialogue_command_maps_preserved=True",
    "changed_components=1, repository_tests": "changed_components=4, repository_tests",
    "previously_localized_records=62, new_contextual_records=0, prose_revisions=32":
        "previously_localized_records=121, new_contextual_records=0, prose_revisions=60",
    "wrap_only_revisions=2, justified_retentions=28": "wrap_only_revisions=2, justified_retentions=59",
    "pagination_fixes=7": "pagination_fixes=0",
    "focused_Rafael_refit_and_sailing_lessons=True": "focused_Hodram_and_Lil_Fernando_exchanges=True",
    "native_revised_pages=34, observed_holds=19, native_choice_captions=4":
        "native_revised_pages=62, observed_holds=30, native_choice_captions=4",
    "prior_records_reviewed=62, observed_Rafael_panels=19, native_pages=34":
        "prior_records_reviewed=121, observed_Hodram_and_Lil_panels=30, native_pages=63",
    "prose_revisions=32, justified_retentions=28": "prose_revisions=60, justified_retentions=59",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Fernando's four route exchanges testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed Fernando scenes from all four story routes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_refit_sailing_lessons", "fernando_parallel_routes")

notes = ancestor.commit_candidate[ancestor.commit_candidate.index("    DOC.write_text"):ancestor.commit_candidate.index("    prefix =")]
commit_candidate = checked_text(ancestor.commit_candidate, {
    "Preserve the flagship refit and sailing candidate, staging and focused emulator ROMs":
        "Preserve the Fernando exchanges candidate, staging and focused emulator ROMs",
    notes: '''    DOC.write_text(f"""# Fernando's exchanges across Hodram, Lil and Maria

Reviewed all 120 records in the three complete scenes, plus Rafael's farewell. The batch has 60 wording revisions, two wrap corrections and 59 justified retentions. Hodram and Maria see the same telling clues when the couple breaks up, while Lil's scene uses Camille's questions to reveal Fernando's loss at Old Maid. The coin wager, distinct offers and Maria's original company substitutions are preserved. Rafael's farewell keeps “See you” together. [Exact source, predecessor and current references](../{REVIEW.as_posix()})

The native checks covered all 62 changed pages, one reflow that reproduced the old bytes, six name-length cases, both retained choice menus and Maria's company-name calls. Focused emulator excerpts verified 30 revised pages across Hodram and Lil, four retained speech panels and Hodram's complete Play and Pass menu. Maria's scene and Rafael's revised wrap were checked offline. Natural activation for these scenes and hardware remain unverified. [Native and play evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters, 17 focused tests and exact clean-input reconstruction passed. The three original coin opcodes and all accepted layers remain intact. Existing editorial credit carries forward. [Cumulative testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_refit_sailing_lessons", "fernando_parallel_routes")

scope = vars(template) | globals()
for source in (verification, build, commit_candidate):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
