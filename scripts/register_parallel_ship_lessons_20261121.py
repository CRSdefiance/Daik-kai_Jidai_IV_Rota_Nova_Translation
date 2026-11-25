"""Register the three verified Alexandria exchanges as a cumulative testing candidate."""
from collections import Counter
from pathlib import Path

from scripts import register_hodram_alexandria_tutorial_20261121 as parent
from scripts import verify_parallel_ship_lessons_20261121 as display
from scripts import verify_parallel_ship_lessons_gameplay_20261121 as live
from scripts.source_locked_derivation_v5118 import checked_text


template = parent.template
stage = display.stage
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-alexandria-ship-lessons-v1-20261121"
ROOT = Path("out/parallel_ship_lessons_registered_20261121")
ROM = ROOT / "Translation_DS_Alexandria_Ship_Lessons_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_alexandria_ship_lessons_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_alexandria_ship_lessons_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
CHECKPOINT = ("Revisited all 175 records in Rafael, Lil and Maria's Alexandria recruitment and ship lessons, "
              "with 110 revisions and 65 justified retentions. The registered checkpoint now includes all four routes.")


verification = checked_text(parent.verification, {
    'draft["decisions"] == {"revision": 22, "retention": 26}':
        'draft["decisions"] == {"revision": 113, "retention": 62}',
    'assert playback["natural_activation"] and playback["exact_native_glyph_matches"]':
        'assert playback["initialized_excerpts"] and playback["exact_native_glyph_matches"]',
    'assert playback["original_port_transition"] and not playback["hardware_verified"]':
        'assert not playback["natural_activation"] and not playback["hardware_verified"]',
    'rendered["newly_rendered_pages"] == 22': 'rendered["newly_rendered_pages"] == 112',
    'assert len(playback["holds"]) == 22 and rendered["native_caption_count"] == 2':
        'assert len(playback["holds"]) == 11 and rendered["native_caption_count"] == 4\n'
        '    assert rendered["exact_menu_routes"] == [0, 2] and playback["extra_armor_notice"]["exact_prior_body_mask"]',
    'set(playback["menu"]["bounds"]) == {"Listen", "Skip"} and playback["menu"]["selected"] == "Listen"':
        'set(playback["captions"]["bounds"]) == {"Listen", "Skip"} and playback["captions"]["selected"] == "Listen"',
    'len(groups) == 2 and before.keys()': 'len(groups) == 3 and before.keys()',
    'changed_paths == {"/data/SC1.DK4"}': 'changed_paths == {"/data/SC0.DK4", "/data/SC2.DK4", "/data/SC3.DK4"}',
    'len(checked) == len(draft["records"]) == 48': 'len(checked) == len(draft["records"]) == 175',
    'assert result.get("native_caption") or (1 <= result["native_pages"] <= 2 and (path, ident) in seen)':
        'assert result.get("native_caption") or 1 <= result["native_pages"] <= 2',
    'row["observed_in_ordinary_gameplay"] = (path, ident) in seen or result.get("native_caption", False)':
        '''row["observed_in_initialized_excerpt"] = ((path, ident) in seen or
            ident in playback["captions"]["ids"] or ident == playback["extra_armor_notice"]["id"])
        if row["finding"] == "wrap":
            group = groups[path, row["block"]]
            command, = [cmd for cmd in group["commands"] if ident in cmd["record_ids"]]
            assert command["current"] == command["stored"]
            row["decision"] = row["finding"] = "retention"
            row["localization_note"] += " The reflow reproduced the existing stored wraps byte for byte."
        if row["route"] == 2 and result.get("native_caption"):
            assert row["source_reference"]["command_offset"] == 1654 and len(row["native_slots"]) == 1
            slot, = row["native_slots"]
            assert (slot, ident) in ((0, "DK4_MES_B164_R0109"), (1, "DK4_MES_B164_R0111"))
            row["paired_record_id"] = ident
            row["id"] = f"DK4_CHOICE_B164_C1654_O{slot}"''',
    '    draft.update(candidate_sha256': '''    draft["decisions"] = dict(Counter(row["decision"] for row in draft["records"]))
    draft["findings"] = dict(Counter(row["finding"] for row in draft["records"]))
    assert draft["decisions"] == {"revision": 110, "retention": 65}
    assert draft["findings"] == {"prose and wrap": 106, "choice caption": 4, "retention": 65}
    draft.update(candidate_sha256''',
    'ordinary_town_replay_evidence=str(live.PROOF)': 'initialized_replay_evidence=str(live.PROOF)',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_alexandria_square_predecessor": "verified_hodram_alexandria_tutorial_predecessor",
    "len(batches) == 989 and len(checks) == 324": "len(batches) == 990 and len(checks) == 325",
    "original_port_and_choice_command_maps_preserved=True": "original_three_exchange_and_choice_command_maps_preserved=True",
    "changed_components=1, repository_tests": "changed_components=3, repository_tests",
    "previously_localized_records=48, new_contextual_records=0, prose_revisions=19":
        "previously_localized_records=175, new_contextual_records=0, prose_revisions=106",
    "wrap_only_revisions=2, justified_retentions=26": "wrap_only_revisions=0, justified_retentions=65",
    "pagination_fixes=4, choice_label_revisions=1, name_consistency_revisions=0":
        "two_page_count_explanations=3, choice_label_revisions=4, name_consistency_revisions=0",
    "ordinary_Hodram_Alexandria_ship_lesson=True": "focused_Rafael_Alexandria_ship_lesson=True",
    "native_revised_pages=22, observed_holds=22, native_choice_captions=2, natural_activation=True":
        "native_revised_pages=109, observed_holds=11, native_choice_captions=4, natural_activation=False",
    "prior_records_reviewed=48, observed_Alexandria_panels=22, native_pages=22":
        "prior_records_reviewed=175, observed_Rafael_panels=11, native_pages=112",
    "prose_revisions=19, justified_retentions=26, wrap_only_revisions=2, choice_label_revisions=1, pagination_fixes=4":
        "prose_revisions=106, justified_retentions=65, wrap_only_revisions=0, choice_label_revisions=4, two_page_count_explanations=3",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Alexandria ship-buying lessons testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the four reviewed Alexandria scenes and Cesare's ship-buying lessons. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_alexandria_tutorial", "parallel_ship_lessons")
# Keep the predecessor's registered name while giving this transaction its own keys.
build = build.replace("verified_parallel_ship_lessons_predecessor", "verified_hodram_alexandria_tutorial_predecessor")

notes = parent.commit_candidate[parent.commit_candidate.index("    DOC.write_text"):parent.commit_candidate.index("    prefix =")]
commit_candidate = checked_text(parent.commit_candidate, {
    "Preserve the Alexandria arrival tutorial candidate and staging ROM":
        "Preserve the Alexandria ship-lessons candidate, staging and focused emulator ROMs",
    notes: '''    DOC.write_text(f"""# Alexandria recruitment and ship-buying lessons

Reviewed 175 records across Rafael, Lil and Maria's complete Alexandria encounters. There are 106 wording revisions, four caption revisions and 65 justified retentions. Rafael's encounter keeps Janus's excitement about the lost Elysion and the original extra-armor unlock. Lil's exchange and Maria's retelling share Cesare's blunt opening without losing the differences in how they recruit him. All three lessons keep the original prices, quantities and advice, including Lil's regional-fleet recommendation. Maria's scene proceeds directly to the lesson. [Exact source, predecessor and current references](../{REVIEW.as_posix()})

The new Listen and Skip captions match Hodram's lesson. The native choice checks exercised both options and cancel. All 109 revised speech pages, three byte-exact rereads, six stress pages and four captions passed native checks and visual review. The focused Rafael emulator excerpt verified eleven revised pages, both captions and the preserved extra-armor notice. Natural activation of these three versions and hardware remain unverified. Hodram's ordinary voyage retains its separate evidence. [Native and play evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters, 17 focused tests and the exact clean-input reconstruction passed. All editorial credit carries forward. [Cumulative testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_alexandria_tutorial", "parallel_ship_lessons")

scope = vars(template) | globals()
for source in (verification, build, commit_candidate):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
