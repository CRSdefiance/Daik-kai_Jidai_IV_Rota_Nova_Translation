"""Compose all branch outcomes from verified native extents, without forcing any game predicate."""
from itertools import product
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B58_source_paths_v8796')
CONTROL=Path('work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json')
GLOSS=Path('work/analysis/Hodram_next_clean_gloss_v8787/82_qualified_clean_glosses_no_unbound_gender_orFA_type.json')
FLOW=Path('work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json')
if __name__=='__main__':
    assert not ROOT.exists();control,gloss,flow=map(read,[CONTROL,GLOSS,FLOW]);group=next(g for g in control['groups'] if g['block']==58)
    source=next(g for g in gloss['groups'] if g['block']==58);commands={c['offset']:c for c in group['all_original_source_commands']}
    branches={c['offset']:c for c in group['source_relative_cases']};queries={c['offset']:c for c in group['source_raw_query_cases']}
    speech={r['source_reference']['header_offset']:r for r in source['records']};assert len(speech)==49 and len(queries)==6 and len(branches)==24
    current=NdsImage.open(control['candidate']);clean=NdsImage.open('work/clean.nds');span=flow['original_caller_span']
    assert current.read_file('/__arm9__.bin')[span['start']:span['end']]==clean.read_file('/__arm9__.bin')[span['start']:span['end']]
    assert sha(current.read_file('/__arm9__.bin')[span['start']:span['end']])==span['sha256'] and len(flow['caller_fragment_cases'])==50
    assert all(c['all_six_return_words_preserved'] and c['next_parser_r3']==(c['result'][1] if c['result'][0]==2 else c['previous_structural_value']) for c in flow['caller_fragment_cases'])
    def compose(values):
        at=min(commands);mode=0;visited=[];ids=[]
        while True:
            assert at in commands and at not in visited and len(visited)<=len(commands)
            c=commands[at];visited.append(at);word=c['word']
            if word==0:assert c['native_extent']==4 and c['whole_command_hex']=='00000000';break
            if at in queries:
                assert queries[at]['native_result'][0]==2;mode=values[at];at+=c['native_extent'];continue
            if at in branches:
                case=next(x for x in branches[at]['cases'] if x['previous_result_structural_argument']==mode)
                at=case['next_offset'];continue
            assert int.from_bytes(bytes.fromhex(c['native_result_hex'])[:4],'little')==3
            if at in speech:ids.append(speech[at]['id'])
            at+=c['native_extent']
        return dict(source_command_offsets=visited,source_speech_IDs=ids,terminal_offset=at)
    sites=sorted(queries);models=[]
    for values in product([0,1],repeat=len(sites)):
        assigned=dict(zip(sites,values,strict=True));models.append(dict(model=len(models),source_query_result_structural_arguments=assigned,**compose(assigned)))
    assert len(models)==64 and all(p['terminal_offset']==group['source_terminal']['offset'] for p in models)
    assert set(speech[r]['id'] for r in speech)=={i for p in models for i in p['source_speech_IDs']}
    membership=[dict(id=r['id'],source_reference=r['source_reference'],source_0100_ancestors=r['source_0100_ancestors'],structural_models=[p['model'] for p in models if r['id'] in p['source_speech_IDs']]) for r in source['records']]
    # For these source0200/0300 wrappers, any value other than1 has the same
    # speech inclusion as0; verify that against all five original native cases.
    for at,q in queries.items():
        first=commands[at+q['native_extent']];second=commands[first['offset']+4];outer=commands[second['offset']+4]
        assert first['word']==0x200 and second['word']==0x300 and outer['word']==0x100
        for value in [0,1,2,3,0xFFFFFFFF]:
            current_at=first['offset']
            for _ in range(3):
                if current_at not in [first['offset'],second['offset'],outer['offset']]:break
                current_at=next(x['next_offset'] for x in branches[current_at]['cases'] if x['previous_result_structural_argument']==value)
            assert (current_at==outer['offset']+4)==(value==1)
    default_values={at:q['native_result'][1] for at,q in queries.items()};default=compose(default_values)
    ROOT.mkdir(parents=True);save(ROOT/'all64_structural_paths_49utterance_memberships_unforced_opening_reference.json',dict(candidate=control['candidate'],candidate_sha256=control['candidate_sha256'],
        all64_binary_equality_to_one_classes_cover_original_five_native_branch_arguments=True,models=models,utterance_membership=membership,
        unconditional_utterances=sum(len(r['structural_models'])==64 for r in membership),conditional_utterances=sum(len(r['structural_models'])<64 for r in membership),
        unforced_current_opening_query_values=default_values,composed_current_opening_reference=default,
        repeated_equal_descriptors_not_assumed_unchanged_through_opaque_effects=True,
        each_site_mode_arguments_are_offline_composition_not_injected_predicate_results=True,
        original_caller_kind2_forwarding_kind3_mode_carry_reused_through_exact_code_andall50_cases=True,
        normal_end_resultword_not_conflated_with_interpreter_mode=True,
        opaque_effects_remain_bridged_so_composed_paths_are_not_actual_scene_reachability_orfuture_state_proof=True,
        no_query_named_as_roster_plot_oritem_condition_without_separate_source_consumer_proof=True,
        current_B54_B60_English_dialogue_bodies_unconsulted=True,new_credit=0,new_emulator_runs=0,no_ROM_orledger_change=True,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [CONTROL,GLOSS,FLOW,Path(__file__)]}))
    print('B58:64structural paths/49exactutterance memberships;'+str(sum(len(r['structural_models'])==64 for r in membership))+'unconditional/'+str(sum(len(r['structural_models'])<64 for r in membership))+'conditional. Original predicates unforced;no actualscene orcredit claim.',flush=True)
