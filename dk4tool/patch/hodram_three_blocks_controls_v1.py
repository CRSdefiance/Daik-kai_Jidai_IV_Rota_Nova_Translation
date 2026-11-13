"""Bind all native dispatch/control/entry evidence to original source and independently rebuilt bytes."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
from scripts import prove_lil_shrines_temples_controls_v3168c as catalog_base

PATH='/data/SC1.DK4'
VOICE={1:1,2:3,9:2,16:1,18:0,113:0}
CAT_ADAPTER='c72d47345156c29d6b902da0804833ddb27222278ad9b4b2940a8641528fd13e'

def check_controls(data,rows,parent,reference,rebuilt,load,require):
    controls=data['native_controls'];research=data['relocation'];source=data['source_controls'];packet=data['current']
    arm=parent.read_file('/__arm9__.bin');cleanarm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    require(sha(arm)=='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b' and reference.read_file('/__arm9__.bin')==arm,'exact registered name/runtime dependency')
    voices=data['native_names']['native_six_source_voices']['rows'];require({v['source_selector']:v['original_voice_class'] for v in voices}==VOICE,'six source-proven static voice classes')
    actor_objects={r['actor_ID']:r['actor_object'] for r in data['native_names']['native_twelve_progressive_andfull_getters']['rows']}
    adapter=controls['source_owned_dispatch_adapters']['bind_current_catalog'];require(sha(adapter.encode())==CAT_ADAPTER,'source-locked current catalogue binder')
    ns={**catalog_base.__dict__,'SOURCE':Path('work/analysis/Hodram_current_review_binding_v8272/28_exact_current_refs_registered_name_dependency_andnative_reuse.json'),'route':1,'route_mask':2}
    exec(compile(adapter,__file__+'::original-current-catalogue-binding','exec'),ns);lookup,binding=ns['bind_current_catalog'](parent)
    require(binding==controls['registered_current_catalogue_binding'] and len(binding['records'])==467,'all467 native catalogue keys/targets/routes/calls')
    require(len(controls['final_dispatches'])==28 and {d['id'] for d in controls['final_dispatches']}=={r['id'] for r in rows},'28 unique final static dispatches')
    for d in controls['final_dispatches']:
        row=next(r for r in rows if r['id']==d['id']);g=next(g for g in rebuilt['groups'] if g['block']==row['block']);ref=next(r for r in g['text_records'] if r['id']==row['id']);selector=row['source_selector'];raw=bytes.fromhex(ref['target_hex'])
        require((d['block'],d['final_offset'],d['source_selector'],d['resolved_actor_ID'],d['source_voice_class'])==(row['block'],ref['new_offset'],selector,selector,VOICE[selector]),'source-qualified final actor/voice/body offset')
        require(d['final_stored_hex']==raw.hex()==row['final_stored_hex'] and raw not in lookup and raw[1:] not in lookup and d['registered_catalog_match'] is None,'literal final body hasno catalogue substitution')
        require(not d['FE_original_null_actor_calls'] and d['all4MiB_actor_role_RNG_input_and_ABI_guards_exact'],'complete static progressive dispatch andABI scope')
        b=d['boundaries'];require(len(b)==2 and b[0]==dict(boundary=0x020940B0,kind='unexecuted-UI-preparation'),'original UI-preparation boundary')
        require(b[1]==dict(boundary=0x02054020,kind='unexecuted-progressive-body',actor_object=actor_objects[selector],FE_incidental_r1=None,text_hex=raw[1:].hex()),'complete original progressive actor/text boundary')
    expected=[];relative_cases=0;query_sites=[]
    for fresh,declared,prior in zip(rebuilt['groups'],research['groups'],packet['groups'],strict=True):
        number=fresh['block'];require(number==declared['block']==prior['block'],'native control group identity')
        for sourcecmd,oldcmd,targetcmd,cm in zip(prior['all_source_commands'],fresh['all_current_commands'],fresh['all_target_commands'],declared['command_map'],strict=True):
            word=sourcecmd['word'];require(word==oldcmd['word']==targetcmd['word'],'source/current/final native control identity')
            if word in [0x4000,0x100,0x200,0x300,0x400]:continue
            require(sourcecmd['whole_command_hex']==oldcmd['whole_command_hex']==targetcmd['whole_command_hex'],'opaque source control/effect/query/end bytes')
            expected.append(dict(block=number,source_offset=sourcecmd['offset'],previous_offset=oldcmd['offset'],target_offset=targetcmd['offset'],word=word,source_current_target_command_hex=sourcecmd['whole_command_hex']))
            if word==0x8000:query_sites.append((number,sourcecmd,oldcmd,targetcmd))
        require(len(declared['relocated_skip_cases'])==len(fresh['relative_fixups']),'all relocated relative evidence sites')
        for fix,probe in zip(fresh['relative_fixups'],declared['relocated_skip_cases'],strict=True):
            require((probe['offset'],probe['word'],probe['span'])==(fix['new_offset'],fix['word'],fix['target_span']),'source-qualified relocated native relative probe')
            require([c['previous_result_structural_argument'] for c in probe['cases']]==[0,1,2,3,0xFFFFFFFF],'five explicit structural previous results')
            for c in probe['cases']:
                prev=c['previous_result_structural_argument'];word=fix['word'];taken=word==0x100 or word==0x200 and prev==0 or word==0x300 and prev==1 or word==0x400 and prev==2
                require(c['taken']==taken and c['native_extent']==4+(fix['target_span'] if taken else 0) and c['next_offset']==fix['new_offset']+c['native_extent'] and c['all4MiB_ABI_owner_input_output_andcanary_guards_exact'],'every original relative result/extent/endpoint/guard')
                relative_cases+=1
        end=next(e for e in controls['normal_end_cases_exact_reused'] if e['block']==number);src=next(g for g in source['groups'] if g['block']==number)
        require(end['target_terminal']==fresh['all_target_commands'][-1] and end['source_andcurrent_same_four_byte_end_exact_reuse']==src['normal_seeded_ends'] and end['target_cases_exact_reuse']==declared['target_seeded_normal_ends'],'exact source/current reused andtarget seeded ends')
        for cases,terminal in [(end['source_andcurrent_same_four_byte_end_exact_reuse'],src['source_terminal']),(end['target_cases_exact_reuse'],fresh['all_target_commands'][-1])]:
            require(len(cases)==25 and {(c['previous_result'],c['initial_value_word']) for c in cases}=={(a,b) for a in [0,1,2,3,0xFFFFFFFF] for b in [0,1,2,3,0xFFFFFFFF]},'all25 native end seed combinations')
            for c in cases:
                require(c['source_offset']==terminal['offset'] and c['source_command_hex']=='00000000' and c['native_extent']==4 and c['native_result']==[0,c['initial_value_word'],0,0,0,0],'fourbyte normal end retains complete value word')
                require(not c['flagged_terminal'] and c['no_leading_or_post_four_byte_payload_read'] and c['all4MiB_owner_input_ABI_output_and_length_guards_exact'],'normal-end source read andABI guards')
                require(all(0<=r['relative_offset'] and r['relative_offset']+r['bytes']<=4 for r in c['source_operand_reads']),'no native reads outside full terminal')
    require(expected==controls['original_nonrelative_nontext_control_maps'] and len(expected)==24 and relative_cases==40,'all24 nonrelative controls/40relative native cases')
    require(controls['source_seeded_ends_reused']==controls['target_seeded_ends_reused']==75 and controls['no_fresh_seeded_end_calls'],'explicit150 reused endcases,no false new execution credit')
    require(len(query_sites)==len(controls['raw_predicates_andqueries'])==2 and controls['fresh_raw_native_evaluations']==6,'two original raw sites/six recorded native evaluations')
    for (number,a,b,c),q in zip(query_sites,controls['raw_predicates_andqueries'],strict=True):
        require((q['block'],q['source_offset'],q['current_offset'],q['target_offset'])==(number,a['offset'],b['offset'],c['offset']),'complete raw query source/current/target reference')
        require([case['version'] for case in q['cases']]==['clean','current','target'] and q['raw_results_not_boolean_menu_orpath_attainability'],'raw query versions andnonboolean scope')
        sourcecase=next(x for x in source['source_raw_predicates_andqueries'] if x['block']==number and x['offset']==a['offset'])
        require(sourcecase['native_result']==[2,0 if number==137 else 1,0,0,0,0],'source-proven ordinary captain1 raw query result')
        for case,command in zip(q['cases'],[a,b,c],strict=True):
            require(case['offset']==command['offset'] and case['word']==0x8000 and case['source_command_hex']==command['whole_command_hex'] and case['native_extent']==8 and case['native_result']==sourcecase['native_result'],'source-qualified complete raw evaluator result')
            require(not case['original_event_completion_calls'] and case['sole_scratch_restore_recovers_all4MiB_exact'] and case['all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact'] and case['no_predicate_or_event_flag_forced'],'raw evaluator original state/ABI/scratch guards')
            writes=case['original_unaligned_operand_read_scratch_writes'];require(len(writes)==(1 if case['offset']%4 else 0),'native unaligned operand scratch ownership')
            for write in writes:require(write['address']==case['source_owned_scratch_address'] and write['size']==4 and write['value']==int.from_bytes(bytes.fromhex(command['whole_command_hex'])[4:8],'little'),'unaligned scratch contains original raw operand')
    require(len(controls['picture_andhide_boundary_cases'])==2,'original4800/4700 boundary pair')
    fresh46=next(g for g in rebuilt['groups'] if g['block']==46)
    for word,case,address,extent in zip([0x4800,0x4700],controls['picture_andhide_boundary_cases'],[0x02028A64,0x02028A8C],[4,2],strict=True):
        command=next(c for c in fresh46['all_target_commands'] if c['word']==word)
        require(case['block']==46 and case['source_offset']==command['offset'] and case['source_command_hex']==command['whole_command_hex'] and case['native_extent']==extent and case['native_result']==[3,0,0,0,0,0],'source-qualified original item/hide dispatch')
        calls=case['original_picture_boundary_calls'];require(len(calls)==1 and calls[0]['address']==address and calls[0]['resource_body_unexecuted'] and case['resource_body_and_selected_scene_unexecuted'] and case['all4MiB_owner_input_ABI_output_and_length_guards_exact'],'bounded native item/hide probe scope')
        require(calls[0]['descriptor']==([0,181,1,5] if word==0x4800 else None) and calls[0]['layout']==([0,0,0] if word==0x4800 else None),'original4800 layout0 and4700 distinct from4821/4720')
    picture=data['source_picture'];require(picture['item_ID']==181 and picture['metadata_field']==0x11F308 and picture['current_English']=='Red Dye' and picture['source_Japanese']=='紅色の顔料','exact original item181 source/current identity')
    at=picture['metadata_field'];require(cleanarm[at:at+24].hex()==picture['clean_metadata_hex'] and arm[at:at+24].hex()==picture['current_metadata_hex'] and cleanarm[at+4:at+24]==arm[at+4:at+24],'original item metadata andunowned fields')
    for prefix,code in [('source',cleanarm),('current',arm)]:
        ptr=picture[prefix+'_name_pointer'];raw=bytes.fromhex(picture[prefix+'_terminated_hex']);require(struct.unpack_from('<I',code,at)[0]==ptr and code[ptr-0x02000000:ptr-0x02000000+len(raw)]==raw and raw[-1]==0,'complete source/current terminated item name')
    require(controls['full_opaque_A000_picture_resource_hide_UI_bodies_not_executed_bythis_native_boundary_probe'] and controls['ordinary_opening_raw_queries_not_natural_scene_activation_orforced_state'],'native probes do not claim fullscene oractivation')
    return dict(final_dispatches=28,nonrelative_controls=24,relative_native_cases=40,raw_native_evaluations_bound=6,reused_source_target_seeded_ends_bound=150,
        original4800_descriptor=[0,181,1,5],original4800_layout=[0,0,0],original4700_hide_verified=True,full_resource_andhide_actual_scope_in_saved_scene_proofs=True)

def check_loaders_and_census(data,parent,reference,result,load,require):
    loader,caller=data['native_loader'],data['native_caller'];archive=reference.read_file(PATH);blocks=IlnkContainer.parse(archive).blocks
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
    require(len(caller['groups'])==3 and caller['source_reference_scope_not_arbitrary_dynamic_pointer_orall_attainable_paths_proof'],'explicit source-reference census scope')
    for group,fresh,declared in zip(caller['groups'],result['groups'],data['relocation']['groups'],strict=True):
        require(group['block']==fresh['block']==declared['block'] and group['all_command_maps']==declared['command_map'] and group['relative_operand_maps']==declared['relative_fixups'] and group['relocated_native_skip_cases']==declared['relocated_skip_cases'] and group['reviewed_text_records']==declared['text_records'],'all caller-selected command/relative/record maps')
        selected=next(a for a in route['actions'] if a.get('native_selected_block')==fresh['block'])
        require(group['original_selected_action']==selected and group['original_entry_payload_offset']==8 and group['no_interior_entry_offset'],'original blockindex entry,not interior offset')
    return dict(native_whole_loads_cache_hits_bound=325,initial_parent_modes_bound=650,original_EV1_actions_bound=326,shipped_code_caller_census_recomputed=True,
        native_loader_cases_not_natural_optional_activation_orall_attainable_paths=True)
