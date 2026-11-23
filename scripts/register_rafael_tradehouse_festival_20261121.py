"""Register Rafael's verified trade house, festival and Maria exchanges."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import check_rafael_tradehouse_festival_gameplay_20261121 as live
from scripts import register_rafael_pereira_village_20261121 as parent
from scripts import verify_rafael_tradehouse_festival_20261121 as display
from scripts.register_amsterdam_tavern_editorial_20261120 import START_FRAMES, checked_report, startup_proof
from scripts.source_locked_derivation_v5118 import checked_text


stage = live.stage
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-rafael-tradehouse-festival-v1-20261121"
ROOT = Path("out/rafael_tradehouse_festival_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_Tradehouse_Festival_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_rafael_tradehouse_festival_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_tradehouse_festival_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
CHECKPOINT = ("Reviewed 200 records across five Rafael exchanges. The registered build has 87 wording revisions, "
              "seven wrap-only fixes and 106 justified retentions.")


def check_startup_report(path, candidate, frames):
    if path == STARTUP_CAPTURE:
        return checked_report(path, candidate, frames)

    def retained_holds(report_path):
        report = base.load(report_path)
        shots = [shot for shot in report["frames_captured"]
                 if shot["frame"] in START_FRAMES and shot["path"].endswith("_cold_boot.png")]
        # The checkpoint cleanup leaves these six sealed comparison holds and the RAM snapshot.
        assert {shot["frame"] for shot in shots} == set(START_FRAMES)
        return report | {"frames_captured": shots}

    return FunctionType(checked_report.__code__, checked_report.__globals__ |
                        {"load": retained_holds})(path, candidate, frames)


startup_check = FunctionType(startup_proof.__code__, startup_proof.__globals__ |
                            {"checked_report": check_startup_report})
verification = checked_text(getsource(parent.verify), {
    '    startup = parent.scope["startup_check"].startup_proof': '    startup = startup_check',
    '    assert rendered["revised_pages"] == 110': '    assert rendered["revised_pages"] == 94 and rendered["festival_FE_panels"] == 5',
    '''    assert len(playback["holds"]) == 23 and len(playback["offline_only"]) == 93
    reward, = [row for row in playback["holds"] if row["system_FE"]]
    assert reward["id"] == "DK4_MES_B61_R0113"''':
        '''    assert len(playback["holds"]) == 28 and len(playback["offline_only"]) == 74
    assert playback["original_picture_switches_copied_and_exercised"]
    assert sum(row["system_FE"] for row in playback["holds"]) == 5''',
    'len(results) == 197 and len(observed) == 23': 'len(results) == 200 and len(observed) == 28',
    '{"revision": 110, "retention": 87}': '{"revision": 94, "retention": 106}',
    '{"prose and wrap": 96, "wrap": 14, "retention": 87}': '{"prose and wrap": 87, "wrap": 7, "retention": 106}',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_rafael_spain_predecessor": "verified_rafael_pereira_village_predecessor",
    "len(batches) == 998 and len(checks) == 333": "len(batches) == 999 and len(checks) == 334",
    "four_original_command_maps_preserved=True": "five_original_command_maps_and_festival_FE_controls_preserved=True",
    "previously_localized_records=197, new_contextual_records=0, prose_revisions=96":
        "previously_localized_records=200, new_contextual_records=0, prose_revisions=87",
    "wrap_only_revisions=14, justified_retentions=87": "wrap_only_revisions=7, justified_retentions=106",
    "initialized_Rafael_dialogue_and_funds_excerpt=True": "initialized_Rafael_festival_and_dialogue_excerpt=True",
    "native_revised_pages=110, observed_holds=23, retained_FE_notice=True":
        "native_revised_pages=94, observed_holds=28, observed_festival_FE_panels=5",
    "prior_records_reviewed=197, observed_Rafael_panels=23, native_pages=110":
        "prior_records_reviewed=200, observed_Rafael_panels=28, native_pages=94",
    "prose_revisions=96, justified_retentions=87, wrap_only_revisions=14":
        "prose_revisions=87, justified_retentions=106, wrap_only_revisions=7",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's trade house, festival and first encounter with Maria

The [testing ROM](../../{ROM.as_posix()}) includes the five reviewed exchanges. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_pereira_village", "rafael_tradehouse_festival").replace(
    "verified_rafael_tradehouse_festival_predecessor", "verified_rafael_pereira_village_predecessor")
notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    '    first_fixture = stage.ROOT / "focused_gameplay/Rafael_Pereira_Village_RESEARCH_ONLY.nds"':
        '    earlier_builds = tuple(stage.ROOT.with_name(tag) / stage.ROM.name for tag in ("staged_v1", "staged_v2"))',
    '    for path in (ROM, stage.ROM, parent.ROM, first_fixture,':
        '    for path in (ROM, stage.ROM, parent.ROM, *earlier_builds,',
    "Preserve the village candidate, its predecessor, staged ROM and focused fixtures":
        "Preserve the trade house and festival candidate, predecessor, staging ROMs and focused fixture",
    notes: '''    DOC.write_text(f"""# Rafael's trade house, festival and first encounter with Maria

The review covers 200 records. There are 87 wording revisions, seven wrap-only fixes and 106 justified retentions. The village exchanges consistently use trade house. The conversation over tea preserves both stated ages and leaves Charlotte's unfinished thought open. The festival retains the original pauses. Maria's bargain preserves the official maritime ban, the wako term and the Bamboo Assembly Plan. [Exact source and registered decisions](../{REVIEW.as_posix()})

Native and visual checks cover all 94 revised pages and the five FE picture panels, including two revised panels. A focused emulator excerpt exercised the original picture switches and verified 28 panels. The replay used the preceding staging ROM. The sampled commands, initialization commands and relevant ARM9 and font files match this candidate byte for byte. Twenty revised pages were observed and 74 received offline verification. The natural story triggers and hardware remain untested. [Native and emulator evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters, 17 focused tests and exact clean-input reconstruction passed. These 200 records already carried editorial credit. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_pereira_village", "rafael_tradehouse_festival")
scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
