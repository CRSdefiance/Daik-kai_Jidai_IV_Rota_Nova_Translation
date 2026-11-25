"""Compose the atomic B181 compiler from reviewed common,row and linear contracts."""
import re
from pathlib import Path
from scripts.seal_lil_B181_references_v4864 import FLAGS
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B181_compiler_tools_v4865')
OUT=Path('dk4tool/patch/lil_B181_editorial_v1.py')

def alter(text,changes):
    for key in changes:assert key in text,key
    return re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],text)

GATES='''    require(len(native['cases'])==10 and native['current_original_macro_alignment_calls']==80
        and native['complete_progressive_planes']==9 and native['complete_FE_logical_and_physical_planes']==1,'complete native consumers required')
    require(len(native['negative_controls'])==20 and all(r['rejected'] for r in native['negative_controls']),'source-consumer negatives required')
    approval=load(conf['native_approval'])
    require(len(approval['formatter_negatives'])==len(set(approval['formatter_negatives']))==28,'formatter negatives required')
    require(len(stored['final_target_parity_cases'])==10 and stored['current_final_stored_macro_alignment_cases']==40
        and stored['new_parity_macro_alignment_cases']==12 and stored['exact_byte_identical_reused_macro_alignment_cases']==28
        and stored['all10_final_targets_complete_native_planes_equal_reviewed_planes'],'complete stored proof required')
    require(len(controls['relocated_dispatch_cases'])==10 and len(controls['all3_source_current_target_nonrelative_nonspeech_leaves'])==3
        and len(controls['relocated_C200_pairs'])==len(controls['relocated_A000_structural_pairs'])==1,'complete relocated controls required')
    ui=controls['relocated_C200_pairs'][0]['cases']
    require(len(ui)==2 and all(r['source_owned_UI_request_words']==[1,2,13,0,0,0,1] for r in ui)
        and ui[0]['source_owned_UI_writes']==ui[1]['source_owned_UI_writes'],'isolated C200 ownership differs')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
        and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',392),('research',376)],'guarded end decodes required')
    require(names['approved_prose_names']=={'166':'Lady','167':'Lady','168':'Lady'}
        and {(r['consumer'],r['actor_ID']):r['text'] for r in names['native_six_consumer_cases']['rows']}=={
            (c,i):'Lady' for i in [166,167,168] for c in ['progressive-nameplate','full-catalogue']},'six original role consumers required')
    require(sample['all10_panels9_progressive1_FE_A000_C200_end_and_normal_parent_return_pass']
        and sample['original13_commands_and_single_declared_tail_endword_preserved'] and sample['no_B181_source_command_omitted']
        and sample['no_open_translation_specific_display_or_control_finding'] and not sample['offline_only_display_IDs'],'representative scope required')
    require(observed['all10_complete_held_planes_and_source_paired_regions_match']
        and observed['all10_speeches9_progressive1_impersonal_FE_actually_observed']
        and observed['nontext_equal_samples']==len(observed['all115_sampled_nontext_region_checks'])==115
        and not observed['nontext_difference_samples'] and observed['whole_RGB_final9001_equal'],'all actual panels/regions required')
    require(observed['exact_timing_difference_counts']==dict(total=0,speech=0,control_or_end=0) and not observed['actual_timing_differences']
        and observed['postscene9001_native_component_equality']==dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True)
        and observed['postscene9001_whole1A04_actor_models_and_captain2_equal'],'measured state/timing scope differs')
    require(observed['PRNG_equality'] and observed['postscene9001_PRNG_seeds']==[790984746,790984746]
        and observed['no_PRNG_causal_or_future_world_equivalence_claim'],'measured equal RNG scope required')
    require(not observed['sampled_postscene_whole_RGB_differences_unmasked'] and observed['all_sampled_postscene_whole_RGB_equal'],'postscene RGB evidence differs')
    require(len(observed['all2_actual_sheets_viewed'])==2 and len(observed['paired_full_screen_views'])==3
        and all(s['viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in observed['all2_actual_sheets_viewed']+observed['paired_full_screen_views'])
        and observed['actual_new_cold_boot_runs']==2 and observed['total_frames']==18002,'viewed current evidence required')
    actual=load(conf['actual_proof'])
    require(actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==10 and not actual['failures']
        and not actual['paired_region_differences'] and not actual['offline_only_display_IDs'],'two complete actual paths required')
    require(len(actual['versions'])==2 and [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[22,22]
        and [v['fixture_exit_frame'] for v in actual['versions']]==[5257,5257],'actual linear source paths differ')
    for v in actual['versions']:
        require(len(v['selected_intervals'])==10 and v['single_source_end392_actually_reached']
            and v['selected_B22_command_pairs'][-1]['result_words']==[0,0]
            and v['selected_B22_command_pairs'][-1]['original_source_offset']==392
            and len(v['source_A000'])==1 and v['source_A000'][0]['original_source_offset']==8
            and v['source_A000'][0]['word']==0xA000 and v['source_A000'][0]['extent']==8
            and v['source_C200']['original_source_offset']==390 and v['source_C200']['word']==0xC200
            and v['source_C200']['extent']==2 and v['source_C200']['UI_request_after']==[1,2,13,0,2,0,1],'actual source controls differ')
    require([{k:s[k] for k in ['path','sha256']} for s in approval['reviewed_sheets']]==native['review_sheets'],'native sheet approval differs')
    for s in approval['reviewed_sheets']:require(s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes())==s['sha256'],'native sheet view differs')
    for s in sample['viewed_actual_sheets']:require(s['viewed'] and s['review'] and sha(Path(s['path']).read_bytes())==s['sha256'],'actual sheet view differs')
'''

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    source=Path('dk4tool/patch/lil_B180_editorial_v4.py');old=source.read_text(encoding='utf-8')
    header=old[:old.index("    require(len(native['cases'])")];a=header.index('FLAGS=');b=header.index('\ndef load',a)
    header=header[:a]+'FLAGS='+repr(FLAGS)+'\n'+header[b:]
    header=alter(header,{'B180':'B181','SELECTORS={166,167,254}':'SELECTORS={166,167,168,254}'})
    a=old.index("    rows=doc['records']");b=old.index('    require(not macros',a)
    rows=alter(old[a:b],{'len(rows)==len(set(ids))==11':'len(rows)==len(set(ids))==10','eleven exact records':'ten exact records',
        "{'progressive':10,'system-FE':1}":"{'progressive':9,'system-FE':1}","{'revise':5,'retain-wording':6}":"{'revise':5,'retain-wording':5}",
        "mapping['blocks'][0]['block']==180":"mapping['blocks'][0]['block']==181",'[180]':'[181]',"row['block']==180":"row['block']==181",'block=180':'block=181'})
    linear_source=Path('dk4tool/patch/lil_B179_editorial_v1.py');linear=linear_source.read_text(encoding='utf-8');tail=linear[linear.index('    require(not macros'):]
    tail=alter(tail,{'end==512 and len(block)==512':'end==396 and len(block)==396','len(logical)==mapped(end)==496':'len(logical)==mapped(end)==380',
        'len(target)==496':'len(target)==380','len(commands)==16':'len(commands)==13',"sum(c['word']==0x4000 for c in commands)==14":"sum(c['word']==0x4000 for c in commands)==10",
        '==[(508,492)]':'==[(392,376)]',"exact=[(8,'00a0ffff01221da1'),(508,'00000000')]":"exact=[(8,'00a0ffff014913a1'),(390,'00c2'),(392,'00000000')]",
        'two exact leaves required':'three exact leaves required','==[0xA000,0]':'==[0xA000,0xC200,0]','[179]':'[181]','==[179]':'==[181]','block=179':'block=181',
        'relative_operands=0':'relative_operands=0','source_commands=16':'source_commands=13',
        'all14_progressive_impersonal_FE_speeches_no_macros_A000_and_single_end_no_C200_preserved':'all10_progressive_FE_speeches_no_macros_A000_C200_and_single_end_preserved',
        'actual_two_retained_B22_fixtures_115_regions_equal_8_timings_4_indicator_differences_and_equal_PRNG_disclosed_not_natural_source_activation':
        'actual_two_retained_B22_fixtures_115_regions_equal_zero_timing_or_RGB_differences_and_equal_PRNG_not_natural_activation'})
    text=header+GATES+rows+tail;compile(text,str(OUT),'exec');OUT.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(compiler=str(OUT),compiler_sha256=sha(OUT.read_bytes()),
        shared_and_row_source=str(source),shared_and_row_source_sha256=sha(source.read_bytes()),linear_source=str(linear_source),linear_source_sha256=sha(linear_source.read_bytes()),
        all_checks_precede_single_replace_file=True,source396_target380_commands13_speeches10_three_exact_leaves=True,
        no_registry_ROM_or_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Prepared atomic B181 compiler:ten reviewed rows,three exact leaves,current native and actual scope.')
