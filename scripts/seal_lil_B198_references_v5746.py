"""Seal all17 source/context/native/entry reviews with honest15-actual/two-offline coverage."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B198_research_v5732 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B198_reference_approval_v5746')
INPUT=Path('translations/lil_B198_editorial_manuscript_v5.json')
OUTPUT=Path('translations/lil_B198_editorial_manuscript_v6.json')
MAP=Path('translations/lil_B198_editorial_relocation_map_v1.json')
CENSUS=Path('work/analysis/lil_B198_reference_census_v5735/all37_commands8_relative_sites_and_shipped_entry_census.json')
CONTROL=Path('work/analysis/lil_B198_relocated_controls_v5737/all17_dispatches_two_predicate_pairs_one_picture_pair_and12_exact_leaves.json')
STORED=Path('work/analysis/lil_B198_stored_v5742/all17_final_stored_targets68_macro_cases_and_complete_planes.json')
ENDS=Path('work/analysis/lil_B198_ends_v5736/two_declared_end_decodes_and_all8_in_block_relative_destinations.json')
ACTUAL=Path('work/analysis/lil_B198_actual_v5743/fifteen_actual_panels_source_matched_controls_and_complete_native_holds.json')
VISUAL=Path('work/analysis/lil_B198_visual_approval_v5745/viewed17_native15_actual56_holds_three_paired_sheets_and_source_style11.json')
STYLE=Path('work/analysis/lil_B198_ellipsis_context_v5740c/original_caller_style11_two_CP932_pauses_and_ASCII_control.json')
FLAGS=['all37_commands_and8_relative_sites_verified','all17_speech_targets_and12_control_leaves_preserved',
    'eleven_progressive_six_null_actor_FE_no_macros_preserved','all544_predecessor_bytes_restored_by_inverse_zero_tailzeros',
    'original_story_style11_complete_native_CP932_pause_reference_bound',
    'fifteen_actual_panels56_holds_and_two_offline_conditional_speeches_scope_explicit',
    'original_predicates_results_and_common_end_actual_verified','representative_shared_rules_approved']
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,MAP])
    doc=deepcopy(read(INPUT));plan,census,control,stored,ends,actual,visual,style=map(read,[PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,VISUAL,STYLE])
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    assert sha(ROM.read_bytes())==census['research_ROM_sha256']==control['research_ROM_sha256']==ends['research_ROM_sha256']
    assert plan['manuscript_sha256']==control['manuscript_sha256']==doc['prior_native_approval_manuscript_sha256']
    assert stored['manuscript_sha256']==sha(INPUT.read_bytes())
    assert not actual['failures'] and not actual['paired_region_differences']
    assert actual['actual_unique_speech_panels']==actual['complete_matching_observations']==15 and actual['complete_matching_holds']==56
    assert not actual['actual_timing_differences'] and not actual['later_whole_RGB_differences']
    assert visual['no_open_changed_scene_translation_display_or_control_finding']
    assert len(control['relocated_dispatch_cases'])==17 and len(control['original_unforced_predicate_pairs'])==2
    assert len(control['all12_source_current_target_control_leaves'])==12
    assert len(ends['cases'])==2 and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',540),('research',640)]
    assert style['source_explicit_style']==11 and all(r['exact_actual_ink'] and r['exact_actual_gray'] for r in style['cases'])
    ids=[r['id'] for r in actual['actual_panels']]
    offline=[r['id'] for r in doc['records'] if r['id'] not in ids]
    assert offline==['DK4_MES_B198_R0065','DK4_MES_B198_R0095']
    for key in ['all_current_native_sheets_viewed','all_actual_consumer_sheets_viewed','paired_full_screen_views']:
        assert len(visual[key])==3
        for s in visual[key]:assert s['viewed_in_full_current_turn'] and s['original_detail'] and sha(Path(s['path']).read_bytes())==s['sha256']
    paths=[INPUT,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,VISUAL,STYLE,Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    ROOT.mkdir(parents=True);sample=ROOT/'representative_display_control_and_transition_reconciliation.json'
    save(sample,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        actual_sampled_display_IDs=ids,offline_only_display_IDs=offline,actual_selected_B198_source_events=[],
        all37_source_commands_plus9_initializers_stored_without_omission=True,
        fifteen_actual_native_panels56_holds_and_two_offline_conditionals_explicit=True,
        six_FE_voice_panels_eleven_progressive_objects_no_macros_preserved=True,
        source_story_style11_binds_complete_CP932_pause_planes_without_ROM_change=True,
        original_predicate_results_and_single_source540_target640_end_and_return_preserved=True,
        source_matched_name_portrait_item_and_background_visibility_preserved=True,
        sampled_nontext_frames=182,command_timing_difference_count=0,later_sampled_whole_RGB_difference_count=0,
        source_and_English_return_frames=[6697,6697],final_13001_PRNG_seeds=[672702422,672702422],
        no_broad_world_effect_full_RAM_or_future_simulation_equivalence_claim=True,
        no_natural_event_activation_original_location_full_route_or_hardware_claim=True,
        no_open_translation_specific_display_or_control_finding=True,representative_shared_rules_approved=True,
        viewed_actual_sheets=visual['all_actual_consumer_sheets_viewed'],viewed_paired_full_screen_sheets=visual['paired_full_screen_views'],
        new_English_runs=1,new_English_frames=13001,reused_Japanese_runs=1,total_successful_frames=26002,
        registered_release_and_current_startup_pending=True,evidence=evidence,full_goal_complete=False))
    block=deepcopy(plan['blocks'][0]);checked=census['blocks'][0]
    assert block['block']==checked['block']==198 and len(block['command_map'])==37 and len(block['text_records'])==17
    assert (block['source_bytes'],block['source_logical_end'],block['research_bytes'],block['research_logical_end'])==(544,544,644,644)
    assert len(block['relative_skip_fixups'])==8 and len(block['target_native_skip_cases'])==40
    assert not block['choice_commands'] and not block['actor_style_commands']
    assert block['inverse_plus_original_zero_tailzeros_recovers_every_stored_source_byte']
    block['target_block_sha256']=block.pop('research_block_sha256')
    block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],
        external_entry_and_actual_revised_paths_approval_pending=False,individual_naturally_selected_source_scene_unobserved=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=offline)
    mapping=dict(format='dk4-lil-B198-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(NdsImage.open(PARENT).read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],**{f:True for f in FLAGS},
        actual_sampled_display_IDs=ids,offline_only_display_IDs=offline,representative_proof=str(sample),source_plan=str(PLAN),source_census=str(CENSUS),
        final_padding_proof=str(STORED),relocated_control_proof=str(CONTROL),termination_decode_proof=str(ENDS),postscene_native_state_proof=str(VISUAL),
        source_original_progressive_style_proof=str(STYLE),evidence={**evidence,str(sample):sha(sample.read_bytes())},
        actual_selected_B198_source_events=[],full_goal_complete=False)
    save(MAP,mapping)
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map_pending=False,
        registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for key,p in [('reference_map',MAP),('representative_proof',sample),('final_padding_proof',STORED),('relocated_control_proof',CONTROL),
        ('termination_decode_proof',ENDS),('postscene_native_state_proof',VISUAL),('source_original_progressive_style_proof',STYLE)]:
        doc[key],doc[key+'_sha256']=str(p),sha(p.read_bytes())
    for r in doc['records']:
        observed=r['id'] in ids
        r.update(status=doc['status'],current_text_hex=r['current_hex'],actual_B22_display_fixture_observed=observed,
            offline_only_native_display_checked=not observed,current_complete_native_display_pending=False,
            individual_actual_source_event_activation_not_claimed=True,
            current_native_UI_body_explicit_unexecuted_boundary=not observed,
            native_display_consumer='original_null_actor_FE_24310_then5473C' if r['kind']=='system-FE' else 'original_progressive_54020')
    assert all(all(r['review'].values()) for r in doc['records']);validate_natural_dialogue_batch(doc);save(OUTPUT,doc)
    save(ROOT/'reference_approval.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        all17_source_native_reference_and_representative_rules_approved=True,source_prose_English_and_compiled_targets_unchanged=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=offline,source_story_style11_and_retained_CP932_pauses_bound=True,
        native_approved_revisions=12,native_approved_retentions=5,all_prior_evidence_and_initial_failures_preserved=True,
        registered_release_and_current_startup_pending=True,evidence=evidence,new_editorial_credit=0,full_goal_complete=False))
    print('B198 sealed17 objects:12 revisions/five retentions;15 actual panels/56holds,two conditional speeches offline. Source-correct style11 and normal return pass;atomic compiler/registered release next.')
