"""Compose source speech membership from already executed native branch cases.

Assignments are offline structural arguments, never injected game conditions.
Each query site varies independently, including repeated descriptors. This does
not establish which combinations are attainable or survive opaque effects.
"""
from itertools import product
import json
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/Hodram_B61_B70_source_paths_v8883')
CONTROL=Path('work/analysis/Hodram_B61_B70_source_controls_v8878/source_controls.json')
GLOSS=Path('work/analysis/Hodram_B61_B70_clean_gloss_v8877/224_complete_clean_first_meanings_all_ten_exchanges_before_current_English.json')
FLOW=Path('work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json')

if __name__=='__main__':
    assert not ROOT.exists()
    control,gloss,flow=map(read,[CONTROL,GLOSS,FLOW])
    assert control['current_B61_B70_English_dialogue_bodies_still_unconsulted']
    current=NdsImage.open(control['candidate']);clean=NdsImage.open('work/clean.nds')
    assert sha(Path(control['candidate']).read_bytes())==control['candidate_sha256']
    span=flow['original_caller_span']
    arm,ja=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    assert arm[span['start']:span['end']]==ja[span['start']:span['end']]
    assert sha(arm[span['start']:span['end']])==span['sha256'] and len(flow['caller_fragment_cases'])==50
    assert all(c['all_six_return_words_preserved'] and c['next_parser_r3']==(c['result'][1] if c['result'][0]==2 else c['previous_structural_value']) for c in flow['caller_fragment_cases'])
    groups=[]
    for group,source in zip(control['groups'],gloss['groups']):
        assert group['block']==source['block'] and group['clean_block_sha256']==source['source_block_sha256']
        commands={c['offset']:c for c in group['all_original_source_commands']}
        branches={c['offset']:c for c in group['source_relative_cases']}
        queries={c['offset']:c for c in group['source_raw_query_cases']}
        speech={r['source_reference']['header_offset']:r for r in source['records']}
        for b in branches.values():
            assert {c['previous_result_structural_argument'] for c in b['cases']}=={0,1,2,3,0xFFFFFFFF}
            assert all(c['all4MiB_ABI_owner_input_output_andcanary_guards_exact'] for c in b['cases'])
        def compose(values):
            at=min(commands);mode=0;visited=[];ids=[]
            while True:
                assert at in commands and at not in visited and len(visited)<=len(commands)
                c=commands[at];visited.append(at)
                if c['word']==0:
                    assert c==group['source_terminal'] and c['native_extent']==4 and c['whole_command_hex']=='00000000'
                    break
                if at in queries:
                    assert queries[at]['native_result'][0]==2
                    mode=values[at];at+=c['native_extent'];continue
                if at in branches:
                    case=next(x for x in branches[at]['cases'] if x['previous_result_structural_argument']==mode)
                    at=case['next_offset'];continue
                assert int.from_bytes(bytes.fromhex(c['native_result_hex'])[:4],'little')==3
                if at in speech:ids.append(speech[at]['id'])
                at+=c['native_extent']
            return dict(source_command_offsets=visited,source_speech_IDs=ids,terminal_offset=at)
        sites=sorted(queries);models=[]
        binary={}
        for values in product([0,1],repeat=len(sites)):
            assigned=dict(zip(sites,values,strict=True));row=dict(model=len(models),source_query_result_structural_arguments=assigned,**compose(assigned))
            binary[values]=row;models.append(row)
        assert set(r['id'] for r in speech.values())=={i for p in models for i in p['source_speech_IDs']}
        checked=0;digests=[]
        for values in product([0,1,2,3,0xFFFFFFFF],repeat=len(sites)):
            assigned=dict(zip(sites,values,strict=True));path=compose(assigned)
            equivalent=binary[tuple(int(v==1) for v in values)]
            assert path['source_speech_IDs']==equivalent['source_speech_IDs'] and path['terminal_offset']==equivalent['terminal_offset']
            digests.append(sha(json.dumps(dict(arguments=values,path=path),sort_keys=True).encode()))
            checked+=1
        assert checked==5**len(sites)
        memberships=[dict(id=r['id'],source_reference=r['source_reference'],source_0100_ancestors=r['source_0100_ancestors'],
            structural_models=[p['model'] for p in models if r['id'] in p['source_speech_IDs']]) for r in source['records']]
        default={at:q['native_result'][1] for at,q in queries.items()}
        assert all(v in [0,1,2,3,0xFFFFFFFF] for v in default.values())
        groups.append(dict(block=group['block'],source_block_sha256=group['clean_block_sha256'],binary_models=models,
            five_native_argument_compositions_checked=checked,five_argument_composition_receipt_sha256=sha(''.join(digests).encode()),
            utterance_membership=memberships,unconditional_utterances=sum(len(m['structural_models'])==len(models) for m in memberships),
            conditional_utterances=sum(len(m['structural_models'])<len(models) for m in memberships),
            unforced_current_opening_query_values=default,composed_current_opening_reference=compose(default)))
        print('SOURCE_MEMBERSHIP',group['block'],'models',len(models),'five-argument checks',checked,
            'unconditional',groups[-1]['unconditional_utterances'],'conditional',groups[-1]['conditional_utterances'],flush=True)
    assert len(groups)==10 and sum(len(g['utterance_membership']) for g in groups)==224
    ROOT.mkdir(parents=True)
    save(ROOT/'all224_source_memberships_original_branch_cases.json',dict(candidate=control['candidate'],candidate_sha256=control['candidate_sha256'],
        groups=groups,original_caller_span=span,all50_kind2_forwarding_kind3_mode_carry_cases_bound_by_exact_clean_current_code=True,
        all_five_tested_native_arguments_have_same_speech_membership_as_equal_to_one_classes=True,
        command_paths_for_other_arguments_not_claimed_identical=True,
        assignments_are_offline_compositions_not_injected_game_predicates_oractual_scene_activation=True,
        repeated_descriptors_independent_not_assumed_unchanged_through_opaque_effects=True,
        no_attainability_chronology_eligibility_roster_plot_orfuture_state_claim=True,
        normal_end_persistent_result_word_not_conflated_with_interpreter_mode=True,
        current_B61_B70_English_dialogue_bodies_unconsulted=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [CONTROL,GLOSS,FLOW,Path(__file__)]}))
