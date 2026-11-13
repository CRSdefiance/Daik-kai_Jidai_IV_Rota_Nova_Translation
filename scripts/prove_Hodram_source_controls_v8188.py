"""Bind all three clean Hodram entries/commands/relative scopes/raw results andseeded ends before English."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.prove_lil_B234_entry_v7576 import native_entry
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.gloss_Hodram_B137_B45_B46_v8183 import PACKETS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B137_B45_B46_source_controls_v8188')
GLOSS=Path('work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183/28_first_clean_glosses_six_identities_explicit_prerequisite_graph_before_current_English.json')
INPUT=Path('work/analysis/current_V8172_Hodram_native_v8187/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packets={b:read(p) for b,p in PACKETS.items()};gloss,inp=map(read,[GLOSS,INPUT])
    assert gloss['source_only_no_current_body_orname_comparison_no_localized_manuscript'] and all(r['current_English_body_not_yet_consulted'] for r in gloss['records'])
    assert len(gloss['records'])==28 and all(gloss['source_packets'][str(b)]['sha256']==sha(p.read_bytes()) for b,p in PACKETS.items())
    current,clean=[NdsImage.open(p) for p in [inp['current_ROM'],'work/clean.nds']]
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256'] and sha(Path('work/clean.nds').read_bytes())==packets[137]['source_ROM_sha256']
    arm,sourcearm=[im.read_file('/__arm9__.bin') for im in [current,clean]]
    spans=[(0x23840,0x23A28),(0x293B8,0x2976C),(0x29874,0x29A9C),(0x2A414,0x2A600),(0x24048,0x24118)]
    assert all(arm[a:b]==sourcearm[a:b] for a,b in spans)
    ev=current.read_file('/data/EV1.DK4');assert ev==clean.read_file('/data/EV1.DK4') and all(sha(ev)==p['EV1_sha256'] for p in packets.values())
    events={e['event_ID']:e for p in packets.values() for e in p['groups'][0]['source_event_anddependencies']}
    assert set(events)=={44,45,46,137}
    assert events[137]['must_be_completed']==[44] and events[45]['must_not_be_completed']==[46] and events[46]['must_be_completed']==[137,45]
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    adapter=checked_text(inspect.getsource(native_entry),{'assert get(0x7F244)==2':'assert get(0x7F244)==1','not_current_eligibility_or_selected_B234_activation':'not_current_eligibility_or_selected_Hodram_B137_B45_B46_activation'})
    env=dict(native_entry.__globals__);exec(compile(adapter,__file__+'::original-EV1-four-entry-context','exec'),env)
    entry=ctx.execute(env['native_entry'],ev,[events[i] for i in sorted(events)]);ctx.machines.pop()
    prior=Path('work/analysis/lil_B218_controls_v6878/two_A000_structural_cases50_normal_seeded_ends_no_relative_or_predicate.json')
    end_adapter=read(prior)['source_owned_seeded_end_adapter'];env=dict(end_case.__globals__);exec(compile(end_adapter,__file__+'::original-normal-end-value-carry','exec'),env)
    inventory,walker,inventory_source=scoped_inventory();groups=[];alloperands=[];allpredicates=[];relativecases=0
    expected={137:(33,21),45:(3,1),46:(24,6)}
    for blocknumber in [137,45,46]:
        g=packets[blocknumber]['groups'][0];block=bytes.fromhex(g['clean_block_hex']);commands=g['commands'];logical=g['clean_logical_end']
        assert (len(commands),len(g['records']))==expected[blocknumber] and block[logical:]==bytes(g['clean_tail_bytes'])
        assert not any(r['source_selector']==254 for r in g['records'])
        counts={m:sum(r['source_Japanese'].count(m) for r in g['records']) for m in ['FI','FA','FO']};assert counts==dict(FI=0,FA=0,FO=0)
        decoded,speeches=inventory(arm,block);assert decoded==commands and len(speeches)==len(g['records'])
        boundaries={c['offset'] for c in commands}|{logical};branches=[];predicates=[];operands=[]
        for command in commands:
            if command['word'] in [0x100,0x200,0x300,0x400]:
                at=command['offset'];span=struct.unpack_from('<H',block,at+2)[0]
                assert at+4 in boundaries and at+4+span in boundaries
                result=ctx.execute(native_skip,block,command);ctx.machines.pop()
                assert all(c['next_offset'] in boundaries for c in result['cases']);branches.append(result);relativecases+=len(result['cases'])
                operands.append(dict(block=blocknumber,offset=at,word=command['word'],span_field_offset=at+2,source_span=span,
                    unmatched_next_offset=at+4,matched_skip_target=at+4+span,ancestor_0100_offsets=command['ancestor_0100_offsets'],source_operand_hex=block[at:at+4].hex()))
            elif command['word'] in [0x8000,0x8100]:
                result=ctx.execute(probe,block,command);ctx.machines.pop();predicates.append(result)
                print('B'+str(blocknumber),'predicate/query',command['offset'],command['whole_command_hex'],result['native_result'],flush=True)
        end=commands[-1];assert end['word']==0 and end['offset']+4==logical and end['native_extent']==4 and block[end['offset']:logical]==bytes(4)
        ends=[env['end_case'](arm,block,end['offset'],p,v) for p in [0,1,2,3,0xFFFFFFFF] for v in [0,1,2,3,0xFFFFFFFF]]
        assert len(ends)==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends)
        alloperands.extend(operands);allpredicates.extend(dict(block=blocknumber,**r) for r in predicates)
        groups.append(dict(block=blocknumber,source_packet=str(PACKETS[blocknumber]),source_packet_sha256=sha(PACKETS[blocknumber].read_bytes()),clean_block_sha256=sha(block),
            all_original_source_commands=commands,complete_source_speech_preambles=[dict(id=r['id'],source_reference=r['source_reference'],complete_preamble_hex=r['source_complete_preamble_hex']) for r in g['records']],
            source_relative_cases=branches,operands_requiring_adjustment_when_resizing=operands,source_raw_predicates_andqueries=predicates,
            original_nontext_commands=[c for c in commands if c['word']!=0x4000],source_terminal=end,
            clean_stored_bytes=len(block),clean_logical_end=logical,separate_zero_tail_bytes=g['clean_tail_bytes'],normal_seeded_ends=ends,
            original_scene_picture_effect_bodies_preserved_butnot_executed_bystructural_census=True))
    assert not ctx.machines and sum(len(g['all_original_source_commands']) for g in groups)==60 and sum(len(g['complete_source_speech_preambles']) for g in groups)==28
    assert relativecases==5*len(alloperands) and sum(len(g['normal_seeded_ends']) for g in groups)==75
    save(ROOT/'three_EV1_entries60_commands28_speeches_native_relative_predicate_and75_seeded_ends.json',dict(
        candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),
        current_native_input=str(INPUT),current_native_input_sha256=sha(INPUT.read_bytes()),source_event_records=[events[i] for i in sorted(events)],original_EV1_entry=entry,
        groups=groups,operands_requiring_adjustment_when_resizing=alloperands,source_raw_predicates_andqueries=allpredicates,
        source_relative_sites=len(alloperands),source_native_relative_cases=relativecases,source_raw_predicate_query_count=len(allpredicates),normal_seeded_end_cases=75,
        all60commands28completepreambles_zero_FE_FI_FA_FO_andthree_whole_terminals_preserved=True,
        source_EV_graph_andnative_getters_not_outer_eligibility_total_chronology_orscheduler_activation=True,
        source_8000_raw_evaluator_results_not_assumed_boolean_or_typed_menu=True,
        five_previous_results_are_structural_arguments_not_forced_gameplay_states=True,
        no_conditions_party_roster_roles_funds_RNG_eventflags_orresults_forced=True,
        original_4800_A000_4700_scene_effects_item_resource_fullbodies_andnatural_context_unclaimed=True,
        current_English_dialogue_bodies_not_yet_consulted=True,source_path_context_item_names_getters_current_prose_native_actual_release_pending=True,
        unchanged_source_runtime_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        source_owned_entry_adapter=adapter,source_owned_skip_probe=inspect.getsource(native_skip),source_owned_predicate_probe=inspect.getsource(probe),source_owned_seeded_end_adapter=end_adapter,
        source_owned_inventory_walker=walker,source_owned_inventory_function=inventory_source,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [*PACKETS.values(),GLOSS,INPUT,prior,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Hodram clean source:60commands/28speeches,',len(alloperands),'relative sites/',relativecases,'cases,',len(allpredicates),'raw predicates/queries,75seeded value-carry ends. CurrentEnglish remainsunread;zero credit.')
