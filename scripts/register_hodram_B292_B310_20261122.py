"""Register the source-reviewed Hodram ruins and expedition candidate."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_hodram_B261_B291_20261122 as parent
from scripts import replay_hodram_B292_B310_20261122 as live
from scripts import verify_hodram_B292_B310_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B292-B310-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B292_B310_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B292_B310_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B292_B310_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B292_B310_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
SPEAKERS = stage.ROOT.parent / "B304_B305_speaker_context_reconciliation_v1.json"
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec, startup_reference = parent.guard_spec, parent.startup_reference
CHECKPOINT = ("Reviewed 380 Hodram records across the hidden ruins, market requests, temple routes and expeditions. "
              "The batch revises 112 records and justifies 268 retentions. Three earlier lines gain fuller opening rows, "
              "and 56 other decisions carry forward.")
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | {"display":display})
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | {"live":live})
pages_saved = FunctionType(parent.pages_saved.__code__, parent.pages_saved.__globals__ | {"display":display})


def historical_credit(draft):
    earlier = [Path(f"translations/hodram_{span}_integrated_final_review_v1.json")
               for span in ("B281_B300","B301_B310")]
    menus = {row["id"]:row for path in earlier for row in base.load(path)["records"] if "CHOICE" in row["id"]}
    captions = [row for row in draft["records"] if row["kind"] == "typed-choice-label"]
    assert len(captions) == 13
    updated = {
        "SC1_B302_CHOICE_2272_0": ("Keep going", "Push through"),
        "SC1_B304_CHOICE_576_0": ("Enter", "Enter the swamp"),
        "SC1_B304_CHOICE_576_1": ("Retreat", "Go back"),
    }
    for row in captions:
        ident = row["id"]
        old = menus[ident]
        assert all(old["review"].values()) and old["source_hex"] == row["source_hex"]
        ref = old["source_reference"]
        assert [ref["source_index"]] == row["native_slots"]
        assert all(ref[key] == row["source_reference"][key] for key in ("command_offset","offset"))
        assert row["decision"] == "retention" and row["english"] == row["previous_English"]
        assert (old["english"],row["english"]) == updated.get(ident,(row["english"],row["english"]))
    return dict(by_census_id={}, direct_keys=len(draft["records"]),
                earlier_menu_decisions={str(path):base.digest(path) for path in earlier})


def reconcile_speaker_notes(rows):
    receipt = base.load(SPEAKERS)
    assert receipt["manuscript_sha256"] == base.digest(stage.OUTPUT)
    assert receipt["historical_name_proof_sha256"] == base.digest(receipt["historical_name_proof"])
    assert receipt["native_controls_and_player_text_preserved"]
    assert len(receipt["corrections"]) == 45 and len(receipt["expected_Sakura_selectors"]) == 7
    for ident, expected in receipt["expected_Sakura_selectors"].items():
        assert rows[ident]["source_selector"] == expected == 203 and rows[ident]["speaker"] == "Sakura"
    for entry in receipt["corrections"]:
        row = rows[entry["id"]]
        assert row["block"] in (304,305)
        for name, change in entry["fields"].items():
            assert name in ("context","source_meaning","localization_note")
            assert row[name] == change["before"] and change["after"] == change["before"].replace("Mihwa","Sakura")
            row[name] = change["after"]


start = parent.verification.index('    assert rendered["FE_panels"]')
end = parent.verification.index('    assert playback["initialized_excerpts"]')
special = parent.verification[parent.verification.index("    carried ="):
                                parent.verification.index('    draft["historical_source_credit"]')]
verification = checked_text(parent.verification, {
    parent.verification[start:end]: '''    assert rendered["FE_panels"] == 17 and len(rendered["style_objects"]) == 26
    assert sum(len(obj["slot_owner_sets"]) for obj in rendered["style_objects"]) == 175
    assert [(m["block"], m["count"]) for m in rendered["menus"]] == list(live.MENUS)
    rows = {r["id"]:r for r in draft["records"]}
    reconcile_speaker_notes(rows)
    changes = {r["id"] for r in draft["records"] if r["decision"] == "revision"}
    actual_plans = {ident:plan for group in stored["groups"] for ident, plan in group["plans"].items() if ident in changes}
    assert len(actual_plans) == len(changes) == 115
    assert rendered["revised_speech_pages"] == sum(p["expected_native_pages"] for p in actual_plans.values())
    assert draft["contextual_records_revisited"] == 383 and draft["contextual_decisions_reused"] == 56
    assert [(m["block"], m["highlight"]) for m in playback["menus"]] == [
        (block, index) for block, count in live.MENUS for index in range(count)]
    assert len(playback["observed_style_owners"]) == len(live.STYLE_OBJECTS)
    assert set(playback["page_transitions"]) == {live.PAGE_TURN[0], live.SERA_NAME[0]}
    earlier_wraps = {row["id"] for row in base.load(writer.FOLLOWUP)["records"]}
    assert earlier_wraps | {"DK4_MES_B309_R0174","DK4_MES_B305_R0031","DK4_MES_B300_R0174"} <= set(playback["observed_ids"])
    assert all(actual_plans[ident]["expected_native_pages"] == 1 for ident in earlier_wraps)
''',
    'len(name_check["records"]) == 25': 'len(name_check["records"]) == 15',
    'len(group["commands"]) for group in groups.values()) == 745': 'len(group["commands"]) for group in groups.values()) == 983',
    '== len(draft["records"]) == 371': '== len(draft["records"]) == 439',
    '{"wording": 142, "wrap-only": 3, "retention": 226}': '{"wording": 115, "retention": 324}',
    special: '''    carried = [r for r in draft["records"] if r.get("decision_carried")]
    assert len(carried) == 56 and {r["block"] for r in carried} == set(writer.EARLIER_BLOCKS)
    assert all(r["previous_registered_reference"]["exact_stored_hex"] == r["registered_reference"]["exact_stored_hex"]
               for r in carried)
    assert all(r["registered_reference"]["candidate_sha256"] == candidate for r in draft["records"])
    assert set(draft["planned_FE"]) == writer.FE_REVISIONS
    assert {rows[f"DK4_MES_B{block}_R{index:04d}"]["english"] for block,index in ((302,203),(304,155))} == {"One day passed."}
    assert {rows[f"DK4_MES_B{block}_R{index:04d}"]["english"] for block,index in ((297,232),(298,147),(299,247))} == {"We still need more."}
    draft["observed_menu_source_offsets"] = list(live.MENU_OFFSETS)
    draft["earlier_wrap_followup_sha256"] = base.digest(writer.FOLLOWUP)
    draft["speaker_context_reconciliation_sha256"] = base.digest(SPEAKERS)
''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1034 and len(checks) == 369': 'len(batches) == 1035 and len(checks) == 370',
    'previously_localized_records=371': 'previously_localized_records=439',
    'contextual_records_revisited=337, contextual_decisions_reused=34':
        'contextual_records_revisited=383, contextual_decisions_reused=56',
    'prior_records_reviewed=337, contextual_decisions_reused=34':
        'prior_records_reviewed=383, contextual_decisions_reused=56',
    'contextual_nameplate_retentions=25': 'contextual_nameplate_retentions=15',
    'actual_menu_samples=9': 'actual_menu_samples=13',
    'display.PROOF, names.PROOF, args.visual_review': 'display.PROOF, names.PROOF, SPEAKERS, args.visual_review',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's ruins and expedition routes

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed dialogue and accepted cumulative layers. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B261_B291","hodram_B292_B310").replace("initialized_Hodram_B261_B291","initialized_Hodram_B292_B310").replace(
    "verified_hodram_B241_B260_predecessor","verified_hodram_B261_B291_predecessor").replace(
    "prose_revisions=142","prose_revisions=115").replace("wrap_only_revisions=3","wrap_only_revisions=0").replace(
    "justified_retentions=192","justified_retentions=268")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B261_B291_FOCUSED_ONLY.nds': 'Hodram_B292_B310_FOCUSED_ONLY.nds',
    'Preserve the Hodram assignments and expedition candidate': 'Preserve the Hodram ruins and expedition candidate',
    notes: '''    DOC.write_text(f"""# Hodram's ruins and expedition routes

Reviewed 380 records from clean Japanese, with 112 revisions and 268 justified retentions. The market quest now uses consistent responses at each threshold. The route instructions preserve how to find the clan guarding the map, and the desert and wolf scenes keep their distinct choices and outcomes. Three earlier opening wraps are fixed. Fifty-six other decisions carry forward with exact references. [Exact source and current records](../{REVIEW.as_posix()})

Native checks cover 983 commands, 17 speakerless panels, 175 crew alternatives in 26 objects, 13 menu captions, 15 nameplates and {native_count()} changed pages. Initialized emulator excerpts cover {observed_count()} dialogue pages and all 13 menu highlights. Original relative branches, additional name lengths and unselected crew alternatives were checked offline. Optional natural triggers and hardware remain unvisited. [Native and emulator evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves 114 accepted layers and the ASCII right-bound correction. Startup and 17 regression tests passed. The clean-input patch reconstructed the candidate byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B261_B291","hodram_B292_B310").replace("B261_B291_staged","B292_B310_staged")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-ruins-and-expeditions", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
