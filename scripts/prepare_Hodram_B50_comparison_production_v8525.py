"""Derive independent complete B50 timing/PRNG/state/RGB and original item transition checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_comparison_production_tools_v8525');assert not root.exists()
    path=Path('dk4tool/patch/hodram_B49_comparison_v1.py');source=path.read_text(encoding='utf-8')
    a=source.index("        whole=choice=='whole'");b=source.index('        boundaries=[]',a)
    resource="""        display=[next(c for c in g['command_pairs'] if c['word']==0x4800) for g in groups]
        hide=[next(c for c in g['command_pairs'] if c['word']==0x4700) for g in groups]
        for g,c in zip(groups,display,strict=True):
            control=next(v for v in g['fixture']['all_original_exchange_commands'] if v['fixture_command_offset']==c['fixture_offset'])
            require(control['whole_command_hex']=='004894a8' and control['canonical_clean_offset']==214,'original B50 item148 operand andsource-qualified site')
        common=sorted(f for f in photos[0] if f in photos[1] and max(c['returned'] for c in display)+30<f<min(c['returned'] for c in hide)-4)
        before=sorted(f for f in photos[0] if f in photos[1] and f<min(c['start'] for c in display))
        after=sorted(f for f in photos[0] if f in photos[1] and f>max(c['returned'] for c in hide)+30)
        require(common and before and after,'actual item display andhide intervals including original native return boundary')
        resource=dict(original_4800_calls=display,original_4700_calls=hide,common_display_sample_frames=common,descriptor=[0,148,1,5],layout=[0,0,0],original_Ullr_Bow_item148_source_4800_layout0=True,
            selected_before_display_frame=before[-1],selected_item_display_frame=common[-1],selected_after_hide_frame=after[0],actual_full_original_resource_andhide_command_executions=True,
            descriptor_layout_from_exact_original_operand_and8384_native_consumer_not_dialogue_UI_request_words=True,visual_item_card_andhide_review_pending=True)
        require(declared['original4800_4700_actual']==resource,'complete original item/hide observations andscope metadata')
        require(declared['unvisited_conditional_text_IDs']==old['unvisited_conditional_text_IDs']==new['unvisited_conditional_text_IDs']==[],'complete three-speech B50 exchange visited')
"""
    wrapper="""
def check_comparisons(data,parent,load,require):
    result=check_base_comparisons(data,parent,load,require);proof=data['comparison']
    require(proof['total_actual_frames']==20002 and proof['initialized_original_Hodram_opening_not_optional_event_activation_original_location_orall_attainable_paths'] and proof['all_measured_differences_retained_no_input_state_seed_orresult_forcing'] and proof['no_every_frame_causality_future_outcome_broad_simulation_fullroute_orhardware_claim'],'original initialized-fixture scope andall measured limitations retained')
    for sheet in proof['review_sheets']:require(sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'original comparison review sheet integrity')
    require([g['later_RGB_differences'] for g in result['groups']]==[4] and [g['duration_differences'] for g in result['groups']]==[2],'all four laterRGB differences andtwo command-duration differences retained')
    require([g['final_PRNG_seeds'] for g in result['groups']]==[list(map(int,['3867090476','3028864251']))],'unequal final PRNG retained despiteequal source-script boundary values without future-outcome inference')
    result.update(new_emulator_runs=0,all_source_qualified_item148_layout0_show_hide_intervals_checked=True,all_measured_PRNG_andRGB_differences_preserved=True)
    return result
"""
    tools=[derive(str(path),'dk4tool/patch/hodram_B50_comparison_v1.py',{
        "comparison=data['comparison'];tail=data['tail_comparison'];require(len(comparison['groups'])==1 and len(tail['groups'])==2,'whole andboth bounded-tail comparison groups')":"comparison=data['comparison'];require(len(comparison['groups'])==1,'one complete B50 exchange comparison')",
        "zip(['whole','accept','decline'],comparison['groups']+tail['groups'],strict=True)":"zip(['whole'],comparison['groups'],strict=True)",
        'number=49':'number=50',
        source[a:b]:resource,
        "unequal=={'whole':[324,416,424,980],'accept':[],'decline':[758,820,904,908,910,952,960,962,966,974,976,980]}[choice]":"unequal==[]",
        "total_rgb==231 and [s['later_RGB_samples'] for s in summaries]==[81,81,69]":"total_rgb==89 and [s['later_RGB_samples'] for s in summaries]==[89]",
        '231laterRGBpairs andall six initialized Hodram captain1 tails':'89laterRGBpairs andboth initialized Hodram captain1 tails',
        source[source.index('\ndef check_comparisons'):]:wrapper,
        'paired B49':'paired B50',
    })]
    old=Path('scripts/validate_Hodram_B49_comparison_v8439.py').read_text(encoding='utf-8')
    lines=[line for line in old.splitlines(True) if " 'tail_comparison':" in line or " 'tail_actual':" in line]
    changes={line:'' for line in lines}
    changes.update({
        'hodram_B49_comparison_v1':'hodram_B50_comparison_v1',
        'validate_Hodram_B49_native_v8433':'validate_Hodram_B50_native_v8520',
        'Hodram_B49_independent_compare_v8439':'Hodram_B50_independent_compare_v8526',
        'Hodram_B49_comparison_v8410':'Hodram_B50_comparison_v8509',
        'Hodram_B49_actual_v8409/B49':'Hodram_B50_actual_v8507/B50',
        'translations/hodram_B49_editorial_manuscript_v4.json':'translations/hodram_B50_editorial_manuscript_v5.json',
        'Independent B49 comparison:231laterRGBpairs,all fiveRGB differences,all timings/PRNG/native-state/raw-calendar/item/hide-wait scope recomputed;no emulator replay orcredit.':'Independent B50 comparison:89laterRGBpairs,all fourRGB differences,two speech-duration differences,allPRNG/native-state/raw-calendar/item/layout0/hide scope recomputed;no emulator replay orcredit.',
    })
    tools.append(derive('scripts/validate_Hodram_B49_comparison_v8439.py','scripts/validate_Hodram_B50_comparison_v8526.py',changes))
    root.mkdir(parents=True);save(root/'derivations.json',dict(tools=tools,all_native_getter_addresses_actor_sizes_PRNG_offsets_andmultiplicity_preserved=True,no_capture_replay_orcontroller_retiming=True,new_credit=0,full_goal_complete=False))
