"""Source-lock B52's original event/branch/opaque/two-end behavior before current English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_source_control_tools_v8620');assert not root.exists()
    path=Path('scripts/prove_Hodram_B49_source_controls_v8384.py');source=path.read_text(encoding='utf-8')
    a=source.index("    assert [p['word'] for p in pictures]");b=source.index("    assert [r['source_selector']",a)
    picture_checks=source[a:b]
    events="events=g['source_event_anddependencies'];assert [(e['event_ID'],e['script_block'],e['must_be_completed']) for e in events]==[(48,48,[]),(49,49,[48])]"
    newevents="""events=g['source_event_anddependencies'];assert [e['event_ID'] for e in events]==[30,52,74]
    selected=g['source_event_records'];assert [(e['event_ID'],e['script_block'],e['must_be_completed'],e['must_not_be_completed']) for e in selected]==[(52,52,[30],[74])]"""
    endchecks="""    terminal=commands[-1];assert terminal['word']==0 and terminal['offset']==980 and terminal['native_extent']==4 and block[980:984]==bytes(4)
    ends=[env['end_case'](arm,block,980,p,v) for p in [0,1,2,3,0xFFFFFFFF] for v in [0,1,2,3,0xFFFFFFFF]];assert all(c['native_result'][1]==c['initial_value_word'] for c in ends)"""
    newends="""    terminals=[c for c in commands if c['word']==0];terminal=commands[-1]
    assert [(c['offset'],c['whole_command_hex'],c['native_extent']) for c in terminals]==[(166,'00000000',4),(224,'00000080',4)]
    ends=[env['end_case'](arm,block,at,p,v) for at in [166,224] for p in [0,1,2,3,0xFFFFFFFF] for v in [0,1,2,3,0xFFFFFFFF]]
    assert all(c['native_result']==([0,c['initial_value_word'],0,0,0,0] if c['source_offset']==166 else [1,0,0,0,0,0]) for c in ends)"""
    result=derive(str(path),'scripts/prove_Hodram_B52_source_controls_v8620.py',{
        'scripts.Hodram_registered_route_context_v8303':'scripts.Hodram_B50_registered_route_context_v8546',
        'Hodram_B49_source_controls_v8384':'Hodram_B52_source_controls_v8620',
        'work/analysis/Hodram_B49_clean_v8357/complete_clean_SC1_B49_EV1_andcoverage_before_current_English.json':'work/analysis/Hodram_B52_clean_v8616/complete_clean_SC1_B52_EV1_andcoverage_before_current_English.json',
        'work/analysis/Hodram_B49_clean_gloss_v8358/fourteen_first_clean_glosses_two_choice_labels_wristband_trade_direction_andqualified_Hodram_reply.json':'work/analysis/Hodram_B52_clean_gloss_v8617/three_first_clean_glosses_two_choice_labels_anddistinct_terminal_risks.json',
        'current_V8300_Hodram_native_v8303':'current_V8543_Hodram_native_v8546',
        'all14_clean_utterances_andtwo_choices_glossed_before_current_English':'all3_clean_utterances_andtwo_choices_glossed_before_current_English',
        "len(g['records'])==14 and len(commands)==36 and logical==len(block)==984":"len(g['records'])==3 and len(commands)==14 and logical==len(block)==228",
        events:newevents,'len(speeches)==14':'len(speeches)==3',
        'selected_Hodram_B49_activation':'selected_Hodram_B52_activation','block=49,offset=at':'block=52,offset=at',
        endchecks:newends,
        'len(branches)==8 and sum(len(c[\'cases\']) for c in branches)==40 and len(queries)==1 and len(pictures)==4 and len(opaque)==7 and len(ends)==25':"len(branches)==4 and sum(len(c['cases']) for c in branches)==20 and len(queries)==0 and len(pictures)==0 and len(opaque)==4 and len(ends)==50",
        picture_checks:"    assert not pictures and not queries\n    assert [(o['source_offset'],o['word']) for o in opaque]==[(164,0xC283),(200,0xA000),(208,0xA000),(216,0xA000)]\n",
        "].count(254)==1": "].count(254)==0",
        'block=49,all_original_source_commands':'block=52,all_original_source_commands',
        'source_event_records=events,original_EV1_entry':'source_event_records=selected,source_event_anddependency_records=events,original_EV1_entry',
        'original_distinct_item148_layouts_2_0_0_and0_0_0=True':'source_has_no_picture_orhide_sites=True',
        'normal_seeded_ends=ends,source_terminal=terminal':'distinct_seeded_ends=ends,source_terminal=terminal,source_both_end_commands=terminals,normal166_carries_seed_flagged224_clears_seed_andreturns_kind1=True',
        'source_FE_count=1':'source_FE_count=0',
        'all36commands14completepreambles8relative_sites_one_query_one_choice_one_FE_andfull_terminal_bound':'all14commands3completepreambles4relative_sites_zeroqueries_onechoice_twoends_bound',
        'current_B49_English_dialogue_bodies_still_unconsulted':'current_B52_English_dialogue_bodies_still_unconsulted',
        'source_FE_glyphs_names_current_editorial_actual_andregistered_integration_pending':'source_speaker_glyphs_names_menu_branch_context_current_editorial_actual_andregistered_integration_pending',
        'Clean B49:36commands/14preambles/8relative sites40cases/one rawquery/25valuecarryends/7opaque pairs;item148layouts[2,0,0]and[0,0,0]/twohide boundaries.Sourcechoice/nativeFE/currentEnglish/actual stillpending;zero credit.':'Clean B52:14commands/3preambles/4relative sites20cases/noqueries/50distinctendcases/4opaque pairs;normal166carries seed,flagged224returns kind1/clears seed. Menu/native speakers/selectedpath/currentEnglish stillpending;zero credit.',
        'Clean B49 source':'Clean B52 source',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,all_original_skip_scratch_restore_both_end_value_carry_ABI_whole4MiB_andsource_input_guards_preserved=True,own_V8543_Hodram_captain1_context_only=True,both_distinct_original_end_words_preserved_not_assumed_equal=True,no_current_English_dialogue_actual_activation_orcredit=True,new_credit=0,full_goal_complete=False))
