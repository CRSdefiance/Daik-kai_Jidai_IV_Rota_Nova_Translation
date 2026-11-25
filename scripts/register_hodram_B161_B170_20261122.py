"""Register the ship and tavern exchanges over the cumulative candidate."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_hodram_B151_B160_20261122 as parent
from scripts import replay_hodram_B161_B170_20261122 as live
from scripts import verify_hodram_B161_B170_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B161-B170-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B161_B170_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B161_B170_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B161_B170_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B161_B170_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec, startup_reference = parent.guard_spec, parent.startup_reference
CHECKPOINT = ("Reviewed 270 Hodram records and carried forward 41 exact decisions from Cesare's ship lesson. "
              "The pass revises 103 turns, improves one wrap without changing the words, and records "
              "166 fresh justified retentions across the ship and tavern encounters.")
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | {"display": display})
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | {"live": live})
pages_saved = FunctionType(parent.pages_saved.__code__, parent.pages_saved.__globals__ | {"display": display})


def historical_credit(draft):
    historic = Path("translations/hodram_B151_B170_contextual_final_review_v1.json")
    choices = {r["id"]:r for r in base.load(historic)["records"] if r["kind"] == "typed-choice-label"}
    reviewed = [r for r in draft["records"] if r["kind"] == "typed-choice-label"]
    assert len(reviewed) == 8 and set(choices) == {r["id"] for r in reviewed}
    intervening_caption_edits = {}
    for row in reviewed:
        prior = choices[row["id"]]
        reference = prior["source_reference"]
        assert all(prior["review"].values()) and prior["source_hex"] == row["source_hex"]
        assert row["native_slots"] == [reference["source_index"]]
        assert all(reference[k] == row["source_reference"][k] for k in ("command_offset","offset"))
        assert row["decision"] == "retention" and row["english"] == row["previous_English"]
        if row["english"] != prior["english"]:
            intervening_caption_edits[row["id"]] = [prior["english"], row["english"]]
    assert intervening_caption_edits == {"SC1_B167_CHOICE_1308_0": ["Listen.", "Listen"]}
    return dict(by_census_id={}, direct_keys=len(draft["records"]),
                prior_choices=str(historic), prior_choices_sha256=base.digest(historic),
                intervening_caption_edits=intervening_caption_edits)


start = parent.verification.index('    assert rendered["FE_panels"]')
end = parent.verification.index('    assert playback["initialized_excerpts"]')
farewell = parent.verification[parent.verification.index("    farewell ="):
                               parent.verification.index('    draft["historical_source_credit"]')]
verification = checked_text(parent.verification, {
    parent.verification[start:end]: '''    assert rendered["FE_panels"] == 7 and not rendered["style_objects"]
    assert [(m["block"],m["count"]) for m in rendered["menus"]] == [(b,2) for b in live.MENU_BLOCKS]
    assert rendered["revised_speech_pages"] == 104 and rendered["alternate_name_width_pages"] == 0
    assert draft["contextual_records_revisited"] == 270 and draft["contextual_decisions_reused"] == 41
    assert len(playback["holds"]) == 1 + sum(isinstance(index, int) for _,index in live.SELECTED)
    assert [(m["block"],m["highlight"]) for m in playback["menus"]] == [
        (b,slot) for b in live.MENU_BLOCKS for slot in range(2)]
    assert not playback["observed_style_owners"]
    assert set(playback["page_transitions"]) == {live.PAGE_TURN[0], live.JULIO_TURN[0]}
    assert writer.OPAQUE in playback["observed_ids"]
''',
    'len(name_check["records"]) == 27': 'len(name_check["records"]) == 16',
    'len(group["commands"]) for group in groups.values()) == 568': 'len(group["commands"]) for group in groups.values()) == 550',
    '== len(draft["records"]) == 331': '== len(draft["records"]) == 311',
    '{"wording": 112, "retention": 219}': '{"wording": 103, "wrap-only": 1, "retention": 207}',
    farewell: '''    carried = [r for r in draft["records"] if r.get("decision_carried")]
    assert len(carried) == 41 and all(r["block"] == 167 and r["decision"] == "retention" for r in carried)
    assert all(r["registered_reference"]["block_sha256"] == r["previous_registered_reference"]["block_sha256"]
               for r in carried)
    tutorial, = (row for row in carried if row["id"] == live.PAGE_TURN[0])
    tutorial["formatting_retention_reason"] = (
        "The focused replay confirmed the two-page layout. Page one completes the advice about expanding "
        "trade routes. Page two gives the complete one-percent purchase rule, including the one-to-five range."
    )
    draft["retained_comic_glyphs"] = [writer.OPAQUE]
''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1027 and len(checks) == 362': 'len(batches) == 1028 and len(checks) == 363',
    'previously_localized_records=331': 'previously_localized_records=311',
    'contextual_records_revisited=331, contextual_decisions_reused=0':
        'contextual_records_revisited=270, contextual_decisions_reused=41',
    'prior_records_reviewed=331, contextual_decisions_reused=0':
        'prior_records_reviewed=270, contextual_decisions_reused=41',
    'contextual_nameplate_retentions=27': 'contextual_nameplate_retentions=16',
    'actual_menu_samples=0': 'actual_menu_samples=8',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's ship and tavern encounters

The [testing ROM](../../{ROM.as_posix()}) includes the new Hodram dialogue and all accepted cumulative layers. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B151_B160", "hodram_B161_B170").replace("initialized_Hodram_B151_B160", "initialized_Hodram_B161_B170").replace(
    "verified_hodram_B131_B150_predecessor", "verified_hodram_B151_B160_predecessor").replace(
    "prose_revisions=112", "prose_revisions=103").replace("wrap_only_revisions=0", "wrap_only_revisions=1").replace(
    "justified_retentions=219", "justified_retentions=166")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B151_B160_FOCUSED_ONLY.nds': 'Hodram_B161_B170_FOCUSED_ONLY.nds',
    'Preserve the Hodram farewell and recruitment candidate': 'Preserve the Hodram ship and tavern candidate',
    notes: '''    DOC.write_text(f"""# Hodram's ship and tavern encounters

Reviewed 270 records from the clean Japanese and carried forward 41 exact decisions from Cesare's ship lesson. The new pass revises 103 turns, improves one wrap without changing the words, and records 166 individual retentions. The scenes include Cristina's dance, Samwell's pitch, Jam's return with the ship, the reunion with the Elysion, Fernando's wager, and both paths where Julio joins. The 16 reviewed nameplates keep their established forms, including the fixed Rafael selector and Fernando's normal-width F. [Exact sources and decisions](../{REVIEW.as_posix()})

Native checks cover 550 commands, seven speakerless panels, eight choice captions and {native_count()} revised pages. The focused emulator replay matches {observed_count()} speech pages and eight highlights across four menus. It also verifies the original mixed glyphs in Cesare's stunned reaction, the Rafael and Gerhard turns, two pages of Cesare's lesson, and the transition after Gerhard interrupts Julio. The original world triggers, ensuing branch behavior and hardware remain unvisited. [Offline and emulator evidence](../{VERIFY.as_posix()})

The registered build preserves 114 accepted layers and the ASCII right-bound correction. The clean-input patch rebuilt the candidate exactly. Its startup comparison and 17 regression tests passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B151_B160", "hodram_B161_B170").replace("B151_B160_staged", "B161_B170_staged")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-ship-and-tavern", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

