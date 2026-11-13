"""Independent original SC1 loaders, cache, parent modes and caller census for complete B51."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
PATH='/data/SC1.DK4'
def check_loaders_and_census(data,parent,reference,result,load,require):
    loader,caller=data['loaders'],data['callers'];archive=reference.read_file(PATH);blocks=IlnkContainer.parse(archive).blocks
    require(len(blocks)==325 and loader['archive_block_counts']=={'1':325} and loader['fresh_native_whole_loads_andcache_hits']==325 and loader['fresh_initial_parent_modes']==650 and loader['original_action_count']==326,'complete original SC1 loader counts')
    for key,h in [('load_proof','load_sha256'),('parent_mode_proof','parent_mode_sha256')]:require(sha(Path(loader[key]).read_bytes())==loader[h],'underlying whole native loader proof integrity')
    loads,modes=load(loader['load_proof']),load(loader['parent_mode_proof']);ev=reference.read_file('/data/EV1.DK4')
    require(ev==parent.read_file('/data/EV1.DK4')==NdsImage.open('work/clean.nds').read_file('/data/EV1.DK4') and ev[:2]==b'VE','unaltered original EV1 actions')
    begin,end=struct.unpack_from('<2I',ev,0x4C);words=struct.unpack_from(f'<{(end-begin)//2}H',ev,96+begin)
    require(len(words)==326 and [w&4095 for w in words if (w>>12)&3==2]==list(range(325)),'original actionwords select all blockindices once')
    require(len(loads['routes'])==1 and loads['complete_SC_loads_and_cache_hits']==325 and loads['native_selected_action_cases']==326 and loads['all_native_executed_code_source_exact'],'whole loaded native source scope')
    route=loads['routes'][0];require(route['route']==1 and route['SC_path']==PATH and route['SC_sha256']==sha(archive) and route['EV_path']=='/data/EV1.DK4' and route['EV_sha256']==sha(ev),'complete native loader archive/event binding')
    require(route['bounded_action_table_body_span']==[begin,end] and route['EV_inline_offset_equals_body_end']==struct.unpack_from('<I',ev,0x5C)[0] and route['maximum_source_block_bytes']==max(map(len,blocks)),'original bounded actiontable/complete payload limits')
    require(len(route['actions'])==326,'all original null andload actions')
    for index,(word,action) in enumerate(zip(words,route['actions'],strict=True)):
        kind=(word>>12)&3;require((action['action'],action['word'],action['kind'])==(index,word,kind),'original action kind/index decode')
        if kind==0:require(action['no_script_load_or_constructor'],'original null action');continue
        number=word&4095;block=blocks[number];start,finish=struct.unpack_from('<2I',archive,8+number*4)
        require(action['native_selected_block']==number and action['complete_native_loaded_payload_bytes']==len(block) and action['payload_sha256']==sha(block) and archive[start:finish]==block,'original index/whole native payload')
        io=[dict(operation='open',requested='\\DATA\\SC1.DK4',ROM_path=PATH),dict(operation='seek',offset=4),dict(operation='read',offset=4,bytes=4),dict(operation='seek',offset=8+number*4),dict(operation='read',offset=8+number*4,bytes=8),dict(operation='seek',offset=start),dict(operation='read',offset=start,bytes=len(block)),dict(operation='close')]
        require(action['only_SDK_open_seek_read_close_bridged']==io and action['whole_native_loader_return_and_saved_register_SP_PC_ABI_pass'] and action['cache_hit_no_IO_complete_object_and_neighbor_bytes_exact'],'original loader I/O andwhole cache/ABI guards')
    cases=modes['native_handoff_and_first_read_cases'];require(len(cases)==650 and {(c['block'],c['mode']) for c in cases}=={(i,m) for i in range(325) for m in [0,1]},'all original two initial parent modes')
    for c in cases:
        block=blocks[c['block']];length=struct.unpack_from('<I',block,4)[0];first=struct.unpack_from('<H',block,8)[0]
        require(c['route']==1 and c['complete_source_block_bytes']==len(block) and c['source_block_sha256']==sha(block) and c['declared_SC_body_bytes']==length and c['stored_zero_alignment_padding_bytes']==len(block)-8-length and c['source_header_bytes_skipped']==8,'complete original parent header/payload/tail')
        require(c['native_first_word']==first and c['native_first_major_category']==(first>>13)&7 and c['original_cache_hit']==[0x02024134,0x027F0010,c['block']],'original firstcommand/cache identity')
        require(c['original_source_reads']==[dict(PC=0x0202A524,address=0x027F0020,bytes=2,read_hex=block[8:10].hex())] and c['whole_source_header_payload_cache_metadata_and_tail_guard_exact'] and c['first_instruction_pointer_and_mode_derived_by_original_parent'],'original payload-plus8 firstread/mode guards')
    arm=reference.read_file('/__arm9__.bin')
    for r in modes['executed_source_words']:require(arm[r['PC']-0x02000000:r['PC']-0x02000000+len(bytes.fromhex(r['hex']))].hex()==r['hex'],'every original parent executed instruction word')
    require(census(reference)==caller['native_call_census'] and caller['external_references_complete'],'independent shipped code caller/literal census')
    require(caller['file_path']==PATH and caller['block']==51 and caller['reference_scope_not_arbitrary_dynamic_pointer_orall_attainable_paths_proof'],'explicit single B51 source-reference scope')
    group,declared=result['groups'][0],data['relocation']['groups'][0]
    require(caller['all_command_maps']==declared['command_map'] and caller['relative_operand_maps']==declared['relative_fixups'] and caller['relocated_native_skip_cases']==declared['relocated_skip_cases'] and caller['all5_text_records']==declared['text_records'] and caller['typed_choice_records']==[],'all20 caller-selected source/current/final command maps and5record references')
    selected=next(a for a in route['actions'] if a.get('native_selected_block')==51)
    require(caller['original_selected_action']==selected and caller['original_entry_payload_offset']==8 and caller['no_interior_entry_offsets_orunmapped_nested_relative_targets'],'original blockindex entry andall nested relative targets')
    require(caller['source_event_records']==data['current']['groups'][0]['source_event_records'] and [(e['event_ID'],e['script_block'],e['must_be_completed']) for e in caller['source_event_records']]==[(51,51,[])],'event51 hasno listed prerequisite,not full eligibility orchronology')
    require(loader['parent_sha256']==caller['parent_sha256']==sha(bytes(parent.rom.save())) and loader['research_ROM_sha256']==caller['research_ROM_sha256']==loads['ROM_sha256']==modes['ROM_sha256']==sha(bytes(reference.rom.save())),'whole predecessor andtested-reference ownership for all proofs')
    prior=load(caller['exact_prior_census']);require(caller['fresh_caller_censuses']==1 and prior['native_call_census']==caller['native_call_census'],'preserved exact prior shippedcode association plus fresh B51 census')
    for key in ['all_original_EV1_actions_select_block_indices_not_interior_offsets','both_original_parent_modes_begin_payload_plus8','all_payload_cache_metadata_neighbor_guards_SP_PC_andABI_exact','original_executed_instructions_exact_only_SDK_IO_bridges','controlled_native_route_global_inputs_not_ordinary_event_activation']:
        require(loader[key],'original loader proof scope:'+key)
    return dict(native_whole_loads_cache_hits_bound=325,initial_parent_modes_bound=650,original_EV1_actions_bound=326,shipped_code_caller_census_recomputed=True,
        native_loader_cases_not_natural_optional_activation_orall_attainable_paths=True)
