"""Parse each original route event table and use its actual current native getters."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.prove_lil_B234_entry_v7576 import native_entry
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_entries_v7628')
SOURCE=Path('work/analysis/papal_trade_SC0_SC1_current_v7620/two_complete_current_exchanges36_source_current_refs_before_new_prose.json')
CONTEXTS=Path('work/analysis/papal_trade_route_native_v7626/two_own_current_route_contexts_actual_captains0_1_strict2b6.json')
def parse_events(ev):
    body=ev[96:];counts=struct.unpack_from('<9H',ev,10);starts=struct.unpack_from('<9I',ev,40);total=sum(counts);events=[]
    action_begin,action_end=struct.unpack_from('<2I',ev,0x4C);words=struct.unpack_from(f'<{(action_end-action_begin)//2}H',body,action_begin)
    for category,count in enumerate(counts):
        offset=starts[category]
        for local in range(count):
            word0,word1=struct.unpack_from('<2I',body,offset);length=(word1&255)*4;assert length>=8
            record=body[offset:offset+length];assert len(record)==length;must=[];must_not=[];following=8
            if word1&(1<<24):
                packed=struct.unpack_from('<H',record,8)[0];yes,no=packed>>8,packed&255
                needed=struct.unpack_from(f'<{yes+no}H',record,10) if yes+no else ()
                must=list(needed[:yes]);must_not=list(needed[yes:]);following+=((yes+no)*2+5)&~3
                assert following<=length and all(v<total or v==65535 for v in [*must,*must_not])
            action=(word0>>16)&0x3FFF;assert action<len(words);native_word=words[action]
            events.append(dict(event_ID=len(events),category=category,category_local_index=local,body_offset=offset,source_record_bytes=length,source_hex=record.hex(),source_word0=word0,source_word1=word1,action_index=action,native_action_word=native_word,script_block=(native_word&4095) if native_word&0xF000==0x2000 else None,must_be_completed=must,must_not_be_completed=must_not,payload_after_dependency_prefix_hex=record[following:].hex(),additional_native_conditions_andouter_scheduler_unexecuted=True));offset+=length
        assert offset==struct.unpack_from('<I',ev,44+category*4)[0]
    assert len(events)==total;return events
if __name__=='__main__':
    assert not ROOT.exists();source,contexts=map(read,[SOURCE,CONTEXTS]);current,clean=[NdsImage.open(p) for p in [source['current_ROM'],'work/clean.nds']]
    assert source['current_ROM_sha256']==contexts['candidate_sha256']==sha(Path(source['current_ROM']).read_bytes())
    ROOT.mkdir(parents=True);groups=[]
    for group in source['groups']:
        route,n=group['route'],group['block'];path=f'/data/EV{route}.DK4';ev=current.read_file(path);assert ev==clean.read_file(path)
        events=parse_events(ev);chosen=[r for r in events if r['script_block']==n];assert len(chosen)==1
        ids={*[r['event_ID'] for r in chosen],*[v for r in chosen for v in r['must_be_completed']+r['must_not_be_completed'] if v!=65535]};selected=[r for r in events if r['event_ID'] in ids]
        cp=next(r for r in contexts['contexts'] if r['route']==route);inp=Path(cp['input']);assert sha(inp.read_bytes())==cp['input_sha256']
        adapter=checked_text(inspect.getsource(native_entry),{'assert get(0x7F244)==2':'assert EXPECTED_CAPTAIN in [0,1] and get(0x7F244)==EXPECTED_CAPTAIN','not_current_eligibility_or_selected_B234_activation':'not_current_eligibility_or_selected_papal_trade_activation'})
        env={**native_entry.__globals__,'EXPECTED_CAPTAIN':route};exec(compile(adapter,__file__+'::actual-route-original-getters','exec'),env)
        ctx=RouteCurrentContext(inp,'unused-no-historical-ROM',ROOT/f'route{route}_current_context');native=ctx.execute(env['native_entry'],ev,selected);ctx.machines.pop();assert not ctx.machines
        groups.append(dict(route=route,route_identity=cp['route_identity'],file_path=group['file_path'],block=n,event_file=path,event_file_sha256=sha(ev),all_original_source_events=events,selected_source_events=chosen,selected_source_event_anddependency_native_getters=native,source_owned_getter_adapter=adapter,actual_captain_ID=route,current_opening_is_not_optional_event_eligibility_oractivation=True,original_event_file_andaction_table_exact=True,actual_selected_optional_event_IDs=[],native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes())))
    save(ROOT/'original_EV0_EV1_events_actions_dependencies_andactual_route_getters.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),own_route_contexts=str(CONTEXTS),own_route_contexts_sha256=sha(CONTEXTS.read_bytes()),groups=groups,all_source_event_files_andaction_tables_exact=True,actual_native_getters_read_source_records_in_own_route_capture=True,all4MiB_actor_roster_event_RNG_andABI_guards_preserved=True,no_original_eligibility_activation_location_earned_progress_orfull_effect_claim=True,new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTEXTS,Path(native_entry.__code__.co_filename),Path(__file__)]},full_goal_complete=False))
    for g in groups:print(dict(route=g['route_identity'],block=g['block'],events=[dict(id=r['event_ID'],action=r['action_index'],requires=r['must_be_completed'],excludes=r['must_not_be_completed']) for r in g['selected_source_events']],native_getters=len(g['selected_source_event_anddependency_native_getters']['rows']),actual_activation=False))
