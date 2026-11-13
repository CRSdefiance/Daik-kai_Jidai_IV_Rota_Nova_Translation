"""Clean B52 source commands, conditional extents, event getters and distinct item-display boundaries before English."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B50_registered_route_context_v8546 import RouteCurrentContext
from scripts.prove_lil_B234_entry_v7576 import native_entry
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.research_wedding_command_v676 import walk
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B52_source_controls_v8620')
SOURCE=Path('work/analysis/Hodram_B52_clean_v8616/complete_clean_SC1_B52_EV1_andcoverage_before_current_English.json')
GLOSS=Path('work/analysis/Hodram_B52_clean_gloss_v8617/three_first_clean_glosses_two_choice_labels_anddistinct_terminal_risks.json')
INPUT=Path('work/analysis/current_V8543_Hodram_native_v8546/current_native_input.json')
END=Path('work/analysis/Hodram_B47_B48_source_controls_v8314/two_EV1_entries15_commands6_preambles7_opaque_effect_pairs50_complete_seeded_ends.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,gloss,inp=map(read,[SOURCE,GLOSS,INPUT]);g=packet['groups'][0];block=bytes.fromhex(g['clean_block_hex']);commands=g['commands'];logical=g['clean_logical_end']
    assert gloss['all3_clean_utterances_andtwo_choices_glossed_before_current_English'] and all(r['current_English_dialogue_still_unconsulted'] for r in gloss['groups'][0]['records']) and len(g['records'])==3 and len(commands)==14 and logical==len(block)==228
    image=NdsImage.open(inp['current_ROM']);clean=NdsImage.open('work/clean.nds');arm,ja=image.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin');assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256'] and sha(Path('work/clean.nds').read_bytes())==packet['source_ROM_sha256']
    spans=[(0x23840,0x23A28),(0x293B8,0x2976C),(0x29874,0x29A9C),(0x2A414,0x2A600),(0x24048,0x24118),(0x29FFC,0x2A0F8),(0x28A64,0x28A8C)]
    assert all(arm[a:b]==ja[a:b] for a,b in spans);ev=image.read_file('/data/EV1.DK4');assert ev==clean.read_file('/data/EV1.DK4') and sha(ev)==packet['EV1_sha256']
    events=g['source_event_anddependencies'];assert [e['event_ID'] for e in events]==[30,52,74]
    selected=g['source_event_records'];assert [(e['event_ID'],e['script_block'],e['must_be_completed'],e['must_not_be_completed']) for e in selected]==[(52,52,[30],[74])]
    inventory,walker,inventory_source=scoped_inventory();decoded,speeches=inventory(arm,block);assert decoded==commands and len(speeches)==3
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    entry_adapter=checked_text(inspect.getsource(native_entry),{'assert get(0x7F244)==2':'assert get(0x7F244)==1','not_current_eligibility_or_selected_B234_activation':'not_current_eligibility_or_selected_Hodram_B52_activation'});env=dict(native_entry.__globals__);exec(compile(entry_adapter,__file__+'::exact-source-entry','exec'),env);entry=ctx.execute(env['native_entry'],ev,events);ctx.machines.pop()
    end_adapter=read(END)['source_owned_seeded_end_adapter'];env=dict(end_case.__globals__);exec(compile(end_adapter,__file__+'::whole-end-value-carry','exec'),env)
    picture_adapter=checked_text(inspect.getsource(picture),{'assert word in [0x4821,0x4822,0x4823,0x4700]':'assert word in [0x4820,0x4800,0x4700]'});pe=dict(picture.__globals__);exec(compile(picture_adapter,__file__+'::original-two-item-layouts-andhide','exec'),pe)
    boundaries={c['offset'] for c in commands}|{logical};branches=[];operands=[];queries=[];pictures=[];opaque=[]
    for command in commands:
        word=command['word'];at=command['offset']
        if word in [0x100,0x200,0x300,0x400]:
            span=struct.unpack_from('<H',block,at+2)[0];assert at+4 in boundaries and at+4+span in boundaries;result=ctx.execute(native_skip,block,command);ctx.machines.pop();assert all(c['next_offset'] in boundaries for c in result['cases']);branches.append(result)
            operands.append(dict(block=52,offset=at,word=word,span_field_offset=at+2,source_span=span,unmatched_next_offset=at+4,matched_skip_target=at+4+span,ancestor_0100_offsets=command['ancestor_0100_offsets'],source_operand_hex=block[at:at+4].hex()))
        elif word in [0x8000,0x8100]:queries.append(ctx.execute(probe,block,command));ctx.machines.pop()
        elif word in [0x4820,0x4800,0x4700]:pictures.append(dict(word=word,**ctx.execute(pe['picture'],block,command)));ctx.machines.pop()
        elif word not in [0x4000,0x2100,0]:
            raw=bytes.fromhex(command['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
            for label,code in [('clean-decoder',ja),('current-decoder',arm)]:
                result=walk(code,isolated);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1 and result['rows'][0]['native_extent']==command['native_extent'];versions.append(dict(version=label,**result))
            assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges'];opaque.append(dict(source_offset=at,word=word,source_command_hex=raw.hex(),versions=versions))
    terminals=[c for c in commands if c['word']==0];terminal=commands[-1]
    assert [(c['offset'],c['whole_command_hex'],c['native_extent']) for c in terminals]==[(166,'00000000',4),(224,'00000080',4)]
    ends=[env['end_case'](arm,block,at,p,v) for at in [166,224] for p in [0,1,2,3,0xFFFFFFFF] for v in [0,1,2,3,0xFFFFFFFF]]
    assert all(c['native_result']==([0,c['initial_value_word'],0,0,0,0] if c['source_offset']==166 else [1,0,0,0,0,0]) for c in ends)
    assert len(branches)==4 and sum(len(c['cases']) for c in branches)==20 and len(queries)==0 and len(pictures)==0 and len(opaque)==4 and len(ends)==50 and not ctx.machines
    assert not pictures and not queries
    assert [(o['source_offset'],o['word']) for o in opaque]==[(164,0xC283),(200,0xA000),(208,0xA000),(216,0xA000)]
    assert [r['source_selector'] for r in g['records']].count(254)==0 and {m:sum(r['source_Japanese'].count(m) for r in g['records']) for m in ['FI','FA','FO']}==dict(FI=0,FA=0,FO=0)
    save(ROOT/'source_controls.json',dict(candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],current_native_input=str(INPUT),current_native_input_sha256=sha(INPUT.read_bytes()),source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),first_clean_gloss=str(GLOSS),first_clean_gloss_sha256=sha(GLOSS.read_bytes()),block=52,all_original_source_commands=commands,complete_source_preambles=[dict(id=r['id'],source_reference=r['source_reference'],preamble_hex=r['source_complete_preamble_hex']) for r in g['records']],source_event_records=selected,source_event_anddependency_records=events,original_EV1_entry=entry,source_relative_cases=branches,operands_requiring_adjustment_when_resizing=operands,source_raw_query_cases=queries,source_picture_andhide_cases=pictures,source_has_no_picture_orhide_sites=True,paired_opaque_structural_decodes=opaque,distinct_seeded_ends=ends,source_terminal=terminal,source_both_end_commands=terminals,normal166_carries_seed_flagged224_clears_seed_andreturns_kind1=True,separate_tail_bytes=0,typed_choice_source=gloss['source_typed_choice'],typed_choice_native_parser_layout_glyph_andselection_behavior_pending=True,source_FE_count=0,source_macro_counts=dict(FI=0,FA=0,FO=0),all14commands3completepreambles4relative_sites_zeroqueries_onechoice_twoends_bound=True,source_event_getters_not_outer_eligibility_original_location_ornatural_activation=True,five_previous_results_are_structural_arguments_not_forced_gameplay=True,picture_resource_UI_bodies_andopaque_effect_gameplay_semantics_not_executed=True,current_B52_English_dialogue_bodies_still_unconsulted=True,source_speaker_glyphs_names_menu_branch_context_current_editorial_actual_andregistered_integration_pending=True,source_owned_entry_adapter=entry_adapter,source_owned_seeded_end_adapter=end_adapter,source_owned_picture_adapter=picture_adapter,source_owned_skip_probe=inspect.getsource(native_skip),source_owned_query_probe=inspect.getsource(probe),inventory_walker=walker,inventory_function=inventory_source,unchanged_source_runtime_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,INPUT,END,Path(__file__)]}))
    print('Clean B52:14commands/3preambles/4relative sites20cases/noqueries/50distinctendcases/4opaque pairs;normal166carries seed,flagged224returns kind1/clears seed. Menu/native speakers/selectedpath/currentEnglish stillpending;zero credit.')
