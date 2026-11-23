"""Register the final source-reviewed Hodram range and the native injury wrap fix."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_hodram_B292_B310_20261122 as parent
from scripts import replay_hodram_B311_B324_20261122 as live
from scripts import verify_hodram_B311_B324_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B311-B324-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B311_B324_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B311_B324_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B311_B324_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B311_B324_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec, startup_reference = parent.guard_spec, parent.startup_reference
CHECKPOINT = ("Reviewed 400 Hodram records through the final SC1 block. The batch revises 75 records and fixes the injury notice's "
              "long-name wrap while documenting 324 wording retentions. Four earlier opening wraps are repaired and 186 other decisions carry forward.")
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | {"display":display})
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | {"live":live})
pages_saved = FunctionType(parent.pages_saved.__code__, parent.pages_saved.__globals__ | {"display":display})


def historical_credit(draft):
    historic = Path("translations/hodram_B311_B324_integrated_final_review_v1.json")
    paths = (parent.REVIEW, historic)
    menus = {row["id"]:row for path in paths for row in base.load(path)["records"] if "CHOICE" in row["id"]}
    captions = [row for row in draft["records"] if row["kind"] == "typed-choice-label"]
    assert len(captions) == 22
    updated = {"SC1_B316_CHOICE_934_0": ("Keep going","Push on anyway")}
    for row in captions:
        ident = row["id"]
        old = menus[ident]
        assert all(old["review"].values()) and old["source_hex"] == row["source_hex"]
        ref = old["source_reference"]
        slots = old["native_slots"] if row["block"] in writer.EARLIER_BLOCKS else [ref["source_index"]]
        assert slots == row["native_slots"]
        assert all(ref[key] == row["source_reference"][key] for key in ("command_offset","offset"))
        assert row["decision"] == "retention" and row["english"] == row["previous_English"]
        assert (old["english"],row["english"]) == updated.get(ident,(row["english"],row["english"]))
    return dict(by_census_id={}, direct_keys=len(draft["records"]),
                earlier_menu_decisions={str(path):base.digest(path) for path in paths})


ALL_MENUS = ((294,2), (302,2), (302,2), (309,3), (311,2), (311,2), (313,3), (316,2), (316,2), (317,2))
start = parent.verification.index('    assert rendered["FE_panels"]')
end = parent.verification.index('    assert playback["initialized_excerpts"]')
special = parent.verification[parent.verification.index("    carried ="):
                                parent.verification.index('    draft["historical_source_credit"]')]
verification = checked_text(parent.verification, {
    parent.verification[start:end]: '''    assert rendered["FE_panels"] == 21 and len(rendered["style_objects"]) == 58
    assert sum(len(obj["slot_owner_sets"]) for obj in rendered["style_objects"]) == 366
    assert [(m["block"], m["count"]) for m in rendered["menus"]] == list(ALL_MENUS)
    rows = {r["id"]:r for r in draft["records"]}
    changes = {r["id"] for r in draft["records"] if r["decision"] == "revision"}
    actual_plans = {ident:plan for group in stored["groups"] for ident, plan in group["plans"].items() if ident in changes}
    assert len(actual_plans) == len(changes) == 80
    assert rendered["revised_speech_pages"] == sum(p["expected_native_pages"] for p in actual_plans.values())
    assert draft["contextual_records_revisited"] == 404 and draft["contextual_decisions_reused"] == 186
    assert [(m["block"], m["highlight"]) for m in playback["menus"]] == [
        (block, index) for block, count in live.MENUS for index in range(count)]
    assert len(playback["observed_style_owners"]) == len(live.STYLE_OBJECTS)
    assert set(playback["page_transitions"]) == {live.PAGE_TURN[0], live.SERA_NAME[0]}
    past = {r["id"] for r in base.load(writer.FOLLOWUP)["records"]}
    observed = set(playback["observed_ids"])
    assert (past - {"SC1_B309_STYLE_24_62"}) | {writer.INJURY,"DK4_MES_B318_R0109","DK4_MES_B324_R0058"} <= observed
    assert all(actual_plans[ident]["expected_native_pages"] == 1 for ident in past)
''',
    'len(name_check["records"]) == 15': 'len(name_check["records"]) == 13',
    'len(group["commands"]) for group in groups.values()) == 983': 'len(group["commands"]) for group in groups.values()) == 711',
    '== len(draft["records"]) == 439': '== len(draft["records"]) == 590',
    '{"wording": 115, "retention": 324}': '{"wording": 79, "wrap-only": 1, "retention": 510}',
    special: '''    carried = [r for r in draft["records"] if r.get("decision_carried")]
    assert len(carried) == 186 and {r["block"] for r in carried} == set(writer.EARLIER_BLOCKS)
    assert all(r["previous_registered_reference"]["exact_stored_hex"] == r["registered_reference"]["exact_stored_hex"]
               for r in carried)
    assert all(r["registered_reference"]["candidate_sha256"] == candidate for r in draft["records"])
    assert set(draft["planned_FE"]) == writer.FE_REVISIONS
    injury = rows[writer.INJURY]
    assert injury["english"] == injury["previous_English"] and injury["change_class"] == "wrap-only"
    layout = draft["planned_FE"][writer.INJURY]
    assert len(layout["name_width_rows"]) == 4
    for name,result in layout["name_width_rows"].items():
        assert [line[2] for line in result["rows"]] == [name + " was injured.",writer.INJURY_SENTENCE]
    assert {rows[f"DK4_MES_B{block}_R{index:04d}"]["english"] for block,index in ((316,254),(318,75))} == {"One day passed."}
    for offset in (0,56,88,136,182,234,278):
        assert rows[f"SC1_B313_STYLE_856_{offset}"]["english"] == rows[f"SC1_B313_STYLE_1252_{offset}"]["english"]
    draft["observed_menu_source_offsets"] = list(live.MENU_OFFSETS)
    draft["earlier_wrap_followup_sha256"] = base.digest(writer.FOLLOWUP)
''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1035 and len(checks) == 370': 'len(batches) == 1036 and len(checks) == 371',
    'previously_localized_records=439': 'previously_localized_records=590',
    'contextual_records_revisited=383, contextual_decisions_reused=56':
        'contextual_records_revisited=404, contextual_decisions_reused=186',
    'prior_records_reviewed=383, contextual_decisions_reused=56':
        'prior_records_reviewed=404, contextual_decisions_reused=186',
    'contextual_nameplate_retentions=15': 'contextual_nameplate_retentions=13',
    'actual_menu_samples=13': 'actual_menu_samples=15',
    'display.PROOF, names.PROOF, SPEAKERS, args.visual_review': 'display.PROOF, names.PROOF, args.visual_review',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's final SC1 exchanges

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed dialogue and accepted cumulative layers. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B292_B310","hodram_B311_B324").replace("initialized_Hodram_B292_B310","initialized_Hodram_B311_B324").replace(
    "verified_hodram_B261_B291_predecessor","verified_hodram_B292_B310_predecessor").replace(
    "prose_revisions=115","prose_revisions=79").replace("wrap_only_revisions=0","wrap_only_revisions=1").replace(
    "justified_retentions=268","justified_retentions=324")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B292_B310_FOCUSED_ONLY.nds': 'Hodram_B311_B324_FOCUSED_ONLY.nds',
    'Preserve the Hodram ruins and expedition candidate': 'Preserve the final Hodram range candidate',
    notes: '''    DOC.write_text(f"""# Hodram's final SC1 exchanges

Reviewed 400 records from clean Japanese. The batch revises 75, records 324 wordings that stay as written, and repairs the injury notice's long-name wrap. The old panel split "spend" at 15 and 16 name cells. Both sentences now keep complete words at all supported widths. Four earlier lines gain fuller opening rows. Another 186 decisions carry forward with exact references. [Exact source and current records](../{REVIEW.as_posix()})

Native checks cover 711 commands, 21 speakerless panels, 366 crew alternatives in 58 objects, 22 menu captions, 13 names and {native_count()} changed pages. Initialized emulator excerpts cover {observed_count()} dialogue pages and 15 menu highlights. They verify the Rafael and Lil nameplates, the injury notice at the default name width and three earlier wrap fixes. Long alternate names, other personality slots, and the earlier map-question wrap were checked offline. Optional natural triggers and hardware remain unvisited. [Native and emulator evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves 114 accepted layers and the ASCII right-bound correction. Startup and 17 regression tests passed. The clean-input patch reconstructed the candidate byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B292_B310","hodram_B311_B324").replace("B292_B310_staged","B311_B324_staged")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-final-hodram-range", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
