"""Observe original contact,Aim,roll andannouncement boundaries without state writes."""
import ctypes as ct
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_committed_gpu_v646 import CORE,CORE_SHA,ImageReader
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.observe_file_requests_v681 import assemble
from scripts.trace_file_ids_v683 import mapped_read
from scripts.verify_village_wrap_v608 import read,save

CONTRACT=Path('work/analysis/shot_observer_contract_v1796/source_contract.json')

class Observer:
    def __init__(self,core,folder):
        self.folder=Path(folder);self.folder.mkdir(parents=True,exist_ok=True)
        self.native,self.image=NativeMemory(),ImageReader(core);self.source=read(CONTRACT)
        self.cpu=self.image.anchor('9REG',4,16)-16;self.wram=self.image.anchor('WRAM',1,0x400000)
        self.dtcm=self.image.anchor('DTCM',1,0x4000);self.dtcm_base=self.image.anchor('MDTC',4,1)
        self.itcm=self.image.anchor('ITCM',1,0x8000)
        assert self.image.anchor('9INS',4,1)==self.cpu+4 and self.image.anchor('9INA',4,1)==self.cpu+8
        self.header=(ct.c_uint32*4)(0,1,0,0);self.rows=[];self.errors=[];self.slots=[];self.closed=False
        def callback(frame):
            try:
                assert len(self.rows)<20000
                cpu=ct.string_at(self.cpu,128);values=struct.unpack('<32I',cpu)
                target=next(t for t in self.source['targets']if t['PC']==values[2]);assert values[1]==target['word']
                raw=ct.string_at(self.wram,0x400000);dtcm=self.image.read(self.dtcm,0x4000)
                itcm=self.image.read(self.itcm,0x8000);base_raw=self.image.read(self.dtcm_base,4);base=struct.unpack('<I',base_raw)[0]
                packet=mapped_read(raw,dtcm,base,values[17]+0x78,32)
                a,b=struct.unpack('<4I',packet[:16]),struct.unpack('<4I',packet[16:])
                row={'frame':frame,'kind':target['name'],'PC':values[2],'CPU128_hex':cpu.hex(),
                    'R0':values[4],'R4':values[8],'R7':values[11],'SP':values[17],
                    'own_contact_words':list(a),'other_contact_words':list(b),
                    'WRAM_sha256':sha(raw),'DTCM_sha256':sha(dtcm),'ITCM_sha256':sha(itcm)}
                if target['name']=='native_roll_compare':
                    row.update(original_RNG_roll=values[4],original_Aim_div10_threshold=values[8],
                        native_shot_condition_met=values[4]<=values[8])
                if target['name']in ('shot_announcement','shot_message_return'):
                    prefix=self.folder/f'event_{len(self.rows):05d}_{frame:06d}'
                    saved=[]
                    for name,data in [('WRAM',raw),('CPU',cpu),('DTCM',dtcm),('ITCM',itcm)]:
                        path=prefix.with_name(prefix.name+'_'+name+'.bin');path.write_bytes(data)
                        saved.append({'path':str(path),'sha256':sha(data)})
                    row['read_only_event_snapshots']=saved
                assert ct.string_at(self.cpu,128)==cpu and ct.string_at(self.wram,0x400000)==raw
                assert self.image.read(self.dtcm,0x4000)==dtcm and self.image.read(self.itcm,0x8000)==itcm
                assert self.image.read(self.dtcm_base,4)==base_raw
                row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']=True;self.rows.append(row)
            except BaseException as error:
                self.errors.append(repr(error));self.header[1]=0
        self.callback=ct.WINFUNCTYPE(None,ct.c_uint32)(callback)
        for index in sorted({t['instruction_index']for t in self.source['targets']}):
            targets=[t for t in self.source['targets']if t['instruction_index']==index]
            slot=core._handle+self.source['interpreter_table']['RVA']+index*8;original=self.image.qword(slot)
            assert all(original==core._handle+t['handler_RVA']for t in targets)
            address=self.native.alloc(None,4096,0x3000,0x04)
            code,assembly=assemble(self.cpu,ct.addressof(self.header),ct.cast(self.callback,ct.c_void_p).value,original,targets,address)
            assert len(code)<4096;ct.memmove(address,code,len(code));old=ct.c_uint32()
            assert self.native.protect(address,4096,0x20,ct.byref(old)) and self.native.flush(self.native.process,address,len(code))
            self.slots.append({'slot':slot,'original':original,'address':address,'code_hex':code.hex(),
                'assembly':assembly,'instruction_index':index})
    def install(self):
        for row in self.slots:
            assert self.image.qword(row['slot'])==row['original'];self.native.pointer(row['slot'],row['address'])
    def next_frame(self):self.header[0]+=1
    def close(self):
        if not self.closed:
            for row in self.slots:self.native.pointer(row['slot'],row['original'])
            self.closed=True
        assert all(self.image.qword(r['slot'])==r['original']for r in self.slots)
        assert sha(CORE.read_bytes())==CORE_SHA
    def progress(self):
        return {'rows':self.rows,'errors':self.errors,'callbacks':self.header[2],'mismatches':self.header[3],
            'live_not_terminal_proof':not self.closed}
    def save(self):
        assert self.closed
        save(self.folder/'original_shot_trace.json',{**self.progress(),'all_host_slots_restored_and_core_file_exact':True,
            'source_contract_sha256':sha(CONTRACT.read_bytes()),'observer_sha256':sha(Path(__file__).read_bytes()),
            'host_filters':self.slots,'entry_boundary_checks_do_not_exclude_temporary_write_restore':True,'full_goal_complete':False})
        for row in self.slots:assert self.native.free(row['address'],0,0x8000)
        assert not self.errors and not self.header[3]
