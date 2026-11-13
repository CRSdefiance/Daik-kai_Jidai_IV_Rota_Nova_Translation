"""Source-lock complete B51 native event/query/branch/opaque/end checks before English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B51_source_control_tools_v8555');assert not root.exists()
    path=Path('scripts/prove_Hodram_B49_source_controls_v8384.py');source=path.read_text(encoding='utf-8')
    events="""events=g['source_event_anddependencies'];assert [(e['event_ID'],e['script_block'],e['must_be_completed']) for e in events]==[(48,48,[]),(49,49,[48])]"""
    replacement="""selected=g['source_event_records'];assert [(e['event_ID'],e['script_block'],e['must_be_completed'],e['must_not_be_completed']) for e in selected]==[(51,51,[],[])]
    events=sorted([*selected,*[e for e in packet['all_original_source_events'] if e['event_ID']==30]],key=lambda e:e['event_ID']);assert [e['event_ID'] for e in events]==[30,51]"""
    picture_checks="""    assert [p['word'] for p in pictures]==[0x4820,0x4700,0x4800,0x4700]
    requests=[p['original_picture_boundary_calls'][0] for p in pictures];assert requests[0]['descriptor']==requests[2]['descriptor']==[0,148,1,5] and requests[0]['layout']==[2,0,0] and requests[2]['layout']==[0,0,0]"""
    result=derive(str(path),'scripts/prove_Hodram_B51_source_controls_v8555.py',{
        'scripts.Hodram_registered_route_context_v8303':'scripts.Hodram_B50_registered_route_context_v8546',
        'Hodram_B49_source_controls_v8384':'Hodram_B51_source_controls_v8555',
        'work/analysis/Hodram_B49_clean_v8357/complete_clean_SC1_B49_EV1_andcoverage_before_current_English.json':'work/analysis/Hodram_B51_clean_v8548/complete_clean_SC1_B51_EV1_andcoverage_before_current_English.json',
        'work/analysis/Hodram_B49_clean_gloss_v8358/fourteen_first_clean_glosses_two_choice_labels_wristband_trade_direction_andqualified_Hodram_reply.json':'work/analysis/Hodram_B51_clean_gloss_v8549/five_first_clean_glosses_warning_andconditional_reactions.json',
        'current_V8300_Hodram_native_v8303':'current_V8543_Hodram_native_v8546',
        'all14_clean_utterances_andtwo_choices_glossed_before_current_English':'all5_clean_utterances_glossed_before_current_English',
        "len(g['records'])==14 and len(commands)==36 and logical==len(block)==984":"len(g['records'])==5 and len(commands)==20 and logical==len(block)==340",
        events:replacement,
        'len(speeches)==14':'len(speeches)==5',
        'selected_Hodram_B49_activation':'selected_Hodram_B51_activation',
        'block=49,offset=at':'block=51,offset=at',
        'terminal[\'offset\']==980':"terminal['offset']==336",
        'block[980:984]':'block[336:340]',
        "env['end_case'](arm,block,980,p,v)":"env['end_case'](arm,block,336,p,v)",
        'len(queries)==1 and len(pictures)==4 and len(opaque)==7':'len(queries)==2 and len(pictures)==0 and len(opaque)==4',
        picture_checks:"    assert not pictures\n    event_query=next(q for q in queries if q['word']==0x8100);assert int.from_bytes(bytes.fromhex(event_query['source_command_hex'])[2:4],'little')==30 and len(event_query['original_event_completion_calls'])==1 and event_query['original_event_completion_calls'][0]['args'][1]==30\n    raw_query=next(q for q in queries if q['word']==0x8000);assert raw_query['original_event_completion_calls']==[]",
        "].count(254)==1":
            "].count(254)==0",
        'block=49,all_original_source_commands':'block=51,all_original_source_commands',
        'source_event_records=events,original_EV1_entry':'source_event_records=selected,source_event_andexplicit_query_records=events,original_EV1_entry',
        'original_distinct_item148_layouts_2_0_0_and0_0_0=True':'source_has_no_picture_orhide_sites=True',
        "typed_choice_source=gloss['source_typed_choice'],typed_choice_native_parser_layout_glyph_andselection_behavior_pending=True,source_FE_count=1":"source_has_no_typed_choice_orFE_panel=True,source_FE_count=0",
        'all36commands14completepreambles8relative_sites_one_query_one_choice_one_FE_andfull_terminal_bound':'all20commands5completepreambles8relative_sites_two_queries_no_menu_FE_andfull_terminal_bound',
        'current_B49_English_dialogue_bodies_still_unconsulted':'current_B51_English_dialogue_bodies_still_unconsulted',
        'source_FE_glyphs_names_current_editorial_actual_andregistered_integration_pending':'source_speaker_glyphs_names_branch_context_current_editorial_actual_andregistered_integration_pending',
        'Clean B49:36commands/14preambles/8relative sites40cases/one rawquery/25valuecarryends/7opaque pairs;item148layouts[2,0,0]and[0,0,0]/twohide boundaries.Sourcechoice/nativeFE/currentEnglish/actual stillpending;zero credit.':'Clean B51:20commands/5preambles/8relative sites40cases/two queries/25valuecarryends/4opaque pairs;event30 query/event51 source getter bound.No pictures/menu/FE;currentEnglish unread,native speaker/branch context pending;zero credit.',
        'Clean B49 source':'Clean B51 source',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,all_original_query_skip_scratch_restore_end_value_carry_ABI_whole4MiB_andsource_input_guards_preserved=True,own_V8543_Hodram_captain1_context_only=True,extra_event30_is_explicit_query_not_invented_prerequisite=True,no_current_English_dialogue_oractual_activation_ornew_credit=True,new_credit=0,full_goal_complete=False))
