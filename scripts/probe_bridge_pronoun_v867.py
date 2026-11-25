"""Prove source1477 IC pronoun and established role/name spellings natively."""

import struct
from pathlib import Path
from unicorn.arm_const import UC_ARM_REG_R0
from dk4tool.patch.common_literal_prefix import guard
from dk4tool.patch.crew_role_labels import ORIGINAL
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_call_abi_v764 import call
from scripts.prepare_work_comments_v842 import snapshot,machine_at
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/bridge_duties_v867')
INPUT,OUTPUT=0x02450020,0x02451020


def main():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'source_pronoun_and_terms.json').exists()
    rom=NdsImage.open('out/all_routes_combined_v863_candidate.nds');clean=NdsImage.open('work/clean.nds')
    a,j=rom.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    source=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),j)[1477].text
    assert source.count(b'IC')==1
    assert sha(j[0x53914:0x53AC4])=='71f0a5626d1992a8e2a2f0fb5a287bb42d719c0861488c64aec7ea5fe5386d87'
    assert a[0x7E9B8:0x7E9D0]==j[0x7E9B8:0x7E9D0]
    restored=bytearray(a[0x53914:0x53AC4]);literal=read('out/all_routes_combined_v863_candidate.manifest.json')['relocations']['/__arm9__.bin']['common_literal_prefix']
    for at,prefix in ((0x5397C,'F'),(0x53A44,'I')):
        row=next(r for r in literal['changes'] if r['offset']==at)
        assert struct.unpack_from('<I',a,at)[0]==row['after'] and struct.unpack_from('<I',j,at)[0]==row['before']
        restored[at-0x53914:at-0x53914+4]=j[at:at+4]
    assert bytes(restored)==j[0x53914:0x53AC4]
    cases=[]
    folders={0:('personal_activity_v839_838_Rafael_later',3200),1:('planning_finance_v864_863_JoakimPlanning',3400),
        2:('ceremony_Lil_approach_v825',23000),3:('ceremony_Maria_approach_v825',26000)}
    for actor in range(25):
        raw,receipt=snapshot(*folders[actor if actor<4 else 1]);cpu,get=machine_at(a,raw)
        assert bytes(cpu.mem_read(0x02053914,0x1B0))==a[0x53914:0x53AC4]
        for prefix in ('F','I'):
            entry=literal['helpers'][prefix]['entry'];code=guard(entry,prefix)
            assert bytes(cpu.mem_read(entry,len(code)))==code
        actors=get(0xCB184);obj=actors+0x19E4 if actor<4 else actors+4+actor*32
        if actor<4:assert get(0x7F244)==actor
        kind=get(0x7E9B8,obj);assert kind in (0,1)
        pronoun=('アタシ' if kind==1 else '僕').encode('cp932');expected=source.replace(b'IC',pronoun)
        variants=[]
        for surface in ('current','clean_parser_control'):
            if surface=='clean_parser_control':cpu.mem_write(0x02053914,j[0x53914:0x53AC4])
            cpu.mem_write(INPUT-16,b'\xA5'*(len(source)+33));cpu.mem_write(INPUT,source+b'\0')
            before=bytes(cpu.mem_read(INPUT-16,len(source)+33));cpu.mem_write(OUTPUT-16,b'\xA5'*560)
            call(cpu,0x53914,(OUTPUT,INPUT,obj))
            actual=bytes(cpu.mem_read(OUTPUT,512)).split(b'\0',1)[0]
            assert actual==expected
            assert bytes(cpu.mem_read(INPUT-16,len(source)+33))==before
            assert bytes(cpu.mem_read(OUTPUT-16,560))==b'\xA5'*16+expected+b'\0'+b'\xA5'*(543-len(expected))
            variants.append({'surface':surface,'expanded_hex':actual.hex(),'expanded_Japanese':actual.decode('cp932'),'source_output_guards_and_ABI_pass':True})
        cases.append({'actor_ID':actor,'source_snapshot':receipt,'native_pronoun_kind':kind,'variants':variants})
    raw,receipt=snapshot(*folders[1]);cpu,get=machine_at(a,raw)
    labels=get(0x86314);mate_ptr=struct.unpack('<I',cpu.mem_read(labels+4,4))[0]
    assert bytes(cpu.mem_read(mate_ptr,32)).split(b'\0',1)[0].rstrip()==b'First Mate'
    original_ptr=struct.unpack_from('<I',j,ORIGINAL-0x02000000+4)[0]
    assert j[original_ptr-0x02000000:].split(b'\0',1)[0].decode('cp932')=='副官'
    actors=get(0xCB184);obj=actors+4+10*32
    vtable=struct.unpack('<I',cpu.mem_read(obj,4))[0];method=struct.unpack('<I',cpu.mem_read(vtable+0x20,4))[0]
    name=get(method-0x02000000,obj);native_name=bytes(cpu.mem_read(name,64)).split(b'\0',1)[0].decode('cp932').strip()
    assert native_name=='Xien',native_name
    save(ROOT/'source_pronoun_and_terms.json',{'candidate_sha256':sha(Path('out/all_routes_combined_v863_candidate.nds').read_bytes()),
        'ARM9_sha256':sha(a),'source1477_hex':source.hex(),'all25_current_and_clean_parser_control_cases':cases,
        'IC_is_first_person_not_actor_name':True,'English_pronoun_can_be_I_me_or_our_as_grammar_requires':True,
        'native_role1_Japanese':'副官','native_role1_current_English':'First Mate',
        'native_actor10_given_name':native_name,'source1498_シエン_uses_existing_Xien_not_Shen':True,
        'no_ROM_or_actual_gameplay_changes':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('50 complete original/current IC expansions pass;source1477 is first person. Native First Mate and Xien verified.',flush=True)


if __name__=='__main__':main()
