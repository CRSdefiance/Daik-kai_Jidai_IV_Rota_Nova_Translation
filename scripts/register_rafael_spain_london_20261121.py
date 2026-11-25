"""Register Rafael's contextual bullfight, recruitment and London rescue review."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import bind_rafael_B84_current_pages_20261121 as next_pages
from scripts import check_rafael_spain_london_gameplay_20261121 as live
from scripts import register_rafael_east_asia_followup_20261121 as parent
from scripts import register_rafael_pereira_village_20261121 as template
from scripts import review_rafael_spain_london_nameplates_20261121 as names
from scripts import verify_rafael_spain_london_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage = live.stage
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-rafael-spain-london-v1-20261121"
ROOT = Path("out/rafael_spain_london_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_Spain_London_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_rafael_spain_london_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_spain_london_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
PAGINATION = EVIDENCE / "pagination_comparison.json"
CHECKPOINT = ("Reviewed 199 Rafael records through the bullfight and London rescue. The registered build has 105 wording "
              "revisions, five wrap-only fixes, 89 justified retentions and two fewer page turns.")


report_reader = parent.report_reader
startup_check = FunctionType(parent.startup_check.__code__, parent.startup_check.__globals__ |
    {"checked_report": FunctionType(report_reader.__code__, report_reader.__globals__ | {"STARTUP_CAPTURE": STARTUP_CAPTURE})})


verification = checked_text(getsource(template.verify), {
    '    assert rendered["revised_pages"] == 110':
        '''    assert rendered["revised_pages"] == 110 and rendered["speakerless_panels"] == 4
    assert rendered["name_stress_pages"] == 16
    pagination = base.load(PAGINATION)
    assert pagination["candidate_sha256"] == candidate and len(pagination["records"]) == 2
    assert all((row["previous_pages"], row["current_pages"]) == (2, 1) for row in pagination["records"])
    names_receipt = base.load(names.PROOF)
    assert names_receipt["candidate_sha256"] == candidate and len(names_receipt["records"]) == 15
    assert all(row["decision"] == "retention" and row["localization_note"] and len(row["native_getters"]) == 2
               for row in names_receipt["records"])''',
    '''    assert len(playback["holds"]) == 23 and len(playback["offline_only"]) == 93
    reward, = [row for row in playback["holds"] if row["system_FE"]]
    assert reward["id"] == "DK4_MES_B61_R0113"''':
        '''    assert len(playback["holds"]) == 43 and playback["reclaimed_page_turns_observed"] == 2
    assert sum(row["system_FE"] for row in playback["holds"]) == 4
    assert playback["original_picture_switches_exercised"]
    observed_revisions = {row["id"] for row in playback["holds"] if row["decision"] == "revision"}
    assert len(observed_revisions) + len(playback["offline_only"]) == 110''',
    '    startup = parent.scope["startup_check"].startup_proof': '    startup = startup_check',
    'len(results) == 197 and len(observed) == 23': 'len(results) == 199 and len(observed) == 43',
    '{"revision": 110, "retention": 87}': '{"revision": 110, "retention": 89}',
    '{"prose and wrap": 96, "wrap": 14, "retention": 87}': '{"prose and wrap": 105, "wrap": 5, "retention": 89}',
    '    assert all(native.digest(old[n]) == groups[n]["before"] and native.digest(new[n]) == groups[n]["after"] for n in numbers)':
        '''    assert all(native.digest(old[n]) == groups[n]["before"] and native.digest(new[n]) == groups[n]["after"] for n in numbers)
    following = base.load(next_pages.OUTPUT)
    assert following["candidate_sha256"] == previous["candidate_sha256"]
    assert native.digest(old[84]) == native.digest(new[84]) == following["current_block_sha256"]''',
    'new_contextual_credit=0, shared_payload_and_lookup_exact=True, native_preview_evidence=str(display.PROOF),':
        'new_contextual_credit=0, shared_payload_and_lookup_exact=True, native_preview_evidence=str(display.PROOF),\n'
        '        scoped_nameplate_review={"path": str(names.PROOF), "sha256": base.digest(names.PROOF)},',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_rafael_tradehouse_festival_predecessor": "verified_rafael_east_asia_showdown_predecessor",
    "len(batches) == 1000 and len(checks) == 335": "len(batches) == 1001 and len(checks) == 336",
    "display.PROOF, nameplates.PROOF, args.visual_review": "display.PROOF, names.PROOF, PAGINATION, args.visual_review",
    "ten_original_command_maps_preserved=True": "three_original_command_maps_and_FE_preambles_preserved=True",
    "previously_localized_records=142, new_contextual_records=0, prose_revisions=82":
        "previously_localized_records=199, new_contextual_records=0, prose_revisions=105",
    "wrap_only_revisions=9, justified_retentions=51": "wrap_only_revisions=5, justified_retentions=89",
    "pagination_fixes=1": "pagination_fixes=2",
    "initialized_Rafael_dialogue_and_single_press_transition=True": "initialized_Rafael_bullfight_and_rescue_excerpts=True",
    "native_revised_pages=92, observed_holds=33, contextual_nameplate_retentions=17, reclaimed_page_turns=1":
        "native_revised_pages=110, observed_holds=43, contextual_nameplate_retentions=15, reclaimed_page_turns=2",
    "prior_records_reviewed=142, observed_Rafael_panels=33, native_pages=92":
        "prior_records_reviewed=199, observed_Rafael_panels=43, native_pages=110",
    "prose_revisions=82, justified_retentions=51, wrap_only_revisions=9":
        "prose_revisions=105, justified_retentions=89, wrap_only_revisions=5",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's bullfight and London exchanges

The [testing ROM](../../{ROM.as_posix()}) includes the three reviewed exchanges. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_east_asia_showdown", "rafael_spain_london").replace(
    "verified_rafael_spain_london_predecessor", "verified_rafael_east_asia_showdown_predecessor")
notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'for tag in ("staged_v1", "staged_v2", "staged_v3")': 'for tag in ("spanish_london_staged_v1", "spanish_london_staged_v2")',
    "Preserve the East Asia and Mediterranean candidate, predecessor, staged ROMs and focused fixtures":
        "Preserve the Spain and London candidate, predecessor, staged ROM and focused fixture",
    notes: '''    DOC.write_text(f"""# Rafael's bullfight and London exchanges

The review covers 199 records. There are 105 wording revisions, five wrap-only fixes and 89 justified retentions. Julio's family relationship with Cristina remains explicit. The bullfight preserves the distinction between the picador and the matador and leads into Emilio's recruitment. Cristina's decision about marriage stands through the rescue and her later thanks to Mivor. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Native and visual checks cover all 110 revised pages and 16 alternate name-width cases. Fifteen names and role labels were reviewed and kept. Focused emulator excerpts verified 43 pages, including the four speakerless panels and two shorter speeches that now advance in one press. The prior replay's sampled controls, artwork and unchanged speech commands were checked against the final candidate. The natural story triggers and hardware remain untested. [Native, nameplate and emulator evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters, 17 focused tests and exact clean-input reconstruction passed. These 199 records already carried editorial credit. The following block's five choice captions and two additional FE panels have exact source and current references for the next editorial pass. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md) · [Next B84 source and installed pages](../{next_pages.OUTPUT.as_posix()})
""", encoding="utf-8")
''',
}).replace("rafael_east_asia_showdown", "rafael_spain_london")
scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
