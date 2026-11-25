"""Register Rafael's revised refit and sailing lessons with their display evidence."""
from pathlib import Path
from types import SimpleNamespace

from scripts import register_parallel_ship_lessons_20261121 as parent
from scripts import verify_rafael_refit_sailing_gameplay_20261121 as live
from scripts import verify_rafael_refit_sailing_lessons_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


template, stage = parent.template, display.stage
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-rafael-refit-sailing-lessons-v1-20261121"
ROOT = Path("out/rafael_refit_sailing_lessons_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_Refit_And_Sailing_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_rafael_refit_sailing_lessons_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_refit_sailing_lessons_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
CHECKPOINT = ("Reviewed all 62 records in Rafael's flagship refit and sailing lessons. The registered build "
              "has 34 revisions and 28 justified retentions. Seven revised speeches fit on one page.")


def previous_pages(image, records):
    arm = image.read_file(native.ARM)
    font = image.read_file("/GRP/KANJI.FNT")
    painter = display.display.clipped_renderer(SimpleNamespace(image=image, arm=arm))
    reduced = []
    for row in records:
        if row["decision"] != "revision":
            continue
        old = bytes.fromhex(row["current_hex"])[1:]
        if old.count(10) < 4:
            continue
        assert not stage.review.TOKEN.findall(old.decode("ascii"))
        before = painter(arm, font, old)["pages"]
        assert len(before) == 2 and row["native_formatting_evidence"]["native_pages"] == 1
        reduced.append(row["id"])
        row["previous_native_pages"] = len(before)
    assert len(reduced) == 7 and live.QUESTION in reduced
    return reduced


verification = checked_text(parent.parent.verification, {
    'draft["decisions"] == {"revision": 22, "retention": 26}': 'draft["decisions"] == {"revision": 34, "retention": 28}',
    'assert playback["natural_activation"] and playback["exact_native_glyph_matches"]':
        'assert playback["initialized_excerpts"] and playback["exact_native_glyph_matches"]',
    'assert playback["original_port_transition"] and not playback["hardware_verified"]':
        'assert not playback["natural_activation"] and not playback["hardware_verified"]',
    'rendered["newly_rendered_pages"] == 22': 'rendered["newly_rendered_pages"] == 34',
    'assert len(playback["holds"]) == 22 and rendered["native_caption_count"] == 2':
        'assert len(playback["holds"]) == 19 and rendered["native_caption_count"] == 4\n'
        '    assert playback["uninterrupted_wind_angle_question"]["id"] == live.QUESTION',
    'assert set(playback["menu"]["bounds"]) == {"Listen", "Skip"} and playback["menu"]["selected"] == "Listen"':
        'assert [m["block"] for m in playback["captions"]] == [179, 180] and all(m["selected"] == 0 for m in playback["captions"])',
    'changed_paths == {"/data/SC1.DK4"}': 'changed_paths == {"/data/SC0.DK4"}',
    'len(checked) == len(draft["records"]) == 48': 'len(checked) == len(draft["records"]) == 62',
    'assert result.get("native_caption") or (1 <= result["native_pages"] <= 2 and (path, ident) in seen)':
        'assert result["native_pages"] == 1',
    'row["observed_in_ordinary_gameplay"] = (path, ident) in seen or result.get("native_caption", False)':
        '''row["observed_in_initialized_excerpt"] = ((path, ident) in seen or
            any(ident in m["ids"] for m in playback["captions"]) or
            any(ident == f["id"] for f in playback["unchanged_immediate_followups"]))''',
    '    draft.update(candidate_sha256': '''    draft["shorter_pagination"] = previous_pages(previous_rom, draft["records"])
    draft.update(candidate_sha256''',
    'ordinary_town_replay_evidence=str(live.PROOF)': 'initialized_replay_evidence=str(live.PROOF)',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_hodram_alexandria_tutorial_predecessor": "verified_alexandria_ship_lessons_predecessor",
    "len(batches) == 990 and len(checks) == 325": "len(batches) == 991 and len(checks) == 326",
    "original_three_exchange_and_choice_command_maps_preserved=True": "original_refit_and_sailing_command_maps_preserved=True",
    "changed_components=3, repository_tests": "changed_components=1, repository_tests",
    "previously_localized_records=175, new_contextual_records=0, prose_revisions=106":
        "previously_localized_records=62, new_contextual_records=0, prose_revisions=32",
    "wrap_only_revisions=0, justified_retentions=65": "wrap_only_revisions=2, justified_retentions=28",
    "two_page_count_explanations=3, choice_label_revisions=4, name_consistency_revisions=0":
        "two_page_count_explanations=0, pagination_fixes=7, choice_label_revisions=0, name_consistency_revisions=0",
    "focused_Rafael_Alexandria_ship_lesson=True": "focused_Rafael_refit_and_sailing_lessons=True",
    "native_revised_pages=109, observed_holds=11, native_choice_captions=4":
        "native_revised_pages=34, observed_holds=19, native_choice_captions=4",
    "prior_records_reviewed=175, observed_Rafael_panels=11, native_pages=112":
        "prior_records_reviewed=62, observed_Rafael_panels=19, native_pages=34",
    "prose_revisions=106, justified_retentions=65, wrap_only_revisions=0, choice_label_revisions=4, two_page_count_explanations=3":
        "prose_revisions=32, justified_retentions=28, wrap_only_revisions=2, choice_label_revisions=0, pagination_fixes=7",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's flagship refit and sailing lessons testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed lessons and preserves the previous cumulative release. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("parallel_ship_lessons", "rafael_refit_sailing_lessons")

notes = parent.commit_candidate[parent.commit_candidate.index("    DOC.write_text"):parent.commit_candidate.index("    prefix =")]
commit_candidate = checked_text(parent.commit_candidate, {
    "Preserve the Alexandria ship-lessons candidate, staging and focused emulator ROMs":
        "Preserve the flagship refit and sailing candidate, staging and focused emulator ROMs",
    notes: '''    DOC.write_text(f"""# Rafael's flagship refit and sailing lessons

Reviewed all 62 records in two complete exchanges. The batch has 32 wording revisions, two wrap-only revisions and 28 justified retentions. Manuel still speaks of the ship as a living thing. His refit advice uses the existing room and job names and preserves their effects. The shipwright's wind-angle question now fits on one page and leads straight into Manuel's answer. Six other revised speeches also fit on one page. [Exact source, predecessor and current references](../{REVIEW.as_posix()})

All 34 revised pages, three additional name-length cases and four retained choice captions passed native checks and visual review. A focused initialized emulator excerpt matched 19 revised pages, both choice menus and the two unchanged panels that follow the wind-angle question. Original menu cancellation and alternate choices passed offline. Natural story activation and hardware remain unverified. [Native and play evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters, 17 focused tests and exact clean-input reconstruction passed. All editorial credit carries forward. [Cumulative testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("parallel_ship_lessons", "rafael_refit_sailing_lessons")

scope = vars(template) | globals()
for source in (verification, build, commit_candidate):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
