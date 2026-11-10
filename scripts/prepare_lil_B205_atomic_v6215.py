"""Derive semantic rejection controls for B205's actual scopes,source names and two-byte target tail."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B205_atomic_tools_v6215')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/validate_lil_B204_atomic_v6150b.py','scripts/validate_lil_B205_atomic_v6216.py',{
        'B204':'B205','lil_B204_editorial_v2':'lil_B205_editorial_v1','seal_lil_B204_references_v6148':'seal_lil_B205_references_v6213','prepare_lil_B204_references_v6135':'prepare_lil_B205_references_v6200','atomic_v6150b':'atomic_v6216','reference_approval_v6148':'reference_approval_v6213','verification_v6134':'verification_v6198',
        "len(proof['changed_records'])==20":"len(proof['changed_records'])==17",'Positive20-object':'Positive17-object','positive_records=20':'positive_records=17','Atomic20-object':'Atomic17-object',
        'research_logical_end=1342':'research_logical_end=576','source_bytes=1310':'source_bytes=618','actual_unique_speech_panels=19':'actual_unique_speech_panels=16',
        "('lost-timing-difference',PROOFS['actual_proof'],lambda v:next(iter(v['source_English_command_timing_differences'].values())).pop())":"('invented-timing-witness',PROOFS['actual_proof'],lambda v:v['source_English_command_timing_differences'].append(dict(source=v['versions'][0]['command_pairs'][0],English=v['versions'][1]['command_pairs'][0])))",
        "('lost-RNG-witness',PROOFS['actual_proof'],lambda v:next(iter(v['source_English_command_RNG_differences'].values())).pop())":"('invented-RNG-witness',PROOFS['actual_proof'],lambda v:v['source_English_command_RNG_differences'].append(dict(source=v['versions'][0]['command_pairs'][0],English=v['versions'][1]['command_pairs'][0])))",
        "v['same_frame_comparisons']['current-Japanese-V6110-prefix-before-menu'][0]":"v['same_frame_comparisons'][0]",
        'no_whole_state_equivalence_claim_from_cross_build_getter_comparison':'no_whole_state_or_future_sequence_equivalence_claim',
        "('lost-later-prompt-difference',doc['postscene_native_state_proof'],lambda v:v['later_source_English_RGB_differences'].pop())":"('lost-postscene-RGB-sample',doc['postscene_native_state_proof'],lambda v:v.update(later_whole_RGB_equal_samples=97))",
        "('claimed-equal-PRNG',doc['postscene_native_state_proof'],lambda v:v.update(final_PRNG_equal=True))":"('claimed-unequal-PRNG',doc['postscene_native_state_proof'],lambda v:v.update(final_PRNG_equal=False))",
        'actual_old_source_and_English_ARM9_hashes_differ':'source_and_English_identical_ARM9_COMMON_and_input_schedule',
        'all6_source_current_target_control_leaves':'all8_source_current_target_control_leaves',"{'124':'Captain'}":"{'15':'Captain Angelo'}","{'130':'King'}":"{'2':'Queen Lil'}","{'145':'Aunt'}":"{'2':'Aunt Lil'}","{'11':'Jam Jack Ludwyan'}":"{'15':'Brother Angelo'}",'fresh5_actor_names':'fresh2_actor_names','all20_five_gates_approved':'all17_five_gates_approved',
        'invented-FI-in-letter':'invented-FI-in-echo-or-sound','target_alignment_tail_bytes=2':'target_alignment_tail_bytes=0',
        "('lost-current-notice',PROOFS['representative_proof'],lambda v:v.update(current_Shachihoko_notice5530_whole_frame_equal_to_current_source=False))":"('lost-current-notice',doc['postscene_native_state_proof'],lambda v:v.update(generated_Rainbow_Parrot_notice_same_frame_whole_RGB_equal_at7150=False))",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_semantic_negative_derivation.json',dict(tool=tool,no_ROM_registry_or_ledger_change=True,all_native_addresses_assembler_and_pre_mutation_test_guards_preserved=True,full_goal_complete=False));print('B205 atomic positive/semantic rejection runner prepared;exact observed timing/RNG/RGB,name and target-tail mutations.')
