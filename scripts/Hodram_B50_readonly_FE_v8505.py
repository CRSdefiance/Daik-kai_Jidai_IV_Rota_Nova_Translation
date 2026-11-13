"""Read-only FE factory and held-state exporter from immutable B49 producers."""
import ctypes as ct,inspect,struct,textwrap
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import observe_lil_modal_v1733 as original
from scripts.inspect_committed_gpu_v646 import CORE,CORE_SHA
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

def create(corelib,folder,cap,arm,body):
    contract=read('work/analysis/script_sources_v733/source_contract.json');core=CORE.read_bytes();assert sha(core)==CORE_SHA==contract['core_sha256'];preferred=contract['interpreter_table']['source_VA']-contract['interpreter_table']['RVA'];targets=[]
    for at,name in [(0x548A8,'modal_entry'),(0x54924,'modal_paint')]:
        word=struct.unpack_from('<I',arm,at)[0];index=((word>>16)&0xFF0)|((word>>4)&15);address=struct.unpack_from('<Q',core,contract['interpreter_table']['file_offset']+index*8)[0];targets.append(dict(PC=0x02000000+at,word=word,name=name,instruction_index=index,handler_RVA=address-preferred))
    contract['targets']=targets
    adapter=checked_text(textwrap.dedent(inspect.getsource(original.Observer.__init__)),{
        "    packet=read('work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json')\n    self.FE_bodies={r['current_native_macro_output_hex'] for block in packet['blocks'] if block['block']==120 for r in block['records'] if r['source_presentation_prefix_hex']=='fe'}":"    self.FE_bodies={FE_BODY_HEX}\n    self.snapshot_count=0",
        "if target['name']=='modal_paint' and body.hex() in self.FE_bodies:":"if target['name']=='modal_paint' and body.hex() in self.FE_bodies and not self.snapshot_count:\n                self.snapshot_count+=1",
    })
    env={**original.__dict__,'FE_BODY_HEX':body};exec(compile(adapter,__file__+'::source-qualified-one-FE-boundary','exec'),env)
    class Observer(original.Observer):
        __init__=env['__init__']
    contractpath=folder/'modal_source_contract.json';save(contractpath,contract)
    observer=Observer(corelib,cap/'modal_observer',contractpath);observer.install()
    return observer,contractpath,adapter

def export_held(o,frame,folder,snapshots):
    def snapshot(o,frame):
        cpu=ct.string_at(o.cpu,128);raw=ct.string_at(o.wram,0x400000)
        dtcm=o.image.read(o.dtcm,0x4000);itcm=o.image.read(o.itcm,0x8000);base_raw=o.image.read(o.dtcm_base,4)
        paths={}
        for key,data in [('CPU',cpu),('WRAM',raw),('DTCM',dtcm),('ITCM',itcm)]:
            p=folder/f'FE_hold_frame{frame}_{key}.bin';assert not p.exists();p.write_bytes(data)
            paths[key]=dict(path=str(p),sha256=sha(data),bytes=len(data))
        assert ct.string_at(o.cpu,128)==cpu and ct.string_at(o.wram,0x400000)==raw
        assert o.image.read(o.dtcm,0x4000)==dtcm and o.image.read(o.itcm,0x8000)==itcm and o.image.read(o.dtcm_base,4)==base_raw
        snapshots.append(dict(frame=frame,files=paths,DTCM_base=struct.unpack('<I',base_raw)[0],all_CPU_WRAM_DTCM_ITCM_andconfiguration_exact_before_after_readonly_export=True))
    snapshot(o,frame)
