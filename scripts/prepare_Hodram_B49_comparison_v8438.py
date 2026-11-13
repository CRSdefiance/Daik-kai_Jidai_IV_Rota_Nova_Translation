"""Derive independent B49 saved-comparison reader without changing native constants."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/Hodram_B49_comparison_tools_v8438')
SOURCE=Path('dk4tool/patch/hodram_outcomes_comparison_v1.py')
TARGET=Path('dk4tool/patch/hodram_B49_comparison_v1.py')

if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text=SOURCE.read_text(encoding='utf-8')
    old_resource=text[text.index('        resource=None'):text.index('        summaries.append')]
    resource='''        whole=choice=='whole'
        display_word=0x4820 if whole else 0x4800
        source_offset=32 if whole else 962
        source_hex='204894a8' if whole else '004894a8'
        display=[next(c for c in g['command_pairs'] if c['word']==display_word) for g in groups]
        hide=[next(c for c in g['command_pairs'] if c['word']==0x4700) for g in groups]
        for g,c in zip(groups,display,strict=True):
            control=next(v for v in g['fixture']['all_original_exchange_commands'] if v['fixture_command_offset']==c['fixture_offset'])
            require(control['whole_command_hex']==source_hex and control['canonical_clean_offset']==source_offset,'original B49 item148 operand andsource-qualified site')
        upper=min(c['start'] if whole else c['returned'] for c in hide)-4
        common=sorted(f for f in photos[0] if f in photos[1] and max(c['returned'] for c in display)+30<f<upper)
        before=sorted(f for f in photos[0] if f in photos[1] and f<min(c['start'] for c in display))
        after=sorted(f for f in photos[0] if f in photos[1] and f>max(c['returned'] for c in hide)+30)
        require(common and before and after,'actual item display andhide sample intervals including original blocking wait')
        resource=dict(original_4700_calls=hide,common_display_sample_frames=common,descriptor=[0,148,1,5],layout=[2,0,0] if whole else [0,0,0],
            selected_before_display_frame=before[-1],selected_item_display_frame=common[-1],selected_after_hide_frame=after[0],
            actual_full_original_resource_andhide_command_executions=True,descriptor_layout_from_exact_original_operand_and8384_native_consumer_not_dialogue_UI_request_words=True,
            visual_item_card_andhide_review_pending=True)
        if whole:resource.update(original_4820_calls=display,original_Ullr_Bow_item148_source_4820_layout2=True)
        else:resource.update(original_4800_calls=display,original_Ullr_Bow_item148_source_4800_layout0=True,item_card_observed_during_original_hide_command_wait_not_assumed_instant_hide=True)
        require(declared['original4820_4700_actual' if whole else 'original4800_4700_actual']==resource,'complete original item/hide observations andscope metadata')
        if whole:require(declared['unvisited_conditional_text_IDs']==old['unvisited_conditional_text_IDs']==new['unvisited_conditional_text_IDs'] and len(old['unvisited_conditional_text_IDs'])==8,'whole no-item branch retains eight conditional speech limits')
        boundaries=[]
        for a,b in zip(old['command_pairs'],new['command_pairs'],strict=True):
            boundaries.append(dict(source_offset=a['canonical_source_offset'],before=[a['before_RNG'],b['before_RNG']],after=[a['after_RNG'],b['after_RNG']],equal=a['before_RNG']==b['before_RNG'] and a['after_RNG']==b['after_RNG']))
        unequal=[b['source_offset'] for b in boundaries if not b['equal']]
        require(unequal=={'whole':[324,416,424,980],'accept':[],'decline':[758,820,904,908,910,952,960,962,966,974,976,980]}[choice],'all measured script-boundary PRNG differences preserved')
'''
    old_wrapper=text[text.index('\ndef check_comparisons'):]
    wrapper='''
def check_comparisons(data,parent,load,require):
    result=check_base_comparisons(data,parent,load,require)
    for key,frames,scope in [('comparison',20002,'initialized_original_Hodram_opening_not_optional_event_activation_original_location_orall_attainable_paths'),('tail_comparison',40004,'initialized_bounded_possession_dialogue_tail_not_whole_B49_inventory_eligibility_original_location_oroptional_event_activation')]:
        proof=data[key]
        require(proof['total_actual_frames']==frames and proof[scope] and proof['all_measured_differences_retained_no_input_state_seed_orresult_forcing'] and proof['no_every_frame_causality_future_outcome_broad_simulation_fullroute_orhardware_claim'],'original initialized-fixture scope andall measured limitations retained')
        for sheet in proof['review_sheets']:require(sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'original comparison review sheet integrity')
    require([g['later_RGB_differences'] for g in result['groups']]==[2,3,0] and [g['duration_differences'] for g in result['groups']]==[2,1,4],'all five laterRGB differences andseven command-duration differences retained')
    require([g['final_PRNG_seeds'] for g in result['groups']]==[[1633251573,1633251573],[996112413,155404999],[3478759668,3478759668]],'unequal accept final PRNG andequal whole/decline final PRNG retained without future-outcome inference')
    result.update(new_emulator_runs=0,all_source_qualified_item148_layout2_andlayout0_hide_waits_checked=True,all_measured_PRNG_andRGB_differences_preserved=True)
    return result
'''
    changes={
        "comparison=data['comparison'];require(len(comparison['groups'])==2,'two exact actual comparison blocks')":"comparison=data['comparison'];tail=data['tail_comparison'];require(len(comparison['groups'])==1 and len(tail['groups'])==2,'whole andboth bounded-tail comparison groups')",
        "for number,declared in zip([47,48],comparison['groups'],strict=True):\n        require(declared['block']==number,'exact paired comparison block');groups=data[f'actual{number}']['groups'];old,new=groups":"for choice,declared in zip(['whole','accept','decline'],comparison['groups']+tail['groups'],strict=True):\n        number=49\n        require(declared['block']==number and (choice=='whole' or declared['choice']==choice),'exact paired B49 comparison membership');groups=data['actual']['groups'] if choice=='whole' else [g for g in data['tail_actual']['groups'] if g['choice']==choice];old,new=groups\n        require([g['version'] for g in groups]==['clean_Japanese','revised_English'],'exact comparison language order')",
        old_resource:resource,
        "summaries.append(dict(block=number,":"summaries.append(dict(block=number,choice=choice,script_boundary_PRNG=boundaries,",
        "require(total_rgb==186 and all(s['final_captain_IDs']==[1,1] for s in summaries),'186laterRGBpairs andboth initialized Hodram captain1 tails')":"require(total_rgb==231 and [s['later_RGB_samples'] for s in summaries]==[81,81,69] and all(s['final_captain_IDs']==[1,1] for s in summaries),'231laterRGBpairs andall six initialized Hodram captain1 tails')",
        old_wrapper:wrapper,
    }
    result=derive(SOURCE,TARGET,changes);ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(derivation=result,all_native_getter_addresses_actor_sizes_PRNG_offsets_andmultiplicity_unchanged=True,no_capture_replay=True,new_credit=0))
    print('Prepared source-locked independent B49 comparison reader.')
