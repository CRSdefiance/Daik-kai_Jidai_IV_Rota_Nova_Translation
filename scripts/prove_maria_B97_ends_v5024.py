"""Guarded original B97 end1898 and relocated end2042 decode without reading padding."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_MEM_READ
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.maria_B97_reference_paths_v5021 import PARENT,ROM
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B97_ends_v5024')
if __name__=='__main__':
    assert not ROOT.exists();cases=[]
    for label,path,at,end in [('current',PARENT,1898,1902),('research',ROM,2042,2046)]:
        im=NdsImage.open(path);arm=im.read_file('/__arm9__.bin');block=IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks[97];assert 8+struct.unpack_from('<H',block,4)[0]==end and block[at:end]==bytes(4) and block[end:]==bytes(2)
        cpu=machine(arm);stream,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100
        cpu.mem_write(stream-16,b'\xA5'*(len(block)+64));cpu.mem_write(stream,block[:end]);cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream+at,0,0));ownerbytes=bytes(cpu.mem_read(owner-16,64));cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4));before=bytes(cpu.mem_read(0x02000000,0x400000));reads=[]
        hook=cpu.hook_add(UC_HOOK_MEM_READ,lambda u,a,p,s,v,d:reads.append(dict(address=p,size=s)),begin=stream+end,end=stream+end+31)
        try:call(cpu,0x2A510,(result,owner,length,0),instruction_limit=100000)
        finally:cpu.hook_del(hook)
        values=list(struct.unpack('<6I',cpu.mem_read(result,24)));extent=struct.unpack('<I',cpu.mem_read(length,4))[0]
        assert values==[0]*6 and extent==4 and not reads and bytes(cpu.mem_read(0x02000000,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==ownerbytes
        assert bytes(cpu.mem_read(stream,end))==block[:end] and bytes(cpu.mem_read(stream+end,32))==b'\xA5'*32
        for p in [stream-16,result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(p,16))==b'\xA5'*16
        cases.append(dict(version=label,end_offset=at,logical_end=end,native_result=values,native_extent=extent,no_post_logical_payload_reads=True,all4MiB_ABI_owner_input_result_length_and_poison_guards_exact=True))
    ROOT.mkdir(parents=True);save(ROOT/'two_guarded_tail_end_decodes_no_padding_dependency.json',dict(cases=cases,all2_declared_end_decodes_return_type0_extent4_without_post_payload_read=True,no_relative_sites_or_outer_VM_execution_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('Both halfword-aligned tail ends return type0/extent4 with unread poisoned padding.')
