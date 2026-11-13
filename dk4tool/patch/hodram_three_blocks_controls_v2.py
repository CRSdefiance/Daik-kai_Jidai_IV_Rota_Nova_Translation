"""Retain v1's detailed checks; also reject contradictory loader/census summaries and ownership."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_three_blocks_controls_v1 import check_controls
from dk4tool.patch.hodram_three_blocks_controls_v1 import check_loaders_and_census as original_check

def check_loaders_and_census(data,parent,reference,result,load,require):
    loader,caller=data['native_loader'],data['native_caller']
    for flag in ['all_original_EV1_actions_select_block_indices_not_interior_offsets','both_original_parent_modes_begin_payload_plus8',
        'all_payload_cache_metadata_neighbor_guards_SP_PC_andABI_exact','original_executed_instructions_exact_only_SDK_IO_bridges',
        'controlled_native_route_global_inputs_not_ordinary_event_activation']:
        require(loader[flag] is True,'loader declared guards andcontrolled-native scope:'+flag)
    for flag in ['all_shipped_decoded_units_andwhole_ARM9_components_byte_exact_to_registered_parent',
        'only_original24070_interpreter_call_no_literal_alias','all_original_EV1_block_indices325_loads650_parent_modes_verified',
        'all60_source_current_target_commands8_relative_sites28_complete_preambles_bound',
        'no_interior_entries_unmapped_nested_targets_orunowned_component_changes','exact_code_census_reuse_not_a_second_fresh_census',
        'source_reference_scope_not_arbitrary_dynamic_pointer_orall_attainable_paths_proof']:
        require(caller[flag] is True,'caller declared source andscope guards:'+flag)
    loads,modes=load(loader['load_proof']),load(loader['parent_mode_proof'])
    require(loads['ROM_sha256']==modes['ROM_sha256']==loader['research_ROM_sha256']==caller['research_ROM_sha256']==sha(bytes(reference.rom.save())),
        'all loader/census proofs belong toexact approved reference ROM')
    require(loader['parent_sha256']==caller['parent_sha256']==sha(bytes(parent.rom.save())),'loader/census exact predecessor ownership')
    prior=load(caller['exact_reused_same_complete_code_census'])
    require(sha(Path(caller['exact_reused_same_complete_code_census']).read_bytes())==caller['exact_reused_same_complete_code_census_sha256'] and
        prior['native_call_census']['research']==caller['native_call_census'] and caller['fresh_caller_censuses']==1,'one fresh andexact reused complete-code census association')
    return original_check(data,parent,reference,result,load,require)
