"""Register Rafael's reviewed East Asia and Mediterranean exchanges."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import check_rafael_east_asia_gameplay_20261121 as live
from scripts import register_rafael_tradehouse_festival_20261121 as parent
from scripts import review_rafael_east_asia_nameplates_20261121 as nameplates
from scripts import verify_rafael_east_asia_followup_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage = live.stage
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-rafael-east-asia-showdown-v1-20261121"
ROOT = Path("out/rafael_east_asia_showdown_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_East_Asia_Showdown_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_rafael_east_asia_showdown_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_east_asia_showdown_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
CHECKPOINT = ("Reviewed 142 Rafael records through the king's summons. The registered build has 82 wording revisions, "
              "nine wrap-only fixes, 51 justified retentions and one fewer page turn.")


startup_check = parent.startup_check
report_reader = parent.check_startup_report
startup_check = FunctionType(startup_check.__code__, startup_check.__globals__ |
    {"checked_report": FunctionType(report_reader.__code__, report_reader.__globals__ | {"STARTUP_CAPTURE": STARTUP_CAPTURE})})


verification = checked_text(getsource(parent.parent.verify), {
    '    assert rendered["revised_pages"] == 110':
        '''    assert rendered["revised_pages"] == 92 and rendered["name_stress_pages"] == 39
    assert rendered["verified_pagination_changes"] == [
        dict(id="DK4_MES_B78_R0005", previous_pages=2, registered_pages=1)]
    names = base.load(nameplates.PROOF)
    assert names["candidate_sha256"] == candidate and len(names["records"]) == 17
    assert all(row["decision"] == "retention" and row["localization_note"] and len(row["native_getters"]) == 2
               for row in names["records"])''',
    '''    assert len(playback["holds"]) == 23 and len(playback["offline_only"]) == 93
    reward, = [row for row in playback["holds"] if row["system_FE"]]
    assert reward["id"] == "DK4_MES_B61_R0113"''':
        '''    assert len(playback["holds"]) == 33 and playback["single_press_page_turn_reclaimed"]
    observed_revisions = {row["id"] for row in playback["holds"] if row["decision"] == "revision"}
    assert len(observed_revisions) + len(playback["offline_only"]) == 91
    assert not any(row["system_FE"] for row in playback["holds"])''',
    '    startup = parent.scope["startup_check"].startup_proof': '    startup = startup_check',
    'len(results) == 197 and len(observed) == 23': 'len(results) == 142 and len(observed) == 32',
    '{"revision": 110, "retention": 87}': '{"revision": 91, "retention": 51}',
    '{"prose and wrap": 96, "wrap": 14, "retention": 87}': '{"prose and wrap": 82, "wrap": 9, "retention": 51}',
    'new_contextual_credit=0, shared_payload_and_lookup_exact=True, native_preview_evidence=str(display.PROOF),':
        'new_contextual_credit=0, shared_payload_and_lookup_exact=True, native_preview_evidence=str(display.PROOF),\n'
        '        scoped_nameplate_review={"path": str(nameplates.PROOF), "sha256": base.digest(nameplates.PROOF)},',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_rafael_pereira_village_predecessor": "verified_rafael_tradehouse_festival_predecessor",
    "len(batches) == 999 and len(checks) == 334": "len(batches) == 1000 and len(checks) == 335",
    "for source in (stage.PROOF, STARTUP, QA, live.PROOF, display.PROOF, args.visual_review,":
        "for source in (stage.PROOF, STARTUP, QA, live.PROOF, display.PROOF, nameplates.PROOF, args.visual_review,",
    "five_original_command_maps_and_festival_FE_controls_preserved=True": "ten_original_command_maps_preserved=True",
    "previously_localized_records=200, new_contextual_records=0, prose_revisions=87":
        "previously_localized_records=142, new_contextual_records=0, prose_revisions=82",
    "wrap_only_revisions=7, justified_retentions=106": "wrap_only_revisions=9, justified_retentions=51",
    "pagination_fixes=0": "pagination_fixes=1",
    "initialized_Rafael_festival_and_dialogue_excerpt=True": "initialized_Rafael_dialogue_and_single_press_transition=True",
    "native_revised_pages=94, observed_holds=28, observed_festival_FE_panels=5":
        "native_revised_pages=92, observed_holds=33, contextual_nameplate_retentions=17, reclaimed_page_turns=1",
    "prior_records_reviewed=200, observed_Rafael_panels=28, native_pages=94":
        "prior_records_reviewed=142, observed_Rafael_panels=33, native_pages=92",
    "prose_revisions=87, justified_retentions=106, wrap_only_revisions=7":
        "prose_revisions=82, justified_retentions=51, wrap_only_revisions=9",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's East Asia and Mediterranean exchanges

The [testing ROM](../../{ROM.as_posix()}) includes the ten reviewed exchanges. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_tradehouse_festival", "rafael_east_asia_showdown").replace(
    "verified_rafael_east_asia_showdown_predecessor", "verified_rafael_tradehouse_festival_predecessor")
notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'for tag in ("staged_v1", "staged_v2")': 'for tag in ("staged_v1", "staged_v2", "staged_v3")',
    "Preserve the trade house and festival candidate, predecessor, staging ROMs and focused fixture":
        "Preserve the East Asia and Mediterranean candidate, predecessor, staged ROMs and focused fixtures",
    notes: '''    DOC.write_text(f"""# Rafael's East Asia and Mediterranean exchanges

The review covers 142 records. There are 82 wording revisions, nine wrap-only fixes and 51 justified retentions. Eirene's advice and the banter that follows retain their distinct tones. Simon's claims about Portugal and the Invincible Armada stay in his voice. Rafael names the Estado and explains the trading network. The two summons remain distinct. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Native and visual checks cover 92 pages across 91 revised speeches, plus 39 alternate name-width pages. Seventeen existing names and role labels were retained after comparison with the clean fields and 34 native getter outputs. The focused emulator excerpts verified 33 pages across 32 speeches. Both pages of Valdes's boast and the single-press transition from Claudio to Rafael match the final stored commands and renderer assets byte for byte. A fresh excerpt verified four final lines, including the revised company punctuation and port greeting. The natural story triggers and hardware remain untested. [Native, nameplate and emulator evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters, 17 focused tests and exact clean-input reconstruction passed. These 142 records already carried editorial credit. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_tradehouse_festival", "rafael_east_asia_showdown")
scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
