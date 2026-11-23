"""Register the Hodram treasure and letter checkpoint."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_hodram_B201_B220_20261122 as parent
from scripts import replay_hodram_B221_B240_20261122 as live
from scripts import verify_hodram_B221_B240_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B221-B240-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B221_B240_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B221_B240_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B221_B240_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B221_B240_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec, startup_reference = parent.guard_spec, parent.startup_reference
CHECKPOINT = ("Reviewed 274 Hodram records in the treasure rumors, town scenes and letters. The batch revises 120 turns, "
              "corrects three pause glyphs, fixes an additional wrap and justifies 150 wording retentions. Janus's signature has its own row, "
              "and the other 16 B218 decisions carry forward with exact references.")
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | {"display": display})
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | {"live": live})
pages_saved = FunctionType(parent.pages_saved.__code__, parent.pages_saved.__globals__ | {"display": display})


def historical_credit(draft):
    historic = Path("translations/hodram_B211_B230_integrated_final_review_v1.json")
    choices = {row["id"]: row for row in base.load(historic)["records"]
               if row.get("kind") == "typed-choice-label" and row["block"] == 224}
    reviewed = [r for r in draft["records"] if r["kind"] == "typed-choice-label"]
    assert len(reviewed) == 2 and set(choices) == {r["id"] for r in reviewed}
    for row in reviewed:
        prior = choices[row["id"]]
        ref = prior["source_reference"]
        assert all(prior["review"].values()) and prior["source_hex"] == row["source_hex"]
        assert row["native_slots"] == [ref["source_index"]]
        assert all(ref[k] == row["source_reference"][k] for k in ("command_offset", "offset"))
        assert row["decision"] == "retention" and row["english"] == row["previous_English"] == prior["english"]
    return dict(by_census_id={}, direct_keys=len(draft["records"]), prior_choices=str(historic),
                prior_choices_sha256=base.digest(historic))


start = parent.verification.index('    assert rendered["FE_panels"]')
end = parent.verification.index('    assert playback["initialized_excerpts"]')
special = parent.verification[parent.verification.index("    assert not any(r.get"):
                                parent.verification.index('    draft["historical_source_credit"]')]
verification = checked_text(parent.verification, {
    parent.verification[start:end]: '''    assert rendered["FE_panels"] == 0 and len(rendered["style_objects"]) == 4
    assert [(m["block"], m["count"]) for m in rendered["menus"]] == [(224, 2)]
    rows = {r["id"]: r for r in draft["records"]}
    no_change, = [r for r in rendered["records"] if r.get("existing_wrap_already_exact")]
    assert no_change["id"] == "DK4_MES_B226_R0028"
    old = rows[no_change["id"]]
    old.update(decision="retention", change_class="retention",
        localization_note="Ian states when and where he found the book. The deployed English and native wrapping already match the review.")
    reflow = rows["DK4_MES_B232_R0013"]
    assert reflow["english"] == reflow["previous_English"]
    reflow.update(change_class="wrap-only",
        localization_note="Keep the approved rumor and question intact. Reflow the lines to avoid the sparse opening on the tortoise's name.")
    draft["findings"] = {"wording": 120, "wrap-only": 2, "glyph": 3, "retention": 166}
    changes = {r["id"] for r in draft["records"] if r["decision"] == "revision"}
    actual_plans = {ident: plan for group in stored["groups"] for ident, plan in group["plans"].items() if ident in changes}
    assert len(actual_plans) == len(changes) == 125
    assert rendered["revised_speech_pages"] == sum(p["expected_native_pages"] for p in actual_plans.values())
    assert rendered["alternate_name_width_pages"] == 0
    assert draft["contextual_records_revisited"] == 275 and draft["contextual_decisions_reused"] == 16
    assert [(m["block"], m["highlight"]) for m in playback["menus"]] == [(224, 0), (224, 1)]
    assert len(playback["observed_style_owners"]) == 3
    assert set(playback["page_transitions"]) == {live.PAGE_TURN[0], writer.SIGNATURE_ID}
    assert {writer.SIGNATURE_ID, "DK4_MES_B225_R0005", "DK4_MES_B227_R0011", "DK4_MES_B237_R0005"} <= set(playback["observed_ids"])
    assert actual_plans[writer.SIGNATURE_ID]["lines"] == ["I shall write again", "if I learn anything else.", "Janus Pasar"]
''',
    'len(name_check["records"]) == 28': 'len(name_check["records"]) == 20',
    'len(group["commands"]) for group in groups.values()) == 514': 'len(group["commands"]) for group in groups.values()) == 349',
    '== len(draft["records"]) == 350': '== len(draft["records"]) == 291',
    '{"wording": 155, "wrap-only": 3, "retention": 192}': '{"wording": 120, "wrap-only": 2, "glyph": 3, "retention": 166}',
    special: '''    carried = [r for r in draft["records"] if r.get("decision_carried")]
    assert len(carried) == 16 and all(r["block"] == 218 for r in carried)
    assert all(r["previous_registered_reference"]["exact_stored_hex"] == r["registered_reference"]["exact_stored_hex"]
               for r in carried)
    assert {r["english"] for r in draft["records"] if r["change_class"] == "glyph"} == {"...", "......", "........."}
    assert all(r["registered_reference"]["candidate_sha256"] == candidate for r in draft["records"])
    dialogue = {r["id"]: r["english"] for r in draft["records"]}
    assert {dialogue[f"DK4_MES_B{block}_R0005"] for block in (231, 232, 233)} == {"Got a minute, Admiral?"}
    assert dialogue["DK4_MES_B231_R0028"].endswith(dialogue["DK4_MES_B232_R0034"])
    assert dialogue["DK4_MES_B231_R0046"] == dialogue["DK4_MES_B232_R0059"]
    assert actual_plans["DK4_MES_B226_R0048"]["lines"][-1] == "Ian Dukov"
    draft["observed_menu_source_offsets"] = list(live.MENU_OFFSETS)
    draft["janus_wrap_followup_sha256"] = base.digest(writer.SIGNATURE)
''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1031 and len(checks) == 366': 'len(batches) == 1032 and len(checks) == 367',
    'previously_localized_records=350': 'previously_localized_records=291',
    'contextual_records_revisited=350, contextual_decisions_reused=0':
        'contextual_records_revisited=275, contextual_decisions_reused=16',
    'prior_records_reviewed=350, contextual_decisions_reused=0':
        'prior_records_reviewed=275, contextual_decisions_reused=16',
    'contextual_nameplate_retentions=28': 'contextual_nameplate_retentions=20',
    'actual_menu_samples=14': 'actual_menu_samples=2',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's treasure rumors and letters

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed dialogue and the accepted cumulative layers. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B201_B220", "hodram_B221_B240").replace("initialized_Hodram_B201_B220", "initialized_Hodram_B221_B240").replace(
    "verified_hodram_B181_B200_predecessor", "verified_hodram_B201_B220_predecessor").replace(
    "prose_revisions=155", "prose_revisions=120").replace("wrap_only_revisions=3", "wrap_only_revisions=2").replace(
    "justified_retentions=192", "justified_retentions=150").replace("punctuation_glyph_corrections=0", "punctuation_glyph_corrections=3").replace(
    "text_display_revisions=0", "text_display_revisions=3")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B201_B220_FOCUSED_ONLY.nds': 'Hodram_B221_B240_FOCUSED_ONLY.nds',
    'Preserve the Hodram encounter and letter candidate': 'Preserve the Hodram treasure and letter candidate',
    notes: '''    DOC.write_text(f"""# Hodram's treasure rumors and letters

Reviewed 274 records from clean Japanese, with 120 wording revisions, three pause glyph corrections, a wrap fix and 150 justified retentions. Samwell's repeated pitches preserve the joke across three scenes. Janus's signature now has a separate row, and 16 other records in his letter scene carry forward with exact references. [Exact source and current records](../{REVIEW.as_posix()})

Native checks cover 349 commands, four personality objects, two choice captions, 20 nameplates and {native_count()} changed pages. Initialized emulator excerpts verify {observed_count()} dialogue pages, both Crusades menu highlights, the three revised pauses, and the letter signoffs. Original branch destinations and personality alternatives were checked offline. Natural triggers and hardware are unvisited for this batch. [Offline and emulator evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves 114 accepted layers and the ASCII right-bound correction. Startup and 17 regression tests passed. The clean-input patch reconstructed the ROM byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B201_B220", "hodram_B221_B240").replace("B201_B220_staged", "B221_B240_staged")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-rumors-and-letters", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
