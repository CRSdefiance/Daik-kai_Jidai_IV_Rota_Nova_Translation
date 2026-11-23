"""Register the finished Stockholm Square and Tavern dialogue follow-up."""
from inspect import getsource
from pathlib import Path

from scripts import register_athens_london_trends_20261121 as european
from scripts import register_numbered_fleet_spacing_20261121 as parent
from scripts import stage_stockholm_dialogue_followup_20261121 as stage
from scripts import verify_stockholm_dialogue_display_20261121 as display
from scripts import verify_stockholm_dialogue_replay_20261121 as live
from scripts.source_locked_derivation_v5118 import checked_text


template = european.template
base,native,workflow = stage.base,stage.native,parent.workflow
PROFILE = "all-routes-stockholm-dialogue-v1-20261121"
ROOT = Path("out/stockholm_dialogue_followup_registered_20261121")
ROM = ROOT / "Translation_DS_Stockholm_Dialogue_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_stockholm_dialogue_candidate")
VERIFY,PATCH = PACKAGE / "verification",PACKAGE / "translation.xdelta"
REVIEW,RELEASE = VERIFY / "registered_review.json",VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_stockholm_dialogue_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP,QA = EVIDENCE / "own_startup_verification.json",EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
CHECKPOINT = "Stockholm's fur exchange and recruiting lesson now include three revised lines. The December Square event and Tavern lesson passed ordinary gameplay."


verification = checked_text(european.verification,{
    "stage.review.OUTPUT": "stage.REBOUND",
    'draft["decisions"] == {"revision": 10, "retention": 62}': 'draft["decisions"] == {"revision": 3, "retention": 36}',
    'rendered["newly_rendered_pages"] == 10 and not rendered["actual_gameplay"]':
        'rendered["newly_rendered_pages"] == 3 and rendered["offline_native_only"]',
    'len(playback["holds"]) == 18 and {h["route"] for h in playback["holds"]} == {1}':
        'len(playback["holds"]) == 3 and len(playback["unchanged_controls"]) == 16',
    'and len(viewed) == 5': 'and len(viewed) == 2',
    'assert len(groups) == 8': 'assert len(groups) == 5',
    'assert changed_paths == {"/data/SC1.DK4", "/data/SC3.DK4"}': 'assert changed_paths == {"/data/SC1.DK4"}',
    'len(checked) == len(draft["records"]) == 72': 'len(checked) == len(draft["records"]) == 39',
    'assert ((path, ident) in seen) == (row["route"] == 1) and result["native_pages"] == 1':
        'assert (path, ident) in seen and result["native_pages"] == 1',
    'seen = {(r["file_path"], r["id"]) for r in playback["holds"]}':
        'seen = {(r["file_path"], r["id"]) for r in playback["holds"]}\n'
        '    observed_frames = {r["frame"] for r in playback["holds"] + playback["unchanged_controls"]}',
    'row["observed_in_ordinary_gameplay"] = (path, ident) in seen':
        'row["observed_in_ordinary_gameplay"] = bool(row["previous_capture"] and row["previous_capture"]["frame"] in observed_frames)',
})

main_source = getsource(template.main)
readme = main_source[main_source.index('    (PACKAGE / "README.md").write_text'):main_source.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(main_source,{
    "verified_search_forage_wrap_predecessor": "verified_numbered_fleet_spacing_predecessor",
    "len(batches) == 979 and len(checks) == 314": "len(batches) == 984 and len(checks) == 319",
    "source_movie_preserved=True": "original_stockholm_event_and_tutorial_branches_preserved=True",
    "changed_components=2, repository_tests": "changed_components=1, repository_tests",
    "previously_localized_records=37, new_contextual_records=0, prose_revisions=4":
        "previously_localized_records=39, new_contextual_records=0, prose_revisions=2",
    "wrap_only_revisions=0, justified_retentions=32, name_label_revisions=0, text_display_revisions=1":
        "wrap_only_revisions=1, justified_retentions=36, name_label_revisions=0, text_display_revisions=0",
    "initialized_Rafael_and_Hodram_excerpts=True": "ordinary_Hodram_Tavern_and_December_Square=True",
    "native_revised_pages=5, observed_panels=21, natural_activation=False":
        "native_revised_pages=3, observed_holds=19, natural_activation=True",
    "prior_records_reviewed=37, actual_Rafael_and_Hodram_panels=21, offline_pages=5":
        "prior_records_reviewed=39, actual_Hodram_holds=19, offline_pages=3",
    "prose_revisions=4, justified_retentions=32, text_display_revisions=1":
        "prose_revisions=2, justified_retentions=36, wrap_only_revisions=1",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Stockholm dialogue testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the revised December fur exchange and recruiting lesson. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("moonlit_violin","stockholm_dialogue")

commit_source = getsource(template.commit)
checkpoint_prose = commit_source[commit_source.index("    DOC.write_text"):commit_source.index("    prefix =")]
commit_candidate = checked_text(commit_source,{
    "Preserve the violin candidate or replay ROM": "Preserve the Stockholm candidate and staging ROM",
    checkpoint_prose: '''    DOC.write_text(f"""# Stockholm Square and Tavern dialogue

Reviewed all 32 fur exchange records across the four storylines and seven records in Hodram's recruitment lesson. Two lines were revised for natural dialogue, one line was reflowed, and 36 other texts have individual reasons for retention. The Tavern advice keeps both “boarding battles” and “cruising range” together, and the December Square exchange keeps the wish for a fur coat intact. [Exact source and registered references](../{REVIEW.as_posix()})

The staged ROM repeated the ordinary Riga voyage, the original Tavern choice and all Inn stays. All three revised panels and sixteen unchanged holds matched, including the December 19 forecast and return to the Square. The delegation branch received offline review. Six startup holds, 24 protected name getters and 17 focused tests passed. [Before and after](../{(VERIFY / 'stockholm_before_after_gameplay.png').as_posix()}) · [Cumulative candidate and clean-input patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("moonlit_violin","stockholm_dialogue")

scope = vars(template) | globals()
for source in (verification,build,commit_candidate):
    exec(compile(source,__file__,"exec"),scope)


if __name__=="__main__":
    scope["main"]()
