"""Compose B48 paths from original branch cases; no condition,party,event or RNG forcing."""
from collections import Counter
from itertools import product
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_source_paths_v8025')
SOURCE=Path('work/analysis/Rafael_next_clean_v8020/complete_clean_SC0_B48_EV0_andcoverage_before_current_English.json')
CONTROL=Path('work/analysis/Rafael_B48_source_controls_v8024/source_EV0_28_relative_sites140_cases5_raw_predicates2_queries25_seeded_ends.json')
GLOSS=Path('work/analysis/Rafael_B48_clean_gloss_v8022/91_fresh_clean_glosses_nine_source_identities_before_current_English.json')
if __name__=='__main__':
    assert not ROOT.exists()
    source,control,gloss=map(read,[SOURCE,CONTROL,GLOSS])
    assert control['source_packet_sha256']==sha(SOURCE.read_bytes()) and control['current_B48_English_bodies_still_unread']
    g=source['groups'][0];commands={c['offset']:c for c in g['commands']}
    speeches={r['source_reference']['header_offset']:r for r in g['records']}
    relative={r['offset']:r for r in control['source_relative_cases']}
    operands=list(control['unique_raw_predicate_andquery_results'])
    assert set(operands)=={'0080ffff04fe0030','0080ffff0dfe0030','0080ffff07fe0030','00818000','00812500'}
    domains=[[0,1] if k.startswith('0081') else [0,1,2,3,0xFFFFFFFF] for k in operands]
    def compose(values):
        at=8;last=0;visited=[];texts=[];steps=[]
        while at<g['clean_logical_end']:
            assert len(visited)<len(commands) and at not in visited
            c=commands[at];visited.append(at)
            if at in speeches:texts.append(speeches[at]['id'])
            if c['word'] in [0x8000,0x8100]:
                last=values[c['whole_command_hex']]
                steps.append(dict(offset=at,source_operand=c['whole_command_hex'],raw_result=last,
                    original_kind='event-completion-query' if c['word']==0x8100 else 'raw-expression'))
            if at in relative:
                case=next(r for r in relative[at]['cases'] if r['previous_result_structural_argument']==last)
                at=case['next_offset']
            else:at+=c['native_extent']
        assert at==g['clean_logical_end'] and visited[-1]==5248
        return dict(raw_results=values,visited_source_offsets=visited,source_speech_IDs=texts,
            source_speech_count=len(texts),original_predicate_steps=steps,
            composed_from_independently_measured_native_relative_cases_not_full_interpreter_oractual_gameplay=True)
    paths=[compose(dict(zip(operands,values,strict=True))) for values in product(*domains)]
    assert len(paths)==500
    assert set().union(*(set(r['visited_source_offsets']) for r in paths))==set(commands)
    assert set().union(*(set(r['source_speech_IDs']) for r in paths))=={r['id'] for r in g['records']}
    def ident(index):return f'DK4_MES_B48_R{index:04d}'
    for p in paths:
        ids=set(p['source_speech_IDs']);v=p['raw_results']
        assert all((ident(i) in ids)==(v['0080ffff04fe0030']==1) for i in [17,232,236,239,273])
        assert (ident(32) in ids)==(v['0080ffff0dfe0030']==1)
        assert (ident(49) in ids)==(v['0080ffff07fe0030']==1)
        assert all((ident(i) in ids)==(v['00818000']==0) for i in [71,75])
        assert all((ident(i) in ids)==(v['00818000']==1) for i in [81,86])
        assert (ident(379) in ids)==(v['00812500']==0)
        assert all((ident(i) in ids)==(v['00812500']==1) for i in [385,389,393,396])
    representative={}
    for p in paths:representative.setdefault(tuple(p['source_speech_IDs']),p)
    assert len(representative)==32
    observed={k:v[1] for k,v in control['unique_raw_predicate_andquery_results'].items()}
    opening=compose(observed)
    event_queries=[]
    for predicate in control['source_raw_predicates_andqueries']:
        if predicate['word']!=0x8100:continue
        event=int.from_bytes(bytes.fromhex(predicate['source_command_hex'])[2:4],'little')
        row=next(r for r in source['all_original_source_events'] if r['event_ID']==event)
        event_queries.append(dict(source_offset=predicate['offset'],event_ID=event,source_event=row,
            native_completion_calls=predicate['original_event_completion_calls'],opening_native_result=predicate['native_result'],
            not_source_trigger_dependency_orcompleted_natural_gameplay=True))
    assert {r['event_ID'] for r in event_queries}=={128,37}
    ROOT.mkdir(parents=True)
    save(ROOT/'500_source_result_compositions32_text_paths_two_exclusive_pairs.json',dict(
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        source_controls=str(CONTROL),source_controls_sha256=sha(CONTROL.read_bytes()),
        source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),
        source_operand_order=operands,source_operand_structural_domains=dict(zip(operands,domains,strict=True)),
        source_result_compositions=paths,representative_text_paths=list(representative.values()),
        speech_count_distribution=dict(Counter(p['source_speech_count'] for p in paths)),
        opening_native_result_composition=opening,source_event_completion_queries=event_queries,
        all163_source_commands_all91_speeches_in_structural_union=True,
        Janus_five_speeches_Cesare_one_Cristina_one_exact_operand_conditional=True,
        R71_R75_versusR81_R86_exclusive_by_event128_original_completion_query=True,
        R379_versusR385_R389_R393_R396_exclusive_by_event37_original_completion_query=True,
        B37_context_previously_read_B128_context_to_read_before_current_English=True,
        source_8000_raw_values_preserved_8100_domains_boolean_only=True,
        hypothetical_structural_results_not_gameplay_state_party_conditions_orRNG_forcing=True,
        no_claim_ofsource_event48_outer_scheduler_activation_orcomplete_natural_route=True,
        current_B48_English_bodies_still_unread=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [SOURCE,CONTROL,GLOSS,Path(__file__)]},full_goal_complete=False))
    print('500 structural compositions/32 text paths;',dict(Counter(p['source_speech_count'] for p in paths)))
    print('Opening unforced composition',opening['source_speech_count'],'not actual gameplay.')
    print('Completion queries',[(r['event_ID'],r['source_event']['script_block']) for r in event_queries])
