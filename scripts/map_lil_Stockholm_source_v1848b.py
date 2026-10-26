"""Complete original B27 clean/current inventory and native actor/macro context."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Stockholm_source_v1848b')
ROM=Path('out/all_routes_combined_v1841_candidate.nds')
CONTEXT=Path('work/analysis/lil_destination_contexts_v1847/source_destinations_and_original_random_query_classification.json')
INV=Path('work/analysis/lil_after_Amsterdam_inventory_v1846/all336_states_and_original_town_eligibility.json')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    context=read(CONTEXT);inv=read(INV);assert context['London26_and_Stockholm27_predicates_accept_offline_destination_inputs']
    image=NdsImage.open(ROM);clean=NdsImage.open('work/clean.nds');arm=image.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes())==context['candidate_sha256']==inv['candidate_sha256']
    source=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[27]
    current=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[27]
    old,speeches=inventory(clean.read_file('/__arm9__.bin'),source);now,current_speeches=inventory(arm,current)
    assert len(old)==len(now)==102 and len(speeches)==len(current_speeches)==51
    shape=lambda rs:[(r['word'],r['offset'],r['native_extent'],r['ancestor_0100_offsets'])for r in rs]
    assert shape(old)==shape(now)
    raw=Path(inv['snapshot']).read_bytes();assert sha(raw)==inv['snapshot_sha256']
    cpu,get=get_machine(arm,raw);actors=get(0xCB184);captain=actors+0x19E4
    assert get(0x7F244)==get(0x2E58C)==2
    hook=cpu.hook_add(UC_HOOK_CODE,lambda c,a,z,d:c.reg_write(UC_ARM_REG_PC,0x027E0000),begin=BASE+0x242CC,end=BASE+0x242CC)
    rows=[];speaker_map={}
    try:
        for index,(a,b)in enumerate(zip(speeches,current_speeches,strict=True)):
            at=a['offset']+5;where=b['offset']+5
            original=source[at:source.index(b'\0',at)];value=current[where:current.index(b'\0',where)]
            prefix=original[0];assert value[0]==prefix and prefix in(1,2,9,16,20)
            assert source[at-5:at+1]==current[where-5:where+1]==bytes.fromhex('0040ffff00')+bytes([prefix])
            actor_ID=get(0x2434C,prefix);assert actor_ID==prefix
            actor=captain if actor_ID==2 else actors+4+actor_ID*32
            vt=struct.unpack('<I',cpu.mem_read(actor,4))[0];name_fn=struct.unpack('<I',cpu.mem_read(vt+8,4))[0]
            assert name_fn==0x0207EDD4
            catalog,name_get=get_machine(arm,raw)
            pointer=name_get(name_fn-BASE,actor);name=bytes(catalog.mem_read(pointer,80)).split(b'\0')[0].decode('cp932')
            catalog_after=bytes(catalog.mem_read(BASE,0x400000))
            delta=[{'address':BASE+i,'before':a,'after':b}for i,(a,b)in enumerate(zip(raw,catalog_after,strict=True))if a!=b]
            speaker_map[str(prefix)]={'actor_ID':actor_ID,'native_full_name':name,'name_getter':name_fn,
                'original_name_getter_cache_delta_on_separate_offline_copy':delta,
                'name_getter_not_claimed_pure_or_shared_with_macro_machine':True}
            text=value[1:];assert len(text)<2048
            cpu.mem_write(0x02660000-16,b'\xA5'*2080);cpu.mem_write(0x02660000,text+b'\0')
            guarded=bytes(cpu.mem_read(0x02660000-16,2080));cpu.mem_write(0x02662000-16,b'\xA5'*4128)
            call(cpu,0x242C8,(0x02662000,0x02660000,actor),instruction_limit=400000)
            expanded=bytes(cpu.mem_read(0x02662000,4096)).split(b'\0')[0]
            assert bytes(cpu.mem_read(BASE,0x400000))==raw
            assert bytes(cpu.mem_read(0x02660000-16,2080))==guarded
            assert bytes(cpu.mem_read(0x02662000-16,16))==b'\xA5'*16
            assert bytes(cpu.mem_read(0x02662000+len(expanded)+1,4095-len(expanded)))==b'\xA5'*(4095-len(expanded))
            record=source[:at].count(b'\0')
            rows.append({'id':f'DK4_MES_B27_R{record:04d}','file_path':'/data/SC2.DK4','block':27,'record_index':record,
                'source_reference':{'offset':at,'bytes':len(original),'header_offset':at-5},
                'current_reference':{'offset':where,'bytes':len(value),'header_offset':where-5,'record_index':current[:where].count(b'\0')},
                'source_hex':original.hex(),'current_text_hex':value.hex(),'source_complete_preamble_hex':source[at-5:at+1].hex(),
                'source_presentation_prefix_hex':f'{prefix:02x}','source_Japanese':original[1:].decode('cp932'),
                'current_stored_English':value[1:].decode('cp932'),'current_native_macro_English':expanded.decode('cp932'),
                'current_native_macro_output_hex':expanded.hex(),'speaker':name,'macro_probe_actor_ID':actor_ID,
                'native_command_extent':a['native_extent'],'ancestor_0100_offsets':a['ancestor_0100_offsets'],
                'original_macro_entire4MiB_input_output_guards_and_ABI_preserved':True,
                'spoken_sequence_index':index,'not_yet_source_prose_formatting_or_actual_completion':True})
    finally:cpu.hook_del(hook)
    for i,row in enumerate(rows):
        row['previous_spoken_ID']=rows[i-1]['id']if i else None
        row['next_spoken_ID']=rows[i+1]['id']if i+1<len(rows)else None
    ROOT.mkdir(parents=True)
    save(ROOT/'all51_clean_current_native_source_context.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'ARM9_sha256':sha(arm),
        'file_path':'/data/SC2.DK4','block':27,'clean_block_sha256':sha(source),'current_block_sha256':sha(current),
        'clean_block_bytes':len(source),'current_block_bytes':len(current),'all_clean_native_commands':old,
        'all_current_native_commands':now,'all102_command_offsets_extents_and_nested_ancestors_match':True,
        'all51_complete_speech_headers_match_independent_native_inventory':True,'records':rows,'native_speaker_catalog':speaker_map,
        'source_event27':inv['all336_original_events'][27],'offline_original_Stockholm_context':next(r for r in context['original_source_destination_cases']if r['event_ID']==27),
        'source_context_proof':str(CONTEXT),'source_context_proof_sha256':sha(CONTEXT.read_bytes()),
        'actual_Stockholm_arrival_B27_activation_portraits_and_returns_still_pending':True,
        'structural_inventory_bridges_opaque_effects_not_all_branch_gameplay':True,
        'no_ROM_edit_source_prose_count_or_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'native_commands':102,'speeches':51,'native_macro_and_actor_calls':51,'speaker_names':{k:v['native_full_name']for k,v in speaker_map.items()}},flush=True)
