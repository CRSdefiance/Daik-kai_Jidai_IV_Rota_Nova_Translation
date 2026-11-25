"""Derive complete whole-archive loader/caller production reader for single B49 exchange."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B49_loader_tools_v8442')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('dk4tool/patch/hodram_outcomes_loaders_v1.py');text=source.read_text('utf8')
    a=text.index("    require(len(caller['groups'])");b=text.index('    return dict(',a)
    tail='''    require(caller['file_path']==PATH and caller['block']==49 and caller['reference_scope_not_arbitrary_dynamic_pointer_orall_attainable_paths_proof'],'explicit single B49 source-reference scope')
    group,declared=result['groups'][0],data['relocation']['groups'][0]
    require(caller['all_command_maps']==declared['command_map'] and caller['relative_operand_maps']==declared['relative_fixups'] and caller['relocated_native_skip_cases']==declared['relocated_skip_cases'] and caller['all14_text_records']==declared['text_records'] and caller['typed_choice_records']==declared['choice_commands'],'all36 caller-selected source/current/final command maps and16record references')
    selected=next(a for a in route['actions'] if a.get('native_selected_block')==49)
    require(caller['original_selected_action']==selected and caller['original_entry_payload_offset']==8 and caller['no_interior_entry_offsets_orunmapped_nested_relative_targets'],'original blockindex entry andall nested relative targets')
    require(caller['source_event_records']==data['current']['groups'][0]['source_event_records'] and [(e['event_ID'],e['script_block'],e['must_be_completed']) for e in caller['source_event_records']]==[(49,49,[48])],'event49 original prerequisite48,not full eligibility orchronology')
    require(loader['parent_sha256']==caller['parent_sha256']==sha(bytes(parent.rom.save())) and loader['research_ROM_sha256']==caller['research_ROM_sha256']==loads['ROM_sha256']==modes['ROM_sha256']==sha(bytes(reference.rom.save())),'whole predecessor andtested-reference ownership for all proofs')
    prior=load(caller['exact_prior_census']);require(caller['fresh_caller_censuses']==1 and prior['native_call_census']==caller['native_call_census'],'preserved exact prior shippedcode association plus fresh B49 census')
    for key in ['all_original_EV1_actions_select_block_indices_not_interior_offsets','both_original_parent_modes_begin_payload_plus8','all_payload_cache_metadata_neighbor_guards_SP_PC_andABI_exact','original_executed_instructions_exact_only_SDK_IO_bridges','controlled_native_route_global_inputs_not_ordinary_event_activation']:
        require(loader[key],'original loader proof scope:'+key)
'''
    result=derive(source,'dk4tool/patch/hodram_B49_loaders_v1.py',{text[a:b]:tail,'for B47/B48.':'for complete B49.'})
    ROOT.mkdir(parents=True);save(ROOT/'derivation.json',dict(derivation=result,all_original_instruction_addresses_cache_layouts_native_sizes_andmultiplicity_preserved=True,new_credit=0))
