"""Bind complete B48 source,28 relative sites,raw predicates,two event queries and normal carry."""
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
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_source_controls_v8024')
SOURCE=Path('work/analysis/Rafael_next_clean_v8020/complete_clean_SC0_B48_EV0_andcoverage_before_current_English.json')
GLOSS=Path('work/analysis/Rafael_B48_clean_gloss_v8022/91_fresh_clean_glosses_nine_source_identities_before_current_English.json')
INPUT=Path('work/analysis/current_V8013_Rafael_native_v8016/current_native_input.json')
NAMES=Path('work/analysis/Rafael_B48_names_v8023/nine_static_speakers18_getters_clean_fields36_synthetic_macro_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists()
    source,gloss,inp,names=map(read,[SOURCE,GLOSS,INPUT,NAMES])
    assert names['source_gloss_sha256']==sha(GLOSS.read_bytes()) and names['current_English_B48_bodies_still_unread']
    current,clean=[NdsImage.open(p) for p in [inp['current_ROM'],source['source_ROM']]]
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']==names['candidate_sha256']
    assert sha(Path(source['source_ROM']).read_bytes())==source['source_ROM_sha256']
    arm,ja_arm=[im.read_file('/__arm9__.bin') for im in [current,clean]]
    spans=[(0x23840,0x23A28),(0x293B8,0x2976C),(0x29874,0x29A9C),(0x2A414,0x2A600),(0x24048,0x24118)]
    assert all(arm[a:b]==ja_arm[a:b] for a,b in spans)
    ev=current.read_file('/data/EV0.DK4');assert ev==clean.read_file('/data/EV0.DK4') and sha(ev)==source['EV0_sha256']
    g=source['groups'][0];block=bytes.fromhex(g['clean_block_hex']);commands=g['commands']
    assert len(block)==g['clean_logical_end']==5252 and g['clean_tail_bytes']==0 and len(commands)==163 and len(g['records'])==91
    assert all(r['current_English_body_unread'] for r in gloss['records'])
    assert sum(bytes.fromhex(r['source_hex'])[1:].count(b'FI') for r in g['records'])==1
    assert all(bytes.fromhex(r['source_hex'])[1:].count(t)==0 for r in g['records'] for t in [b'FA',b'FO'])
    selected=g['source_event_records']
    assert [(r['event_ID'],r['action_index'],r['script_block'],r['must_be_completed'],r['must_not_be_completed']) for r in selected]==[(48,49,48,[],[])]
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    adapter=checked_text(inspect.getsource(native_entry),{
        'assert get(0x7F244)==2':'assert get(0x7F244)==0',
        'not_current_eligibility_or_selected_B234_activation':'not_current_eligibility_or_selected_B48_activation'})
    env=dict(native_entry.__globals__);exec(compile(adapter,__file__+'::original-EV0-entry','exec'),env)
    entry=ctx.execute(env['native_entry'],ev,selected);ctx.machines.pop()
    boundaries={c['offset'] for c in commands}|{5252};branches=[];operands=[];predicates=[]
    for c in commands:
        if c['word'] in [0x100,0x200,0x300,0x400]:
            result=ctx.execute(native_skip,block,c);ctx.machines.pop()
            assert all(r['next_offset'] in boundaries for r in result['cases']);branches.append(dict(block=48,**result))
            at=c['offset'];span=struct.unpack_from('<H',block,at+2)[0]
            operands.append(dict(block=48,offset=at,word=c['word'],span_field_offset=at+2,source_span=span,
                unmatched_next_offset=at+4,matched_skip_target=at+4+span,ancestor_0100_offsets=c['ancestor_0100_offsets'],
                source_operand_hex=block[at:at+4].hex()))
        elif c['word'] in [0x8000,0x8100]:
            result=ctx.execute(probe,block,c);ctx.machines.pop();predicates.append(result)
            print('Predicate/query',c['offset'],c['whole_command_hex'],result['native_result'],flush=True)
    assert len(branches)==28 and sum(len(r['cases']) for r in branches)==140
    assert len(predicates)==7 and sum(p['word']==0x8000 for p in predicates)==5
    same={}
    for p in predicates:
        same.setdefault(p['source_command_hex'],p['native_result']);assert same[p['source_command_hex']]==p['native_result']
    assert len(same)==5
    inventory,walker,inventory_source=scoped_inventory()
    current_commands,current_speeches=inventory(arm,block)
    assert current_commands==commands
    assert len(current_speeches)==91
    end=commands[-1];assert end['word']==0 and end['offset']==5248 and end['native_extent']==4 and block[5248:]==bytes(4)
    ep=Path('work/analysis/lil_B218_controls_v6878/two_A000_structural_cases50_normal_seeded_ends_no_relative_or_predicate.json')
    end_adapter=read(ep)['source_owned_seeded_end_adapter'];env=dict(end_case.__globals__)
    exec(compile(end_adapter,__file__+'::source-normal-end-value-carry','exec'),env)
    ends=[env['end_case'](arm,block,5248,p,s) for p in [0,1,2,3,0xFFFFFFFF] for s in [0,1,2,3,0xFFFFFFFF]]
    assert len(ends)==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends) and not ctx.machines
    save(ROOT/'source_EV0_28_relative_sites140_cases5_raw_predicates2_queries25_seeded_ends.json',dict(
        candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        source_event_records=selected,current_native_EV_entry=entry,source_relative_cases=branches,
        operands_requiring_adjustment_when_resizing=operands,source_raw_predicates_andqueries=predicates,unique_raw_predicate_andquery_results=same,
        source_terminal=end,normal_seeded_ends=ends,current_runtime_complete_source_command_census=current_commands,
        current_runtime_complete_source_speech_census=current_speeches,
        all163_source_commands91_speeches_andcomplete_preambles_equal_under_clean_andcurrent_native_decoders=True,
        structural_decoder_bridges_opaque_scene_effects_not_gameplay_orcomplete_effect_semantics=True,
        source_8000_raw_evaluator_not_assumed_boolean_8100_original_completion_getter_returns_boolean=True,
        source_Ev48_no_explicit_dependency_list_not_proof_ofouter_scheduler_city_conditions_orcurrent_eligibility=True,
        actual_opening_predicate_values_not_natural_B48_activation_orall_possible_values=True,
        current_B48_English_bodies_still_unread=True,source_path_composition_andprecise_characterization_pending=True,
        no_gameplay_state_condition_roster_role_funds_seed_orresult_forced=True,
        unchanged_source_runtime_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        source_owned_entry_adapter=adapter,source_owned_skip_probe=inspect.getsource(native_skip),
        source_owned_predicate_probe=inspect.getsource(probe),source_owned_seeded_end_adapter=end_adapter,
        source_owned_census_walker=walker,source_owned_census_inventory=inventory_source,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,INPUT,NAMES,ep,Path(__file__)]},
        new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('B48 source:28 relative sites/140 cases,5 raw predicates/2completion queries,25seeded ends;all163commands/91speeches decoded under both runtimes.Current English bodies unread.')
