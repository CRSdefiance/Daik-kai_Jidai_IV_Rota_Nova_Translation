"""Read-only original COMMON-copy entry requests; no engine or state substitution."""
import ctypes as ct
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.common_single_cache_v861 import entries
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE,CORE_SHA,ImageReader
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_file_requests_v681 import assemble
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.observe_script_sources_v733 import Observer as Host
from scripts.trace_file_ids_v683 import mapped_read
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/town_services_actual_v2053')
ROM=Path('out/all_routes_combined_v2047_candidate.nds')
PC=0x020534F4

def prepare_contract():
    assert not ROOT.exists()
    image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');word=struct.unpack_from('<I',arm,PC-0x02000000)[0]
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');assert arm[0x534F4:0x535E0]==clean[0x534F4:0x535E0]
    raw=CORE.read_bytes();assert sha(raw)==CORE_SHA;base,table=tables(raw);index=word>>16&0xff0|word>>4&15
    target=dict(PC=PC,name='original_COMMON_copy_entry',word=word,instruction_index=index,
        handler_RVA=struct.unpack_from('<Q',raw,table['file_offset']+index*8)[0]-base)
    ROOT.mkdir(parents=True)
    save(ROOT/'source_contract.json',dict(targets=[target],interpreter_table=table,original_function_before_first_instruction=True,
        source_ARM9_sha256=sha(arm),COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),core_sha256=CORE_SHA))

class Observer:
    install,close=Host.install,Host.close
    def __init__(self,core,folder):
        self.core,self.folder=core,Path(folder);self.folder.mkdir(parents=True,exist_ok=True)
        self.native,self.image=NativeMemory(),ImageReader(core);self.source=read(ROOT/'source_contract.json')
        self.cpu=self.image.anchor('9REG',4,16)-16;self.wram=self.image.anchor('WRAM',1,0x400000)
        self.dtcm=self.image.anchor('DTCM',1,0x4000);self.dtcm_base=self.image.anchor('MDTC',4,1);self.itcm=self.image.anchor('ITCM',1,0x8000)
        assert self.image.anchor('9INS',4,1)==self.cpu+4 and self.image.anchor('9INA',4,1)==self.cpu+8
        self.header=(ct.c_uint32*4)(0,1,0,0);self.rows,self.errors,self.slots,self.seen=[],[],[],set();self.closed=False
        image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
        directory=read('translations/reinforcement_faction_prose_release_v1.json')['directory_sha256'];self.entries=entries(common,arm,directory)
        def callback(frame):
            try:
                cpu=ct.string_at(self.cpu,128);values=struct.unpack('<32I',cpu);n=values[5]
                assert values[2]==PC and values[1]==self.source['targets'][0]['word']
                if not 0<=n<=84 or n==64:return
                key=n,values[18]
                if key in self.seen:return
                self.seen.add(key);assert len(self.rows)<1000
                raw=ct.string_at(self.wram,0x400000);dtcm=self.image.read(self.dtcm,0x4000);itcm=self.image.read(self.itcm,0x8000)
                base_raw=self.image.read(self.dtcm_base,4);base=struct.unpack('<I',base_raw)[0]
                prefix=self.folder/f'event_{len(self.rows):04d}_ID{n:04d}';snapshots={}
                for label,data in(('WRAM',raw),('DTCM',dtcm),('ITCM',itcm),('CPU',cpu)):
                    p=prefix.with_name(prefix.name+'_'+label+'.bin');p.write_bytes(data);snapshots[label]=dict(path=str(p),sha256=sha(data),bytes=len(data))
                try:stack=mapped_read(raw,dtcm,base,values[17],512).hex()
                except(AssertionError,ValueError):stack=None
                e=self.entries[n]
                row=dict(frame=frame,message_ID=n,PC=PC,caller_LR=values[18],SP=values[17],registers=list(values[4:20]),
                    current_native_selection=dict(block=e.block,offset=e.block_offset,copy_end=e.copy_end,hex=e.text.hex()),
                    stack_512_hex=stack,DTCM_base=base,complete_readonly_snapshots=snapshots)
                assert ct.string_at(self.cpu,128)==cpu and ct.string_at(self.wram,0x400000)==raw
                assert self.image.read(self.dtcm,0x4000)==dtcm and self.image.read(self.itcm,0x8000)==itcm and self.image.read(self.dtcm_base,4)==base_raw
                row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']=True;self.rows.append(row)
            except BaseException as exc:
                self.errors.append(repr(exc));self.header[1]=0
        self.callback=ct.WINFUNCTYPE(None,ct.c_uint32)(callback)
        for target in self.source['targets']:
            slot=core._handle+self.source['interpreter_table']['RVA']+target['instruction_index']*8;original=self.image.qword(slot)
            assert original==core._handle+target['handler_RVA'];address=self.native.alloc(None,4096,0x3000,0x04)
            code,assembly=assemble(self.cpu,ct.addressof(self.header),ct.cast(self.callback,ct.c_void_p).value,original,[target],address)
            assert len(code)<4096;ct.memmove(address,code,len(code));old=ct.c_uint32()
            assert self.native.protect(address,4096,0x20,ct.byref(old))and self.native.flush(self.native.process,address,len(code))
            self.slots.append(dict(slot=slot,original=original,address=address,code_hex=code.hex(),assembly=assembly))
    def next_frame(self):self.header[0]+=1
    def save(self):
        assert self.closed
        save(self.folder/'requests.json',dict(rows=self.rows,errors=self.errors,callbacks=self.header[2],mismatches=self.header[3],
            all_host_slots_restored_and_core_file_exact=True,source_contract_sha256=sha((ROOT/'source_contract.json').read_bytes()),
            observer_sha256=sha(Path(__file__).read_bytes()),host_filters=self.slots,
            first_request_per_message_and_caller_only_not_all_invocations=True,entry_boundaries_do_not_exclude_temporary_write_then_restore=True,full_goal_complete=False))
        for row in self.slots:assert self.native.free(row['address'],0,0x8000)
        assert not self.errors and not self.header[3]
