"""Register the canonical room labels in a clean-input cumulative candidate."""

from inspect import getsource
from pathlib import Path
from xml.etree import ElementTree as ET

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_maria_tutorial_followup_20261122 as parent
from scripts import register_rafael_tradehouse_festival_20261121 as startup_template
from scripts import reconcile_shared_display_20261121 as pending
from scripts import stage_ship_room_names_20261122 as writer
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
stage = writer
PROFILE = "all-routes-shared-ship-room-names-v1-20261122"
ROOT = parent.ROOT.with_name("ship_room_names_registered_20261122")
ROM = ROOT / "Translation_DS_Ship_Room_Names_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_ship_room_names_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_ship_room_names_registered_20261122.md")
EVIDENCE = writer.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
ITEMS = EVIDENCE / "item_gameplay/verified_gameplay.json"
ITEM_NATIVE, DECK_NATIVE = [EVIDENCE / "native_display" / f"{name}_proof.json" for name in ("item", "deck")]
CHECKPOINT = "Registered Lounge in Cristina's fatigue dialogue and Nursery in the Gauze Mask and Stylish Boots descriptions."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard


startup_source = checked_text(getsource(startup_template.startup_proof), {
    "original_ARM9_and_overlay_preserved=True": "original_ARM9_and_overlay_preserved=False, "
    "private_item_text_bytes_only_in_ARM9=True, original_overlay_preserved=True",
})
startup_env = startup_template.startup_proof.__globals__ | {"STARTUP":STARTUP, "STARTUP_CAPTURE":STARTUP_CAPTURE,
    "checked_report":startup_template.check_startup_report}
exec(compile(startup_source,__file__+"::startup","exec"),startup_env)


def observed_count():
    return len(base.load(ITEMS)["observed"])


