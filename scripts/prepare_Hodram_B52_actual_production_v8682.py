"""Derive B52 whole-fixture/trace/glyph reader for both choices and focused withdrawal."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B52_actual_production_tools_v8682')
    assert not root.exists()
    source = Path('dk4tool/patch/hodram_B51_actual_evidence_v1.py').read_text(encoding='utf-8')
    normal_start = source.index('                if word==0:')
    normal_end = source.index("                if at not in f['records']", normal_start)
    group_start = source.index("            ids=['DK4_MES_B51_R0006'")
    group_end = source.index('    return dict(summary=', group_start)
    new_end = """                if word==0:
                    flagged=c['whole_command_hex']=='00000080'
                    require(c['native_extent']==4 and row['result_words']==([1,0] if flagged else [0,pairs[-2]['native_result'][1]]),'original full normal-preserving/flagged-clearing end')
                    normal=dict(frame=row['frame'],native_result=row['result_words'],complete_four_byte_end=True)
                    if scope=='opposition':
                        normal.update(source_end_hex=c['whole_command_hex'],flagged_end_clears_carried_value=True)
"""
    new_tail = """            ids=['DK4_MES_B52_R0006','DK4_MES_B52_R0033' if choice==1 else 'DK4_MES_B52_R0021']
            require(len(pairs)==(18 if choice==1 else 14) and sum(p['word']==0x2100 for p in pairs)==1,'selected B52 path has one native typed menu/all original selected commands')
            require([s['id'] for s in speechrows]==ids and group['unvisited_conditional_text_IDs']==[r['id'] for r in f['declared']['original_text_records'] if r['id'] not in ids],'exact observed andexplicitly unvisited case membership')
            results.append(dict(scope=scope,version=version,choice=choice,actual_pages=len(speechrows),complete_holds=sum(len(s['complete_holds']) for s in speechrows),script_return=normal,original_selected_commands=len(pairs)-8,all_trace_source_payloads_inputs_callbacks_anddistinct_returns_bound=True))
    for row in rows:
        actual=observations[row['id']]
        require({r['version'] for r in actual}=={'clean_Japanese','revised_English'} and len(actual)==(6 if row['id'].endswith('R0006') else 2 if row['id'].endswith('R0033') else 4),'all unique source-qualified actual speech andcase memberships')
    require(len(results)==6 and page_occurrences==12 and totalholds==138,'six actual groups/twelve page occurrences/138 complete body-name holds')
"""
    changes = {
        'B51': 'B52', '[51]': '[52]', 'original_block=51': 'original_block=52',
        "f['source_block']==51": "f['source_block']==52", "group['block']==51": "group['block']==52",
        "len(source_commands)==20": "len(source_commands)==14",
        'all20 original B51 commands': 'all14 original B52 commands',
        "len(selected_speeches)==5 and len(selected_commands)==20": "len(selected_speeches)==3 and len(selected_commands)==14",
        "relative==f['source_relative_sites']==8": "relative==f['source_relative_sites']==4",
        "len(objects)==20 and len(texts)==5": "len(objects)==14 and len(texts)==3",
        "for scope,key in [('whole','actual')]:": "for scope,key in [('withdrawal','actual'),('opposition','opposition_actual'),('focus','focus_actual')]:",
        "len(groups)==(2 if scope=='whole' else 4)": "len(groups)==2",
        "if scope=='whole':require([g['version'] for g in groups]==['clean_Japanese','revised_English'],'ordered whole-source languages')\n        else:require([(g['choice'],g['version']) for g in groups]==[(c,v) for c in ['accept','decline'] for v in ['clean_Japanese','revised_English']],'ordered tail languages/both choices')": "require([g['version'] for g in groups]==['clean_Japanese','revised_English'],'ordered source/English languages')",
        "version=group['version'];choice=group.get('choice');f=canonical[scope,version]": "version=group['version'];choice=1 if scope=='opposition' else 0;f=canonical['whole',version];frames=5201 if scope=='focus' else 10001",
        "group['actual_frames']==10001": "group['actual_frames']==frames",
        "root=(Path('work/analysis/Hodram_B51_scene_runs_v8574')/f'route1_B51_{version}') if scope=='whole' else Path('work/analysis/Hodram_B51_tail_runs_v8416')/f'route1_{version}_{choice}'": "root=Path({'withdrawal':'work/analysis/Hodram_B52_scene_runs_v8649','opposition':'work/analysis/Hodram_B52_opposition_runs_v8652','focus':'work/analysis/Hodram_B52_postreturn_focus_runs_v8656'}[scope])/f'route1_B52_{version}'",
        "report['frames']==10001": "report['frames']==frames",
        "schedule=base+[dict(start=frame,duration=5,buttons=['A']) for frame in range(4000,9521 if scope=='whole' else 9501,240)]\n            if choice=='decline':schedule=sorted(schedule+[dict(start=4350,duration=5,buttons=['DOWN'])],key=lambda r:r['start'])": "schedule=base+[dict(start=frame,duration=5,buttons=['A']) for frame in range(4000,4481 if scope=='focus' else 9521,240)]\n            if choice==1:schedule=sorted(schedule+[dict(start=4100,duration=5,buttons=['DOWN'])],key=lambda r:r['start'])",
        source[normal_start:normal_end]: new_end,
        "normal==group['normal_return']": "normal==group['script_return' if scope=='opposition' else 'normal_return']",
        source[group_start:group_end]: new_tail,
        'whole_actual_frames=20002,complete_actual_page_occurrences=8,complete_actual_holds=56,unique_speech_IDs=4,all20_original_commands_retained_selected15_andnormal_value_carry_verified=True': 'whole_actual_frames=50406,main_frames=40004,focused_frames=10402,complete_actual_page_occurrences=12,complete_actual_holds=138,unique_speech_IDs=3,all14_original_commands_retained_both_choices_anddistinct_normal_flagged_ends_verified=True',
    }
    receipt = derive('dk4tool/patch/hodram_B51_actual_evidence_v1.py', 'dk4tool/patch/hodram_B52_actual_evidence_v1.py', changes)
    root.mkdir(parents=True)
    save(root / 'derivation.json',dict(derivation=receipt,all_original_fixture_ROM_inverse_resident_payload_trace_ABI_body_name_pixel_guards_retained=True,
         no_new_capture_orproducer_replay=True,initialized_fixture_scope_not_natural_activation=True))
