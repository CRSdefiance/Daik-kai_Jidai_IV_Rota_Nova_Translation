"""Observe actual D5340 caption context/view/backing arguments without changing emulated state."""
import ctypes as ct,struct,sys
from pathlib import Path
import pefile
from scripts import headless_desmume_v193 as harness
from scripts.inspect_committed_gpu_v646 import CORE,CORE_SHA,ImageReader
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.observe_file_requests_v681 import assemble
from scripts.trace_file_ids_v683 import mapped_read
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B166_menu_owner_trace_v4086')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_B166_menu_owner_v4086')
class OwnerObserver:
    def __init__(self,core,arm):
        self.core=core;self.image=ImageReader(core);self.native=NativeMemory();self.cpu=self.image.anchor('9REG',4,16)-16;self.wram=self.image.anchor('WRAM',1,0x400000);self.dtcm=self.image.anchor('DTCM',1,0x4000);self.dtcm_base=self.image.anchor('MDTC',4,1);self.itcm=self.image.anchor('ITCM',1,0x8000);self.rows=[];self.errors=[];self.closed=False;self.header=(ct.c_uint32*4)(0,1,0,0)
        contract=read('work/analysis/script_sources_v733/source_contract.json');pc=0x020D5340;word=struct.unpack_from('<I',arm,pc-0x02000000)[0];assert word==0xE92D4030;index=((word>>16)&0xFF0)|((word>>4)&15);pe=pefile.PE(str(CORE),fast_load=True);file_at=contract['interpreter_table']['file_offset']+index*8;handler=struct.unpack_from('<Q',CORE.read_bytes(),file_at)[0]-pe.OPTIONAL_HEADER.ImageBase;target=dict(PC=pc,word=word,instruction_index=index,handler_RVA=handler);self.slot=core._handle+contract['interpreter_table']['RVA']+index*8;self.original=self.image.qword(self.slot);assert self.original==core._handle+handler
        def callback(frame):
            try:
                if frame<2200 or len(self.rows)>=12:return
                cpu=ct.string_at(self.cpu,128);values=struct.unpack('<32I',cpu);assert values[2]==pc and values[1]==word;raw=ct.string_at(self.wram,0x400000);dtcm=self.image.read(self.dtcm,0x4000);itcm=self.image.read(self.itcm,0x8000);base_raw=self.image.read(self.dtcm_base,4);base=struct.unpack('<I',base_raw)[0]
                memory=lambda a,n:mapped_read(raw,dtcm,base,a,n)
                text=memory(values[5],64).split(b'\0')[0]
                if not(text.startswith(b'Please do') or text.startswith(b'Decline')):return
                context=memory(values[4],72);view=struct.unpack_from('<I',context,0x2C)[0];viewdata=memory(view,64);bitmap=struct.unpack_from('<I',viewdata,0x10)[0];head=memory(bitmap,20);h=struct.unpack('<5I',head);assert h[0] in [4,16] and 0<h[1]<1024 and 0<h[2]<1024;size=h[1]*h[2]*2;assert size<0x100000;pixel_pointer=(bitmap+h[4])&0xFFFFFFFF;pixels=memory(pixel_pointer,size);out=ROOT/f'caption_backing_{len(self.rows):02d}.bin';out.write_bytes(pixels)
                assert ct.string_at(self.cpu,128)==cpu and ct.string_at(self.wram,0x400000)==raw and self.image.read(self.dtcm,0x4000)==dtcm and self.image.read(self.itcm,0x8000)==itcm and self.image.read(self.dtcm_base,4)==base_raw
                self.rows.append(dict(frame=frame,PC=pc,text=text.decode('ascii'),text_hex=text.hex(),context_address=values[4],context_words=list(struct.unpack('<18I',context)),view_address=view,view_words=list(struct.unpack('<16I',viewdata)),bitmap_header_address=bitmap,bitmap_header_words=list(h),backing_pointer=pixel_pointer,backing_bytes=size,backing=str(out),backing_sha256=sha(pixels),CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback=True))
            except BaseException as e:self.errors.append(repr(e));self.header[1]=0
        self.callback=ct.WINFUNCTYPE(None,ct.c_uint32)(callback);self.address=self.native.alloc(None,4096,0x3000,0x04);code,assembly=assemble(self.cpu,ct.addressof(self.header),ct.cast(self.callback,ct.c_void_p).value,self.original,[target],self.address);assert len(code)<4096;ct.memmove(self.address,code,len(code));old=ct.c_uint32();assert self.native.protect(self.address,4096,0x20,ct.byref(old)) and self.native.flush(self.native.process,self.address,len(code));self.target=target;self.assembly=assembly;self.code=code;self.native.pointer(self.slot,self.address)
    def next_frame(self):self.header[0]+=1
    def close(self):
        if not self.closed:self.native.pointer(self.slot,self.original);self.closed=True
        assert self.image.qword(self.slot)==self.original and sha(CORE.read_bytes())==CORE_SHA
    def save(self):
        assert self.closed;save(ROOT/'actual_caption_context_view_and_backing.json',dict(rows=self.rows,errors=self.errors,callbacks=self.header[2],mismatches=self.header[3],target=self.target,host_filter_assembly=self.assembly,host_filter_hex=self.code.hex(),all_host_slots_restored_and_core_file_exact=True,read_only_argument_observation_not_emulated_code_or_memory_edit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));assert self.native.free(self.address,0,0x8000);assert not self.errors and not self.header[3] and self.rows
if __name__=='__main__':
    assert not ROOT.exists() and not CAP.exists() and sha(CORE.read_bytes())==CORE_SHA;fixturepath=Path('work/analysis/lil_B166_menu_fixture_v4076/focused_typed_menu_constructor_fixtures.json');fixture=read(fixturepath);spec=next(r for r in fixture['fixtures'] if r['case']=='reviewed');rom=Path(spec['research_ROM']);assert sha(rom.read_bytes())==spec['research_ROM_sha256'];arm=NdsImage.open(rom).read_file('/__arm9__.bin');ROOT.mkdir(parents=True);observers=[]
    class Proxy:
        def __getattr__(self,k):return getattr(ct,k)
        def CDLL(self,path,*args,**kwargs):
            core=ct.CDLL(path,*args,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer=OwnerObserver(core,arm);observers.append(observer);original=core.retro_run;original.restype=None
                def run():observer.next_frame();original()
                core.retro_run=run
            return core
    inputs=Path('work/analysis/lil_B166_menu_run_v4077/reviewed_inputs.json');save(ROOT/'plan.json',dict(ROM=str(rom),ROM_sha256=sha(rom.read_bytes()),fixture=str(fixturepath),fixture_sha256=sha(fixturepath.read_bytes()),inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),frames=3501,read_only_caption_context_observer=True,no_new_ROM_or_RAM_savestate_battery_fixture=True,source_B166_menu_only_not_story_activation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));old=harness.ct;harness.ct=Proxy();sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(CAP),'--frames','3501','--inputs-json',str(inputs),'--capture-every','999999','--capture-at','3000','3500','--dump-ram']
    try:harness.main()
    finally:
        harness.ct=old
        for o in observers:o.close()
    for o in observers:o.save()
    rp=CAP/'capture_report.json';report=read(rp);assert report['frames']==3501 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'];save(ROOT/'terminal.json',dict(terminal=True,report=str(rp),report_sha256=sha(rp.read_bytes()),ROM_sha256=spec['research_ROM_sha256'],observer_rows=sum(len(o.rows) for o in observers),all_host_slots_restored=True,full_goal_complete=False));print('Focused menu owner trace terminal;original caption view/backing arguments captured.',flush=True)
