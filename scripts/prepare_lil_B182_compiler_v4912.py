"""Freeze the conditional B182 compiler with exact scratch, display and actual scope."""
from pathlib import Path
import re
from scripts.seal_lil_B182_references_v4909b import FLAGS
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B182_compiler_tools_v4912')
OUT=Path('dk4tool/patch/lil_B182_editorial_v1.py')
GATES='''    require(len(native['cases'])==8 and native['current_original_macro_alignment_calls']==64
        and native['complete_progressive_planes']==7 and native['complete_FE_logical_and_physical_planes']==1,'complete native consumers required')
    require(len(native['negative_controls'])==18 and all(r['rejected'] for r in native['negative_controls']),'source-consumer negatives required')
    approval=load(conf['native_approval'])
    require(len(approval['formatter_negatives'])==len(set(approval['formatter_negatives']))==28
        and all(isinstance(r,str) and r for r in approval['formatter_negatives']),'formatter negatives required')
    require(len(stored['final_target_parity_cases'])==8 and stored['current_final_stored_macro_alignment_cases']==32
        and stored['new_parity_macro_alignment_cases']==16 and stored['exact_byte_identical_reused_macro_alignment_cases']==16
        and stored['all8_final_targets_complete_native_planes_equal_reviewed_planes'],'complete stored proof required')
    require(len(controls['relocated_dispatch_cases'])==8 and len(controls['all7_exact_nonrelative_leaves'])==7
        and len(controls['predicate_pairs'])==2 and len(controls['C200_pairs'])==1 and len(controls['A000_structural_pairs'])==3
        and len(controls['all25_source_and_relocated_structural_paths_identical'])==25,'complete relocated controls required')
    require([(p['old_offset'],p['new_offset']) for p in controls['predicate_pairs']]==[(512,530),(544,562)],'exact predicate sites required')
    for pair in controls['predicate_pairs']:
        require(len(pair['cases'])==2 and pair['old_offset']%4==0 and pair['new_offset']%4==2,'source predicate alignment differs')
        a,b=pair['cases'];require(a['native_result']==b['native_result'] and a['after_seed']==b['after_seed'],'predicate pair differs')
        require(all(r['unforced_current_snapshot'] and r['full4MiB_difference_exactly_original_owned_RNG_and_optional_operand_scratch'] for r in pair['cases']),'original RNG and operand ownership required')
        require(not a['operand_pointer_unaligned'] and b['operand_pointer_unaligned']
            and not a['unaligned_operand_scratch_writes']
            and b['unaligned_operand_scratch_writes']==[dict(PC=0x0202A5D8,address=0x02279600,size=4,value=500)],'original operand scratch differs')
    ownership=load(conf['operand_ownership_proof'])
    require(len(ownership['cases'])==24 and ownership['unforced_cases']==6 and ownership['CPU_only_boundary_fixture_cases']==18
        and ownership['actual_emulator_seed_writes']==0,'complete operand alignment proof required')
    require(Counter(r['version'] for r in ownership['cases'])=={'clean':8,'current':8,'relocated':8}
        and sum(r['operand_pointer_unaligned'] for r in ownership['cases'])==8,'aligned and unaligned coverage required')
    require({(r['version'],r['offset'],r['supplied_CPU_only_seed_fixture']) for r in ownership['cases']}=={
        (version,at,fixture) for version,sites in [('clean',[512,544]),('current',[512,544]),('relocated',[530,562])]
        for at in sites for fixture in {r['supplied_CPU_only_seed_fixture'] for r in ownership['cases']}},'operand coverage keys differ')
    for r in ownership['cases']:
        expected_seed=(r['before_seed']*0x41C64E6D+0x3039)&0xFFFFFFFF
        roll=((expected_seed>>16)&0x7FFF)%1000;result=0 if roll<500 else 1 if roll==500 else 2
        writes=([dict(PC=0x0202A5D8,address=0x02279600,size=4,value=500)] if r['operand_pointer_unaligned'] else [])
        writes.append(dict(PC=0x020D984C,address=0x02168EB8,size=4,value=expected_seed))
        require(r['after_seed']==expected_seed and r['roll']==roll and r['native_result']==[2,result,0,0,0,0]
            and r['bound']==1000 and r['threshold']==500 and r['all_original_native_writes']==writes
            and r['full4MiB_difference_exactly_original_owned_RNG_and_optional_operand_scratch']
            and r['cleanup_restores_only_owned_seed_and_optional_scratch_and_recovers_all4MiB'],'exact native ownership differs')
    require({r['roll'] for r in ownership['cases'] if not r['unforced_current_snapshot']}=={499,500,501},'three threshold boundaries required')
    ui=controls['C200_pairs'][0]['cases']
    require(len(ui)==2 and all(r['source_owned_UI_request_words']==[1,2,13,0,0,0,1] for r in ui)
        and ui[0]['source_owned_UI_writes']==ui[1]['source_owned_UI_writes'],'isolated C200 source ownership differs')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
        and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',632),('research',648)],'guarded end decodes required')
    require(names['approved_prose_names']=={'166':'Lady','167':'Lady'}
        and {(r['consumer'],r['actor_ID']):r['text'] for r in names['native_four_consumer_cases']['rows']}=={
            (c,i):'Lady' for i in [166,167] for c in ['progressive-nameplate','full-catalogue']},'four original role consumers required')
    require(sample['all8_panels_seven_progressive_one_FE_selected_effect_C200_end_and_parent_return_pass']
        and sample['source_all25_commands_ten_branches_two_predicates_three_alternative_effects_preserved']
        and sample['actual_conditional_paths_verified_without_forcing_same_outcome']
        and sample['original_scene_RNG_outcome_equal_final_RNG_and_timing_indicator_differences_disclosed']
        and sample['no_open_translation_specific_display_or_control_finding'] and not sample['offline_only_display_IDs'],'representative scope required')
    require(observed['all8_complete_held_planes_and_source_paired_regions_match']
        and observed['all8_speeches7_progressive1_impersonal_FE_actually_observed']
        and observed['nontext_equal_samples']==len(observed['all115_sampled_nontext_region_checks'])==115
        and not observed['nontext_difference_samples'] and observed['whole_RGB_final9001_equal'],'all actual panels/regions required')
    require(observed['exact_timing_difference_counts']==dict(total=13,speech=7,control_or_end=6)
        and len(observed['actual_timing_differences'])==13
        and observed['postscene9001_native_component_equality']==dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True)
        and observed['postscene9001_whole1A04_actor_models_and_captain2_equal'],'measured state/timing limits required')
    require(observed['PRNG_equality'] is False and observed['postscene9001_PRNG_seeds']==[3723009301,403514907]
        and observed['no_PRNG_causal_trace_or_future_world_equivalence_claim'],'unequal final RNG observations must stay disclosed')
    require(len(observed['sampled_postscene_whole_RGB_differences_unmasked'])==18
        and all(r['whole_frame_difference_bbox']==[224,360,240,376] for r in observed['sampled_postscene_whole_RGB_differences_unmasked'])
        and observed['measured_timing_RGB_and_final_RNG_differences_retained_without_equivalence_claim'],'unmasked indicator differences required')
    require(len(observed['all_actual_consumer_sheets_viewed'])==2 and len(observed['paired_full_screen_views'])==12
        and all(s['viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in observed['all_actual_consumer_sheets_viewed']+observed['paired_full_screen_views'])
        and observed['actual_new_cold_boot_runs']==2 and observed['total_frames']==18002,'viewed current evidence required')
    actual=load(conf['actual_proof'])
    require(actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==8
        and not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_display_IDs'],'two complete actual paths required')
    require(len(actual['versions'])==2 and [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[23,23]
        and [v['fixture_exit_frame'] for v in actual['versions']]==[4776,4775]
        and actual['observed_random_path_difference']['original_effects_by_case']==dict(clean_Japanese=[532],reviewed_English=[532]),'original conditional paths differ')
    for version in actual['versions']:
        require(len(version['selected_intervals'])==8 and version['single_source_end632_actually_reached']
            and version['selected_B22_command_pairs'][-1]['result_words']==[0,0]
            and version['selected_B22_command_pairs'][-1]['original_source_offset']==632
            and len(version['source_A000'])==len(version['source_C200'])==1
            and version['source_A000'][0]['word']==0xA000 and version['source_A000'][0]['original_source_offset']==532
            and version['source_C200'][0]['word']==0xC200 and version['source_C200'][0]['original_source_offset']==630
            and version['source_C200'][0]['UI_request_after']==[1,2,13,0,2,0,1],'actual source controls differ')
        require(len(version['actual_predicate_transitions'])==1 and all(
            (r['source_offset'],r['roll'],r['result'])==(512,52,0) and r['actual_unforced_original_LCG_transition']
            for r in version['actual_predicate_transitions']),'actual unforced predicate differs')
    require([{k:s[k] for k in ['path','sha256']} for s in approval['reviewed_sheets']]==native['review_sheets'],'native sheet approval binding differs')
    for sheet in approval['reviewed_sheets']:
        require(sheet['viewed_in_full_current_turn'] and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'native sheet view differs')
    for sheet in sample['viewed_actual_sheets']:
        require(sheet['viewed'] and sheet['review'] and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'actual sheet view differs')
'''

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    source=Path('dk4tool/patch/lil_B180_editorial_v4.py');old=source.read_text(encoding='utf-8')
    a=old.index("    require(len(native['cases'])");b=old.index("    rows=doc['records']",a)
    text=old[:a]+GATES+old[b:]
    a=text.index('FLAGS=');b=text.index('\ndef load',a);text=text[:a]+'FLAGS='+repr(FLAGS)+'\n'+text[b:]
    changes={
        'B180':'B182','len(rows)==len(set(ids))==11':'len(rows)==len(set(ids))==8','eleven exact records':'eight exact records',
        "{'progressive':10,'system-FE':1}":"{'progressive':7,'system-FE':1}",
        "{'revise':5,'retain-wording':6}":"{'revise':6,'retain-wording':2}",
        "mapping['blocks'][0]['block']==180":"mapping['blocks'][0]['block']==182",'[180]':'[182]',
        "row['block']==180":"row['block']==182",'block=180':'block=182',
        "end <= len(block) and not any(block[end:])":"end == len(block) == 636 and not any(block[end:])",
        '[460, 464, 468, 480, 492, 496, 500, 512, 524, 528]':'[520, 524, 528, 540, 552, 556, 560, 572, 584, 588]',
        'len(logical)==mapped(end)<0x2400':'len(logical)==mapped(end)==652<0x2400',
        "len(commands) == 28 and sum(command['word'] == 0x4000 for command in commands) == 11":
        "len(commands) == 25 and sum(command['word'] == 0x4000 for command in commands) == 8",
        "[c['old_offset'] for c in stops]==[572] and len(stops)==1 and stops[0]['new_offset']==542":
        "[c['old_offset'] for c in stops]==[632] and len(stops)==1 and stops[0]['new_offset']==648",
        'target[542:546]':'target[648:652]',
        "exact=[(452,'0080fffff4010000'),(472,'00a0ffff013d0ba1'),(484,'0080fffff4010000'),\n        (504,'00a0ffff013b0ba1'),(516,'00a0ffff013c0ba1'),(570,'00c2'),(572,'00000000')]":
        "exact=[(512,'0080fffff4010000'),(532,'00a0ffff014700a1'),(544,'0080fffff4010000'),\n        (564,'00a0ffff014800a1'),(576,'00a0ffff014600a1'),(630,'00c2'),(632,'00000000')]",
        'source_commands=28':'source_commands=25','all11_progressive_FE_speeches':'all8_progressive_FE_speeches'}
    for k in changes:assert k in text,k
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],text)
    compile(text,str(OUT),'exec');OUT.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(compiler=str(OUT),compiler_sha256=sha(OUT.read_bytes()),
        conditional_source=str(source),conditional_source_sha256=sha(source.read_bytes()),
        source636_target652_commands25_speeches8_ten_relative_sites_and7_leaves=True,
        exact_original_optional_scratch_and_seed_ownership_bound=True,all_checks_precede_single_replace_file=True,
        no_registry_ROM_or_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Prepared atomic B182 compiler:8 reviewed rows,25 commands,10 relative sites,exact optional scratch/RNG ownership and measured actual scope.')
