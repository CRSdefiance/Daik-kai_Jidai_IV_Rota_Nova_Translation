"""Compose source paths from measured native relative results; do not force game conditions."""
from collections import Counter
from itertools import product
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_source_paths_v7978')
SOURCE=Path('work/analysis/Rafael_next_clean_v7971/complete_clean_SC0_B47_EV0_andcoverage_before_current_English.json')
CONTROL=Path('work/analysis/Rafael_B47_source_controls_v7977/source_EV0_24_relative_sites120_cases6_raw_predicates25_seeded_ends.json')
GLOSS=Path('work/analysis/Rafael_B47_clean_gloss_v7973/15_fresh_clean_glosses_complete_B37_context_before_current_English.json')
if __name__=='__main__':
    assert not ROOT.exists();source,control,gloss=map(read,[SOURCE,CONTROL,GLOSS])
    assert control['source_packet_sha256']==sha(SOURCE.read_bytes()) and control['current_B47_English_bodies_still_unread']
    g=source['groups'][0];commands={c['offset']:c for c in g['commands']}
    speeches={r['source_reference']['header_offset']:r for r in g['records']}
    relative={r['offset']:r for r in control['source_relative_cases']}
    operands=list(control['unique_raw_predicate_results'])
    assert set(operands)=={'0080ffff04fe0030','0080ffff000009a0','0080ffff000c2170','0080ffff000007a0'}
    def compose(values):
        at=8;last=0;visited=[];texts=[];steps=[]
        while at<g['clean_logical_end']:
            assert len(visited)<len(commands) and at not in visited
            c=commands[at];visited.append(at)
            if at in speeches:texts.append(speeches[at]['id'])
            if c['word']==0x8000:
                last=values[c['whole_command_hex']];steps.append(dict(offset=at,source_operand=c['whole_command_hex'],raw_result=last))
            if at in relative:
                case=next(r for r in relative[at]['cases'] if r['previous_result_structural_argument']==last)
                at=case['next_offset']
            else:at+=c['native_extent']
        assert at==g['clean_logical_end'] and visited[-1]==1280
        return dict(raw_predicate_results=values,visited_source_offsets=visited,source_speech_IDs=texts,
            source_speech_count=len(texts),original_predicate_steps=steps,
            composed_from_independently_measured_native_relative_cases_not_full_interpreter_oractual_gameplay=True)
    paths=[compose(dict(zip(operands,values,strict=True))) for values in product([0,1,2,3,0xFFFFFFFF],repeat=4)]
    assert len(paths)==625
    assert set().union(*(set(r['visited_source_offsets']) for r in paths))==set(commands)
    assert set().union(*(set(r['source_speech_IDs']) for r in paths))=={r['id'] for r in g['records']}
    short='DK4_MES_B47_R0063';both='DK4_MES_B47_R0070';janus={r['id'] for r in g['records'] if r['source_selector']==4}
    assert len(janus)==3
    for p in paths:
        ids=set(p['source_speech_IDs']);values=p['raw_predicate_results'];main=values['0080ffff000009a0']==1
        assert not {short,both}<=ids
        assert (both in ids)==(main and values['0080ffff000007a0']==1)
        assert (short in ids)==(main and values['0080ffff000007a0']!=1)
        assert ('DK4_MES_B47_R0017' in ids)==('DK4_MES_B47_R0122' in ids)==(values['0080ffff04fe0030']==1)
        assert ('DK4_MES_B47_R0092' in ids)==(main and values['0080ffff04fe0030']==1)
        assert (250 in p['visited_source_offsets'])==(main and values['0080ffff000c2170']==1)
        assert p['source_speech_count']==(14 if main else 7) if values['0080ffff04fe0030']==1 else p['source_speech_count']==(11 if main else 5)
    representative={}
    for p in paths:representative.setdefault(tuple(p['source_speech_IDs']),p)
    assert len(representative)==6
    observed={k:v[1] for k,v in control['unique_raw_predicate_results'].items()}
    opening=compose(observed);assert opening['source_speech_count']==11 and both in opening['source_speech_IDs'] and not janus&set(opening['source_speech_IDs'])
    ROOT.mkdir(parents=True)
    save(ROOT/'625_source_result_compositions_six_text_paths_two_exclusive_alternatives.json',dict(
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),source_controls=str(CONTROL),source_controls_sha256=sha(CONTROL.read_bytes()),
        source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),source_predicate_operand_order=operands,
        structural_raw_result_values=[0,1,2,3,0xFFFFFFFF],source_result_compositions=paths,representative_text_paths=list(representative.values()),
        speech_count_distribution=dict(Counter(p['source_speech_count'] for p in paths)),opening_native_result_composition=opening,
        all48_source_commands_all15_speeches_in_structural_union=True,
        R63_Ottoman_only_andR70_both_powers_mutually_exclusive=True,
        three_Janus_speeches_conditioned_by_same_exact_operand_without_assuming_natural_party_state=True,
        middle_Janus_R92_also_requires_main_advice_block=True,
        A000_at250_independently_gated_without_assigning_unproved_effect_semantics=True,
        raw_operands_bound_without_inventing_global_plot_flag_meanings=True,
        observed_opening_values_not_natural_B47_activation_oractual_11_speech_gameplay=True,
        hypothetical_result_compositions_not_source_condition_orRAM_forcing=True,
        current_B47_English_still_unread=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,GLOSS,Path(__file__)]},full_goal_complete=False))
    print('625 native-result compositions yield6 distinct text paths:5/7/11/14 speeches;R63/R70 mutually exclusive,three Janus lines conditional.Opening result composition11,not actual B47 gameplay;current English unread.')
