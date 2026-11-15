"""Independently audit sealed B176 coverage and every preserved ledger/scope value."""
import gzip
import json
from collections import Counter
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.checkpoint_lil_B176_references_v4591 import ROOT as CHECKPOINT,DOC,INPUT,APPROVAL,FAMILY
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4592')

def unchanged_outside(before,after,allowed):
    assert {k:v for k,v in before.items() if k not in allowed}=={k:v for k,v in after.items() if k not in allowed}

if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    before=json.loads(gzip.decompress((CHECKPOINT/'ledger.before.json.gz').read_bytes()))
    unchanged_outside(before,ledger,{'contextual_story_natural_dialogue_pass_v1871','active_source_prose_drafts','coverage_units',
        'unfinished_editorial_scope_v4591','lil_B176_reference_reconciliation_v4591','latest_checkpoint'})
    assert lp.read_bytes()==encode_ledger(ledger) and lp.stat().st_size<100*1024*1024
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5865,5878,3728,2137)
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];old=before['contextual_story_natural_dialogue_pass_v1871']
    unchanged_outside(old,fresh,{'pending_contextual_families','latest_contextual_manuscript','latest_pending_contextual_family','coverage_note'})
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5875,5865,10)
    doc,previous,approval=map(read,[DOC,INPUT,APPROVAL]);validate_natural_dialogue_batch(doc)
    assert len(doc['records'])==10 and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':5,'retain-wording':5}
    assert [r['english'] for r in doc['records']]==[r['english'] for r in previous['records']]
    ids=[r['id'] for r in doc['records']]
    assert approval['actual_sampled_display_IDs']==ids and not approval['offline_only_display_IDs']
    assert approval['manuscripts']=={str(DOC):sha(DOC.read_bytes())}
    assert len(fresh['pending_contextual_families'])==1;pending=fresh['pending_contextual_families'][0]
    assert pending['id']==FAMILY and pending['manuscript']==str(DOC) and pending['manuscript_sha256']==sha(DOC.read_bytes())
    assert pending['actual_sampled_display_IDs']==ids and not pending['offline_only_display_IDs']
    unchanged_outside(old['pending_contextual_families'][0],pending,{'manuscript','manuscript_sha256','manuscripts','pending',
        'actual_sampled_display_IDs','offline_only_display_IDs','new_emulator_runs','reference_approval','reference_approval_sha256'})
    a,b=before['active_source_prose_drafts'],ledger['active_source_prose_drafts']
    unchanged_outside(a,b,{'manuscripts','route_record_subsets_pending','status','note'})
    assert b['manuscripts']==a['manuscripts']+[str(DOC)]
    assert b['route_record_subsets_pending']=={**a['route_record_subsets_pending'],str(INPUT):[],str(DOC):ids}
    for a,b in zip(before['coverage_units'],ledger['coverage_units'],strict=True):
        if a['id']==FAMILY:
            unchanged_outside(a,b,{'manuscript','manuscript_sha256','manuscripts','pending','actual_sampled_display_IDs','offline_only_display_IDs',
                'new_emulator_runs','reference_approval','reference_approval_sha256','status','actual_new_cold_boot_runs','actual_complete_native_panels','registered_release_pending'})
            assert b['actual_sampled_display_IDs']==ids and b['actual_complete_native_panels']==10 and b['registered_release_pending']
        elif a['id']=='all-route-scenes':unchanged_outside(a,b,{'next'});assert (b['reviewed_route_records'],b['completed_route_records'])==(4276,4266)
        else:assert a==b
    scope=ledger['unfinished_editorial_scope_v4591'];oldscope=before['unfinished_editorial_scope_v4573']
    unchanged_outside(oldscope,scope,{'path','sha256'});assert scope['incomplete_route_source_prose']==10 and scope['remaining_B177_B180_physical_speeches']==48
    inventory,oldinventory=read(scope['path']),read(oldscope['path']);assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    unchanged_outside(oldinventory,inventory,{'next_focus','B176_reference_and_actual_coverage_v4591'})
    mapping,sample,stored,control,ends,visual=[read(doc[k]) for k in ['reference_map','representative_proof','final_padding_proof',
        'relocated_control_proof','termination_decode_proof','postscene_native_state_proof']]
    for key in ['reference_map','representative_proof','final_padding_proof','relocated_control_proof','termination_decode_proof','postscene_native_state_proof','native_font_proof']:
        assert sha(Path(doc[key]).read_bytes())==doc[key+'_sha256']
    for p,h in approval['evidence'].items():assert sha(Path(p).read_bytes())==h,p
    assert sample['actual_sampled_display_IDs']==sample['represented_reviewed_display_IDs']==ids and not sample['offline_only_display_IDs']
    assert len(mapping['blocks'])==1 and mapping['external_references_complete']
    block=mapping['blocks'][0];assert block['block']==176 and len(block['command_map'])==13 and len(block['text_records'])==10
    assert not block['relative_skip_fixups'] and not block['target_native_skip_cases']
    assert [(e['source_offset'],e['target_offset']) for e in block['original_declared_end_word_maps']]==[(386,400)]
    source=IlnkContainer.parse(NdsImage.open(doc['current_ROM']).read_file('/data/SC2.DK4')).blocks[176]
    target=Path(block['research_block']).read_bytes()
    assert sha(source)==block['source_block_sha256'] and sha(target)==block['target_block_sha256']
    assert (len(source),len(target))==(392,404)
    for row,final in zip(doc['records'],block['text_records'],strict=True):
        assert row['id']==final['id'] and row['actual_B22_display_fixture_observed'] and not row['current_native_UI_body_explicit_unexecuted_boundary']
        raw=bytes.fromhex(row['current_hex']);at=row['current_reference']['offset']
        assert source[at:at+len(raw)]==raw and source[at+len(raw)]==0
        value=bytes.fromhex(final['target_hex']);at=final['new_offset'];assert target[at:at+len(value)]==value and target[at+len(value)]==0
        if row['editorial_decision']=='retain-wording':
            assert row['fresh_retained_wording_justification'] and row['english'].split('}',1)[1]==row['effective_predecessor_paragraph']
    assert (stored['current_final_stored_macro_alignment_cases'],stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(40,16,24)
    assert len(control['relocated_dispatch_cases'])==10 and sum(r['resolved_actor_ID'] is None for r in control['relocated_dispatch_cases'])==1
    assert len(control['all3_source_current_target_nonrelative_nonspeech_leaves'])==3 and len(control['relocated_C200_pairs'])==1
    assert len(ends['cases'])==2 and all(c['native_result']==[0]*6 and c['native_extent']==4 and not c['post_logical_payload_reads'] for c in ends['cases'])
    assert len(visual['all2_actual_sheets_viewed'])==2 and all(s['viewed'] for s in visual['all2_actual_sheets_viewed'])
    assert len(visual['paired_full_screen_views'])==2 and all(s['viewed'] for s in visual['paired_full_screen_views'])
    assert sum(len(s['frames'])*2 for s in visual['paired_full_screen_views'])==8
    assert len(visual['all115_sampled_nontext_region_checks'])==visual['nontext_equal_samples']==115
    assert not visual['nontext_difference_samples'] and not visual['actual_timing_differences']
    assert visual['all10_complete_held_planes_and_source_paired_regions_match'] and visual['source_A0008_C200384_single_end386_actually_executed']
    assert visual['all_sampled_whole_RGB_from5290_through9001_equal'] and visual['whole_RGB_final9001_equal']
    assert all(visual['postscene9001_native_component_equality'].values()) and visual['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert visual['PRNG_equality'] and visual['postscene9001_PRNG_seeds']==[403514907,403514907]
    assert visual['future_world_equivalence_and_full_RAM_equality_not_claimed']
    assert visual['all_content_jobs_terminal'] and all(r['exit_code']==0 for r in visual['reaped_tool_sessions'])
    assert visual['following_B120_offset606_in_progress_at_end_adds_no_editorial_credit']
    assert len(control['relocated_A000_structural_pairs'])==1
    receipt=read(CHECKPOINT/'checkpoint_receipt.json');assert receipt['ledger_sha256']==sha(lp.read_bytes())
    for p,h in {**receipt['evidence'],**receipt['preserved_release_files']}.items():assert sha(Path(p).read_bytes())==h,p
    for p,h in receipt['updated_files'].items():assert sha(Path(p).read_bytes())==h,p
    promoted=read('translations/promoted_build.json');assert promoted['profile']=='all-routes-unified-v4541'
    assert sha(Path(promoted['rom']).read_bytes())==promoted['rom_sha256']==ledger['current_integrated_candidate']['sha256']
    for f in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        assert Path('docs',f).read_text(encoding='utf-8').endswith((CHECKPOINT/(f+'.before')).read_text(encoding='utf-8').split('\n',1)[1])
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4591')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4591',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5875,integrated=5865,pending=10,
        source_prose=5878,revised=3728,retained=2137,new_source_prose_reviews=0,new_completed_records=0,
        all_prior_ledger_values_history_counts_and_wider_scope_preserved=True,all10_actual_and5_retained_prose_unchanged=True,
        all13_commands_single_end10_relocated_dispatches40_stored_cases_and2_end_decodes_bound=True,
        actual10_panels9_progressive1_impersonal_FE_A000_C200_single_end_and_town_return_approved=True,
        all115_nontext_samples_and_all22_command_timings_equal=True,
        final9001_whole_RGB_components_actor_captain_and_PRNG_equal=True,
        no_natural_event_eligibility_earned_state_earlier_location_full_RAM_future_world_or_hardware_claim=True,
        all_jobs_terminal=True,main_V4541_registry_builder_and_pins_preserved=True,full_goal_active=True,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('V4591 independently audited:ten actual/ref-approved pending;all history/counts/main V4541 preserved. Registered compiler/integration next.')
