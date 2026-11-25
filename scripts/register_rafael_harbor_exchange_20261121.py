"""Register the verified Rafael opening and preparation review."""
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_stockholm_dialogue_followup_20261121 as parent
from scripts import stage_rafael_harbor_exchange_20261121 as stage
from scripts import verify_rafael_harbor_exchange_20261121 as verifier
from scripts.source_locked_derivation_v5118 import checked_text


template=parent.template
base,native,workflow=stage.base,stage.native,parent.workflow
PROFILE="all-routes-rafael-harbor-dialogue-v1-20261121"
ROOT=Path("out/rafael_harbor_exchange_registered_20261121")
ROM=ROOT/"Translation_DS_Rafael_Harbor_20261121_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=Path("releases/all_routes_editorial_20261121_rafael_harbor_candidate")
VERIFY,PATCH=PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE=VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC=Path("docs/editorial_rafael_harbor_registered_20261121.md")
EVIDENCE=stage.ROOT
STARTUP,QA=EVIDENCE/"own_startup_verification.json",EVIDENCE/"qa_passed.xml"
STARTUP_CAPTURE=verifier.run.STARTUP_CAPTURE
display,live=verifier,SimpleNamespace(PROOF=verifier.LIVE)
CHECKPOINT="Rafael's opening and preparation lesson have 30 revised lines and 87 justified retentions. Seven revised panels and both harbor paintings were verified in ordinary gameplay."


verification=checked_text(parent.verification,{
    "stage.REBOUND":"stage.review.OUTPUT",
    'draft["decisions"] == {"revision": 3, "retention": 36}':'draft["decisions"] == {"revision": 30, "retention": 87}',
    'playback["original_notice_dismissal_and_Square_return"]':'len(playback["movie_transition_holds"]) == 4',
    'rendered["newly_rendered_pages"] == 3':'rendered["newly_rendered_pages"] == 45',
    'len(playback["holds"]) == 3 and len(playback["unchanged_controls"]) == 16':
        'len(playback["holds"]) == 7 and len(playback["unchanged_controls"]) == 11',
    'and len(viewed) == 2':'and len(viewed) == 9',
    'assert len(groups) == 5':'assert len(groups) == 1',
    'assert changed_paths == {"/data/SC1.DK4"}':'assert changed_paths == {"/data/SC0.DK4"}',
    'len(checked) == len(draft["records"]) == 39':'len(checked) == len(draft["records"]) == 117',
    'assert (path, ident) in seen and result["native_pages"] == 1':
        'assert ((path, ident) in seen) == bool(row["previous_capture"]) and result["native_pages"] == 1',
    '    startup = startup_check.startup_proof':
        '    assert all(after[p] == before[p] for p in ("/FLS/M20.fls", "/FLS/m21.fls"))\n'
        '    startup = startup_check.startup_proof',
})

main_source=getsource(template.main)
readme=main_source[main_source.index('    (PACKAGE / "README.md").write_text'):main_source.index('    base.save(PACKAGE / "checksums.json"')]
build=checked_text(main_source,{
    "verified_search_forage_wrap_predecessor":"verified_stockholm_dialogue_predecessor",
    "len(batches) == 979 and len(checks) == 314":"len(batches) == 985 and len(checks) == 320",
    "source_movie_preserved=True":"original_harbor_and_ship_movies_preserved=True",
    "changed_components=2, repository_tests":"changed_components=1, repository_tests",
    "previously_localized_records=37, new_contextual_records=0, prose_revisions=4":
        "previously_localized_records=117, new_contextual_records=0, prose_revisions=17",
    "wrap_only_revisions=0, justified_retentions=32, name_label_revisions=0, text_display_revisions=1":
        "wrap_only_revisions=13, justified_retentions=87, name_label_revisions=0, text_display_revisions=0",
    "initialized_Rafael_and_Hodram_excerpts=True":"ordinary_Rafael_harbor_opening=True",
    "native_revised_pages=5, observed_panels=21, natural_activation=False":
        "native_revised_pages=30, native_name_stress_pages=15, observed_holds=22, natural_activation=True",
    "prior_records_reviewed=37, actual_Rafael_and_Hodram_panels=21, offline_pages=5":
        "prior_records_reviewed=117, actual_Rafael_harbor_holds=22, offline_pages=45",
    "prose_revisions=4, justified_retentions=32, text_display_revisions=1":
        "prose_revisions=17, justified_retentions=87, wrap_only_revisions=13",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael harbor and preparation testing candidate

The [testing ROM](../../{ROM.as_posix()}) revises the opening harbor exchange, Julio's loan and the preparation lesson. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("moonlit_violin","rafael_harbor")

commit_source=getsource(template.commit)
checkpoint_prose=commit_source[commit_source.index("    DOC.write_text"):commit_source.index("    prefix =")]
commit_candidate=checked_text(commit_source,{
    "Preserve the violin candidate or replay ROM":"Preserve the Rafael harbor candidate and staging ROM",
    checkpoint_prose:'''    DOC.write_text(f"""# Rafael's opening and departure preparation

Reviewed the complete 117-record opening against clean Japanese. Seventeen lines have new wording, 13 were reflowed and 87 have individual reasons for retention. The restored ship stays the Carteira. The dialogue keeps Rafael's decision to ask Julio, his promise to repay the loan and all three responsibilities Julio gives him. The two original preparation choices and their branches remain exact. [Record-level review](../{REVIEW.as_posix()})

Ordinary New Game gameplay reproduced the harbor reveal and seven revised panels, including the given-name substitution. Fourteen whole screens and the ship artwork over one changed line match the predecessor. The later revised lines passed offline native rendering, including 15 name-length stress pages. Six separate startup holds, 24 protected name getters and 17 focused tests passed. [Source artwork and baseline replay](editorial_rafael_harbor_shared_artwork_20261121.md) · [Testing ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("moonlit_violin","rafael_harbor")

scope=vars(template)|globals()
for source in (verification,build,commit_candidate):
    exec(compile(source,__file__,"exec"),scope)


if __name__=="__main__":
    scope["main"]()
