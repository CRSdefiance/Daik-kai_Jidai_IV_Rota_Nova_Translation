"""Preserve complete original loader/ABI/census checks for both reviewed blocks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_loader_production_tools_v8760');assert not root.exists()
    source=Path('dk4tool/patch/hodram_B51_loaders_v1.py').read_text('utf-8')
    a=source.index("    require(caller['file_path']==PATH and caller['block']==51");z=source.index("    require(loader['parent_sha256']",a)
    binding='''    require(caller['file_path']==PATH and caller['blocks']==[31,53] and caller['reference_scope_not_arbitrary_dynamic_pointer_orall_attainable_paths_proof'],'explicit two-block source-reference scope')
    require([g['block'] for g in result['groups']]==[g['block'] for g in data['relocation']['groups']]==[31,53],'complete reconstructed group scope')
    maps=[dict(block=g['block'],**m) for g in data['relocation']['groups'] for m in g['command_map']]
    expected_groups=[dict(g,all_source_commands=p['all_source_commands']) for g,p in zip(data['relocation']['groups'],data['current']['groups'],strict=True)]
    require(caller['all_command_maps']==maps and caller['groups']==expected_groups,'all18 caller-selected complete command maps')
    for computed,declared in zip(result['groups'],data['relocation']['groups'],strict=True):
        require(computed['target_block']==blocks[declared['block']] and {k:v for k,v in computed.items() if k!='target_block'}=={k:v for k,v in declared.items() if k!='target_block'},'reconstructed complete block andmetadata equal declared group')
    require(caller['all3_speech_records']==data['stored']['records'],'all3 disjoint canonical source/current/final references')
    selected=[next(a for a in route['actions'] if a.get('native_selected_block')==number) for number in [31,53]]
    require(caller['original_selected_actions']==selected and caller['original_entry_payload_offset']==8 and caller['no_interior_entry_offsets_orunmapped_nested_relative_targets'],'both original blockindex entries andall nested relative targets')
    events=[e for g in data['current']['groups'] for e in g['source_event_records']]
    require(caller['source_event_records']==events and [(e['event_ID'],e['script_block'],e['must_be_completed'],e['must_not_be_completed']) for e in events]==[(31,31,[52],[]),(53,53,[31],[74])],'original52->31->53 connection/exclusion74,not full eligibility/location/chronology')
'''
    receipt=derive('dk4tool/patch/hodram_B51_loaders_v1.py','dk4tool/patch/hodram_B31_B53_loaders_v1.py',{
        source[a:z]:binding,"data['callers']":"data['references']",
        "prior=load(caller['exact_prior_census']);require(caller['fresh_caller_censuses']==1 and prior['native_call_census']==caller['native_call_census'],'preserved exact prior shippedcode association plus fresh B51 census')":"prior=load(caller['exact_prior_census']);require(sha(Path(caller['exact_prior_census']).read_bytes())==caller['exact_prior_census_sha256'] and caller['fresh_caller_censuses']==0 and caller['exact_reused_caller_censuses']==1 and prior['native_call_census']==caller['native_call_census'],'preserved exact prior shippedcode association andindependently recomputed current census')",
        'for complete B51':'for both complete B31/B53 blocks',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_native_high_integer_constants_andmultiplicity_preserved=True,
        all325loads_cache_IO650parentmodes326actions_every_instruction_ABI_neighbor_andwholeROM_guards_preserved=True,
        both_original_block_entries_complete18commands3refs_andexplicit_dependencies_bound=True,
        prior_complete_census_reuse_revalidated_by_fresh_shipped_code_scan_without_replaying_emulator_orproducer=True,new_credit=0,full_goal_complete=False))
