"""Save native/menu/name/static/storage andrepresentative English evidence atomically."""
import copy
import gzip
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT=Path('work/analysis/Hodram_B151_B170_reconstruction_inputs_20261102')
DOC=Path('docs/editorial_hodram_B151_B170_stored_and_cinematic_20261102.md')
SUMMARY=('B151–B170:642 four-prose-gate comparisons/269 proposed revisions/373 retentions preserved;634 speeches/650 final offline pages and26 layout fixes. '
         'Eight captions/four menus,41 scoped name strings,two typed static-label proposals,stored634 speeches/700 branch cases and325 archive loads pass. '
         'One15001-frame English content coldboot observes31 selected speeches/all23 cinematic FE panels;three QA sheets viewed,not natural endgame. '
         'Actual menu/new page-spacing/static-widget evidence andregistered integration/exact clean patch/own startup remain. '
         '8856 completions/current7fb6f6d7/main unchanged;full scope preserved;no guide photos.')

if __name__=='__main__':
    target=ROOT/'stored_cinematic_checkpoint_v1.json';assert not target.exists()
    old_checkpoint=Path('work/analysis/Hodram_B151_B170_formatting_20261102/speech_display_checkpoint_v1.json');old=load(old_checkpoint)
    for p,h in old['evidence'].items():assert sha(Path(p).read_bytes())==h,p
    rebuilt_path=Path('work/analysis/Hodram_B151_B170_rebuilt_20261102/reconstruction.json');rebuilt=load(rebuilt_path)
    stored_path=Path('work/analysis/Hodram_B151_B170_stored_20261102/stored_native_verification.json');stored=load(stored_path)
    assert stored['reconstruction_sha256']==sha(rebuilt_path.read_bytes()) and stored['complete_stored_pages']==650
    assert len(stored['records'])==634 and stored['typed_labels_checked']==8 and stored['fresh_relocated_native_relative_cases']==700
    assert stored['fresh_parity_dependent_pages']==331 and stored['exact_compiled_pages_reused']==319
    assert len(rebuilt['groups'])==len(rebuilt['changed_blocks'])==20 and rebuilt['command_count']==1118 and rebuilt['relative_sites']==140
    assert sha(Path(rebuilt['research_ROM']).read_bytes())==rebuilt['research_ROM_sha256']=='bf84098bbdce739c27617a5ab61db7b11c13e9c6da8acbbc143bed4b557a5b97'
    loaders_path=Path('work/analysis/Hodram_B151_B170_loaders_20261102/verification.json');loader=load(loaders_path)
    assert loader['reconstruction_sha256']==sha(rebuilt_path.read_bytes()) and loader['fresh_whole_archive_loads_andcache_hits']==325
    assert loader['fresh_parent_cases']==40 and loader['exact_reused_parent_cases']==610
    menu_visual=Path('work/analysis/Hodram_B151_B170_formatting_20261102/menus_v1/caption_visual_review.json');assert load(menu_visual)['all8_reviewed_captions_visually_approved']
    name_visual=Path('work/analysis/Hodram_B151_B170_scoped_name_planes_20261102/visual_review.json');assert load(name_visual)['all41_native_strings_visually_approved']
    static_path=Path('work/analysis/Hodram_B151_B170_static_labels_20261102/native_static_labels_qualification.json');static=load(static_path)
    assert static['all_native_getter_copy_full_characters_bounds_canaries_andparent_inverse_pass'] and len(static['negative_cases_rejected'])==10
    assert static['complete_owned_data_plan']['owned_span_bytes']==15 and static['complete_owned_data_plan']['changed_bytes']==12
    actual_path=Path('work/analysis/Hodram_B156_cinematic_English_actual_20261102/observed_English_panels.json');actual=load(actual_path)
    assert actual['English_speech_objects_observed']==31 and actual['FE_panels_observed']==23 and actual['actual_coldboot_frames']==15001
    assert actual['all31_stored_English_bodies_andmacros_observed_in_original_sequence'] and actual['all23_FE_geometries_match_qualified_source']
    assert len(actual['review_sheets'])==3
    for sheet in actual['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    actual_visual=actual_path.with_name('actual_visual_review.json')
    save(actual_visual,dict(observation=str(actual_path),observation_sha256=sha(actual_path.read_bytes()),directly_viewed_sheets=actual['review_sheets'],
        actual_English_objects_visually_reviewed=31,all23_FE_panels_and8_other_dialogue_holds_visually_approved=True,
        observed_headers=['Sera Shahrbaraz','Hodram Bergstrom','Sirwood Eme','Gerhard Adernkatz'],
        complete_text_normal_glyphs_embedded_headings_left_right_staging_andtransitions_pass=True,
        source_wrapper_andother_dialogue_excluded=True,natural_endgame=False,earned_progress=False,full_route=False,hardware=False,
        observed_records=[dict(id=r['id'],frame=r['actual_paint_frame'],capture=r['capture']) for r in actual['selected_records']],
        unvisited_scope='Other B151–B170 conditional dialogue,menu interaction,new two-page spacing,Rafael0/Claudio/Arcadius headers,full catalogue UI,city87 andrenamed-ship widgets remain unvisited in this batch.',
        later_opening_text_not_additional_editorial_credit=True,new_credit=0,guide_photos=False))
    ledger_path=Path('translations/editorial_review_current_v1.json');before=ledger_path.read_bytes();ledger=load(ledger_path);prior=copy.copy(ledger)
    assert sha(before)==old['ledger_after_sha256']
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(8856,5540,3316)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==8859
    registry=Path('translations/release_stack.json');registry_before=registry.read_bytes();assert sha(registry_before)=='dde90af7920d7562851e16858cb9fef923d25268691c8d9fa1ced156ecd9265a'
    assert sha(Path(rebuilt['parent']).read_bytes())=='7fb6f6d78441a705c137003d8bfc92d4f5b43fd56b85178a59224f3b4570bc04'
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes())=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    backup=ROOT/'ledger_before_stored_cinematic_checkpoint.json.gz';assert not backup.exists();backup.write_bytes(gzip.compress(before,mtime=0));assert gzip.decompress(backup.read_bytes())==before
    key='Hodram_B151_B170_clean_next_20261102';entry=copy.deepcopy(ledger[key])
    entry.update(pending_typed_captions=0,pending_typed_menu_commands=0,typed_menu_objects_offline_native_andvisual_approved=4,
        typed_caption_objects_offline_native_andvisual_approved=8,pending_actual_menu_controller=True,
        scoped_name_native_display_pending=False,scoped_name_literals_native_andvisually_approved=41,
        scoped_names_bound_getters_reused=72,scoped_ordinary_actors=36,mentioned_name=MIVOR if False else 'Mivor',
        static_labels_source_ownership_native_getters_copy_andfont_planes_qualified=2,pending_static_label_native_checks=0,
        pending_static_label_integration=2,pending_static_label_widget_compatibility_oractual_tests=True,
        static_owned_prefix_bytes=15,static_actually_changed_bytes=12,static_label_ROM_mutation=False,
        stored_mixed_objects_allocation_andbranch_checks_pending=False,stored_speech_records=634,stored_captions=8,
        stored_pages=650,stored_fresh_parity_pages=331,stored_reused_pages=319,native_relative_branch_cases=700,
        archive_load_checks_pending=False,native_archive_loads=325,fresh_parent_handoffs=40,exact_reused_parent_handoffs=610,
        source_reconstruction=str(rebuilt_path),source_reconstruction_sha256=sha(rebuilt_path.read_bytes()),
        research_story_ROM=rebuilt['research_ROM'],research_story_ROM_sha256=rebuilt['research_ROM_sha256'],
        research_story_ROM_not_registered_handoff=True,stored_native_proof=str(stored_path),archive_loader_proof=str(loaders_path),
        actual_English_batch_gameplay_observed=True,actual_English_content_fixture_objects=31,actual_English_content_fixture_FE_objects=23,
        actual_English_coldboot_frames=15001,actual_English_visual_review=str(actual_visual),actual_English_visual_review_sha256=sha(actual_visual.read_bytes()),
        actual_source_condition_wrapper_excluded_not_natural_endgame=True,new_two_page_spacing_gameplay_pending=True,
        full_catalogue_UI_Rafael0_in_this_batch_andstatic_label_widgets_unvisited=True,
        registered_integration_exact_clean_input_patch_andown_startup_pending=True,
        stored_cinematic_checkpoint=str(target),documentation=str(DOC),prior_latest_checkpoint=ledger['latest_checkpoint'])
    ledger[key]=entry;ledger['latest_checkpoint']=SUMMARY;assert all(ledger[k]==v for k,v in prior.items() if k not in [key,'latest_checkpoint'])
    encoded=encode_ledger(ledger);staged=ledger_path.with_name('editorial_review_current_v1.pending_B151_B170_stored.json');assert not staged.exists()
    staged.write_bytes(encoded);assert staged.read_bytes()==encoded and ledger_path.read_bytes()==before;os.replace(staged,ledger_path)
    assert load(ledger_path)==ledger and registry.read_bytes()==registry_before
    deps=[DOC,old_checkpoint,ROOT/'input_binding.json',rebuilt_path,stored_path,loaders_path,menu_visual,name_visual,static_path,actual_path,actual_visual,Path(__file__)]
    save(target,dict(summary=SUMMARY,all_jobs_terminal=True,terminal_exits=dict(name_job_36875=0,rebuild_job_84086=0,stored_job_7009=0,English_job_38270=0,
        menus=0,static_native=0,archive_loader=0,English_binder=0),new_completion_credit=0,completed_records=8856,
        all_other_ledger_keys_preserved=True,ledger_before_sha256=sha(before),ledger_after_sha256=sha(ledger_path.read_bytes()),ledger_backup=str(backup),
        registry_unchanged_sha256=sha(registry_before),registered_candidate_andmain_unchanged=True,new_registered_ROMs=0,
        new_research_ROMs=2,new_English_coldboots=1,new_English_frames=15001,full_goal_complete=False,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in deps}))
    print('Checkpoint saved:menus/names/static native+visual,634 stored speeches/eight captions,700 branch cases,325 loads and31 observed English speeches. All prior credit/releases preserved;necessary actual/release checks remain explicit.')
