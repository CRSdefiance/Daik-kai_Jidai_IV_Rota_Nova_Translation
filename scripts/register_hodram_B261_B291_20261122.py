"""Register the Hodram guild assignments, royal audience, and expedition checkpoint."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_hodram_B241_B260_20261122 as parent
from scripts import replay_hodram_B261_B291_20261122 as live
from scripts import verify_hodram_B261_B291_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B261-B291-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B261_B291_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B261_B291_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B261_B291_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B261_B291_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec, startup_reference = parent.guard_spec, parent.startup_reference
CHECKPOINT = ("Reviewed 335 Hodram records in the guild assignments, the king's audience, and the forest and cave encounters. "
              "The batch revises the wording of 140 records, fixes three additional wraps and justifies 192 retentions. "
              "Two earlier figurehead lines now use fuller opening rows, and 34 other decisions carry forward.")
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | {"display": display})
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | {"live": live})
pages_saved = FunctionType(parent.pages_saved.__code__, parent.pages_saved.__globals__ | {"display": display})


def historical_credit(draft):
    earlier = Path("translations/hodram_B281_B300_integrated_final_review_v1.json")
    menus = {row["id"]:row for row in base.load(earlier)["records"] if "CHOICE" in row["id"]}
    carried = {row["id"]:row for row in base.load(parent.REVIEW)["records"] if row["block"] == 243
               and row["kind"] == "typed-choice-label"}
    captions = [row for row in draft["records"] if row["kind"] == "typed-choice-label"]
    assert len(captions) == 9
    updated_captions = {
        "SC1_B290_CHOICE_876_0": ("Fight bravely", "Stand and fight"),
        "SC1_B290_CHOICE_876_2": ("Other", "Try something else"),
        "SC1_B290_CHOICE_1876_1": ("Run away", "Run for it"),
    }
    for row in captions:
        ident = row["id"]
        old = carried.pop(ident) if row["block"] == 243 else menus[ident]
        assert all(old["review"].values()) and old["source_hex"] == row["source_hex"]
        ref = old["source_reference"]
        slots = old["native_slots"] if row["block"] == 243 else [ref["source_index"]]
        assert slots == row["native_slots"]
        assert all(ref[key] == row["source_reference"][key] for key in ("command_offset", "offset"))
        assert row["decision"] == "retention" and row["english"] == row["previous_English"]
        assert (old["english"], row["english"]) == updated_captions.get(ident,(row["english"], row["english"]))
    assert not carried
    return dict(by_census_id={}, direct_keys=len(draft["records"]),
                earlier_menu_decisions={str(path):base.digest(path) for path in (earlier,parent.REVIEW)})


start = parent.verification.index('    assert rendered["FE_panels"]')
end = parent.verification.index('    assert playback["initialized_excerpts"]')
special = parent.verification[parent.verification.index("    carried ="):
                                parent.verification.index('    draft["historical_source_credit"]')]
verification = checked_text(parent.verification, {
    parent.verification[start:end]: '''    assert rendered["FE_panels"] == 27 and len(rendered["style_objects"]) == 15
    assert sum(len(obj["slot_owner_sets"]) for obj in rendered["style_objects"]) == 108
    assert [(m["block"], m["count"]) for m in rendered["menus"]] == list(live.MENUS)
    rows = {r["id"]:r for r in draft["records"]}
    changes = {r["id"] for r in draft["records"] if r["decision"] == "revision"}
    wraps = {ident for ident in changes if rows[ident]["english"] == rows[ident]["previous_English"]}
    wrap_notes = {
        "DK4_MES_B276_R0005": "Keep the guildmaster's greeting and trust. Give the surname token and the favor clear rows.",
        "DK4_MES_B279_R0015": "Keep the Mediterranean lead and offer of an advance. Let the formatter remove the old sentence padding.",
        "SC1_B291_STYLE_824_92": "Keep the alarm and the short question tag with the crew member's reply.",
    }
    assert wraps == wrap_notes.keys()
    for ident, note in wrap_notes.items():
        rows[ident].update(change_class="wrap-only", layout_refinement=note)
    draft["findings"] = {"wording": 142, "wrap-only": 3, "retention": 226}
    actual_plans = {ident:plan for group in stored["groups"] for ident, plan in group["plans"].items() if ident in changes}
    assert len(actual_plans) == len(changes) == 145
    assert rendered["revised_speech_pages"] == sum(p["expected_native_pages"] for p in actual_plans.values())
    assert draft["contextual_records_revisited"] == 337 and draft["contextual_decisions_reused"] == 34
    assert [(m["block"], m["highlight"]) for m in playback["menus"]] == [
        (block, index) for block, count in live.MENUS for index in range(count)]
    assert len(playback["observed_style_owners"]) == len(live.STYLE_OBJECTS)
    assert set(playback["page_transitions"]) == {live.PAGE_TURN[0], live.SERA_NAME[0]}
    assert {"DK4_MES_B243_R0029", "DK4_MES_B243_R0044", "DK4_MES_B291_R0119", "DK4_MES_B290_R0305"} <= set(playback["observed_ids"])
    assert all(actual_plans[ident]["expected_native_pages"] == 1
               for ident in ("DK4_MES_B243_R0029","DK4_MES_B243_R0044","DK4_MES_B266_R0009"))
''',
    'len(name_check["records"]) == 19': 'len(name_check["records"]) == 25',
    'len(group["commands"]) for group in groups.values()) == 478': 'len(group["commands"]) for group in groups.values()) == 745',
    '== len(draft["records"]) == 240': '== len(draft["records"]) == 371',
    '{"wording": 83, "wrap-only": 1, "retention": 156}': '{"wording": 142, "wrap-only": 3, "retention": 226}',
    special: '''    carried = [r for r in draft["records"] if r.get("decision_carried")]
    assert len(carried) == 34 and all(r["block"] == 243 for r in carried)
    assert all(r["previous_registered_reference"]["exact_stored_hex"] == r["registered_reference"]["exact_stored_hex"]
               for r in carried)
    assert all(r["registered_reference"]["candidate_sha256"] == candidate for r in draft["records"])
    assert set(draft["planned_FE"]) == {"DK4_MES_B291_R0119"}
    assert [rows[f"SC1_B290_CHOICE_876_{i}"]["english"] for i in range(3)] == ["Stand and fight", "Play dead", "Try something else"]
    assert rows["SC1_B291_STYLE_2194_44"]["english"] == rows["SC1_B291_STYLE_2194_418"]["english"]
    draft["observed_menu_source_offsets"] = list(live.MENU_OFFSETS)
    draft["figurehead_followup_sha256"] = base.digest(writer.FIGURE)
''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1033 and len(checks) == 368': 'len(batches) == 1034 and len(checks) == 369',
    'previously_localized_records=240': 'previously_localized_records=371',
    'contextual_records_revisited=225, contextual_decisions_reused=15':
        'contextual_records_revisited=337, contextual_decisions_reused=34',
    'prior_records_reviewed=225, contextual_decisions_reused=15':
        'prior_records_reviewed=337, contextual_decisions_reused=34',
    'contextual_nameplate_retentions=19': 'contextual_nameplate_retentions=25',
    'actual_menu_samples=9, actual_style_objects=2': 'actual_menu_samples=9, actual_style_objects=len(live.STYLE_OBJECTS)',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's guild assignments and expedition encounters

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed dialogue and the accepted cumulative layers. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B241_B260", "hodram_B261_B291").replace("initialized_Hodram_B241_B260", "initialized_Hodram_B261_B291").replace(
    "verified_hodram_B221_B240_predecessor", "verified_hodram_B241_B260_predecessor").replace(
    "prose_revisions=83","prose_revisions=142").replace("wrap_only_revisions=1","wrap_only_revisions=3").replace(
    "justified_retentions=141","justified_retentions=192")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B241_B260_FOCUSED_ONLY.nds': 'Hodram_B261_B291_FOCUSED_ONLY.nds',
    'Preserve the Hodram ruins and guild candidate': 'Preserve the Hodram assignments and expedition candidate',
    notes: '''    DOC.write_text(f"""# Hodram's guild assignments and expedition encounters

Reviewed 335 records from clean Japanese, with 140 wording revisions, three wrap-only fixes and 192 justified retentions. The audience with the king keeps the seven Proofs of Conquest and their role in establishing the strongest fleet. The guild reminders distinguish finding a pirate from capturing him, and the expedition scenes retain the differences between crew voices and outcomes. Two earlier figurehead lines now use fuller opening rows. Thirty-four other decisions from that scene carry forward with exact references. [Exact source and current records](../{REVIEW.as_posix()})

Native checks cover 745 commands, 27 speakerless panels, 108 crew alternatives across 15 style objects, nine menu captions, 25 nameplates and {native_count()} changed pages. Initialized emulator excerpts cover {observed_count()} dialogue pages and nine choice highlights. The original relative branch destinations and additional name lengths and crew alternatives were checked offline. Optional natural triggers and hardware remain unvisited for this batch. [Offline and emulator evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves 114 accepted layers and the ASCII right-bound correction. Startup and 17 regression tests passed. The clean-input patch reconstructed the ROM byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B241_B260", "hodram_B261_B291").replace("B241_B260_staged", "B261_B291_staged")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-guild-and-expeditions", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
