"""Compare the original short-control stream pointer at its mapped instruction."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B197_picture_comparison_v5681e')
if __name__=='__main__':
    assert not ROOT.exists()
    evidence=Path('work/analysis/lil_B197_picture_args_v5681d/six_original_picture_calls_and_unmodified_callee_instructions.json')
    for row in read(evidence)['cases']:
        if row['word']==0x4821:continue
        first,last=[r['original_picture_boundary_calls'][0] for r in row['cases']]
        assert first['args'][:3]==last['args'][:3]
        assert first['args'][3]==0x02660000+row['old_offset'] and last['args'][3]==0x02660000+row['new_offset']
    old=Path('scripts/prove_lil_B197_relocated_controls_v5681b.py');new=Path('scripts/prove_lil_B197_relocated_controls_v5681e.py')
    target="            assert versions[0]['original_picture_boundary_calls']==versions[1]['original_picture_boundary_calls']"
    replacement="""            left,right=[v['original_picture_boundary_calls'] for v in versions]
            assert len(left)==len(right)==1
            if word==0x4821:assert left==right
            else:
                before_call,after_call=left[0],right[0]
                assert {k:v for k,v in before_call.items() if k!='args'}=={k:v for k,v in after_call.items() if k!='args'}
                assert before_call['args'][:3]==after_call['args'][:3]
                stream_base=0x02660000
                assert before_call['args'][3]==stream_base+a and after_call['args'][3]==stream_base+b
""".rstrip()
    tool=derive(old,new,{"ROOT=Path('work/analysis/lil_B197_relocated_controls_v5681b')":"ROOT=Path('work/analysis/lil_B197_relocated_controls_v5681e')",
        target:replacement,
        'original47xx_entire_word_argument_and_source_return_address_exact=True,':'original47xx_entire_word_argument_and_source_return_address_exact=True,original47xx_R3_is_exact_mapped_stream_instruction_pointer=True,'})
    before,after=[native_numbers(p.read_text(encoding='utf-8')) for p in [old,new]]
    assert not before-after and after-before==Counter({0x02660000:1})
    ROOT.mkdir(parents=True);save(ROOT/'mapped_instruction_pointer_comparison_not_control_mutation.json',dict(tool=tool,
        diagnostic=str(evidence),diagnostic_sha256=sha(evidence.read_bytes()),
        only_added_high_literal_is_existing_native_adapter_owned_stream_buffer_not_instruction_address=True,
        R3_current_and_target_exactly_follow_old_and_new_command_offsets=True,
        all_other_call_registers_descriptors_layout_return_and_callee_addresses_equal=True,
        original5681b_strict_absolute_pointer_failure_and_partial_context_preserved=True,
        no_ROM_or_command_or_native_instruction_or_result_or_snapshot_mutation=True,new_credit=0,full_goal_complete=False))
