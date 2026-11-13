"""Prepare the lossless six-target completion after all remaining release gates."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B195_completion_tools_v5585')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/complete_lil_B193_v5483.py');text=source.read_text(encoding='utf-8')
    a=text.index("    assert not transitions['sampled_postscene_whole_RGB_differences_unmasked']")
    b=text.index("    assert transitions['representative_actual_coverage_sufficient",a)
    measured="""    assert [(r['frame'],r['whole_frame_difference_bbox']) for r in transitions['sampled_postscene_whole_RGB_differences_unmasked']]==[
        (f,[224,370,240,376]) for f in [8410,8590,8770,8950]]
    assert not transitions['all_sampled_postscene_whole_RGB_equal']
    assert transitions['fifteen_timing_four_later_indicator_RGB_and_unequal_PRNG_differences_retained_without_masking_or_retiming']
    assert transitions['original_three_roles_R17_three_rows_two_chewing_beats_R69_intention_and_FE_clear_observed']
    assert transitions['whole_RGB_final9001_equal'] and transitions['postscene9001_PRNG_seeds']==[3942509462,3085513495] and not transitions['PRNG_equality']
"""
    c=text.index("        inventory=deepcopy(read(old['unfinished_editorial_scope_v5442'")
    e=text.index("        for unit in inventory['broader_coverage_units']:",c)
    inventory="""        inventory=deepcopy(read(old['unfinished_editorial_scope_v5576']['path']));inventory['next_focus']=NEXT
        inventory['Lil_B195_completed_v5585']=dict(final_review=str(FINAL),completed_objects=20,registered_candidate=release['candidate'],natural_event195_not_selected=True)
        inventory['historical_Lil_B195_actual_approved_before_v5585']=inventory.pop('next_Lil_B195_reference_actual_approved_uncredited_v5576')
        inventory['next_Lil_B196_clean_review_pending']=dict(file_path='/data/SC2.DK4',block=196,clean_inventory_and_full_exchange_gloss_before_prior_English=True,
            reviewed_objects=0,new_completion_credit=0,no_B196_command_actor_or_control_assumptions_inherited=True)
"""
    row=derive(source,'scripts/complete_lil_B195_v5585.py',{
        text[a:b]:measured,text[c:e]:inventory,
        "NEXT_SOURCE=Path('work/analysis/lil_B194_clean_context_v5488/all11_clean_exchange_and_fresh_glosses.json')\n":'',
        "    source=read(NEXT_SOURCE);assert len(source['records'])==11 and source['read_no_predecessor_English'] and source['new_review_credit']==0\n":'',
        ',NEXT_SOURCE,':',',
        'B193':'B195','fifteen':'twenty','Fifteen':'Twenty','completion_v5483':'completion_v5585','verification_v5484':'verification_v5586',
        'release_v5479':'release_v5581','startup_v5481':'startup_v5583','registration_v5477':'registration_v5579',
        'actual_v5472/actual_all15':'actual_v5572/actual_all20',
        'actual_review_v5473/all15_panels12_fullscreens_three_Ladies_return':'actual_review_v5573/all20_panels20_fullscreens_three_roles_return',
        'verification_v5443':'verification_v5577',
        'Lil-B193-three-Ladies-cooking-reported-spice-price-concern-friendship-and-prospective-Seoul15':
        'Lil-B195-three-roles-cheese-specialty-coaxing-shared-order-taste-intention-and-prospective-Veracruz20',
        'editorial_scope_v5483':'editorial_scope_v5585','B193_v5483':'B195_v5585','completion_text_v5483':'completion_text_v5585',
        'all577':'all579','V5437':'V5531',"reg['negative_count']==76":"reg['negative_count']==85",
        "sum(len(r['holds']) for r in actual['actual_panels'])==59":"sum(len(r['holds']) for r in actual['actual_panels'])==79",
        '[6457,6457]':'[7655,7657]','dict(total=10,speech=10,control_or_end=0)':'dict(total=15,speech=13,control_or_end=2)',
        'regressions_v5478':'regressions_v5580',"len(manifest['batches'])==577":"len(manifest['batches'])==579",'retention_v5482':'retention_v5584',
        '[-15:]':'[-20:]',"{'revise':8,'retain-wording':7}":"{'revise':3,'retain-wording':17}",
        'blocks[193]':'blocks[195]','block=193':'block=195','blocks=[193]':'blocks=[195]',
        '6109':'6135','6124':'6155','6127':'6158','3867':'3874','2257':'2281','4224':'4250','4239':'4270','4525':'4556',
        'revised=8':'revised=3','revised_count=8':'revised_count=3','fresh_revisions=8':'fresh_revisions=3','new_revisions=8':'new_revisions=3',
        'retained=7':'retained=17','retained_count=7':'retained_count=17','fresh_retentions=7':'fresh_retentions=17','justified_retentions=7':'justified_retentions=17',
        'actual_matching_holds=59':'actual_matching_holds=79','all15':'all20','exactly15':'exactly20','==15':'==20','=15':'=20',
        'event193':'event195','source193':'source195',
        'Lil_B194_clean_only_uncredited_objects=11':'Lil_B196_clean_review_pending=True',
        'goal_turn_new_emulator_runs=4':'goal_turn_new_emulator_runs=2','goal_turn_new_frames=39404':'goal_turn_new_frames=21402',
        '## V5483:':'## V5585:','cumulative V5478':'cumulative V5580','handoff - V5483':'handoff - V5585',
        'new_clean_only_Lil_B194_uncredited_objects=11':'next_Lil_B196_clean_review_pending=True',
        'ten_speech_timings_and_measured_postscene_RGB_PRNG_scope_preserved':'fifteen_timings_four_lower_indicators_and_unequal_PRNG_preserved',
        'V5478 integration verified;':'V5580 integration verified;',
        'Eleven conditional B194 clean-only glosses pending':'Next B196 clean-source review pending'})
    old,new=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert old-new==Counter({463267532:2}) and new-old==Counter({3942509462:1,3085513495:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_reversible_completion.json',dict(derivation=row,
        full_nested_history_inverse_preserved=True,expected_completed=6155,expected_source_prose=6158,
        revisions=3874,retentions=2281,SC2=4270,routes=4556,new_keys=20,next_clean_review_block196_pending=True,
        no_source_prose_OR_completion_credit_added_by_preparation=True,full_goal_complete=False))
