"""Compare all six actual scene pairs,keeping all timing/state differences as evidence."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_comparison_tools_v8821');assert not root.exists()
    source=Path('scripts/compare_Hodram_B31_B53_actual_v8743.py');text=source.read_text(encoding='utf-8')
    oldloop="""    for number,proofpath,value in [
        (31,'work/analysis/Hodram_B31_B53_actual_v8742/B31/paired_actual_dialogue_headers_flow_returns.json',1),
        (53,'work/analysis/Hodram_B31_B53_actual_v8742b/B53/paired_actual_dialogue_headers_flow_returns.json',0)]:"""
    loop="""    for number in [54,56,57,58,59,60]:
        proofpath='work/analysis/Hodram_B56_actual_v8818/B56/paired_actual_dialogue_headers_flow_returns.json' if number==56 else f'work/analysis/Hodram_B54_B60_actual_v8820/B{number}/paired_actual_dialogue_headers_flow_returns.json'
        value=1 if number==58 else 0"""
    start=text.index('        expectedIDs=');end=text.index('        reports=',start);oldexpect=text[start:end]
    expected="""        assert old['unvisited_conditional_text_IDs']==new['unvisited_conditional_text_IDs']
        assert [s['id'] for s in old['speeches']]==[s['id'] for s in new['speeches']]
        assert len(old['speeches'])=={54:4,56:3,57:8,58:31,59:7,60:10}[number]
        assert len(old['unvisited_conditional_text_IDs'])==(18 if number==58 else 0)
        assert [c['canonical_source_offset'] for c in old['command_pairs']]==[c['canonical_source_offset'] for c in new['command_pairs']]
        assert not any(c['word']==0x2100 for g in [old,new] for c in g['command_pairs'])
"""
    result=derive(source,'scripts/compare_Hodram_B54_B60_actual_v8821.py',{
        'Hodram_B31_B53_comparison_v8743':'Hodram_B54_B60_comparison_v8821',oldloop:loop,oldexpect:expected,
        'total_actual_frames=24004':'total_actual_frames=116012',
        'current_registered_V8704_andmainV4701_unchanged':'current_registered_V8778_andmainV4701_unchanged',
    })
    root.mkdir(parents=True);save(root/'source_locked_six_pair_state_comparison.json',dict(derivation=result,
        all_selected_command_signatures_results_andidentical_inputs_must_match=True,
        all_duration_UI_RNG_calendar_component_actor_andlater_RGB_differences_retained=True,
        terminalresult_value_B58one_otherfivezero_not_conflated_with_r3=True,
        all_native_addresses_andoriginal_snapshot_extractors_preserved=True,no_capture_replay_retiming_orforced_results=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
