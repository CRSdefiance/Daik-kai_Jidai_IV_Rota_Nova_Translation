"""Execute original COMMON loader with the bounded single-cache successor.

Successful file open/read operations are host contracts, not physical I/O.
No ROM, release registration, prose approval or gameplay credit is produced.
"""

import argparse
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.common_single_cache_v861 import CACHE_AT, ORIGINAL, entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.livestock_prayer_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP
from scripts.native_call_abi_v764 import call
from scripts.probe_common_copy_arm946_alignment import arm946_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/common_single_cache_v862')
SOURCE=Path('work/analysis/common_single_cache_v861')


class Loader:
    def __init__(self, arm, common):
        self.arm,self.common=arm,common
        self.blocks=IlnkContainer.parse(common).blocks
        self.directory=[struct.unpack_from('<HH',arm,DIRECTORY_OFFSET+i*4) for i in range(41)]
        self.uc=arm946_machine(arm)
        self.owner=struct.unpack_from('<I',arm,0x552A0)[0]
        self.output=self.owner+0x2030
        self.reads=[];self.opens=[];self.executed=set();self.write_count=0
        self.uc.hook_add(UC_HOOK_CODE,self.code)
        self.uc.hook_add(UC_HOOK_MEM_WRITE,self.write)
        self.reset()

    def reset(self):
        self.uc.mem_write(self.owner,b'\0'*0x2230)
        self.uc.mem_write(self.owner,self.arm[0xD20B4:0xD20B8])
        self.uc.mem_write(self.owner+0x2C,b'\xff\xff\0\1')

    def code(self,uc,address,size,_):
        if address in (BASE+0x534F4,BASE+0x53628,BASE+0x535E0,BASE+0xCEC74,BASE+0xD2018,BASE+0xD1EF0,BASE+0xD1F50,BASE+0xD1EE0):
            self.executed.add(address-BASE)
        if address==BASE+0xD0398:
            owner,pointer,mode=[uc.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2)]
            path=bytes(uc.mem_read(pointer,64)).split(b'\0',1)[0]
            assert owner==self.owner and mode==0 and b'MESFILE.DK4' in path.upper()
            self.opens.append(path.decode('ascii'));uc.mem_write(self.owner+8,struct.pack('<I',1))
            uc.reg_write(UC_ARM_REG_R0,1)
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
        elif address==BASE+0xD0170:
            owner,offset,dest,count=[uc.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3)]
            assert owner==self.owner and 0<=offset<offset+count<=len(self.common)
            if not (self.owner<=dest<dest+count<=self.output or STACK-0x1000<=dest<dest+count<=STACK):
                raise ValueError(f'Native read exceeds existing input allocation: {dest:#x}+{count}')
            uc.mem_write(dest,self.common[offset:offset+count]);self.reads.append((offset,dest,count))
            uc.reg_write(UC_ARM_REG_R0,count)
            for reg in (UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3):uc.reg_write(reg,0x02400000+reg)
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))

    def write(self,uc,access,address,size,value,_):
        assert (self.owner<=address<address+size<=self.output+512 or STACK-0x1000<=address<address+size<=STACK),f'Escaped native write {address:#x}+{size}'
        self.write_count+=1

    def copy(self,n,expected,mode):
        block=max(i for i,(first,size) in enumerate(self.directory) if first<=n)
        start,following=struct.unpack_from('<2H',self.arm,TABLE_OFFSET+n*2)
        finish=following if following>=start else len(self.blocks[block])
        assert 0<=start<finish<=len(self.blocks[block])<=8192 and finish-start<512
        if mode in ('cold','warm'):
            self.reset()
            if mode=='warm':
                self.uc.mem_write(self.owner+0x2C,bytes((block,255,0,1)))
                self.uc.mem_write(self.owner+0x30,self.blocks[block])
        cache_before=bytes(self.uc.mem_read(self.owner+0x30,8192))
        self.uc.mem_write(self.output,b'\xA5'*528)
        self.reads=[];self.opens=[];self.executed=set();self.write_count=0
        call(self.uc,0x534F4,(self.owner,n))
        assert self.uc.reg_read(UC_ARM_REG_R0)==self.output
        payload=self.blocks[block][start:finish]
        assert bytes(self.uc.mem_read(self.output,528))==payload+b'\0'+b'\xA5'*(527-len(payload))
        assert payload.split(b'\0',1)[0]==expected
        after=bytes(self.uc.mem_read(self.owner+0x30,8192))
        assert after==((self.blocks[block]+cache_before[len(self.blocks[block]):]) if self.reads else cache_before)
        assert {0x534F4,0x53628,0x535E0,0xCEC74}<=self.executed
        if mode=='cold':
            assert len(self.opens)==1 and len(self.reads)==3
            assert {0xD2018,0xD1EF0,0xD1F50,0xD1EE0}<=self.executed
        if mode=='warm':assert not self.opens and not self.reads
        return {'id':n,'block':block,'span':len(payload),'source_phase':start%4,'reads':len(self.reads),'opens':len(self.opens),'native_writes':self.write_count}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--surface',choices=('code_only','target','boundary'),required=True);args=parser.parse_args()
    ROOT.mkdir(parents=True,exist_ok=True);out=ROOT/f'{args.surface}_native.json';assert not out.exists()
    proof=read(SOURCE/'prospective_repack.json')
    rom=NdsImage.open('out/all_routes_combined_v855_candidate.nds')
    old_arm,old_common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    assert sha(old_arm)==proof['source_ARM9_sha256'] and sha(old_common)==proof['source_COMMON_sha256']
    arm=(SOURCE/('code_only_ARM9.bin' if args.surface=='code_only' else 'target_ARM9.bin')).read_bytes()
    common=old_common if args.surface=='code_only' else (SOURCE/'target_COMMON.bin').read_bytes()
    assert sha(arm)==proof[f'{"code_only" if args.surface=="code_only" else "target"}_ARM9_sha256']
    if args.surface=='code_only':rows=current_entries(old_common,old_arm)
    else:rows=entries(common,arm,proof['directory_sha256'])
    negative=None
    if args.surface=='boundary':
        blocks=IlnkContainer.parse(common).blocks;first=struct.unpack_from('<H',arm,DIRECTORY_OFFSET+40*4)[0]
        assert first==3561 and len(rows[first:])==107
        target=bytearray(arm);body=bytearray();expected={}
        for i,n in enumerate(range(first,3668)):
            size=77 if i<60 else 76;raw=(f'Boundary {n:04d} '.encode()+b'x'*size)[:size-1]
            struct.pack_into('<H',target,TABLE_OFFSET+n*2,len(body));body.extend(raw+b'\0');expected[n]=raw
        assert len(body)==8192
        blocks[40]=bytes(body);struct.pack_into('<HH',target,DIRECTORY_OFFSET+160,first,8192)
        common=IlnkContainer(blocks).to_bytes();arm=bytes(target)
        rows=entries(common,arm,sha(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
        assert all(r.text==expected.get(r.message_id,r.text) for r in rows)
    loader=Loader(arm,common);cases=[]
    selected=rows if args.surface!='boundary' else rows[3561:]
    for mode in ('warm','cold'):
        for i,row in enumerate(selected):
            cases.append(loader.copy(row.message_id,row.text,mode))
            if (i+1)%500==0:print(args.surface,mode,i+1,'complete',flush=True)
    loader.reset();sequence=[]
    # Every physical block enters a real cache state; adjacent hits avoid I/O.
    order=list(range(41))+list(reversed(range(41)))+[0,18,0,18,40,0,40]
    for block in order:
        n=loader.directory[block][0]
        for _ in range(2):sequence.append(loader.copy(n,rows[n].text,'sequence'))
    assert all(row['reads']==0 for row in sequence[1::2])
    if args.surface!='code_only':
        original=bytearray(arm);original[CACHE_AT:CACHE_AT+8]=ORIGINAL
        bad=Loader(bytes(original),common)
        bad.copy(0,rows[0].text,'cold')
        big=40 if args.surface=='boundary' else 18;n=bad.directory[big][0]
        try:bad.copy(n,rows[n].text,'sequence')
        except ValueError as error:
            assert 'exceeds existing input allocation' in str(error);negative=str(error)
        else:raise AssertionError('Original two-slot overflow negative did not reject')
    save(out,{'surface':args.surface,'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),'complete_native_copies':len(cases),
        'cases':cases,'sequenced_cache_cases':sequence,'original_two_slot_large_block_overflow_reproduced':negative,
        'all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass':True,
        'callee_saved_ABI_and_stack_pass':True,'no_guard_inserted_inside_valid_cache':True,
        'host_open_read_contract_only_not_actual_ROM_or_hardware':True,
        'boundary8192_synthetic_only':args.surface=='boundary','actual_boot_and_gameplay_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(args.surface,len(cases),'complete native copies and',len(sequence),'sequence cases pass.',flush=True)


if __name__=='__main__':main()
