"""Replace a rejected equality assumption with measured timing,RNG and full-frame differences."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/audit_shachihoko_B204_card_v6084.py','scripts/audit_shachihoko_B204_card_v6084b.py',{
        "ROOT=Path('work/analysis/shachihoko_B204_card_actual_v6084')":"ROOT=Path('work/analysis/shachihoko_B204_card_actual_v6084b')",
        "a,b=runs;assert a['pairs']==b['pairs'];scene=[p for p in b['pairs'] if p['block']==22]":"""a,b=runs
    assert len(a['pairs'])==len(b['pairs'])
    differences=[];duration_changes=[]
    for old,new in zip(a['pairs'],b['pairs'],strict=True):
        assert all(old[k]==new[k] for k in ['route','block','offset','word','native_result','decoded_length'])
        if old!=new:differences.append(dict(block=old['block'],fixture_offset=old['offset'],word=old['word'],changes={k:[old[k],new[k]] for k in old if old[k]!=new[k]}))
        x,y=old['returned']-old['start'],new['returned']-new['start']
        if x!=y:duration_changes.append(dict(block=old['block'],fixture_offset=old['offset'],word=old['word'],parent_duration=x,target_duration=y,delta=y-x))
    scene=[p for p in b['pairs'] if p['block']==22]""",
        "and scene[-1]['returned']==7894":"and scene[-1]['word']==0",
        "assert 88<=bounds[0]<bounds[2]<=176 and 238<=bounds[1]<bounds[3]<=249,('unexpected full-frame difference',old['frame'],bounds)":"""classes=dict(item_title=0,advance_prompt=0)
            for yy in range(bounds[1],bounds[3]):
                for xx in range(bounds[0],bounds[2]):
                    if images[0].getpixel((xx,yy))==images[1].getpixel((xx,yy)):continue
                    if 88<=xx<176 and 237<=yy<249:classes['item_title']+=1
                    elif 224<=xx<240 and 360<=yy<376:classes['advance_prompt']+=1
                    else:raise AssertionError(('unclassified actual RGB difference',old['frame'],xx,yy))
            different[-1]['measured_difference_pixel_counts']=classes""",
        'parent_target_all_observed_SC_command_paths_timings_results_and_interval_RNG_exact=True':'parent_target_all_completed_SC_paths_results_and_decoder_lengths_exact=True,command_timing_and_interval_RNG_differences=differences,command_duration_changes=duration_changes',
        'source_end_return_frame=7894':'source_parent_end_return_frame=7894,target_end_return_frame=scene[-1]["returned"]',
        'whole_frames_with_measured_title_difference=different':'whole_frames_with_measured_differences=different',
        'all_measured_RGB_differences_inside_original_item_title_bounds=True':'all_measured_RGB_differences_classified_as_item_title_or_advance_prompt=True',
        'source_names_portraits_Japanese_text_cultural_item_image_category_and_other_UI_exact_at_same_frames=True':'source_names_portraits_Japanese_text_cultural_item_image_category_and_UI_outside_title_and_prompt_exact_at_same_frames=True,no_full_RAM_future_random_sequence_or_complete_timing_cause_claim=True',
        'title_only_differences=len(different)':'title_or_prompt_differences=len(different)',
        'B204_end=7894':'B204_end=scene[-1]["returned"],timing_or_RNG_differing_pairs=len(differences)',
    }))
