"""Independently audit B174 reference coverage, unchanged counts and preserved history."""
import gzip
import json
from collections import Counter
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.checkpoint_lil_B174_references_v4492 import ROOT as CHECKPOINT,INPUT,DOC,APPROVAL,FAMILY
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4493')

def unchanged_outside(a,b,allowed):
    assert {k:v for k,v in a.items() if k not in allowed}=={k:v for k,v in b.items() if k not in allowed}

if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    raw=gzip.decompress((CHECKPOINT/'ledger.before.json.gz').read_bytes());before=json.loads(raw)
    assert sha(raw)==read('work/analysis/editorial_handoff_verification_v4480/verified_handoff.json')['ledger_sha256']
    assert lp.read_bytes()==encode_ledger(ledger) and lp.stat().st_size<100*1024*1024
    allowed={'contextual_story_natural_dialogue_pass_v1871','active_source_prose_drafts','coverage_units',
        'unfinished_editorial_scope_v4492','lil_B174_reference_reconciliation_v4492','latest_checkpoint'}
    unchanged_outside(before,ledger,allowed)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    fresh,old=[p['contextual_story_natural_dialogue_pass_v1871'] for p in [ledger,before]]
    unchanged_outside(old,fresh,{'latest_contextual_manuscript','latest_pending_contextual_family','coverage_note','pending_contextual_families'})
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5833,5800,33)
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5800,5836,3686,2114)
    doc,previous,approval=map(read,[DOC,INPUT,APPROVAL]);validate_natural_dialogue_batch(doc)
    assert len(doc['records'])==33 and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':23,'retain-wording':10}
    assert [r['english'] for r in doc['records']]==[r['english'] for r in previous['records']]
    ids=[r['id'] for r in doc['records']];offline=['DK4_MES_B174_R0069']
    actual_ids=approval['actual_sampled_display_IDs']
    assert len(actual_ids)==32 and approval['offline_only_display_IDs']==offline
    assert set(actual_ids)|set(offline)==set(ids) and not set(actual_ids)&set(offline)
    assert approval['manuscripts']=={str(DOC):sha(DOC.read_bytes())}
    assert len(fresh['pending_contextual_families'])==1;pending=fresh['pending_contextual_families'][0]
    assert pending['id']==FAMILY and pending['manuscript']==str(DOC) and pending['manuscript_sha256']==sha(DOC.read_bytes())
    assert pending['actual_sampled_display_IDs']==actual_ids and pending['offline_only_display_IDs']==offline
    unchanged_outside(old['pending_contextual_families'][0],pending,{'manuscript','manuscript_sha256','manuscripts','pending',
        'actual_sampled_display_IDs','offline_only_display_IDs','new_emulator_runs','reference_approval','reference_approval_sha256'})
    a,b=before['active_source_prose_drafts'],ledger['active_source_prose_drafts']
    unchanged_outside(a,b,{'manuscripts','route_record_subsets_pending','status','note'})
    assert b['manuscripts']==a['manuscripts']+[str(DOC)]
    assert b['route_record_subsets_pending']=={**a['route_record_subsets_pending'],str(INPUT):[],str(DOC):ids}
    assert len(ledger['coverage_units'])==len(before['coverage_units'])
    for a,b in zip(before['coverage_units'],ledger['coverage_units'],strict=True):
        if a['id']=='all-route-scenes':
            unchanged_outside(a,b,{'next'});assert (b['reviewed_route_records'],b['completed_route_records'])==(4234,4201)
        elif a['id']==FAMILY:
            unchanged_outside(a,b,set(pending)|{'status','actual_new_cold_boot_runs','actual_complete_native_panels','registered_release_pending'})
            assert b['actual_complete_native_panels']==32 and b['completion_credit_added']==0 and b['registered_release_pending']
        else:assert a==b
    receipt=read(CHECKPOINT/'checkpoint_receipt.json')
    for path,digest in {**receipt['evidence'],**receipt['preserved_release_files'],**approval['evidence']}.items():
        assert sha(Path(path).read_bytes())==digest,path
    assert receipt['all_jobs_terminal'] and receipt['ROMs_pinned']==0 and receipt['previously_pinned_ROMs_preserved']==3
    for path,digest in receipt['updated_files'].items():assert sha(Path(path).read_bytes())==digest,path
    for key in ['reference_map','representative_proof','final_padding_proof','relocated_control_proof','termination_decode_proof','postscene_native_state_proof']:
        assert sha(Path(doc[key]).read_bytes())==doc[key+'_sha256']
    mapping=read(doc['reference_map']);block=mapping['blocks'][0]
    assert mapping['format']=='dk4-lil-B174-source-relocation-map-v1' and mapping['external_references_complete'] and mapping['representative_shared_rules_approved']
    assert block['block']==174 and len(block['text_records'])==33 and len(block['command_map'])==45
    assert len(block['relative_skip_fixups'])==4 and len(block['target_native_skip_cases'])==20
    assert block['original_declared_end_word_maps']==[dict(source_offset=2086,target_offset=2204,extent=4,source_four_zero_bytes_exact=True)]
    assert (block['source_bytes'],block['research_bytes'],block['source_logical_end'],block['research_logical_end'])==(2092,2208,2090,2208)
    stored=read(doc['final_padding_proof']);controls=read(doc['relocated_control_proof']);ends=read(doc['termination_decode_proof'])
    assert (stored['current_final_stored_macro_alignment_cases'],stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(132,48,84)
    assert len(controls['relocated_dispatch_cases'])==33 and len(controls['relocated_predicate_pairs'])==len(controls['relocated_C200_pairs'])==1
    assert len(ends['cases'])==2 and ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
    parent=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds')
    current,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[174] for im in [parent,clean]]
    target=Path(block['research_block']).read_bytes();assert sha(target)==block['target_block_sha256']
    text={r['id']:r for r in block['text_records']}
    for row,oldrow in zip(doc['records'],previous['records'],strict=True):
        assert all(row['review'].values()) and row['source_hex']==oldrow['source_hex'] and row['source_complete_preamble_hex']==oldrow['source_complete_preamble_hex']
        for data,ref,value in [(jp,row['source_reference'],row['source_hex']),(current,row['current_reference'],row['current_hex'])]:
            at=ref['offset'];raw=bytes.fromhex(value);assert data[at:at+len(raw)]==raw and data[at+len(raw)]==0
            assert data[at-5:at+1].hex()==row['source_complete_preamble_hex']
        new=text[row['id']];value=bytes.fromhex(new['target_hex']);assert target[new['new_offset']:new['new_offset']+len(value)]==value
        assert row['actual_B22_display_fixture_observed']==(row['id'] in actual_ids)
        assert row['offline_only_native_display_checked']==(row['id'] in offline)
        assert row['current_native_UI_body_explicit_unexecuted_boundary']==(row['id'] in offline)
        if row['editorial_decision']=='retain-wording':assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    sample=read(doc['representative_proof']);visual=read(doc['postscene_native_state_proof'])
    actual_paths=[p for p in sample['evidence'] if p.endswith('actual_all33_unforced_predicate_paths_effects_C200_and_end.json')]
    assert len(actual_paths)==1;actual=read(actual_paths[0])
    assert not actual['failures'] and not actual['paired_region_differences'] and actual['complete_matching_observations']==32
    assert actual['offline_only_display_IDs']==sample['offline_only_display_IDs']==offline
    assert len(actual['versions'])==2 and [v['fixture_exit_frame'] for v in actual['versions']]==[10776,10774]
    for version in actual['versions']:
        assert version['frames']==16001 and version['unforced_predicate_result']==0 and len(version['selected_B22_command_pairs'])==51
        assert version['single_source_end_offset']==2086 and version['selected_B22_command_pairs'][-1]['result_words']==[0,0]
        assert [r['original_source_offset'] for r in version['actual_source_A000s']]==[2068,2076]
        assert version['actual_source_C200'][0]['original_source_offset']==2084
        assert [r['original_source_offset'] for r in version['actual_source_relative_commands']]==[882,890]
        assert [r['source_offset'] for r in version['unvisited_declared_source_objects']]==[886,894,938]
    assert [v['actual_source_relative_commands'][1]['extent'] for v in actual['versions']]==[52,62]
    assert len(visual['all6_actual_sheets_viewed'])==6 and len(visual['paired_full_screen_views'])==6
    assert len(visual['all232_sampled_nontext_region_checks'])==232 and visual['all232_sampled_nontext_regions_equal']
    assert visual['whole_RGB_town10810_and_final16001_equal'] and all(visual['postscene16001_native_component_equality'].values())
    assert visual['postscene16001_whole1A04_actor_models_and_captain2_equal'] and visual['PRNG_equality_or_future_world_equivalence_not_claimed']
    assert visual['exact_timing_difference_counts']==dict(total=28,speech=20,control_or_end=8)
    assert visual['join_notice_full_RGB_difference_is_original_A_button_indicator']==[224,360,240,376]
    assert visual['join_notice10570_complete_shared_text_plane_equal'] and visual['join_notice_leading_J_full_Julian_Lopes_and_trailing_exclamation_viewed']
    scope=ledger['unfinished_editorial_scope_v4492'];oldscope=before['unfinished_editorial_scope_v4475']
    unchanged_outside(oldscope,scope,{'path','sha256'});assert scope['incomplete_route_source_prose']==33 and scope['remaining_B175_B180_physical_speeches']==90
    inventory,oldinventory=read(scope['path']),read(oldscope['path']);assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    unchanged_outside(oldinventory,inventory,{'next_focus','B174_reference_and_actual_coverage_v4492'})
    assert inventory['B174_reference_and_actual_coverage_v4492']==pending
    promoted=read('translations/promoted_build.json');assert promoted['profile']=='all-routes-unified-v4445'
    assert sha(Path(promoted['rom']).read_bytes())==promoted['rom_sha256']==doc['current_ROM_sha256']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4492')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4492',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5833,
        integrated=5800,pending=33,source_prose=5836,revised=3686,retained=2114,
        candidate=promoted['rom'],candidate_sha256=promoted['rom_sha256'],promoted_main_unchanged=True,
        all33_source_current_target_references_and10_retentions_verified=True,
        all45_commands_four_relative_sites20_native_cases132_stored_cases_C200_and_single_end_bound=True,
        actual32_complete_planes_two_unforced_result0_paths_two_effects_C200_and_town_return_verified=True,
        optional_Emilio_R69_and_unvisited886894938_offline_native_only=True,
        all6_actual_sheets_and6_full_screens_viewed=True,all232_nontext_regions_equal=True,
        source_and_English_relative_skip_extents52_and62_verified=True,
        join_notice_leading_J_full_name_and_trailing_exclamation_verified=True,
        postscene16001_five_native_components_and_whole_actor_scope_verified=True,
        every_prior_ledger_record_completion_and_full_objective_preserved=True,
        remaining_B175_B180_physical_speeches=90,new_source_prose_reviews=0,new_completed_records=0,
        new_emulator_runs=2,all_jobs_terminal=True,registered_release_and_startup_pending=True,
        full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4492 independently verified:33 reference-approved pending,32 actual/one offline;all old history/counts/full scope preserved. Main V4445 unchanged.')
