"""Register the reviewed Hodram town, forecast, and bargaining scenes."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_hodram_B171_B180_20261122 as parent
from scripts import replay_hodram_B181_B200_20261122 as live
from scripts import verify_hodram_B181_B200_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B181-B200-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B181_B200_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B181_B200_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B181_B200_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B181_B200_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec, startup_reference = parent.guard_spec, parent.startup_reference
CHECKPOINT = ("Reviewed 284 Hodram town and bargaining records from clean Japanese. The pass revises 68 records, "
              "improves four additional wraps and justifies retaining 212 records. Six forecasts now fit one line, "
              "and Carlo's private bargaining advice fits one page.")
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | {"display": display})
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | {"live": live})
pages_saved = FunctionType(parent.pages_saved.__code__, parent.pages_saved.__globals__ | {"display": display})


def historical_credit(draft):
    historic = Path("translations/hodram_B191_B210_contextual_final_review_v1.json")
    choices = {row["id"]: row for row in base.load(historic)["records"]
               if row["kind"] == "typed-choice-label" and row["block"] == 200}
    reviewed = [row for row in draft["records"] if row["kind"] == "typed-choice-label"]
    assert len(reviewed) == 12 and set(choices) == {row["id"] for row in reviewed}
    for row in reviewed:
        prior = choices[row["id"]]
        ref = prior["source_reference"]
        assert all(prior["review"].values()) and prior["source_hex"] == row["source_hex"]
        assert row["native_slots"] == [ref["source_index"]]
        assert all(ref[key] == row["source_reference"][key] for key in ("command_offset", "offset"))
        assert row["decision"] == "retention" and row["english"] == row["previous_English"] == prior["english"]
    return dict(by_census_id={}, direct_keys=len(draft["records"]), prior_choices=str(historic),
                prior_choices_sha256=base.digest(historic))


start = parent.verification.index('    assert rendered["FE_panels"]')
end = parent.verification.index('    assert playback["initialized_excerpts"]')
special = parent.verification[parent.verification.index("    carried ="):
                                parent.verification.index('    draft["historical_source_credit"]')]
verification = checked_text(parent.verification, {
    parent.verification[start:end]: '''    assert rendered["FE_panels"] == 21 and not rendered["style_objects"]
    assert [(m["block"], m["count"]) for m in rendered["menus"]] == [(200, 2)] * 6
    assert rendered["revised_speech_pages"] == 72 and rendered["alternate_name_width_pages"] == 3
    assert draft["contextual_records_revisited"] == 284 and draft["contextual_decisions_reused"] == 0
    assert len(playback["holds"]) == sum(isinstance(index, int) for _, index in live.SELECTED)
    assert [(m["block"], m["highlight"]) for m in playback["menus"]] == [(200, 0), (200, 1)] * 2
    assert not playback["observed_style_owners"]
    assert set(playback["page_transitions"]) == {live.PAGE_TURN[0], live.CHARM_TURN[0]}
    assert {writer.CHARM_PANEL, "DK4_MES_B188_R0022"} <= set(playback["observed_ids"])
''',
    'len(name_check["records"]) == 22': 'len(name_check["records"]) == 37',
    'len(group["commands"]) for group in groups.values()) == 450': 'len(group["commands"]) for group in groups.values()) == 498',
    '== len(draft["records"]) == 315': '== len(draft["records"]) == 284',
    '{"wording": 119, "retention": 196}': '{"wording": 68, "wrap-only": 4, "retention": 212}',
    special: '''    assert not any(r.get("decision_carried") for r in draft["records"])
    assert len(draft["planned_FE"]) == 6 and all(len(p["rows"]) == 1 for p in draft["planned_FE"].values())
    draft["observed_bargaining_menu_source_offsets"] = [218, 1588]
''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1029 and len(checks) == 364': 'len(batches) == 1030 and len(checks) == 365',
    'previously_localized_records=315': 'previously_localized_records=284',
    'contextual_records_revisited=288, contextual_decisions_reused=27':
        'contextual_records_revisited=284, contextual_decisions_reused=0',
    'prior_records_reviewed=288, contextual_decisions_reused=27':
        'prior_records_reviewed=284, contextual_decisions_reused=0',
    'contextual_nameplate_retentions=22': 'contextual_nameplate_retentions=37',
    'actual_menu_samples=2': 'actual_menu_samples=4',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's town conversations and bargaining

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed dialogue and the accepted cumulative layers. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B171_B180", "hodram_B181_B200").replace("initialized_Hodram_B171_B180", "initialized_Hodram_B181_B200").replace(
    "verified_hodram_B161_B170_predecessor", "verified_hodram_B171_B180_predecessor").replace(
    "prose_revisions=119", "prose_revisions=68").replace("wrap_only_revisions=0", "wrap_only_revisions=4").replace(
    "justified_retentions=169", "justified_retentions=212")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B171_B180_FOCUSED_ONLY.nds': 'Hodram_B181_B200_FOCUSED_ONLY.nds',
    'Preserve the Hodram Proofs and harbor candidate': 'Preserve the Hodram town and bargaining candidate',
    notes: '''    DOC.write_text(f"""# Hodram's town conversations and bargaining

Reviewed 284 records from clean Japanese, with 68 wording revisions, four other wrap fixes and 212 justified retentions. The bread discussion now asks whether baking it yourself makes it taste better. The established Woman and Man captions fit the tea exchange. Six market forecasts follow the same wording and fit one line. The private bargaining advice takes one page. All six prices and choice pairs keep their original terms. [Exact source and current records](../{REVIEW.as_posix()})

Native checks cover 498 commands, 21 speakerless panels, 12 choice captions, 37 nameplates, {native_count()} changed pages and three additional name widths. The Charm notice fits a 16-cell name in the native renderer. Focused emulator playback verifies {observed_count()} dialogue holds, including the default name on the Charm notice, and both highlights in the first and last offer menus. The emulator excerpts use initialized town scenes. Natural event triggering, original purchase outcomes and hardware remain unvisited. [Offline and emulator evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves 114 accepted layers and the ASCII right-bound correction. Startup and 17 regression tests passed. The clean-input patch reconstructed the ROM byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B171_B180", "hodram_B181_B200").replace("B171_B180_staged", "B181_B200_staged")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-town-and-bargaining", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
