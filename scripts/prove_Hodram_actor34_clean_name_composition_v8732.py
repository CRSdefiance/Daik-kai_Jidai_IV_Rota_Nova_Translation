"""Run original actor34 name composition on an explicit clean-only ordinary fixture.

This is a disposable native source consumer test, not clean gameplay or a current
RAM overlay. Current getters and glyph planes are reused from their own V8704 run.
"""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_map_entity_tooltip_copy import machine_for
from scripts.probe_button_prompt_native import call
from scripts.audit_native_given_name_table import string
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_actor34_clean_name_composition_v8732')
PRIOR=Path('work/analysis/Hodram_B31_actor34_names_v8719/source_names_native_getters_andplanes.json')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists();prior=read(PRIOR);clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');current=NdsImage.open(prior['candidate']).read_file('/__arm9__.bin')
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256'] and sha(current)==prior['ARM9_sha256']
    spans=[]
    for a,z in [(0x7EA48,0x7EEA4),(0xAC000,0xAC02C),(0xCED50,0xCEDC4),(0xCB184,0xCB190),(0xCDAB4,0xCDAC4)]:
        assert clean[a:z]==current[a:z];spans.append(dict(start=a,end=z,source_andcurrent_sha256=sha(clean[a:z])))
    cpu=machine_for(clean);whole=bytes(cpu.mem_read(BASE,0x400000));root=struct.unpack_from('<I',clean,0xCB18C)[0];actor=root+4+32*34
    assert BASE<=actor and actor+32<=BASE+0x400000
    executed=set()
    def exact(u,pc,size,unused):
        assert BASE<=pc and pc+size<=BASE+len(clean),hex(pc)
        assert bytes(u.mem_read(pc,size))==clean[pc-BASE:pc-BASE+size],hex(pc)
        executed.add(pc)
    eh=cpu.hook_add(UC_HOOK_CODE,exact)
    call(cpu,0x7EB3C,(actor,));constructed=bytes(cpu.mem_read(BASE,0x400000));inverse=bytearray(constructed)
    inverse[actor-BASE:actor-BASE+4]=whole[actor-BASE:actor-BASE+4];assert bytes(inverse)==whole
    table=struct.unpack_from('<I',clean,0xCDAC0)[0];fields=[]
    for col,kind in [(0,'given'),(4,'surname'),(8,'middle')]:
        at=table-BASE+32*34+col;fields.append(dict(kind=kind,table_field=at,table_field_hex=clean[at:at+4].hex(),**string(clean,struct.unpack_from('<I',clean,at)[0])))
    assert [f['text'] for f in fields]==['バルバロッサ','ハイレディン','ファーズル']
    separator_fields=[]
    for field in [0x7EEA8,0x7EEAC]:
        pointer=struct.unpack_from('<I',clean,field)[0];separator_fields.append(dict(literal_field=field,**string(clean,pointer)))
    values={r['kind']:bytes.fromhex(r['hex']) for r in fields};seps=[bytes.fromhex(r['hex']) for r in separator_fields]
    rows=[]
    for kind,offset in [('progressive-nameplate',0x7ED88),('full-catalogue',0x7EDD4)]:
        before=bytes(cpu.mem_read(BASE,0x400000));rings=[];writes=[];reads=[]
        def ring(u,pc,size,unused):
            owner=u.reg_read(UC_ARM_REG_R0);index=struct.unpack('<I',u.mem_read(owner+8,4))[0];assert index<32
            rings.append(dict(owner=owner,index=index,counter=owner+8,slot=owner+12+index*128))
        h=cpu.hook_add(UC_HOOK_CODE,ring,begin=BASE+0xAC000,end=BASE+0xAC000)
        w=cpu.hook_add(UC_HOOK_MEM_WRITE,lambda u,a,address,size,value,d:writes.append(dict(address=address,size=size,value=value,PC=u.reg_read(UC_ARM_REG_PC))),begin=BASE,end=BASE+0x400000-1)
        r=cpu.hook_add(UC_HOOK_MEM_READ,lambda u,a,address,size,value,d:reads.append(dict(address=address,size=size)),begin=table+32*34,end=table+32*34+11)
        try:call(cpu,offset,(actor,));pointer=cpu.reg_read(UC_ARM_REG_R0)
        finally:cpu.hook_del(h);cpu.hook_del(w);cpu.hook_del(r)
        value=bytes(cpu.mem_read(pointer,128)).split(b'\0')[0]
        expected=values['given']+(seps[0]+values['middle'] if kind=='full-catalogue' else b'')+seps[1]+values['surname']
        assert value==expected and len(rings)==1 and pointer==rings[0]['slot'] and len(value)<128
        assert {p['address'] for p in reads}=={table+32*34+c for c in ([0,4,8] if kind=='full-catalogue' else [0,4])}
        owner=rings[0];counter=owner['counter'];end=pointer+len(value)+1
        for write in writes:
            if write['address']==counter:assert write['size']==4 and write['PC'] in [BASE+0xAC00C,BASE+0xAC020]
            else:assert pointer<=write['address'] and write['address']+write['size']<=end and write['size']==1 and write['PC'] in [BASE+0xCED7C,BASE+0xCED90,BASE+0xCEDAC,BASE+0xCEDC0]
        assert struct.unpack('<I',cpu.mem_read(counter,4))[0]==(owner['index']+1)%32
        restored=bytearray(cpu.mem_read(BASE,0x400000))
        for a,z in [(counter,counter+4),(pointer,end)]:restored[a-BASE:z-BASE]=before[a-BASE:z-BASE];cpu.mem_write(a,before[a-BASE:z-BASE])
        assert bytes(restored)==before==bytes(cpu.mem_read(BASE,0x400000))
        rows.append(dict(consumer=kind,getter=BASE+offset,actor_fixture=actor,text=value.decode('cp932'),text_hex=value.hex(),native_table_field_reads=reads,original_ring=rings[0],original_writes=writes,
            exact_source_composition_verified=True,all_original_ABI_andunowned4MiB_exact=True))
    cpu.hook_del(eh);assert bytes(cpu.mem_read(BASE,0x400000))==constructed
    cpu.mem_write(actor,whole[actor-BASE:actor-BASE+4]);assert bytes(cpu.mem_read(BASE,0x400000))==whole
    ROOT.mkdir(parents=True);save(ROOT/'clean_source_full_andprogressive_name_composition.json',dict(clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),clean_ARM9_sha256=sha(clean),
        current_candidate=prior['candidate'],current_candidate_sha256=prior['candidate_sha256'],current_ARM9_sha256=sha(current),
        source_fields=fields,original_separator_fields=separator_fields,source_native_getters=rows,complete_clean_current_original_consumer_spans=spans,
        original_constructor_only_fourbyte_ordinary_actor_vtable_fixture=True,no_actual_current_actor_roster_role_orflags_changed=True,
        every_executed_instruction_exact_clean_ARM9=True,executed_instruction_addresses=len(executed),all_fixture_constructor_andring_writes_reversible_to_initial4MiB=True,
        current_two_getters_andtwo_nameplanes_reused_from=str(PRIOR),current_two_getters_andtwo_nameplanes_reused_sha256=sha(PRIOR.read_bytes()),
        source_middle_field_is_actually_composed_byoriginal_full_getter_not_automatically_unused=True,
        no_historical_initialized_RAM_snapshot_oroverlay=True,no_actual_clean_gameplay_orcatalogue_UI_claim=True,
        romanization_editorial_decision_andcurrent_actual_scene_headers_pending=True,no_ROM_registry_orcredit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,Path(__file__)]}))
    print([(r['consumer'],r['text']) for r in rows],flush=True)
    print('Original clean composition confirms middle field;ordinary fixture only,all ABI/ring/unowned memory preserved. No current getter replay or gameplay claim.',flush=True)
