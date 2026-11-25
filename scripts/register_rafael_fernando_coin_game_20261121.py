"""Register the reviewed Fernando exchange and verified cumulative candidate."""
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_rafael_refit_sailing_lessons_20261121 as parent
from scripts import verify_rafael_fernando_coin_game_20261121 as display
from scripts import verify_rafael_fernando_coin_gameplay_20261121 as live
from scripts import verify_rafael_fernando_coin_ui_20261121 as coin
from scripts.source_locked_derivation_v5118 import checked_text


template, stage = parent.template, display.stage
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-rafael-fernando-coin-game-v1-20261121"
ROOT = Path("out/rafael_fernando_coin_game_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_Fernando_Coin_Game_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_rafael_fernando_coin_game_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_fernando_coin_game_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
CHECKPOINT = ("Reviewed all 65 records in Fernando's coin game and recruitment. The registered build has "
              "33 revisions and 32 justified retentions. Both flagged page breaks are gone.")


previous_pages_source = checked_text(getsource(parent.previous_pages), {
    'assert len(reduced) == 7 and live.QUESTION in reduced':
        'assert set(reduced) == {live.STRATEGY, live.CLUE}',
})
verification = checked_text(parent.verification, {
    'draft["decisions"] == {"revision": 34, "retention": 28}': 'draft["decisions"] == {"revision": 34, "retention": 31}',
    'rendered["native_caption_count"] == 4': 'rendered["native_caption_count"] == 2',
    'assert playback["uninterrupted_wind_angle_question"]["id"] == live.QUESTION':
        '''assert [h["id"] for h in playback["uninterrupted_strategy_and_clue"]] == [live.STRATEGY, live.CLUE]
    board = base.load(coin.PROOF)
    assert board["candidate_sha256"] == candidate and board["original_coin_opcode"] == "01c1"
    assert board["round_completed"] and board["original_opening_resumed"]
    assert all(base.digest(name) == digest for name, digest in board["evidence"].items())''',
    '[m["block"] for m in playback["captions"]] == [179, 180]':
        '[m["block"] for m in playback["captions"]] == [178]',
    'viewed == {s["path"]: s["sha256"] for s in rendered["sheets"] + playback["sheets"]}':
        'viewed == {s["path"]: s["sha256"] for s in rendered["sheets"] + playback["sheets"] + board["sheets"]}',
    'len(groups) == 2 and before.keys()': 'len(groups) == 1 and before.keys()',
    'len(checked) == len(draft["records"]) == 62': 'len(checked) == len(draft["records"]) == 65',
    'any(ident == f["id"] for f in playback["unchanged_immediate_followups"]))':
        '''any(ident == f["id"] for f in playback["unchanged_sample_panels"]))
        if ident == live.BYTE_EXACT:
            group = groups[path, row["block"]]
            command, = [cmd for cmd in group["commands"] if ident in cmd["record_ids"]]
            assert row["finding"] == "wrap" and command["current"] == command["stored"]
            row["decision"] = row["finding"] = "retention"
            row["localization_note"] += " The native reflow reproduced the existing wording and line breaks exactly."''',
    '    draft["shorter_pagination"] = previous_pages(previous_rom, draft["records"])':
        '''    from collections import Counter
    draft["decisions"] = dict(Counter(r["decision"] for r in draft["records"]))
    draft["findings"] = dict(Counter(r["finding"] for r in draft["records"]))
    assert draft["decisions"] == {"revision": 33, "retention": 32}
    assert draft["findings"] == {"prose and wrap": 32, "wrap": 1, "retention": 32}
    draft["shorter_pagination"] = previous_pages(previous_rom, draft["records"])
    draft["focused_coin_ui_evidence"] = str(coin.PROOF)''',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_alexandria_ship_lessons_predecessor": "verified_rafael_refit_sailing_lessons_predecessor",
    "len(batches) == 991 and len(checks) == 326": "len(batches) == 992 and len(checks) == 327",
    "original_refit_and_sailing_command_maps_preserved=True": "original_coin_opcode_and_branch_maps_preserved=True",
    "previously_localized_records=62": "previously_localized_records=65",
    "wrap_only_revisions=2, justified_retentions=28": "wrap_only_revisions=1, justified_retentions=32",
    "pagination_fixes=7": "pagination_fixes=2",
    "focused_Rafael_refit_and_sailing_lessons=True": "focused_Fernando_dialogue_and_coin_UI=True",
    "native_revised_pages=34, observed_holds=19, native_choice_captions=4":
        "native_revised_pages=33, observed_holds=19, native_choice_captions=2, observed_original_coin_round=True",
    "prior_records_reviewed=62": "prior_records_reviewed=65",
    "justified_retentions=28, wrap_only_revisions=2": "justified_retentions=32, wrap_only_revisions=1",
    "QA, live.PROOF, display.PROOF, args.visual_review": "QA, live.PROOF, display.PROOF, coin.PROOF, args.visual_review",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Fernando's coin game and recruitment testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the complete reviewed scene and preserves the previous cumulative release. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_refit_sailing_lessons", "rafael_fernando_coin_game")
build = build.replace("verified_rafael_fernando_coin_game_predecessor", "verified_rafael_refit_sailing_lessons_predecessor")

notes = parent.commit_candidate[parent.commit_candidate.index("    DOC.write_text"):parent.commit_candidate.index("    prefix =")]
commit_candidate = checked_text(parent.commit_candidate, {
    "Preserve the flagship refit and sailing candidate, staging and focused emulator ROMs":
        "Preserve the Fernando candidate, staging and focused emulator ROMs",
    'base.load(live.PROOF)["evidence"] if p.endswith(".nds")':
        '(base.load(live.PROOF)["evidence"] | base.load(coin.PROOF)["evidence"]) if p.endswith(".nds")',
    notes: '''    DOC.write_text(f"""# Fernando's coin game and recruitment

Reviewed all 65 records in the game and recruitment exchange. The batch has 32 wording revisions, one wrap-only revision and 32 justified retentions. Janus's rule still leaves one more than a multiple of four, and Rafael's nine-coin example fits on one page. Fernando's clue about the woman's clenched fist also fits on one page. Man and Woman remain the role labels for the couple. [Exact source, predecessor and current references](../{REVIEW.as_posix()})

The native check covered 33 changed pages, one byte-exact reflow, nine name-length cases and both retained choice captions. A focused emulator excerpt matched 19 revised pages, five unchanged panels and the choice menu, including the ordinary Man and Woman nameplates. A separate fixture played a complete round through the original coin interface and observed the return to the opening scene. Natural story activation, unplayed recruitment branches and hardware remain unverified. [Native and play evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters, 17 focused tests and exact clean-input reconstruction passed. All editorial credit carries forward. [Cumulative testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_refit_sailing_lessons", "rafael_fernando_coin_game")

scope = vars(parent.template) | globals()
for source in (previous_pages_source, verification, build, commit_candidate):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
