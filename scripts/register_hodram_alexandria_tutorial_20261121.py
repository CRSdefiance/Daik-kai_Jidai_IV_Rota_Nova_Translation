"""Register the verified Hodram arrival and ship-advice revision."""
from pathlib import Path

from scripts import register_alexandria_dialogue_20261121 as parent
from scripts import verify_hodram_alexandria_tutorial_20261121 as display
from scripts import verify_hodram_alexandria_tutorial_gameplay_20261121 as live
from scripts.source_locked_derivation_v5118 import checked_text


template = parent.template
stage = display.stage
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-hodram-alexandria-tutorial-v1-20261121"
ROOT = Path("out/hodram_alexandria_tutorial_registered_20261121")
ROM = ROOT / "Translation_DS_Hodram_Alexandria_Tutorial_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_hodram_alexandria_tutorial_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_hodram_alexandria_tutorial_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
CHECKPOINT = ("Hodram's Alexandria warning and Cesare's ship-buying lesson have 22 revisions and 26 justified "
              "retentions. Ordinary gameplay verified the revised pages and both menu captions.")


verification = checked_text(parent.verification, {
    'draft["decisions"] == {"revision": 10, "retention": 38}':
        'draft["decisions"] == {"revision": 22, "retention": 26}',
    'playback["original_notice_dismissal_and_Square_return"]': 'playback["original_port_transition"]',
    'rendered["newly_rendered_pages"] == 10': 'rendered["newly_rendered_pages"] == 22',
    'len(playback["holds"]) == 2 and playback["full_scene_panels"] == 12':
        'len(playback["holds"]) == 22 and rendered["native_caption_count"] == 2\n'
        '    assert set(playback["menu"]["bounds"]) == {"Listen", "Skip"} and playback["menu"]["selected"] == "Listen"',
    'len(groups) == 4 and before.keys()': 'len(groups) == 2 and before.keys()',
    'changed_paths == {f"/data/SC{i}.DK4" for i in range(4)}': 'changed_paths == {"/data/SC1.DK4"}',
    'assert result["native_pages"] == 1 and ((path, ident) in seen) == (row["route"] == 1)':
        'assert result.get("native_caption") or (1 <= result["native_pages"] <= 2 and (path, ident) in seen)',
    'row["observed_in_ordinary_gameplay"] = row["route"] == 1':
        'row["observed_in_ordinary_gameplay"] = (path, ident) in seen or result.get("native_caption", False)',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_mediterranean_dialogue_predecessor": "verified_alexandria_square_predecessor",
    "len(batches) == 988 and len(checks) == 323": "len(batches) == 989 and len(checks) == 324",
    "four_original_town_event_and_command_maps_preserved=True": "original_port_and_choice_command_maps_preserved=True",
    "changed_components=4, repository_tests": "changed_components=1, repository_tests",
    "previously_localized_records=48, new_contextual_records=0, prose_revisions=10":
        "previously_localized_records=48, new_contextual_records=0, prose_revisions=19",
    "wrap_only_revisions=0, justified_retentions=38": "wrap_only_revisions=2, justified_retentions=26",
    "pagination_fixes=0, name_consistency_revisions=0": "pagination_fixes=4, choice_label_revisions=1, name_consistency_revisions=0",
    "ordinary_Hodram_Alexandria_Square=True": "ordinary_Hodram_Alexandria_ship_lesson=True",
    "native_revised_pages=10, observed_holds=12, natural_activation=True":
        "native_revised_pages=22, observed_holds=22, native_choice_captions=2, natural_activation=True",
    "prior_records_reviewed=48, observed_Alexandria_panels=12, offline_pages=10":
        "prior_records_reviewed=48, observed_Alexandria_panels=22, native_pages=22",
    "prose_revisions=10, justified_retentions=38, wrap_only_revisions=0":
        "prose_revisions=19, justified_retentions=26, wrap_only_revisions=2, choice_label_revisions=1, pagination_fixes=4",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's Alexandria arrival and ship-buying tutorial candidate

The [testing ROM](../../{ROM.as_posix()}) includes the revised port warning, recruitment and ship lesson. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("alexandria_dialogue", "hodram_alexandria_tutorial")

notes = parent.commit_candidate[parent.commit_candidate.index("    DOC.write_text"):parent.commit_candidate.index("    prefix =")]
commit_candidate = checked_text(parent.commit_candidate, {
    "Preserve the Alexandria Square candidate and the staging ROM": "Preserve the Alexandria arrival tutorial candidate and staging ROM",
    notes: '''    DOC.write_text(f"""# Hodram's port warning and Cesare's ship-buying tutorial

Reviewed all 48 records across the two complete exchanges. The batch has 19 wording revisions, two wrap-only revisions, one revised caption and 26 justified retentions. The port warning keeps “southern Mediterranean” together. Cesare's advice restores why more supply holds let players open routes to distant towns, and keeps the original ship prices, holds, mast counts and crew requirements. Four advice panels fit on one page where the earlier versions used two. [Exact source, current and registered references](../{REVIEW.as_posix()})

The ordinary voyage replay selected **Listen**, displayed all 22 revised speech pages and both captions with complete glyph masks, and returned to the same Alexandria Port screen. The native menu check exercised Listen, Skip and cancel at both tested alignments. The two original Skip speeches have offline and stored-script coverage. The maximum tested given-name substitution fits Charles's reply. Hardware remains unverified. [Gameplay and native evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters and 17 focused tests passed. The clean-input patch reconstructs the cumulative ROM exactly. All 48 records already carried ledger credit. [Cumulative testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("alexandria_dialogue", "hodram_alexandria_tutorial")

scope = vars(template) | globals()
for source in (verification, build, commit_candidate):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
