"""Compose every measured raw-result class;retain distinct command paths even when words coincide."""
import struct,hashlib
from collections import Counter
from itertools import product
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.gloss_Hodram_B137_B45_B46_v8183 import PACKETS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B137_B45_B46_source_paths_v8191')
CONTROL=Path('work/analysis/Hodram_B137_B45_B46_source_controls_v8188/three_EV1_entries60_commands28_speeches_native_relative_predicate_and75_seeded_ends.json')
GLOSS=Path('work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183/28_first_clean_glosses_six_identities_explicit_prerequisite_graph_before_current_English.json')
if __name__=='__main__':
    assert not ROOT.exists();control,gloss=map(read,[CONTROL,GLOSS]);assert control['current_English_dialogue_bodies_not_yet_consulted']
    assert control['source_gloss_sha256']==sha(GLOSS.read_bytes()) and len(gloss['records'])==28
    groups=[];total=0;allwords=set()
    for block in [137,45,46]:
        source=read(PACKETS[block]);g=source['groups'][0];cg=next(g for g in control['groups'] if g['block']==block)
        assert cg['source_packet_sha256']==sha(PACKETS[block].read_bytes()) and cg['all_original_source_commands']==g['commands']
        commands={c['offset']:c for c in g['commands']};speeches={r['source_reference']['header_offset']:r for r in g['records']}
        relative={r['offset']:{c['previous_result_structural_argument']:c['next_offset'] for c in r['cases']} for r in cg['source_relative_cases']}
        raw={p['source_command_hex']:p['native_result'][1] for p in cg['source_raw_predicates_andqueries']}
        operands=list(raw);domains=[[0,1] if op.startswith('0081') else [0,1,2,3,0xFFFFFFFF] for op in operands]
        assert len(operands)==(0 if block==45 else 1)
        def compose(values):
            at=8;last=0;visited=[];texts=[];steps=[]
            while at<g['clean_logical_end']:
                assert at in commands and at not in visited and len(visited)<len(commands)
                c=commands[at];visited.append(at)
                if at in speeches:texts.append(speeches[at]['id'])
                if c['word'] in [0x8000,0x8100]:
                    last=values[c['whole_command_hex']];steps.append(dict(offset=at,source_operand=c['whole_command_hex'],raw_result=last))
                at=relative[at][last] if at in relative else at+c['native_extent']
            assert at==g['clean_logical_end'] and visited[-1]==g['commands'][-1]['offset']
            return dict(raw_results=values,visited_source_offsets=visited,source_speech_IDs=texts,source_speech_count=len(texts),original_predicate_steps=steps,
                independent_native_branch_composition_not_full_effect_interpreter_oractual_gameplay=True)
        representatives={};counts=Counter();distribution=Counter();unioncommands=set();unionspeeches=set();digest=hashlib.sha256();evaluated=0
        for values in product(*domains):
            result=compose(dict(zip(operands,values,strict=True)));key=tuple(result['visited_source_offsets']);evaluated+=1
            representatives.setdefault(key,result);counts[key]+=1;distribution[result['source_speech_count']]+=1
            unioncommands.update(key);unionspeeches.update(result['source_speech_IDs'])
            digest.update(struct.pack('<I',len(values)));digest.update(struct.pack('<'+str(len(values))+'I',*values))
            digest.update(struct.pack('<I',len(key)));digest.update(struct.pack('<'+str(len(key))+'I',*key))
        assert unioncommands==set(commands) and unionspeeches=={r['id'] for r in g['records']}
        paths=[dict(path=i,composition_count=counts[key],**p) for i,(key,p) in enumerate(representatives.items())]
        textpaths={tuple(p['source_speech_IDs']) for p in paths};opening=compose(raw)
        memberships=[dict(id=r['id'],source_reference=r['source_reference'],source_selector=r['source_selector'],source_0100_ancestors=r['source_0100_ancestors'],
            distinct_command_path_indices=[p['path'] for p in paths if r['id'] in p['source_speech_IDs']],structurally_common_to_every_command_path=all(r['id'] in p['source_speech_IDs'] for p in paths)) for r in g['records']]
        groups.append(dict(block=block,source_packet=str(PACKETS[block]),source_packet_sha256=sha(PACKETS[block].read_bytes()),source_operand_order=operands,source_operand_structural_domains=dict(zip(operands,domains,strict=True)),
            structural_compositions_evaluated=evaluated,ordered_domains_andvisited_stream_sha256=digest.hexdigest(),distinct_complete_command_path_count=len(paths),distinct_complete_text_path_count=len(textpaths),
            representative_command_paths=paths,source_speech_count_distribution=dict(distribution),source_speech_memberships=memberships,opening_native_result_composition=opening,
            every_original_source_command_andparagraph_in_structural_union=True))
        total+=evaluated;allwords.update(unionspeeches)
        print('B'+str(block),'compositions',evaluated,'commandpaths',len(paths),'textpaths',len(textpaths),'speechcounts',dict(distribution),'opening-unforced-composition',opening['source_speech_count'])
    assert total==11 and len(allwords)==28
    ROOT.mkdir(parents=True);save(ROOT/'11_structural_compositions_all60_commands28_source_memberships.json',dict(
        source_controls=str(CONTROL),source_controls_sha256=sha(CONTROL.read_bytes()),source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),groups=groups,
        structural_compositions_evaluated=total,all60_original_commands_and28_source_speeches_in_structural_union=True,
        exact_native_branch_case_composition_not_proof_all_raw_results_are_attainable=True,
        distinct_effect_command_paths_retained_even_if_text_paths_identical=True,
        source_graph137_requires44_45_excludes46_46_requires137and45_not_totalchronology_oractivation=True,
        current_unforced_predicate_values_are_opening_snapshot_only_no_full_scene_selected=True,
        no_actual_gameplay_state_conditions_results_orRNG_forced=True,current_English_bodies_still_not_consulted=True,
        original_4800_resource_andA000_effect_semantics_actual_scene_font_prose_names_andrelease_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [CONTROL,GLOSS,*PACKETS.values(),Path(__file__)]}))
