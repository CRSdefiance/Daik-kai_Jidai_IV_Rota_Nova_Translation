"""Atomically save the verified speech-display checkpoint without completion credit."""
import copy
import gzip
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT=Path('work/analysis/Hodram_B151_B170_formatting_20261102')
MANUSCRIPT=Path('translations/hodram_B151_B170_contextual_editorial_manuscript_v3.json')
DOC=Path('docs/editorial_hodram_B151_B170_speech_display_20261102.md')
SUMMARY=('B151–B170:all642 four-prose-gate comparisons pass,269 proposed revisions/373 retentions;39 scoped name/term decisions. '
         'All634 speeches/650 final pages pass fresh offline native checks anddirect visual review;26 wrap/layout corrections without prose changes. '
         'One15001-frame source-content coldboot qualifies23 cinematic FE panels,not natural endgame orEnglish gameplay. '
         'Eight captions,name display,two static text consumers,stored/gameplay/release remain. '
         'No new completion credit;8856 completed,current7fb6f6d7/main unchanged. All scope/evidence/ROMs preserved;no guide photos.')

if __name__=='__main__':
    target=ROOT/'speech_display_checkpoint_v1.json';assert not target.exists()
    doc=load(MANUSCRIPT);assert len(doc['records'])==doc['complete_four_gate_comparisons']==642
    assert (doc['proposed_revisions'],doc['wording_retentions'],doc['place_name_questions'])==(269,373,0)
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    prose=Path('work/analysis/Hodram_B151_B170_clean_20261102/complete_prose_draft_consistency_v2.json');assert load(prose)['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    names=Path('translations/hodram_B151_B170_scoped_names_andterms_v1.json')
    native_path=ROOT/'ordinary_native_v2/compiled_native_pages.json';native=load(native_path)
    assert len(native['records'])==611 and native['pages']==627 and len(native['reused_record_ids'])==587 and len(native['changed_layout_ids'])==24
    fresh=load(native['fresh_native']);assert len(fresh['records'])==24 and fresh['pages']==37 and fresh['fresh_compiled_alignments']==96
    assert len(native['review_sheets'])==10
    initial_path=ROOT/'ordinary_visual_review_progress_v2.json';initial=load(initial_path)
    assert initial['all_initial_pages_directly_viewed'] and initial['initial_pages_directly_viewed']==627 and len(initial['directly_viewed_sheets'])==63
    plan_path=Path(native['plan']);plans=load(plan_path);planned={r['id']:r for r in plans['records']}
    assert not plans['failures'] and not any(i['severity'] in ['error','warning'] for r in planned.values() for i in r['base_QA']['issues'])
    for sheet in native['review_sheets']+initial['directly_viewed_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    visual_path=ROOT/'ordinary_visual_review_progress_v3.json'
    save(visual_path,dict(**{k:v for k,v in initial.items() if k not in ['findings','unresolved_findings']},
        findings=[dict(**{k:v for k,v in r.items() if k!='resolved'},resolved=True,final_lines=planned[r['id']]['lines']) for r in initial['findings']],
        unresolved_findings=0,resolved_visual_findings=24,earlier_apology_wrap_resolved=True,
        final_native=str(native_path),final_native_sha256=sha(native_path.read_bytes()),replacement_pages_directly_viewed=37,
        replacement_sheets_directly_viewed=native['review_sheets'],all_final_627_ordinary_pages_visually_approved=True,
        fresh_native_job_session=14922,fresh_native_job_terminal=True,fresh_native_job_terminal_exit=0,
        unchanged_native_record_proofs_reused=587,actual_gameplay=False))
    cine_path=Path('work/analysis/Hodram_B156_cinematic_English_v4_20261102/compiled_cinematic_pages.json');cine=load(cine_path)
    assert len(cine['records'])==cine['pages']==23 and cine['exact_native_panels_reused']==22 and cine['fresh_native_panels']==1 and cine['runtime']==native['runtime']
    old_cine=load(cine['previous_native']);assert len(old_cine['review_sheets'])==2
    for sheet in old_cine['review_sheets']+cine['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    cine_visual=cine_path.with_name('visual_review.json')
    save(cine_visual,dict(final_native=str(cine_path),final_native_sha256=sha(cine_path.read_bytes()),
        initial_23_pages_directly_viewed=True,initial_sheets=old_cine['review_sheets'],fresh_one_page_directly_viewed=True,fresh_sheets=cine['review_sheets'],
        resolved_findings=[dict(id='DK4_MES_B156_R0188',finding='We shall/meet again split',resolution='Two complete sentences on separate rows; source right-side placement retained.',final_lines=next(r['lines'] for r in cine['records'] if r['id']=='DK4_MES_B156_R0188'))],
        final23_pages_visually_approved=True,source_individual_staging_andembedded_headings_preserved=True,native_English_not_actual_gameplay=True,
        overall_fifth_gates_still_false=True,new_credit=0))
    ledger_path=Path('translations/editorial_review_current_v1.json');before=ledger_path.read_bytes();ledger=load(ledger_path);prior=copy.copy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(8856,5540,3316)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==8859
    registry=Path('translations/release_stack.json');registry_before=registry.read_bytes();assert sha(registry_before)=='dde90af7920d7562851e16858cb9fef923d25268691c8d9fa1ced156ecd9265a'
    candidate=Path(native['runtime']['candidate']);assert sha(candidate.read_bytes())=='7fb6f6d78441a705c137003d8bfc92d4f5b43fd56b85178a59224f3b4570bc04'
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes())=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    backup=ROOT/'ledger_before_speech_display_checkpoint.json.gz';assert not backup.exists();backup.write_bytes(gzip.compress(before,mtime=0));assert gzip.decompress(backup.read_bytes())==before
    key='Hodram_B151_B170_clean_next_20261102';entry=copy.deepcopy(ledger[key])
    entry.update(complete_four_gate_comparisons=642,open_localization_record_questions=0,
        contextual_manuscript=str(MANUSCRIPT),contextual_manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        scoped_name_andterm_localization_decisions=39,scoped_name_decisions=str(names),scoped_name_decisions_sha256=sha(names.read_bytes()),
        scoped_names_andAbkhaz_Abhaz_cross_consumer_localization_pending=False,
        source_first_draft_prose_gates_not_final_current_comparison=False,
        B156_cinematic_geometry_andall642_formatting_pending=False,B156_source_cinematic_geometry_qualified=True,
        ordinary_offline_native_speech_objects=611,ordinary_offline_final_pages=627,cinematic_FE_native_objects=23,
        total_offline_speech_objects=634,total_offline_speech_pages=650,all650_final_speech_pages_directly_viewed=True,
        resolved_visual_layout_findings=25,earlier_apology_wrap_fix=1,total_new_speech_layout_corrections=26,
        source_content_coldboot_frames=15001,source_content_fixture_not_natural_endgame=True,actual_English_batch_gameplay_observed=False,
        native_speech_proof=str(native_path),cinematic_proof=str(cine_path),speech_visual_review=str(visual_path),cinematic_visual_review=str(cine_visual),
        pending_typed_captions=8,pending_typed_menu_commands=4,pending_static_text_proposals=2,pending_static_owned_prefix_bytes=15,
        scoped_name_native_display_pending=True,stored_mixed_objects_allocation_andbranch_checks_pending=True,
        representative_English_gameplay_andregistered_cumulative_release_pending=True,all642_fifth_formatting_gates_pending=True,
        speech_display_checkpoint=str(target),documentation=str(DOC),prior_latest_checkpoint=ledger['latest_checkpoint'])
    ledger[key]=entry;ledger['latest_checkpoint']=SUMMARY
    assert all(ledger[k]==v for k,v in prior.items() if k not in [key,'latest_checkpoint'])
    encoded=encode_ledger(ledger);staged=ledger_path.with_name('editorial_review_current_v1.pending_B151_B170_display.json');assert not staged.exists()
    staged.write_bytes(encoded);assert staged.read_bytes()==encoded and ledger_path.read_bytes()==before
    os.replace(staged,ledger_path);assert load(ledger_path)==ledger and registry.read_bytes()==registry_before
    dependencies=[MANUSCRIPT,DOC,prose,names,native_path,plan_path,visual_path,cine_path,cine_visual,
        Path('work/analysis/Hodram_B156_cinematic_geometry_20261102/observed_cinematic_geometry.json'),
        Path('work/analysis/Hodram_B151_B170_clean_20261102/two_static_text_slots_proposal_v1.json'),Path(__file__)]
    save(target,dict(summary=SUMMARY,prose_comparisons=642,revisions=269,retentions=373,scoped_name_term_decisions=39,
        offline_speech_objects=634,final_speech_pages=650,all_final_speech_pages_directly_viewed=True,
        ordinary_native_job_3445_terminal_exit=0,refresh_job_14922_terminal_exit=0,all_jobs_terminal=True,
        new_editorial_completion_credit=0,completed_records=8856,all_other_ledger_keys_exact=True,
        ledger_before_sha256=sha(before),ledger_after_sha256=sha(ledger_path.read_bytes()),ledger_backup=str(backup),
        registry_unchanged_sha256=sha(registry_before),main_andregistered_candidate_unchanged=True,
        new_registered_ROMs=0,source_only_research_ROMs=1,actual_source_content_coldboots=1,actual_source_content_frames=15001,
        actual_English_gameplay=False,guide_photo_collection_discontinued=True,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in dependencies}))
    print('Checkpoint saved atomically:642 prose comparisons;634 speeches/650 final offline pages;26 layout corrections;all prior credit/releases preserved. Remaining caption/name/static/stored/gameplay/release gates explicit.')
