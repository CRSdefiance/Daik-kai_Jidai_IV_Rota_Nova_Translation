"""Compose B180's atomic compiler from reviewed row and conditional-map contracts."""
import re
from pathlib import Path
from scripts.seal_lil_B180_references_v4816 import FLAGS
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B180_compiler_tools_v4819')
OUT=Path('dk4tool/patch/lil_B180_editorial_v1.py')

def alter(text,changes):
    for old in changes:assert old in text,old
    return re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],text)

GATES='''    require(len(native['cases'])==11 and native['current_original_macro_alignment_calls']==88
        and native['complete_progressive_planes']==10 and native['complete_FE_logical_and_physical_planes']==1,'complete native consumers required')
    require(len(native['negative_controls'])==18 and all(r['rejected'] for r in native['negative_controls']),'source-consumer negatives required')
    approval=load(conf['native_approval'])
    require(len(approval['formatter_negatives'])==28 and all(r['rejected'] for r in approval['formatter_negatives']),'formatter negatives required')
    require(len(stored['final_target_parity_cases'])==11 and stored['current_final_stored_macro_alignment_cases']==44
        and stored['new_parity_macro_alignment_cases']==20 and stored['exact_byte_identical_reused_macro_alignment_cases']==24
        and stored['all11_final_targets_complete_native_planes_equal_reviewed_planes'],'complete stored proof required')
    require(len(controls['relocated_dispatch_cases'])==11 and len(controls['all7_exact_nonrelative_leaves'])==7
        and len(controls['predicate_pairs'])==2 and len(controls['C200_pairs'])==1 and len(controls['A000_structural_pairs'])==3
        and len(controls['all25_source_and_relocated_structural_paths_identical'])==25,'complete relocated controls required')
    for pair in controls['predicate_pairs']:
        require(len(pair['cases'])==2 and pair['old_offset']%4==pair['new_offset']%4==0,'source predicate alignment differs')
        a,b=pair['cases'];require(a['native_result']==b['native_result'] and a['after_seed']==b['after_seed'],'predicate pair differs')
        require(all(r['unforced_current_snapshot'] and r['full4MiB_difference_exactly_one_original_owned_RNG_word'] for r in pair['cases']),'original RNG ownership required')
    ui=controls['C200_pairs'][0]['cases']
    require(len(ui)==2 and all(r['source_owned_UI_request_words']==[1,2,13,0,0,0,1] for r in ui)
        and ui[0]['source_owned_UI_writes']==ui[1]['source_owned_UI_writes'],'isolated C200 source ownership differs')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
        and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',572),('research',542)],'guarded end decodes required')
    require(names['approved_prose_names']=={'166':'Lady','167':'Lady'}
        and {(r['consumer'],r['actor_ID']):r['text'] for r in names['native_four_consumer_cases']['rows']}=={
            ('progressive-nameplate',166):'Lady',('full-catalogue',166):'Lady',
            ('progressive-nameplate',167):'Lady',('full-catalogue',167):'Lady'},'four original role consumers required')
    require(sample['all11_panels_ten_progressive_one_FE_selected_effect_C200_end_and_parent_return_pass']
        and sample['source_all28_commands_ten_branches_two_predicates_three_alternative_effects_preserved']
        and sample['actual_conditional_paths_verified_without_forcing_same_outcome']
        and sample['original_RNG_and_effect_state_difference_fully_disclosed_within_checked_scope']
        and sample['no_open_translation_specific_display_or_control_finding'] and not sample['offline_only_display_IDs'],'representative scope required')
    require(observed['all11_complete_held_planes_and_source_paired_regions_match']
        and observed['all11_speeches10_progressive1_impersonal_FE_actually_observed']
        and observed['nontext_equal_samples']==len(observed['all115_sampled_nontext_region_checks'])==115
        and not observed['nontext_difference_samples'] and observed['whole_RGB_final9001_equal'],'all actual panels/regions required')
    require(observed['exact_timing_difference_counts']==dict(total=12,speech=8,control_or_end=4)
        and len(observed['actual_timing_differences'])==12
        and observed['postscene9001_native_component_equality']==dict(state=True,models=True,persistent_objects=False,tasks=True,calendar=True)
        and observed['postscene9001_whole1A04_actor_models_and_captain2_equal'],'measured state/timing limits required')
    require(observed['PRNG_equality'] is False and observed['postscene9001_PRNG_seeds']==[2467799992,790984746]
        and observed['PRNG_or_future_world_equivalence_not_claimed'],'unequal original RNG outcomes must stay disclosed')
    require(len(observed['sampled_postscene_whole_RGB_differences_unmasked'])==12
        and all(r['whole_frame_difference_bbox']==[224,360,240,376] for r in observed['sampled_postscene_whole_RGB_differences_unmasked'])
        and observed['all12_following_indicator_differences_viewed_and_retained'],'unmasked indicator differences required')
    require(len(observed['all2_actual_sheets_viewed'])==2 and len(observed['paired_full_screen_views'])==9
        and all(s['viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in observed['all2_actual_sheets_viewed']+observed['paired_full_screen_views'])
        and observed['actual_new_cold_boot_runs']==4 and observed['total_frames']==30004,'viewed current evidence required')
    effect=load(observed['effect_boundary_proof'])
    require(sha(Path(observed['effect_boundary_proof']).read_bytes())==observed['effect_boundary_proof_sha256']
        and effect['both_pre_effect_all_four_persistent_arrays_byte_identical']
        and effect['final_town_difference_is_exact_observed_original_effect_value']
        and effect['no_unresolved_translation_specific_state_difference_within_checked_arrays'],'actual state difference must be resolved')
    require(effect['final9001_four_array_differences']=={
        'all207_actors_and_current_captain':[],'all90_towns':[dict(offset=1294,before=59,after=61)],
        'all218_items':[],'all124_goods_and_reserved_slot':[]},'exact original-effect state difference required')
    actual=load(conf['actual_proof'])
    require(actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==11
        and not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_display_IDs'],'two complete actual paths required')
    require(len(actual['versions'])==2 and [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[31,26]
        and [v['fixture_exit_frame'] for v in actual['versions']]==[5495,5496]
        and actual['observed_random_path_difference']['original_effects_by_case']==dict(clean_Japanese=[504],reviewed_English=[472]),'original conditional paths differ')
    for version in actual['versions']:
        require(len(version['selected_intervals'])==11 and version['single_source_end572_actually_reached']
            and version['selected_B22_command_pairs'][-1]['result_words']==[0,0]
            and version['selected_B22_command_pairs'][-1]['original_source_offset']==572
            and len(version['source_A000'])==len(version['source_C200'])==1
            and version['source_C200'][0]['UI_request_after']==[1,2,13,0,2,0,1],'actual source controls differ')
    for sheet in native['review_sheets']+sample['viewed_actual_sheets']:
        require((sheet.get('viewed') is True or sheet.get('viewed_in_full_current_turn') is True)
            and sheet['review'] and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'viewed sheet differs')
'''

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    row_source=Path('dk4tool/patch/lil_B179_editorial_v1.py');old=row_source.read_text(encoding='utf-8')
    header=old[:old.index("    require(len(native['cases'])")]
    a=header.index('FLAGS=');b=header.index('\ndef load',a)
    header=header[:a]+'FLAGS='+repr(FLAGS)+'\n'+header[b:]
    header=alter(header,{'lil_B179':'lil_B180','B179':'B180','SELECTORS={92,96,152,254}':'SELECTORS={166,167,254}',
        "doc['all14_five_review_gates_true']":"all(all(r['review'].values()) for r in doc['records'])"})
    a=old.index("    rows=doc['records']");b=old.index('    require(not macros',a)
    rows=alter(old[a:b],{'len(rows)==len(set(ids))==14':'len(rows)==len(set(ids))==11',
        'fourteen exact records':'eleven exact records',"{'progressive':13,'system-FE':1}":"{'progressive':10,'system-FE':1}",
        "{'revise':8,'retain-wording':6}":"{'revise':5,'retain-wording':6}",
        "mapping['blocks'][0]['block']==179":"mapping['blocks'][0]['block']==180",'[179]':'[180]',"row['block']==179":"row['block']==180",'block=179':'block=180'})
    cond_source=Path('dk4tool/patch/lil_B173_editorial_v1.py');cond=cond_source.read_text(encoding='utf-8')
    tail=cond[cond.index('    require(not macros'):]
    a=tail.index('    exact=');b=tail.index('    restored =',a)
    tail=tail[:a]+'''    exact=[(452,'0080fffff4010000'),(472,'00a0ffff013d0ba1'),(484,'0080fffff4010000'),
        (504,'00a0ffff013b0ba1'),(516,'00a0ffff013c0ba1'),(570,'00c2'),(572,'00000000')]
    require([(c['old_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==exact,'seven complete source leaves differ')
    require([c['word'] for c in leaves]==[0x8000,0xA000,0x8000,0xA000,0xA000,0xC200,0]
        and all(c['word'] not in [0x2000,0x2100,0x4100] for c in commands),'source predicate/effect/C200 scope differs')
'''+tail[b:]
    edges=read('translations/lil_B180_editorial_relocation_map_v1.json')['blocks'][0]['relative_skip_fixups']
    tail=alter(tail,{'len(edges)==4 and [e[\'offset\'] for e in edges]==[736,740,744,756]':
        'len(edges)==10 and [e[\'offset\'] for e in edges]=='+repr([e['offset'] for e in edges]),
        "len(spec['target_native_skip_cases'])==20":"len(spec['target_native_skip_cases'])==50",
        'len(commands) == 23':'len(commands) == 28',
        "[c['old_offset'] for c in stops]==[762]":"[c['old_offset'] for c in stops]==[572]",
        "stops[0]['new_offset']==794":"stops[0]['new_offset']==542",'target[794:798]':'target[542:546]',
        'new_blocks[173]':'new_blocks[180]','== [173]':'== [180]','block=173':'block=180',
        'relative_operands=4, source_commands=23':'relative_operands=10, source_commands=28',
        'all11_progressive_speeches_zero_macros_resources_predicate_relative_suffix_two_A000s_and8_leaves_preserved':
        'all11_progressive_FE_speeches_two_predicates_three_A000_C200_ten_relative_sites_and7_leaves_preserved'})
    result=header+GATES+rows+tail
    compile(result,str(OUT),'exec');OUT.write_text(result,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True);save(ROOT/'compiler_source_provenance.json',dict(
        row_contract=str(row_source),row_contract_sha256=sha(row_source.read_bytes()),
        conditional_contract=str(cond_source),conditional_contract_sha256=sha(cond_source.read_bytes()),
        compiler=str(OUT),compiler_sha256=sha(OUT.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),
        all_checks_precede_single_replace_file=True,original_outcome_differences_preserved=True,
        no_registry_builder_ROM_orledger_change=True,full_goal_complete=False))
    print('Prepared atomic B180 compiler:11 reviewed rows,ten relative operands,seven exact leaves and current actual limits.')
