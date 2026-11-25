"""Read real FE modal bitmap/context fields at exact original native boundaries."""
import ctypes as ct
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_committed_gpu_v646 import CORE,CORE_SHA,ImageReader
from scripts.observe_file_requests_v681 import assemble
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.trace_file_ids_v683 import mapped_read
from scripts.observe_script_sources_v733 import Observer as Prior
from scripts.verify_village_wrap_v608 import read,save


class Observer:
    def __init__(self,core,folder,contract):
        self.core,self.folder=core,Path(folder);self.folder.mkdir(parents=True,exist_ok=True)
        self.source=read(contract);self.contract=Path(contract)
        self.native,self.image=NativeMemory(),ImageReader(core)
        self.cpu=self.image.anchor('9REG',4,16)-16
        self.wram=self.image.anchor('WRAM',1,0x400000)
        self.dtcm=self.image.anchor('DTCM',1,0x4000)
        self.dtcm_base=self.image.anchor('MDTC',4,1)
        self.itcm=self.image.anchor('ITCM',1,0x8000)
        assert self.image.anchor('9INS',4,1)==self.cpu+4 and self.image.anchor('9INA',4,1)==self.cpu+8
        self.header=(ct.c_uint32*4)(0,1,0,0);self.rows=[];self.errors=[];self.slots=[];self.closed=False
        packet=read('work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json')
        self.FE_bodies={r['current_native_macro_output_hex'] for block in packet['blocks'] if block['block']==120 for r in block['records'] if r['source_presentation_prefix_hex']=='fe'}

        def callback(frame):
            try:
                assert len(self.rows)<20000
                cpu=ct.string_at(self.cpu,128);raw=ct.string_at(self.wram,0x400000)
                dtcm=self.image.read(self.dtcm,0x4000);itcm=self.image.read(self.itcm,0x8000)
                base_raw=self.image.read(self.dtcm_base,4);base=struct.unpack('<I',base_raw)[0]
                values=struct.unpack('<32I',cpu)
                target=next(t for t in self.source['targets'] if t['PC']==values[2]);assert target['word']==values[1]
                def memory(address,length):return mapped_read(raw,dtcm,base,address,length)
                r0,r1,r9=values[4],values[5],values[13]
                if target['name']=='modal_entry':bitmap=r0;context=None
                else:bitmap=r9;context=r0
                body=memory(r1,512).split(b'\0')[0]
                row={'frame':frame,'PC':values[2],'kind':target['name'],'CPU128_hex':cpu.hex(),
                    'R0':r0,'R1':r1,'R9':r9,'SP':values[17],
                    'bitmap':bitmap,'bitmap_100_hex':memory(bitmap,100).hex(),
                    'context':context,'context_76_hex':memory(context,76).hex() if context is not None else None,
                    'text_hex':body.hex(),'text_CP932':body.decode('cp932'),
                    'WRAM_sha256':sha(raw),'DTCM_sha256':sha(dtcm),'ITCM_sha256':sha(itcm),'DTCM_base':base}
                font_pointer=struct.unpack_from('<I',raw,0xD5088)[0]
                row['font_metrics_object']=font_pointer
                row['font_object_24_hex']=memory(font_pointer,24).hex()
                if target['name']=='modal_paint' and body.hex() in self.FE_bodies:
                    prefix=self.folder/f'FE_{frame:06d}_{len(self.rows):04d}'
                    row['complete_readonly_snapshots']={}
                    for label,data in [('WRAM',raw),('DTCM',dtcm),('ITCM',itcm),('CPU',cpu)]:
                        file=prefix.with_name(prefix.name+'_'+label+'.bin');file.write_bytes(data)
                        row['complete_readonly_snapshots'][label]={'path':str(file),'sha256':sha(data),'bytes':len(data)}
                assert ct.string_at(self.cpu,128)==cpu and ct.string_at(self.wram,0x400000)==raw
                assert self.image.read(self.dtcm,0x4000)==dtcm and self.image.read(self.itcm,0x8000)==itcm
                assert self.image.read(self.dtcm_base,4)==base_raw
                row['CPU_all4MiB_DTCM_ITCM_and_configuration_unchanged_by_callback']=True
                self.rows.append(row)
            except BaseException as exc:
                self.errors.append(repr(exc));self.header[1]=0
        self.callback=ct.WINFUNCTYPE(None,ct.c_uint32)(callback)
        for index in sorted({t['instruction_index'] for t in self.source['targets']}):
            targets=[t for t in self.source['targets'] if t['instruction_index']==index]
            slot=core._handle+self.source['interpreter_table']['RVA']+index*8
            original=self.image.qword(slot);assert all(original==core._handle+t['handler_RVA'] for t in targets)
            address=self.native.alloc(None,4096,0x3000,0x04)
            code,assembly=assemble(self.cpu,ct.addressof(self.header),ct.cast(self.callback,ct.c_void_p).value,original,targets,address)
            assert len(code)<4096;ct.memmove(address,code,len(code));old=ct.c_uint32()
            assert self.native.protect(address,4096,0x20,ct.byref(old)) and self.native.flush(self.native.process,address,len(code))
            self.slots.append({'slot':slot,'original':original,'address':address,'code_hex':code.hex(),'assembly':assembly,'instruction_index':index})

    install=Prior.install
    next_frame=Prior.next_frame
    close=Prior.close

    def save(self):
        assert self.closed and sha(CORE.read_bytes())==CORE_SHA
        save(self.folder/'actual_modal_contexts.json',{'rows':self.rows,'errors':self.errors,
            'callbacks':self.header[2],'mismatches':self.header[3],
            'all_host_slots_restored_and_core_file_exact':True,
            'observer_sha256':sha(Path(__file__).read_bytes()),'contract_sha256':sha(self.contract.read_bytes()),
            'host_filters':self.slots,'anchors':self.image.entries,
            'snapshots_at_boundaries_do_not_exclude_temporary_write_then_restore':True,'full_goal_complete':False})
        for row in self.slots:assert self.native.free(row['address'],0,0x8000)
        assert not self.errors and not self.header[3]
