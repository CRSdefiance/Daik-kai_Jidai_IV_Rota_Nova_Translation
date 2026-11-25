"""Audit B177's frozen source/actual approval across the subsequent main promotion."""
from collections import Counter
import gzip
import json
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.checkpoint_lil_B177_references_v4641 import ROOT as CHECKPOINT,DOC,INPUT,APPROVAL,FAMILY
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.promote_v4595_checkpoint_v4651b import AUDIT as PROMOTION,validate_plan,same_except
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4652')


if __name__=='__main__':
    assert not ROOT.exists()
    plan=validate_plan(True)
    frozen_index=next(i for i,r in enumerate(plan) if r['target']=='translations/editorial_review_current_v1.json')
    frozen_bytes=(PROMOTION/f'{frozen_index}.before').read_bytes();frozen=json.loads(frozen_bytes)
    current=read('translations/editorial_review_current_v1.json')
    same_except(frozen,current,{'latest_checkpoint','promoted_main_build_v4651'})
    assert Path('translations/editorial_review_current_v1.json').read_bytes()==encode_ledger(current)
    before=json.loads(gzip.decompress((CHECKPOINT/'ledger.before.json.gz').read_bytes()))
    same_except(before,frozen,{'contextual_story_natural_dialogue_pass_v1871','active_source_prose_drafts','coverage_units',
        'unfinished_editorial_scope_v4641','lil_B177_reference_reconciliation_v4641','latest_checkpoint'})
    assert tuple(current[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass',
        'records_revised_and_integrated','retained_wordings_editorially_completed'])==(5875,5888,3733,2142)
    fresh=frozen['contextual_story_natural_dialogue_pass_v1871'];old=before['contextual_story_natural_dialogue_pass_v1871']
    same_except(old,fresh,{'pending_contextual_families','latest_contextual_manuscript','latest_pending_contextual_family','coverage_note'})
    assert tuple(fresh[k] for k in ['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated',
        'fresh_pass_records_pending_native_actual_release'])==(5885,5875,10)
    doc,previous,approval=map(read,[DOC,INPUT,APPROVAL]);validate_natural_dialogue_batch(doc)
    ids=[r['id'] for r in doc['records']]
    assert len(set(ids))==10 and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':5,'retain-wording':5}
    assert [r['english'] for r in doc['records']]==[r['english'] for r in previous['records']]
    assert approval['manuscripts']=={str(DOC):sha(DOC.read_bytes())}
    assert approval['actual_sampled_display_IDs']==ids and not approval['offline_only_display_IDs']
    assert len(fresh['pending_contextual_families'])==1
    pending=fresh['pending_contextual_families'][0]
    assert pending['id']==FAMILY and pending['manuscript']==str(DOC) and pending['manuscript_sha256']==sha(DOC.read_bytes())
    same_except(old['pending_contextual_families'][0],pending,{'manuscript','manuscript_sha256','manuscripts','pending',
        'actual_sampled_display_IDs','offline_only_display_IDs','new_emulator_runs','reference_approval','reference_approval_sha256'})
    a,b=before['active_source_prose_drafts'],frozen['active_source_prose_drafts']
    same_except(a,b,{'manuscripts','route_record_subsets_pending','status','note'})
    assert b['manuscripts']==a['manuscripts']+[str(DOC)]
    assert b['route_record_subsets_pending']=={**a['route_record_subsets_pending'],str(INPUT):[],str(DOC):ids}
    for a,b in zip(before['coverage_units'],frozen['coverage_units'],strict=True):
        if a['id']==FAMILY:
            same_except(a,b,{'manuscript','manuscript_sha256','manuscripts','pending','actual_sampled_display_IDs','offline_only_display_IDs',
                'new_emulator_runs','reference_approval','reference_approval_sha256','status','actual_new_cold_boot_runs','actual_complete_native_panels','registered_release_pending'})
            assert b['actual_sampled_display_IDs']==ids and b['actual_complete_native_panels']==10 and b['registered_release_pending']
        elif a['id']=='all-route-scenes':
            same_except(a,b,{'next'});assert (b['reviewed_route_records'],b['completed_route_records'])==(4286,4276)
        else:assert a==b
    scope=frozen['unfinished_editorial_scope_v4641'];oldscope=before['unfinished_editorial_scope_v4623']
    same_except(oldscope,scope,{'path','sha256'})
    inventory=read(scope['path']);assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    same_except(read(oldscope['path']),inventory,{'next_focus','B177_reference_and_actual_coverage_v4641'})
    assert scope['incomplete_route_source_prose']==10 and scope['remaining_B178_B180_physical_speeches']==38
    for key in ['reference_map','representative_proof','final_padding_proof','relocated_control_proof','termination_decode_proof',
        'postscene_native_state_proof','native_font_proof']:
        assert sha(Path(doc[key]).read_bytes())==doc[key+'_sha256']
    for p,h in approval['evidence'].items():assert sha(Path(p).read_bytes())==h,p
    mapping,sample,stored,control,ends,visual=[read(doc[k]) for k in ['reference_map','representative_proof','final_padding_proof',
        'relocated_control_proof','termination_decode_proof','postscene_native_state_proof']]
    assert sample['actual_sampled_display_IDs']==sample['represented_reviewed_display_IDs']==ids and not sample['offline_only_display_IDs']
    assert len(mapping['blocks'])==1 and mapping['external_references_complete']
    block=mapping['blocks'][0]
    assert block['block']==177 and len(block['command_map'])==13 and len(block['text_records'])==10
    assert not block['relative_skip_fixups'] and not block['target_native_skip_cases']
    assert [(r['source_offset'],r['target_offset']) for r in block['original_declared_end_word_maps']]==[(482,466)]
    source=IlnkContainer.parse(NdsImage.open(doc['current_ROM']).read_file('/data/SC2.DK4')).blocks[177]
    target=Path(block['research_block']).read_bytes()
    assert (len(source),len(target))==(488,472)
    assert sha(source)==block['source_block_sha256'] and sha(target)==block['target_block_sha256']
    for row,final in zip(doc['records'],block['text_records'],strict=True):
        assert row['id']==final['id'] and row['actual_B22_display_fixture_observed'] and not row['current_native_UI_body_explicit_unexecuted_boundary']
        raw=bytes.fromhex(row['current_hex']);at=row['current_reference']['offset']
        assert source[at:at+len(raw)]==raw and source[at+len(raw)]==0
        raw=bytes.fromhex(final['target_hex']);at=final['new_offset']
        assert target[at:at+len(raw)]==raw and target[at+len(raw)]==0
        if row['editorial_decision']=='retain-wording':
            assert row['fresh_retained_wording_justification'] and row['english'].split('}',1)[1]==row['effective_predecessor_paragraph']
    assert tuple(stored[k] for k in ['current_final_stored_macro_alignment_cases','new_parity_macro_alignment_cases',
        'exact_byte_identical_reused_macro_alignment_cases'])==(40,24,16)
    assert len(control['relocated_dispatch_cases'])==10 and sum(r['resolved_actor_ID'] is None for r in control['relocated_dispatch_cases'])==1
    assert len(control['all3_source_current_target_nonrelative_nonspeech_leaves'])==3
    assert len(control['relocated_C200_pairs'])==len(control['relocated_A000_structural_pairs'])==1
    assert len(ends['cases'])==2 and all(c['native_result']==[0]*6 and c['native_extent']==4 and not c['post_logical_payload_reads'] for c in ends['cases'])
    assert len(visual['all2_actual_sheets_viewed'])==2 and all(s['viewed'] for s in visual['all2_actual_sheets_viewed'])
    assert len(visual['paired_full_screen_views'])==3 and all(s['viewed'] for s in visual['paired_full_screen_views'])
    assert sum(len(s['frames'])*2 for s in visual['paired_full_screen_views'])==12
    assert len(visual['all115_sampled_nontext_region_checks'])==visual['nontext_equal_samples']==115 and not visual['nontext_difference_samples']
    assert len(visual['actual_timing_differences'])==11 and visual['exact_timing_difference_counts']=={'total':11,'speech':9,'control_or_end':2}
    assert len(visual['fourteen_following_A_button_indicator_animation_differences_retained_unmasked'])==14
    assert visual['fourteen_following_indicator_differences_viewed_in_representative_full_screens_and_retained']
    assert visual['all10_complete_held_planes_and_source_paired_regions_match'] and visual['source_A0008_C200480_single_end482_actually_executed']
    assert visual['whole_RGB_town5290_through5950_and_final9001_equal'] and visual['whole_RGB_final9001_equal']
    assert all(visual['postscene9001_native_component_equality'].values()) and visual['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert not visual['PRNG_equality'] and visual['postscene9001_PRNG_seeds']==[463267532,403514907]
    assert visual['fixture_return_frames']==[5255,5257] and visual['no_new_PRNG_causal_trace']
    assert visual['future_world_equivalence_and_full_RAM_equality_not_claimed']
    assert visual['all_content_jobs_terminal'] and all(r['exit_code']==0 for r in visual['reaped_tool_sessions'])
    assert visual['following_B120_offset606_in_progress_at_end_adds_no_editorial_credit']
    receipt=read(CHECKPOINT/'checkpoint_receipt.json');assert receipt['ledger_sha256']==sha(frozen_bytes)
    for p,h in receipt['evidence'].items():assert sha(Path(p).read_bytes())==h,p
    promoted=read('translations/promoted_build.json');candidate=current['current_integrated_candidate']
    assert promoted['profile']==candidate['profile']=='all-routes-unified-v4595'
    assert sha(Path(promoted['rom']).read_bytes())==promoted['rom_sha256']==candidate['sha256']
    assert current['goal_status']=='active' and not current['full_goal_complete']
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4651',reference_checkpoint='V4641',ledger_sha256=sha(Path('translations/editorial_review_current_v1.json').read_bytes()),
        fresh_reread=5885,integrated=5875,pending=10,source_prose=5888,revised=3733,retained=2142,
        all_prior_ledger_values_nested_history_and_wider_scope_preserved=True,all10_actual_and5_retained_prose_unchanged=True,
        source488_to472_all13_commands10_relocated_dispatches40_stored_cases_and2_end_decodes_bound=True,
        all115_upper_portrait_name_samples_equal=True,eleven_command_timing_differences_retained=True,
        fourteen_A_indicator_RGB_differences_retained_unmasked=True,five_components_actor_captain_and_town_final_RGB_equal=True,
        unequal_PRNG_seeds=[463267532,403514907],no_full_RAM_future_world_hardware_or_new_causal_trace_claim=True,
        all_jobs_terminal=True,main_V4595_verified=True,full_goal_active=True,full_goal_complete=False,
        evidence={str(DOC):sha(DOC.read_bytes()),str(APPROVAL):sha(APPROVAL.read_bytes())},producer_sha256=sha(Path(__file__).read_bytes())))
    print('V4652 independent audit:ten B177 actual/reference-approved pending;all history and measured timing/indicator/PRNG limits retained. Main V4595 verified.')
