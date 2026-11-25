"""Expose measured later screenshot/RNG differences without retiming, forcing or causal claims."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_later_differences_v8339')
COMPARE=Path('work/analysis/Hodram_outcome_actual_comparison_v8337/two_paired_whole_outcomes_controls_scenes_returns_bounded_later_state.json')
if __name__=='__main__':
    assert not ROOT.exists();comparison=read(COMPARE);groups=[];sheets=[];ROOT.mkdir(parents=True)
    for group in comparison['groups']:
        number=group['block'];root=Path('work/analysis/Hodram_outcome_actual_v8335'+('b' if number==48 else ''))/f'B{number}';proofpath=root/'paired_actual_dialogue_headers_FE_flow_returns.json';proof=read(proofpath);old,new=proof['groups'];assert not proof['unresolved']
        bounds=[]
        for a,b in zip(old['command_pairs'],new['command_pairs'],strict=True):
            assert a['word']==b['word'] and a['source_command_ordinal']==b['source_command_ordinal']
            bounds.append(dict(source_command_ordinal=a['source_command_ordinal'],word=a['word'],source_entry_frame=a['start'],English_entry_frame=b['start'],source_return_frame=a['returned'],English_return_frame=b['returned'],before_PRNG=[a['before_RNG'],b['before_RNG']],after_PRNG=[a['after_RNG'],b['after_RNG']],before_PRNG_equal=a['before_RNG']==b['before_RNG'],after_PRNG_equal=a['after_RNG']==b['after_RNG']))
        differences=[]
        for sample in group['later_RGB_comparisons']:
            if sample['whole_RGB_equal']:continue
            images=[]
            for k in ['clean','revised']:
                ref=sample[k];assert sha(Path(ref['path']).read_bytes())==ref['PNG_sha256'];images.append(Image.open(ref['path']).convert('RGB'))
            coords=[(i%256,i//256) for i,(a,b) in enumerate(zip(images[0].get_flattened_data(),images[1].get_flattened_data(),strict=True)) if a!=b]
            assert ImageChops.difference(*images).getbbox()==tuple(sample['changed_RGB_bbox'])
            differences.append(dict(frame=sample['frame'],source=sample['clean'],English=sample['revised'],changed_RGB_bbox=sample['changed_RGB_bbox'],changed_pixels=len(coords),upper_screen_changed_pixels=sum(y<192 for x,y in coords),lower_screen_changed_pixels=sum(y>=192 for x,y in coords)))
        if number==48:
            for batch,frames in enumerate([[4870,5410,7030],[9550,10000]]):
                sheet=Image.new('RGB',(len(frames)*512,410),'#263238');draw=ImageDraw.Draw(sheet)
                for i,frame in enumerate(frames):
                    sample=next(s for s in differences if s['frame']==frame)
                    for j,key in enumerate(['source','English']):
                        pic=Image.open(sample[key]['path']).convert('RGB');x=(i*2+j)*256;draw.text((x+3,3),f'{key} frame{frame}',fill='white');sheet.paste(pic,(x,24))
                path=ROOT/f'B48_measured_later_differences_sheet{batch+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),frames=frames))
        groups.append(dict(block=number,command_boundary_PRNG_comparisons=bounds,all_observed_script_entry_andreturn_PRNG_pairs_equal=all(b['before_PRNG_equal'] and b['after_PRNG_equal'] for b in bounds),
            final_PRNG_seeds=group['final_PRNG_seeds'],final_PRNG_equal=group['final_PRNG_seeds'][0]==group['final_PRNG_seeds'][1],all_five_final_native_components_equal=all(group['five_native_component_equality'].values()),whole_actor_bytes_equal=group['whole_actors_equal'],
            final_captain_IDs=[v['captain_ID'] for v in group['final_native_values']],normal_returns=group['normal_returns'],actual_duration_differences=group['duration_differences'],actual_UI_request_differences=group['UI_request_differences'],
            later_RGB_pairs=len(group['later_RGB_comparisons']),later_RGB_differences=differences,later_RGB_difference_count=len(differences),no_new_emulation_orchanging_input_seed_RNG_flags_orresults=True))
    assert [g['later_RGB_difference_count'] for g in groups]==[0,13] and all(g['whole_actor_bytes_equal'] and g['all_five_final_native_components_equal'] and g['final_captain_IDs']==[1,1] for g in groups)
    save(ROOT/'observed_later_RGB_andPRNG_differences_not_everyframe_causality.json',dict(groups=groups,review_sheets=sheets,visual_review_pending=True,
        all_actual_differences_preserved_not_repaired_by_retiming_orseed_forcing=True,matching_selected_final_components_not_full_simulation_orfuture_outcome_equivalence=True,
        later_older_record_technical_reaudit_must_retain_this_scope=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [COMPARE,Path(__file__)]}))
    print([(g['block'],g['all_observed_script_entry_andreturn_PRNG_pairs_equal'],g['final_PRNG_equal'],g['later_RGB_difference_count']) for g in groups])
