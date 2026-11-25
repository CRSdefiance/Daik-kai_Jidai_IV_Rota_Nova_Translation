"""Source-lock independent comparison to both outcome groups, preserving nonzero later RGB/RNG scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
EXTRA='''

def check_comparisons(data,parent,load,require):
    result=check_base_comparisons(data,parent,load,require);comparison=data['comparison'];later=data['later'];expected_groups=[]
    require(len(later['groups'])==2,'two later-difference characterization groups')
    for number,c in zip([47,48],comparison['groups'],strict=True):
        old,new=data['actual'+str(number)]['groups'];boundaries=[]
        for a,b in zip(old['command_pairs'],new['command_pairs'],strict=True):
            require(a['word']==b['word'] and a['source_command_ordinal']==b['source_command_ordinal'],'same original later-characterization membership')
            boundaries.append(dict(source_command_ordinal=a['source_command_ordinal'],word=a['word'],source_entry_frame=a['start'],English_entry_frame=b['start'],source_return_frame=a['returned'],English_return_frame=b['returned'],before_PRNG=[a['before_RNG'],b['before_RNG']],after_PRNG=[a['after_RNG'],b['after_RNG']],before_PRNG_equal=a['before_RNG']==b['before_RNG'],after_PRNG_equal=a['after_RNG']==b['after_RNG']))
        differences=[]
        for sample in c['later_RGB_comparisons']:
            if sample['whole_RGB_equal']:continue
            images=[Image.open(sample[k]['path']).convert('RGB') for k in ['clean','revised']]
            points=[(i%256,i//256) for i,(a,b) in enumerate(zip(images[0].get_flattened_data(),images[1].get_flattened_data(),strict=True)) if a!=b]
            require(ImageChops.difference(*images).getbbox()==tuple(sample['changed_RGB_bbox']),'actual later changed-pixel extent')
            differences.append(dict(frame=sample['frame'],source=sample['clean'],English=sample['revised'],changed_RGB_bbox=sample['changed_RGB_bbox'],changed_pixels=len(points),upper_screen_changed_pixels=sum(y<192 for x,y in points),lower_screen_changed_pixels=sum(y>=192 for x,y in points)))
        expected_groups.append(dict(block=number,command_boundary_PRNG_comparisons=boundaries,all_observed_script_entry_andreturn_PRNG_pairs_equal=all(b['before_PRNG_equal'] and b['after_PRNG_equal'] for b in boundaries),final_PRNG_seeds=c['final_PRNG_seeds'],final_PRNG_equal=c['final_PRNG_seeds'][0]==c['final_PRNG_seeds'][1],all_five_final_native_components_equal=all(c['five_native_component_equality'].values()),whole_actor_bytes_equal=c['whole_actors_equal'],final_captain_IDs=[v['captain_ID'] for v in c['final_native_values']],normal_returns=c['normal_returns'],actual_duration_differences=c['duration_differences'],actual_UI_request_differences=c['UI_request_differences'],later_RGB_pairs=len(c['later_RGB_comparisons']),later_RGB_differences=differences,later_RGB_difference_count=len(differences),no_new_emulation_orchanging_input_seed_RNG_flags_orresults=True))
    require(later['groups']==expected_groups,'every recomputed later pixel/PRNG/duration/native-state scope field')
    require([g['later_RGB_difference_count'] for g in expected_groups]==[0,13] and [g['final_PRNG_equal'] for g in expected_groups]==[True,False] and all(g['all_observed_script_entry_andreturn_PRNG_pairs_equal'] for g in expected_groups),'approved nonzero B48 later RGB/PRNG difference andmatching script boundaries')
    require(later['all_actual_differences_preserved_not_repaired_by_retiming_orseed_forcing'] and later['matching_selected_final_components_not_full_simulation_orfuture_outcome_equivalence'] and later['later_older_record_technical_reaudit_must_retain_this_scope'],'explicit later comparison limits')
    result.update(all_later_difference_scope_fields_recomputed=True,nonzero_B48_later_RGB_andPRNG_differences_preserved=True,new_emulator_runs=0)
    return result
'''
if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_comparison_helper_tools_v8350');assert not root.exists();source=Path('dk4tool/patch/hodram_three_blocks_comparison_v1.py').read_text('utf8');ending="    return dict(groups=summaries,later_full_RGB_pairs_recomputed=total_rgb,no_every_frame_future_outcome_orfull_route_equivalence_claim=True)\n"
    result=derive('dk4tool/patch/hodram_three_blocks_comparison_v1.py','dk4tool/patch/hodram_outcomes_comparison_v1.py',{
        'def check_comparisons(data,parent,load,require):':'def check_base_comparisons(data,parent,load,require):',
        "comparison=data['actual_comparison'];require(len(comparison['groups'])==3,'three exact actual comparison blocks')":"comparison=data['comparison'];require(len(comparison['groups'])==2,'two exact actual comparison blocks')",
        '[137,45,46]':'[47,48]',"data[f'actual_B{number}']":"data[f'actual{number}']",
        "total_rgb==532 and summaries[0]['final_captain_IDs']==[0,0] and all(s['final_captain_IDs']==[1,1] for s in summaries[1:])":"total_rgb==186 and all(s['final_captain_IDs']==[1,1] for s in summaries)",
        '532laterRGBpairs andexplicit B137 fixture-tail limit':'186laterRGBpairs andboth initialized Hodram captain1 tails',
        ending:ending+EXTRA,
    })
    root.mkdir(parents=True);save(root/'independent_comparison_nonzero_B48_later_scope_derivation.json',dict(derivation=result,all_native_high_integer_constants_andmultiplicity_preserved=True,no_later_RGB_orPRNG_equality_assumed_forB48=True,new_credit=0,full_goal_complete=False))
