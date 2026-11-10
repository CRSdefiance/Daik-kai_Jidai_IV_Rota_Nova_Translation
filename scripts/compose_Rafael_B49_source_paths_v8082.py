"""Enumerate all native-result compositions,retain distinct complete text paths without huge duplicates."""
import hashlib,struct
from collections import Counter
from itertools import product
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_source_paths_v8082')
SOURCE=Path('work/analysis/Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json')
CONTROL=Path('work/analysis/Rafael_B49_source_controls_v8081/source_EV0_56_relative_sites280_cases13_raw_predicates1_query25_seeded_ends.json')
GLOSS=Path('work/analysis/Rafael_B49_clean_gloss_v8075/61_first_clean_glosses_seven_source_identities_before_current_English.json')
if __name__=='__main__':
    assert not ROOT.exists();source,control,gloss=map(read,[SOURCE,CONTROL,GLOSS])
    assert control['source_packet_sha256']==sha(SOURCE.read_bytes()) and control['current_B49_English_bodies_still_unread']
    g=source['groups'][0];commands={c['offset']:c for c in g['commands']};speeches={r['source_reference']['header_offset']:r for r in g['records']}
    relative={r['offset']:{c['previous_result_structural_argument']:c['next_offset'] for c in r['cases']} for r in control['source_relative_cases']}
    operands=list(control['unique_raw_predicate_andquery_results']);assert len(operands)==8
    domains=[[0,1] if key.startswith('0081') else [0,1,2,3,0xFFFFFFFF] for key in operands]
    assert sum(len(d)==5 for d in domains)==7 and sum(len(d)==2 for d in domains)==1
    def compose(values):
        at=8;last=0;visited=[];texts=[];steps=[]
        while at<g['clean_logical_end']:
            assert len(visited)<len(commands) and at not in visited
            c=commands[at];visited.append(at)
            if at in speeches:texts.append(speeches[at]['id'])
            if c['word'] in [0x8000,0x8100]:
                last=values[c['whole_command_hex']];steps.append(dict(offset=at,source_operand=c['whole_command_hex'],raw_result=last))
            at=relative[at][last] if at in relative else at+c['native_extent']
        assert at==g['clean_logical_end'] and visited[-1]==3970
        return dict(raw_results=values,visited_source_offsets=visited,source_speech_IDs=texts,source_speech_count=len(texts),original_predicate_steps=steps,
            independently_measured_relative_case_composition_not_full_interpreter_oractual_gameplay=True)
    representatives={};counts=Counter();distribution=Counter();union_commands=set();union_speeches=set();digest=hashlib.sha256();total=0
    for values in product(*domains):
        results=dict(zip(operands,values,strict=True));p=compose(results);key=tuple(p['source_speech_IDs']);total+=1
        representatives.setdefault(key,p);counts[key]+=1;distribution[p['source_speech_count']]+=1
        union_commands.update(p['visited_source_offsets']);union_speeches.update(key)
        digest.update(struct.pack('<8I',*values));digest.update(struct.pack('<I',len(p['visited_source_offsets'])));digest.update(struct.pack('<'+str(len(p['visited_source_offsets']))+'I',*p['visited_source_offsets']))
    assert total==156250 and union_commands==set(commands) and union_speeches=={r['id'] for r in g['records']}
    paths=[]
    for i,(key,p) in enumerate(representatives.items()):paths.append(dict(path=i,composition_count=counts[key],**p))
    assert sum(p['composition_count'] for p in paths)==total
    opening=compose({k:v[1] for k,v in control['unique_raw_predicate_andquery_results'].items()})
    memberships=[]
    for r in g['records']:
        memberships.append(dict(id=r['id'],source_reference=r['source_reference'],source_selector=r['source_selector'],source_0100_ancestors=r['source_0100_ancestors'],
            distinct_text_path_indices=[p['path'] for p in paths if r['id'] in p['source_speech_IDs']],
            structurally_common_to_every_text_path=all(r['id'] in p['source_speech_IDs'] for p in paths)))
    query=next(p for p in control['source_raw_predicates_andqueries'] if p['word']==0x8100)
    assert query['source_command_hex']=='00812900' and len(query['original_event_completion_calls'])==1 and query['original_event_completion_calls'][0]['args'][1]==41
    for p in paths:
        ids=set(p['source_speech_IDs']);v=p['raw_results']['00812900']
        assert ('DK4_MES_B49_R0238' in ids)==(v==0) and ('DK4_MES_B49_R0244' in ids)==(v==1)
    event41=next(e for e in source['all_original_source_events'] if e['event_ID']==41)
    ROOT.mkdir(parents=True)
    save(ROOT/'156250_compositions_distinct_complete_text_paths_and61_source_memberships.json',dict(
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),source_controls=str(CONTROL),source_controls_sha256=sha(CONTROL.read_bytes()),
        source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),source_operand_order=operands,source_operand_structural_domains=dict(zip(operands,domains,strict=True)),
        structural_compositions_evaluated=total,ordered_domain_andvisited_offset_stream_sha256=digest.hexdigest(),digest_encoding='Each lexicographic domain tuple:<8I;then visited count:<I;then every visited source offset:<count I.',
        distinct_text_path_count=len(paths),representative_text_paths=paths,source_speech_count_distribution=dict(distribution),source_speech_memberships=memberships,
        opening_native_result_composition=opening,source_event41_completion_query=query,event41_context_to_read_before_current_English=event41,
        R238_Africa_orwestern_NewWorld_vsR244_western_NewWorld_orfarEast_exclusive_by_event41=True,
        all154_commands61_speeches_in_structural_union=True,
        no_full_duplicate156250_path_dump_distinct_complete_text_paths_andexact_stream_digest_retained=True,
        structural_domains_not_forced_gameplay_states_orproof_ofattainable_all_combinations=True,
        B39_prerequisite_read_event41_variant_context_andraw_A0_operand_mechanic_meanings_pending=True,
        current_B49_English_bodies_still_unread=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,GLOSS,Path(__file__)]}))
    print('Compositions',total,'distinct text paths',len(paths),'speech counts',dict(distribution),'opening',opening['source_speech_count'])
    print('Event41 context',event41)
    print('Common',sum(m['structurally_common_to_every_text_path'] for m in memberships),'conditional',sum(not m['structurally_common_to_every_text_path'] for m in memberships))
