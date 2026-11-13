"""Prove numeric UI ownership of the ten-byte prefix corrupted by older Jam text."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_LR,UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
BASE=0x02000000;ROOT=Path('work/analysis/raw_SC3_B109_prefix_controls_v3494')
def probe(arm,block,offset):
    cpu=machine(arm);stream,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100
    cpu.mem_write(stream-16,b'\xA5'*(len(block)+32));cpu.mem_write(stream,block);cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream+offset,0,0));owner_before=bytes(cpu.mem_read(owner-16,64))
    cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4));before=bytes(cpu.mem_read(BASE,0x400000));calls=[];executed={}
    def observe(u,pc,size,unused):
        executed[pc]=bytes(u.mem_read(pc,size)).hex()
        if pc not in [BASE+0x28C80,BASE+0x28AA8,BASE+0x28BAC]:return
        args=[u.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]];cfg=list(struct.unpack('<3I',u.mem_read(args[2],12)))
        calls.append(dict(address=pc,args=args,packed_configuration_words=cfg,explicit_unexecuted_UI_resource_body=True));u.reg_write(UC_ARM_REG_R0,0);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    h=cpu.hook_add(UC_HOOK_CODE,observe,begin=BASE,end=BASE+0x3FFFFF)
    try:call(cpu,0x2A510,(result,owner,length,0xFFFFFFFF),instruction_limit=30000)
    finally:cpu.hook_del(h)
    extent=struct.unpack('<I',cpu.mem_read(length,4))[0];value=list(struct.unpack('<6I',cpu.mem_read(result,24)));assert value[0]==3 and bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==owner_before and bytes(cpu.mem_read(stream,len(block)))==block
    for at in [stream-16,stream+len(block),result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\xA5'*16
    return dict(offset=offset,word=struct.unpack_from('<H',block,offset)[0],native_extent=extent,native_result=value,source_hex=block[offset:offset+extent].hex(),UI_resource_boundaries=calls,executed_native_words=executed,all4MiB_input_owner_canaries_and_ABI_exact=True,no_resource_body_or_actual_scene_execution=True)
if __name__=='__main__':
    assert not ROOT.exists();clean,current=NdsImage.open('work/clean.nds'),NdsImage.open('out/all_routes_combined_v3487_candidate.nds');a,b=[im.read_file('/__arm9__.bin') for im in [clean,current]];jp,en=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks[109] for im in [clean,current]]
    assert jp[:4]==en[:4]==b'CS\1\1' and jp[8:18].hex()=='00450000008084468380' and en[8:18].hex()=='00450000004a616d2020'
    ROOT.mkdir(parents=True);cases=[]
    for label,arm,block,offsets in [('clean',a,jp,[8,14]),('current',b,en,[8,14,16])]:
        for offset in offsets:
            case=probe(arm,block,offset);cases.append(dict(version=label,**case))
            for pc,word in case['executed_native_words'].items():at=int(pc)-BASE;assert a[at:at+len(bytes.fromhex(word))]==b[at:at+len(bytes.fromhex(word))]==bytes.fromhex(word)
    s0,s1,c0,c1,c2=cases;assert [c['native_extent'] for c in cases]==[6,4,6,2,2] and [c['word'] for c in cases]==[0x4500,0x4684,0x4500,0x6D61,0x2020]
    assert [c['address'] for c in s0['UI_resource_boundaries']]==[BASE+0x28C80] and [c['address'] for c in s1['UI_resource_boundaries']]==[BASE+0x28AA8] and [c['address'] for c in c0['UI_resource_boundaries']]==[BASE+0x28C80] and c1['UI_resource_boundaries']==c2['UI_resource_boundaries']==[]
    assert s0['UI_resource_boundaries'][0]['packed_configuration_words']!=c0['UI_resource_boundaries'][0]['packed_configuration_words']
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM);md.skipdata=True;spans=[(0x29AA0,0x29AF8),(0x29EA0,0x29FE4),(0x2A1D8,0x2A350),(0x2A510,0x2A5B8)]
    disasm='\n'.join(f'{i.address:08X} {i.mnemonic} {i.op_str}' for x,y in spans for i in md.disasm(a[x:y],BASE+x));dp=ROOT/'source_native_packed_control_ownership.asm.txt';dp.write_text(disasm,encoding='utf-8')
    save(ROOT/'source_packed_UI_control_bytes_replaced_by_Jam.json',dict(clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM='out/all_routes_combined_v3487_candidate.nds',current_ROM_sha256=sha(Path('out/all_routes_combined_v3487_candidate.nds').read_bytes()),file_path='/data/SC3.DK4',block=109,clean_block_sha256=sha(jp),current_block_sha256=sha(en),source_header_hex=jp[:4].hex(),source_prefix_hex=jp[8:18].hex(),current_prefix_hex=en[8:18].hex(),changed_prefix_offsets=[n for n in range(8,18) if jp[n]!=en[n]],current_accidental_ASCII_at13=en[13:18].decode('ascii'),source_owned_native_control_ranges=[dict(offset=8,bytes=6,word=0x4500),dict(offset=14,bytes=4,word=0x4684)],cases=cases,all_executed_native_instruction_bytes_clean_current_equal=True,first_packed_UI_configuration_changed_and_second_original_UI_request_lost=True,source_prefix_contains_no_name_Cstring=True,source_exact_control_restoration_required_before_editorial_integration=True,restore_owned_range=dict(offset=8,bytes=10,source_hex=jp[8:18].hex()),CS0101_original_header_preserved_not_a_loader_or_eligibility_proof=True,disassembly=str(dp),disassembly_sha256=sha(dp.read_bytes()),no_observed_crash_or_visible_runtime_defect_claim=True,new_emulator_runs=0,no_ROM_registry_ledger_review_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(clean_extents=[6,4],current_extents=[6,2,2],changed_control_offsets=[n for n in range(8,18) if jp[n]!=en[n]],source_configuration=s0['UI_resource_boundaries'][0]['packed_configuration_words'],current_configuration=c0['UI_resource_boundaries'][0]['packed_configuration_words'],source_second_UI_request_preserved=False,no_ROM_mutation=True))
