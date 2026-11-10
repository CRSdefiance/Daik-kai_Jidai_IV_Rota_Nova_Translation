"""Preserve the source's distinct state1 terminator without weakening ordinary end guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B212_flagged_end_tools_v6603b')
if __name__=='__main__':
    assert not ROOT.exists()
    anchor='    adapter=checked_text(inspect.getsource(prior.choice_vm),'
    addition='''    end_adapter=checked_text(inspect.getsource(end_case),{
        'value=block[offset:offset+4];assert value==bytes(4)':"value=block[offset:offset+4];assert value in [bytes(4),bytes.fromhex('00000080')]",
        'assert decoded==[0,0,0,0,0,0] and extent==4 and reads':"flagged=value==bytes.fromhex('00000080');assert decoded==[int(flagged),0,0,0,0,0] and extent==4 and reads",
        'source_operand_reads=reads,':'source_operand_reads=reads,source_high_bit_terminal_return=flagged,'})
    end_env=dict(end_case.__globals__);exec(compile(end_adapter,__file__+'::source-state1-end','exec'),end_env)
'''
    proof=derive('scripts/prove_lil_B212_controls_v6603.py','scripts/prove_lil_B212_controls_v6603b.py',{'lil_B212_controls_v6603':'lil_B212_controls_v6603b',anchor:addition+anchor,"**end_case(arm,block,c['offset'],previous)":"**end_env['end_case'](arm,block,c['offset'],previous)",'assert len(effects)==2 and len(ends)==30;ROOT.mkdir(parents=True)':"assert len(effects)==2 and len(ends)==30 and all(c['native_result']==([1,0,0,0,0,0] if c['source_offset']==664 else [0,0,0,0,0,0]) for c in ends);ROOT.mkdir(parents=True)",'guarded_source_current_end_cases=ends,':'guarded_source_current_end_cases=ends,source_owned_exact_flagged_end_adapter=end_adapter,source_Zhao_end664_hex_00000080_returns_state1_value0=True,source_No152_Guan_Zhuge878_zero_end_returns_state0=True,flagged_termination_full_caller_effect_not_inferred=True,'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_exact_terminal_flag_adapter.json',dict(proof=proof,failed_zero_only_predecessor_preserved='scripts/prove_lil_B212_controls_v6603.py',source_Zhao_terminator='00000080',source_other_terminators='00000000',native_source_2A454_2A488_reads_high_flag_and_sets_state1_value0=True,no_source_byte_control_extent_operand_guard_or_result_mask_waived=True,actual_caller_return_effect_semantics_pending=True,new_ROMs=0,new_review_credit=0,full_goal_complete=False))
