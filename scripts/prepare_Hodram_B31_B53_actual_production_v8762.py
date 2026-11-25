"""Derive complete fixture/trace/pixel readers for all four existing cold boots."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_actual_tools_v8762');assert not root.exists()
    observed="    for row in rows:require(observations[row['id']]==row['actual_display_evidence'],'independent scoped per-record actual approval:'+row['id'])"
    checked='''    expected_observations={r['id']:[] for r in rows}
    for number,key in [(31,'B31_actual'),(53,'B53_actual')]:
        for group in data[key]['groups']:
            for speech in group['speeches']:
                expected_observations[speech['id']].append(dict(version=group['version'],source_selector=speech['source_selector'],name=speech['name'],selected_capture=speech['selected_capture'],complete_holds=len(speech['complete_holds'])))
    for row in rows:
        require(observations[row['id']]==expected_observations[row['id']],'independent scoped per-record actual approval:'+row['id'])
        require(bool(observations[row['id']])==(row['actual_observation_status']=='paired-whole-script-body-name-andportrait-observed'),'approved actual versus offline-only scope:'+row['id'])
    require(sorted(k for k,v in observations.items() if v)==data['actual_review']['actual_unique_text_IDs'] and data['actual_review']['offline_only_text_IDs']==['DK4_MES_B31_R0013'],'two observed utterances andone explicitly unvisited short variant')'''
    receipt=derive('dk4tool/patch/hodram_B51_actual_evidence_v1.py','dk4tool/patch/hodram_B31_B53_actual_evidence_v1.py',{
        'B51 whole fixtures':'B31/B53 whole fixtures',
        'def check_fixtures(data,rows,parent,clean,rebuilt,require):':'def check_fixtures(data,rows,parent,clean,rebuilt,require,number):\n    rows=[r for r in rows if r["block"]==number]',
        'original[51]':'original[number]',"else target)[51]":"else target)[number]",
        "len(source_commands)==20,'all20 original B51 commands'":"len(source_commands)==9,'all9 original block commands'",
        "declared=data[key]['fixtures'];require(len(declared)==2":"declared=[f for f in data[key]['fixtures'] if f['source_block']==number];require(len(declared)==2",
        "len(selected_speeches)==5 and len(selected_commands)==20,'complete selected B51 source commands'":"len(selected_speeches)==len(rows) and len(selected_commands)==9,'complete selected block source commands'",
        "f['source_block']==51":"f['source_block']==number",'original_block=51':'original_block=number',
        "relative==f['source_relative_sites']==8":"relative==f['source_relative_sites']==(4 if number==31 else 0)",
        'len(objects)==20 and len(texts)==5':'len(objects)==9 and len(texts)==len(rows)',
        'canonical[scope,version]':'canonical[number,scope,version]',
        'canonical=check_fixtures(data,rows,parent,clean,rebuilt,require)':'canonical={}',
        "    for scope,key in [('whole','actual')]:":"    for number,key in [(31,'B31_actual'),(53,'B53_actual')]:\n        scope='whole';canonical.update(check_fixtures(data,rows,parent,clean,rebuilt,require,number))",
        "group['block']==51 and group['actual_frames']==10001":"group['block']==number and group['actual_frames']==6001",
        "root=(Path('work/analysis/Hodram_B51_scene_runs_v8574')/f'route1_B51_{version}') if scope=='whole' else Path('work/analysis/Hodram_B51_tail_runs_v8416')/f'route1_{version}_{choice}'":"root=Path('work/analysis/Hodram_B31_B53_scene_runs_v8740')/f'route1_B{number}_{version}'",
        "terminal['frames']==plan['frames']==report['frames']==10001":"terminal['frames']==plan['frames']==report['frames']==6001",
        "range(4000,9521 if scope=='whole' else 9501,240)":"range(4000,5521,240)",
        "normal=dict(frame=row['frame'],native_result=row['result_words'],complete_four_byte_end=True)":"normal=dict(frame=row['frame'],native_result=row['result_words'],complete_four_byte_end=True)\n                    if number==53:normal.update(previous_parser_result_value=pairs[-2]['native_result'][1],separate_interpreter_carried_mode=entry['mode'],source_proven_distinct_channels_not_assumed_equal=True)",
        "ids=['DK4_MES_B51_R0006','DK4_MES_B51_R0010','DK4_MES_B51_R0014','DK4_MES_B51_R0039'];require(len(pairs)==23 and not any(p['word']==0x2100 for p in pairs),'whole B51 exchange selected15commands/four observed speeches/no menu')":"ids=['DK4_MES_B31_R0018'] if number==31 else ['DK4_MES_B53_R0007'];require(len(pairs)==(15 if number==31 else 17) and not any(p['word']==0x2100 for p in pairs),'whole block selected commands/one observed speech/no menu')\n            path=[8,10,18,22,90,188,192] if number==31 else [8,10,12,98,106,114,122,130,132]\n            require([p['canonical_source_offset'] for p in pairs if p['source_command_ordinal'] is not None]==path,'complete unforced selected native source path')",
        'results.append(dict(scope=scope,version=version':'results.append(dict(block=number,scope=scope,version=version',
        observed:checked,
        "len(results)==2 and page_occurrences==8 and totalholds==56,'both actual groups/eight observed page occurrences/56 complete body-name holds'":"len(results)==4 and page_occurrences==4 and totalholds==76,'four actual groups/four page occurrences/76 complete body-name holds'",
        'whole_actual_frames=20002,complete_actual_page_occurrences=8,complete_actual_holds=56,unique_speech_IDs=4,all20_original_commands_retained_selected15_andnormal_value_carry_verified':'whole_actual_frames=24004,complete_actual_page_occurrences=4,complete_actual_holds=76,unique_speech_IDs=2,all18_original_commands_retained_unforced_selected_paths_andnormal_resultword_channels_verified',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_native_high_integer_constants_andmultiplicity_preserved=True,
        all_original_whole_fixture_ROM_inverse_native_command_resident_payload_readonly_CPU_capture_input_complete_body_name_pixel_andreturn_guards_preserved=True,
        allfour_wholeblocks_not_shortened_selected_tail_fixtures=True,actualB31long_andB53warning_shortB31_offline_only=True,
        B53_existing_resultword0_andseparate_r3mode1_preserved_explicitly=True,no_emulator_orproducer_replay_no_ROMcommit_orcredit=True,new_credit=0,full_goal_complete=False))
