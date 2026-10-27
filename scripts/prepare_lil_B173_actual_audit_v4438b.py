"""Correct actual VM descriptor checks;isolated parser outputs are a distinct scope."""
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__=='__main__':
    derive('scripts/audit_lil_B173_actual_v4438.py','scripts/audit_lil_B173_actual_v4438b.py',{
        'lil_B173_actual_v4438':'lil_B173_actual_v4438b',
        "selected[-1]['result_words']==[0,0]":"selected[-1]['result_words']==[0,result]",
        "row['result_words']==[3,0]":"row['result_words']==[3,result]",
        "effect['result_words']==[3,0]":"effect['result_words']==[3,0 if effect['original_source_offset']==720 else result]",
        'source_packed_predicate_and_A000_semantics_not_inferred=True,actual_source_event173_not_selected=True,':'source_packed_predicate_and_A000_semantics_not_inferred=True,actual_source_event173_not_selected=True,\n        actual_result_words_are_player_descriptor_command_type_and_persistent_VM_last_result=True,\n        original_type3_and_end_preserve_post_predicate_last_result_not_isolated_parser_output=True,\n        failed_initial_zero_descriptor_assumption_preserved=True,',
    })
    print('Prepared corrected actual VM last-result checks;original failed audit retained;no ROM,prose or ledger mutation.')
