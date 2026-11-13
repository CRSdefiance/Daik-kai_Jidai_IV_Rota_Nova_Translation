"""Record direct visual review and pending batch work without completion credit."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.make_unique_editorial_page_sheets import pages
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Hodram_B81_B89_editorial_20261101')
DOC=Path('translations/hodram_B81_B89_editorial_manuscript_v2.json')
NATIVE=Path('work/analysis/Hodram_B81_B89_native_20261101c/compiled_native_pages.json')
INITIAL=Path('work/analysis/Hodram_B81_B89_visual_20261101/visual_coverage_pending.json')
LEDGER=Path('translations/editorial_review_current_v1.json')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    doc,native,initial=map(load,[DOC,NATIVE,INITIAL])
    assert native['manuscript_sha256']==sha(DOC.read_bytes())
    sources=[(Path(initial['native']),[Path(s['path']) for s in initial['review_sheets']])]
    for suffix in ['b','c']:
        path=Path(f'work/analysis/Hodram_B81_B89_native_20261101{suffix}/fresh/compiled_native_pages.json')
        report=load(path);sources.append((path,[Path(s['path']) for s in report['review_sheets']]))
    # The reviewer opened all25 initial sheets and all four changed sheets.
    # Exact old planes carry their prior reviewed receipt via the initial map.
    seen={};sheets=[]
    for path,paths in sources:
        for sheet in paths:
            sheets.append(dict(path=str(sheet),sha256=sha(sheet.read_bytes()),directly_viewed=True))
        for record,number,page,key in pages(load(path)):
            seen[key]=dict(report=str(path),id=record['id'],page=number)
    assert len(initial['review_sheets'])==25 and len(sheets)==29
    final=[]
    for record,number,page,key in pages(native):
        assert key in seen
        final.append(dict(id=record['id'],page=number,native_plane_sha256=key[-1],viewed_provenance=seen[key]))
    assert len(final)==306 and len(native['records'])==304
    findings=[
        dict(id='DK4_MES_B84_R0012',type='prose cadence',resolution='One natural invitation preserves the opportunity; no redundant setup.'),
        dict(id='DK4_MES_B85_R0186',type='source fidelity and cadence',resolution='Longer taunt restores awkward posture; two complete rows.'),
        dict(id='DK4_MES_B85_R0018',type='page continuity',resolution='Final rejection begins on page2; no intention/of getting married split.'),
        dict(id='DK4_MES_B85_R0123',type='page continuity',resolution='Whole invitation fits one page by releasing the overconstraining soft quite/a pair. All original QA checks remain; no warning waiver.'),
        dict(id='DK4_MES_B89_R0067',type='page continuity',resolution='Complete permission to claim the discovery begins page2.'),
    ]
    visual=dict(native=str(NATIVE),native_sha256=sha(NATIVE.read_bytes()),records=final,pages=306,
        all_final_pages_directly_viewed_or_exact_plane_reuse=True,review_sheets=sheets,
        initial_visual_coverage=str(INITIAL),initial_visual_coverage_sha256=sha(INITIAL.read_bytes()),
        eight_prior_approved_exact_planes_andfive_intrabatch_duplicates_retained=True,
        findings=findings,all_final_bodies_complete_readable_glyphs_andbounds=True,
        typed_choice_labels_names_stored_gameplay_andrelease_still_pending=True,
        failed_wrapper_drafts_preserved=['scripts/plan_editorial_scene_prose_v3.py','scripts/plan_editorial_scene_prose_v4.py'],
        no_text_shortened_for_fit_no_authored_breaks_padding_font_orviewport_changes=True,
        actual_gameplay=False,new_credit=0,full_goal_complete=False)
    save(ROOT/'visual_review.json',visual)
    before=LEDGER.read_bytes();ledger=load(LEDGER)
    counts={k:ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']}
    assert counts==dict(records_editorially_completed=7687,records_with_source_and_prose_pass=7690,records_with_source_prose_drafts=7690,records_revised_and_integrated=4770,retained_wordings_editorially_completed=2917)
    save(ROOT/'ledger_before_preview_checkpoint.json',ledger)
    key='Hodram_B81_B89_prose_andpreview_20261101';assert key not in ledger
    checkpoint=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        native=str(NATIVE),native_sha256=sha(NATIVE.read_bytes()),visual=str(ROOT/'visual_review.json'),
        visual_sha256=sha((ROOT/'visual_review.json').read_bytes()),
        prose_objects=306,speeches=304,typed_choices=2,revisions=222,justified_retentions=84,
        four_prose_gates_passed=306,formatting_gates_passed=0,final_offline_speech_pages=306,
        original_native_alignments=1216,first_refresh_alignments=20,second_refresh_alignments=4,
        unchanged_final_native_rows_reused=303,errors=0,warnings=0,infos=99,
        current_English_compared=True,clean_first_stage_preserved=True,
        source_current_refs_andindividual_decisions_in_manuscript=True,
        pending=['B87 two typed menu labels/provider/controller','Emilio wide-F name metadata andnative/actual header','stored full batch/relative andarchive checks','focused initialized gameplay/transitions','pure registered integration andclean-input patch/own startup'],
        no_new_ROM_orcompletion_credit=True,new_credit=0,full_goal_complete=False)
    ledger[key]=checkpoint
    assert all(ledger[k]==v for k,v in counts.items()) and LEDGER.read_bytes()==before
    save(LEDGER,ledger);save(ROOT/'preview_checkpoint.json',checkpoint)
    print(dict(prose_objects=306,revisions=222,retentions=84,final_pages=306,visual_sheets=29,completion_credit=0,pending=len(checkpoint['pending'])))
