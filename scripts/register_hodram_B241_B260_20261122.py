"""Register the Hodram ruins, survey, and guild checkpoint."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_hodram_B221_B240_20261122 as parent
from scripts import replay_hodram_B241_B260_20261122 as live
from scripts import verify_hodram_B241_B260_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B241-B260-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B241_B260_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B241_B260_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B241_B260_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B241_B260_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec, startup_reference = parent.guard_spec, parent.startup_reference
CHECKPOINT = ("Reviewed 224 Hodram records in the ruins, survey and guild scenes. The batch revises 82 turns, "
              "fixes one wrap and justifies 141 wording retentions. The ice-puzzle directions have a row each, "
              "and Charles's convoy paragraph now fits on one page. Fifteen other decisions from his letter carry forward.")
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | {"display": display})
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | {"live": live})
pages_saved = FunctionType(parent.pages_saved.__code__, parent.pages_saved.__globals__ | {"display": display})


def historical_credit(draft):
    historical = (Path("translations/hodram_B231_B250_integrated_final_review_v1.json"),
                  Path("translations/hodram_B251_B280_integrated_final_review_v1.json"))
    reviewed = {r["id"]: r for r in draft["records"] if r["kind"] == "typed-choice-label"}
    assert len(reviewed) == 9
    for path in historical:
        for prior in base.load(path)["records"]:
            if prior.get("id") not in reviewed:
                continue
            row = reviewed.pop(prior["id"])
            ref = prior["source_reference"]
            assert all(prior["review"].values()) and prior["source_hex"] == row["source_hex"]
            assert row["native_slots"] == [ref["source_index"]]
            assert all(ref[k] == row["source_reference"][k] for k in ("command_offset", "offset"))
            assert row["decision"] == "retention" and row["english"] == row["previous_English"] == prior["english"]
    assert not reviewed
    return dict(by_census_id={}, direct_keys=len(draft["records"]),
                earlier_menu_decisions={str(path): base.digest(path) for path in historical})


start = parent.verification.index('    assert rendered["FE_panels"]')
end = parent.verification.index('    assert playback["initialized_excerpts"]')
special = parent.verification[parent.verification.index("    carried ="):
                                parent.verification.index('    draft["historical_source_credit"]')]
verification = checked_text(parent.verification, {
    parent.verification[start:end]: '''    assert rendered["FE_panels"] == 20 and len(rendered["style_objects"]) == 3
    assert [(m["block"], m["count"]) for m in rendered["menus"]] == list(live.MENUS)
    rows = {r["id"]: r for r in draft["records"]}
    reflow = rows["DK4_MES_B259_R0086"]
    assert reflow["english"] == reflow["previous_English"]
    reflow.update(change_class="wrap-only",
        localization_note="Retain the map explanation and hearsay. Let the native formatter join phrases that were separated by early breaks and padding.")
    draft["findings"] = {"wording": 83, "wrap-only": 1, "retention": 156}
    changes = {r["id"] for r in draft["records"] if r["decision"] == "revision"}
    actual_plans = {ident: plan for group in stored["groups"] for ident, plan in group["plans"].items() if ident in changes}
    assert len(actual_plans) == len(changes) == 84
    assert rendered["revised_speech_pages"] == sum(p["expected_native_pages"] for p in actual_plans.values())
    assert rendered["alternate_name_width_pages"] == 3
    assert draft["contextual_records_revisited"] == 225 and draft["contextual_decisions_reused"] == 15
    assert [(m["block"], m["highlight"]) for m in playback["menus"]] == [
        (block, index) for block, count in live.MENUS for index in range(count)]
    assert len(playback["observed_style_owners"]) == 2
    assert set(playback["page_transitions"]) == {writer.CONVOY_ID, live.SERA_NAME[0]}
    assert {writer.CONVOY_ID, "DK4_MES_B252_R0009", "DK4_MES_B252_R0012", "DK4_MES_B243_R0163"} <= set(playback["observed_ids"])
    assert actual_plans[writer.CONVOY_ID]["expected_native_pages"] == 1
''',
    'len(name_check["records"]) == 20': 'len(name_check["records"]) == 19',
    'len(group["commands"]) for group in groups.values()) == 349': 'len(group["commands"]) for group in groups.values()) == 478',
    '== len(draft["records"]) == 291': '== len(draft["records"]) == 240',
    '{"wording": 120, "wrap-only": 2, "glyph": 3, "retention": 166}': '{"wording": 83, "wrap-only": 1, "retention": 156}',
    special: '''    carried = [r for r in draft["records"] if r.get("decision_carried")]
    assert len(carried) == 15 and all(r["block"] == 238 for r in carried)
    assert all(r["previous_registered_reference"]["exact_stored_hex"] == r["registered_reference"]["exact_stored_hex"]
               for r in carried)
    assert all(r["registered_reference"]["candidate_sha256"] == candidate for r in draft["records"])
    assert len(draft["planned_FE"]) == 2
    for ident, phrases in writer.ICE_ROWS.items():
        assert [row[2] for row in draft["planned_FE"][ident]["rows"]] == list(phrases)
    assert [rows[f"SC1_B252_CHOICE_270_{i}"]["english"] for i in range(3)] == ["Front stone", "Left stone", "Right stone"]
    for left, right in ((264, 266), (176, 176)):
        assert rows[f"SC1_B252_STYLE_340_{left}"]["english"] == rows[f"SC1_B252_STYLE_822_{right}"]["english"]
    draft["observed_menu_source_offsets"] = list(live.MENU_OFFSETS)
    draft["convoy_followup_sha256"] = base.digest(writer.CONVOY)
''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1032 and len(checks) == 367': 'len(batches) == 1033 and len(checks) == 368',
    'previously_localized_records=291': 'previously_localized_records=240',
    'contextual_records_revisited=275, contextual_decisions_reused=16':
        'contextual_records_revisited=225, contextual_decisions_reused=15',
    'prior_records_reviewed=275, contextual_decisions_reused=16':
        'prior_records_reviewed=225, contextual_decisions_reused=15',
    'contextual_nameplate_retentions=20': 'contextual_nameplate_retentions=19',
    'actual_menu_samples=2, actual_style_objects=3': 'actual_menu_samples=9, actual_style_objects=2',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's ruins and guild assignments

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed dialogue and the accepted cumulative layers. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B221_B240", "hodram_B241_B260").replace("initialized_Hodram_B221_B240", "initialized_Hodram_B241_B260").replace(
    "verified_hodram_B201_B220_predecessor", "verified_hodram_B221_B240_predecessor").replace(
    "prose_revisions=120", "prose_revisions=83").replace("wrap_only_revisions=2", "wrap_only_revisions=1").replace(
    "justified_retentions=150", "justified_retentions=141").replace("punctuation_glyph_corrections=3", "punctuation_glyph_corrections=0").replace(
    "text_display_revisions=3", "text_display_revisions=0")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B221_B240_FOCUSED_ONLY.nds': 'Hodram_B241_B260_FOCUSED_ONLY.nds',
    'Preserve the Hodram treasure and letter candidate': 'Preserve the Hodram ruins and guild candidate',
    notes: '''    DOC.write_text(f"""# Hodram's ruins and guild assignments

Reviewed 224 records from clean Japanese, with 82 wording revisions, one wrap-only change and 141 justified retentions. The ice inscription keeps its floating-ice condition and gives each stone its own instruction row. Charles's convoy letter now uses one page for the same sequence of events, and fifteen other records from his letter keep exact references. [Exact source and current records](../{REVIEW.as_posix()})

Native checks cover 478 commands, 20 speakerless panels, three personality objects, nine menu captions, 19 nameplates and {native_count()} changed pages. Initialized emulator excerpts cover {observed_count()} dialogue pages and nine choice highlights. The original relative branch destinations, long substituted names and additional personality alternatives were checked offline. Natural triggers and hardware are unvisited for this batch. [Offline and emulator evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves 114 accepted layers and the ASCII right-bound correction. Startup and 17 regression tests passed. The clean-input patch reconstructed the ROM byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B221_B240", "hodram_B241_B260").replace("B221_B240_staged", "B241_B260_staged")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-ruins-and-guild", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