def verify(registry, previous, viewed):
    stored, draft, item, native_items, native_deck = map(base.load,
        (stage.PROOF, stage.MANUSCRIPT, ITEMS, ITEM_NATIVE, DECK_NATIVE))
    candidate = base.digest(stage.ROM)
    assert all(r["candidate_sha256"] == candidate for r in (stored,draft,item,native_items,native_deck))
    assert previous["candidate_sha256"] == base.digest(parent.ROM) == stored["predecessor_sha256"] == draft["parent"]
    assert base.digest(stage.MANUSCRIPT) == stored["manuscript_sha256"] and stored["whole_parent_inverse"]
    assert base.digest(stage.INTAKE) == draft["source_preflight_sha256"]
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    assert base.digest(EVIDENCE/"clean_rebuilt.nds") == candidate
    reports = (item, native_items, native_deck)
    assert viewed == {r["sheet"]:r["sheet_sha256"] for r in reports}
    assert all(base.digest(path) == sha for path,sha in viewed.items())
    suite, = ET.parse(QA).iter("testsuite")
    assert [int(suite.get(k,"0")) for k in ("tests","failures","errors","skipped")] == [17,0,0,0]
    assert item["original_town_return_exact"] and item["ordinary_item_controls"] and not item["hardware"]
    assert [(r["message_ID"],r["item_ID"]) for r in item["observed"]] == [(2919,104),(2920,105)]
    assert all(m["complete_foreground_and_blank_cells"] for r in item["observed"] for m in r["screen_masks"])
    assert item["report_sha256"] == base.digest(EVIDENCE/"item_gameplay/capture/capture_report.json")
    assert native_items["tested_all_native_getters"] == 218 and native_items["unchanged_description_getters"] == 216
    cases = {(r["message_ID"],r["page"],r["mode"]):r for r in native_items["cases"]}
    assert len(cases) == 8
    assert len(native_deck["cases"]) == 2 and all(r["complete_native_copy_macro_draw_and_ABI"] and
        r["full252x96_native_and_independent_canvas_equal"] and r["bitmap_and_input_guards_exact"]
        for r in native_deck["cases"])

    clean, predecessor, target = map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    before, after = map(native.files,(predecessor,target))
    assert before.keys() == after.keys()
    names = {stage.ARM,stage.COMMON}
    assert {name for name in before if before[name] != after[name]} == names
    archives = {name:native.digest(after[name]) for name in names}
    assert archives == stored["stored_components"]
    common = stage.common
    arm = after[stage.ARM]
    directory = native.digest(arm[common.DIRECTORY_OFFSET:common.TABLE_OFFSET])
    current = common.owned_entries(before[stage.COMMON],before[stage.ARM],directory)
    installed = common.owned_entries(after[stage.COMMON],arm,directory)
    assert [a.message_id for a,b in zip(current,installed,strict=True) if a.text != b.text] == list(stage.IDS)
    clean_rows = common.common_message_entries(clean.read_file(stage.COMMON),clean.read_file(stage.ARM))
    intake = base.load(stage.INTAKE)
    proposals = {row["message_ID"]:row for row in intake["records"]}
    rebuilt, projections = stage.make_projections(before[stage.ARM],proposals)
    assert rebuilt == arm and projections == stored["private_item_allocations"]
    pending_rows = base.load(pending.OUTPUT)["records"]
    assert len(pending_rows) == 276
    assert all(common.reference(installed[r["message_ID"]]) == r["current_reference"]
               and installed[r["message_ID"]].text.hex() == r["current_hex"] for r in pending_rows)
    for name in names:
        target.replace_file(name,before[name])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    controls = bind_registered_story_percent_guard(registry["profiles"][previous["profile"]]["source25_multiarchive_guard"])(
        native.files(clean),after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    startup_env["startup_proof"](previous,candidate,arm)

    rows = draft["records"]
    assert [r["message_ID"] for r in rows] == list(stage.IDS)
    for row in rows:
        ident = row["message_ID"]
        assert (row["source_hex"],row["current_hex"],row["installed_hex"]) == tuple(
            table[ident].text.hex() for table in (clean_rows,current,installed))
        if ident == 1784:
            assert all(r["generated_native_lines"] == row["expected_lines"] for r in native_deck["cases"])
            row["gameplay_frames"] = []
            row["gameplay_scope"] = "Original ordinary and combat Deck consumers checked offline. Historical combat replay reached frame 15300 without entering combat on the current build."
        else:
            for page in ("main","standalone"):
                for mode in (4,16):
                    case = cases[ident,page,mode]
                    assert case["exact_plane_and_bounds"]
                    assert [d["text"] for d in case["line_draws"]] == row["expected_lines"]
            row["gameplay_frames"] = [r["frame"] for r in item["observed"] if r["message_ID"] == ident]
        row["review"]["formatting"] = True
        row["registered_reference"] = row["installed_reference"] | {"candidate_sha256":candidate}
    draft.update(checked_story_format_guard=controls, native_proof_paths=[str(ITEM_NATIVE),str(DECK_NATIVE)],
        direct_visual_review=viewed, observed_items=str(ITEMS), observed_deck=False,
        unchanged_pending_records=276, historical_source_credit=dict(by_census_id={},direct_keys=3),
        new_contextual_records=0, full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(draft)
    return stored,draft,archives


old_readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build,{
    "len(batches) == 1042 and len(checks) == 377":"len(batches) == 1043 and len(checks) == 378",
    "verified_maria_B51_B70_predecessor=predecessor":"verified_maria_tutorial_followup_predecessor=predecessor",
    "live.LIVE, display.PROOF, args.visual_review":"ITEMS, ITEM_NATIVE, DECK_NATIVE, args.visual_review",
    'source.parent.name + "_" + source.name if source==live.LIVE else source.name':'source.name',
    "native_and_emulator_evidence_sha256=base.digest(live.LIVE),":
        "native_and_emulator_evidence_sha256={str(p):base.digest(p) for p in (ITEMS, ITEM_NATIVE, DECK_NATIVE)},",
    "original_name_substitution_order=True, archive_hashes=archives, command_maps_FE_choice_slots_and_actor_style_aliases_preserved=True,":
        "original_item_description_pointers=True, archive_hashes=archives, original_deck_and_item_display_controls_preserved=True,",
    'target_ARM9_sha256=previous["target_ARM9_sha256"]':'target_ARM9_sha256=archives[stage.ARM]',
    "changed_components=1, repository_tests=17":"changed_components=2, target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON], repository_tests=17",
    "previously_localized_records=12, contextual_records_revisited=12, contextual_decisions_reused=3827, new_contextual_records=0, prose_revisions=6":
        "previously_localized_records=3, contextual_records_revisited=3, contextual_decisions_reused=0, new_contextual_records=0, prose_revisions=3",
    "wrap_only_revisions=0, justified_retentions=6":"wrap_only_revisions=0, justified_retentions=0",
    "two_page_count_explanations=0, pagination_fixes=pages_saved(), choice_label_revisions=0, name_consistency_revisions=0":
        "two_page_count_explanations=0, pagination_fixes=0, choice_label_revisions=0, name_consistency_revisions=3",
    "initialized_Maria_tutorial_followup=True,\n            native_revised_pages=native_count(), observed_holds=observed_count(), contextual_nameplate_retentions=observed_names(), reclaimed_page_turns=pages_saved(), actual_menu_samples=0, actual_style_objects=0, natural_activation=False, hardware=False":
        "initialized_item_inventory=True, native_revised_records=3, deck_fatigue_live=False,\n            observed_holds=observed_count(), actual_menu_samples=2, actual_style_objects=0, natural_activation=False, hardware=False",
    "registered_release_verification=str(RELEASE),":
        'registered_release_verification=str(RELEASE), ARM9_sha256=archives[stage.ARM], MESFILE_sha256=archives[stage.COMMON],',
    "prior_records_reviewed=12, contextual_decisions_reused=3827, observed_Maria_panels=observed_count(), native_pages=native_count(), new_contextual_credit=0,":
        "prior_records_reviewed=3, terminology_revisions=3, observed_holds=observed_count(), native_records=3, new_contextual_credit=0,",
    "prose_revisions=6, punctuation_glyph_corrections=0, justified_retentions=6, wrap_only_revisions=0, choice_label_revisions=0, pagination_fixes=pages_saved()":
        "prose_revisions=3, punctuation_glyph_corrections=0, justified_retentions=0, wrap_only_revisions=0, choice_label_revisions=0, pagination_fixes=0",
    old_readme:'''    (PACKAGE / "README.md").write_text(f"""# Ship room names testing candidate

The [testing ROM](../../{ROM.as_posix()}) uses the established room names in Cristina's fatigue line and two equipment descriptions. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("maria_tutorial_followup","ship_room_names").replace(
    "verified_ship_room_names_predecessor","verified_maria_tutorial_followup_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit,{
    "    research = [live.ROM]":"    research = []",
    "Preserve the Maria tutorial candidate, predecessor, staged ROM and focused fixture":
        "Preserve the ship room names candidate, predecessor and staged ROM",
    old_doc:'''    DOC.write_text(f"""# Ship room names

Cristina refers to the Lounge when she is worn out. The Gauze Mask and Stylish Boots describe their use in the Nursery. Both labels match the crew assignment menu. The Japanese, previous English and the exact installed text in each owner are recorded for all three changes. [Exact editorial decisions](../{REVIEW.as_posix()})

The original renderer verified the Deck line and both item views. The original Items menu displayed both descriptions and returned to town in a focused emulator replay with prepared inventory. Cristina's line passed the original Deck renderer offline in the ordinary and battle contexts. The historical combat replay reached its checkpoint at sea. The current line still awaits observation during live Deck play. Hardware remains unvisited. [Display and emulator checks](../{VERIFY.as_posix()})

The current ROM passed its own startup and 17 focused tests. The full patch rebuilds it byte for byte from the clean input. The 114 accepted layers and the ASCII right-bound correction carry forward. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("maria_tutorial_followup","ship_room_names")
scope = parent.scope | globals()
for source in (build,commit):
    exec(compile(source,__file__+"::registered","exec"),scope)


if __name__ == "__main__":
    scope["main"]()

