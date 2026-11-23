"""Register the Hodram encounters, letters, and treasure rumors."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_hodram_B181_B200_20261122 as parent
from scripts import replay_hodram_B201_B220_20261122 as live
from scripts import verify_hodram_B201_B220_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B201-B220-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B201_B220_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B201_B220_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B201_B220_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B201_B220_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec, startup_reference = parent.guard_spec, parent.startup_reference
CHECKPOINT = ("Reviewed 350 Hodram records across the book and treasure encounters, the parrot scene, and the letters. "
              "The pass revises 155 turns, fixes three additional wraps and justifies retaining 192 records. "
              "Jam's signature now has its own row, and the parrot repeats Angelo's phrasing.")
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | {"display": display})
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | {"live": live})
pages_saved = FunctionType(parent.pages_saved.__code__, parent.pages_saved.__globals__ | {"display": display})


def historical_credit(draft):
    historical = (Path("translations/hodram_B191_B210_contextual_final_review_v1.json"),
                  Path("translations/hodram_B211_B230_integrated_final_review_v1.json"))
    reviewed = {r["id"]: r for r in draft["records"] if r["kind"] == "typed-choice-label"}
    assert len(reviewed) == 14
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
special = parent.verification[parent.verification.index("    assert not any(r.get"):
                                parent.verification.index('    draft["historical_source_credit"]')]
verification = checked_text(parent.verification, {
    parent.verification[start:end]: '''    assert rendered["FE_panels"] == 30 and len(rendered["style_objects"]) == 3
    assert [(m["block"], m["count"]) for m in rendered["menus"]] == list(live.MENUS)
    assert rendered["revised_speech_pages"] == 162 and rendered["alternate_name_width_pages"] == 3
    assert draft["contextual_records_revisited"] == 350 and draft["contextual_decisions_reused"] == 0
    assert [(m["block"], m["highlight"]) for m in playback["menus"]] == [
        (block, index) for block, count in live.MENUS for index in range(count)]
    assert len(playback["observed_style_owners"]) == 3
    assert set(playback["page_transitions"]) == {live.PAGE_TURN[0], live.SERA_NAME[0]}
    assert {live.PAGE_TURN[0], "DK4_MES_B208_R0071", "DK4_MES_B209_R0020"} <= set(playback["observed_ids"])
''',
    'len(name_check["records"]) == 37': 'len(name_check["records"]) == 28',
    'len(group["commands"]) for group in groups.values()) == 498': 'len(group["commands"]) for group in groups.values()) == 514',
    '== len(draft["records"]) == 284': '== len(draft["records"]) == 350',
    '{"wording": 68, "wrap-only": 4, "retention": 212}': '{"wording": 155, "wrap-only": 3, "retention": 192}',
    special: '''    assert not any(r.get("decision_carried") for r in draft["records"])
    assert len(draft["planned_FE"]) == 10
    assert all(len(draft["planned_FE"][ident]["rows"]) == 2
               for ident in ("DK4_MES_B202_R0010", "DK4_MES_B202_R0014", "DK4_MES_B208_R0071"))
    spoken = {r["id"]: r["english"] for r in draft["records"] if r["block"] == 209}
    for call, echo, prefix, suffix in ((9,13,"Whoa! ",""), (17,20,"Mamma mia! ",""), (28,32,"",""),
            (36,40,"",""), (59,63,"Whew! "," Hahahaha!")):
        text = spoken[f"DK4_MES_B209_R{call:04d}"]
        assert text.startswith(prefix) and text.endswith(suffix)
        assert text.removeprefix(prefix).removesuffix(suffix).upper() == spoken[f"DK4_MES_B209_R{echo:04d}"]
    draft["observed_menu_source_offsets"] = list(live.MENU_OFFSETS)
''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1030 and len(checks) == 365': 'len(batches) == 1031 and len(checks) == 366',
    'previously_localized_records=284': 'previously_localized_records=350',
    'contextual_records_revisited=284, contextual_decisions_reused=0':
        'contextual_records_revisited=350, contextual_decisions_reused=0',
    'prior_records_reviewed=284, contextual_decisions_reused=0':
        'prior_records_reviewed=350, contextual_decisions_reused=0',
    'contextual_nameplate_retentions=37': 'contextual_nameplate_retentions=28',
    'actual_menu_samples=4, actual_style_objects=0': 'actual_menu_samples=14, actual_style_objects=3',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's encounters and letters

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed dialogue and the accepted cumulative layers. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B181_B200", "hodram_B201_B220").replace("initialized_Hodram_B181_B200", "initialized_Hodram_B201_B220").replace(
    "verified_hodram_B171_B180_predecessor", "verified_hodram_B181_B200_predecessor").replace(
    "prose_revisions=68", "prose_revisions=155").replace("wrap_only_revisions=4", "wrap_only_revisions=3").replace(
    "justified_retentions=212", "justified_retentions=192")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B181_B200_FOCUSED_ONLY.nds': 'Hodram_B201_B220_FOCUSED_ONLY.nds',
    'Preserve the Hodram town and bargaining candidate': 'Preserve the Hodram encounter and letter candidate',
    notes: '''    DOC.write_text(f"""# Hodram's encounters and letters

Reviewed 350 records from clean Japanese, with 155 wording revisions, three other wrap fixes and 192 justified retentions. The parrot echoes Angelo's phrases, the repeated namahage call has a row for each question, and Jam's signoff and signature occupy separate rows. Yukihisa's letter uses fuller rows while keeping its formal voice. [Exact source and current records](../{REVIEW.as_posix()})

Native checks cover 514 commands, 30 speakerless panels, 14 choice captions, 28 nameplates, 22 bodies across three personality objects and {native_count()} changed pages. Focused playback checks {observed_count()} dialogue pages, all 14 choice highlights, the parrot and signature panels, and the letter page transition. Original branch destinations and all personality alternatives were checked offline. Playback used initialized excerpts. Natural triggers and hardware are unvisited for this batch. [Offline and emulator evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves 114 accepted layers and the ASCII right-bound correction. Startup and 17 regression tests passed. The clean-input patch reconstructed the ROM byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B181_B200", "hodram_B201_B220").replace("B181_B200_staged", "B201_B220_staged")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-encounters-and-letters", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
