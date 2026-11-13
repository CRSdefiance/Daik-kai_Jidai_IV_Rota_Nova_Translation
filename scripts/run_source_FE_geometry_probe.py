"""Observe source FE descriptors in a disclosed content fixture using the frozen read-only observer."""
import argparse
import ctypes as ct
import inspect
import os
import struct
import sys
import textwrap
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import observe_lil_modal_v1733 as original
from scripts.audit_story_glyph_consistency import load,save
from scripts.inspect_committed_gpu_v646 import CORE,CORE_SHA
from scripts.source_locked_derivation_v5118 import checked_text


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ['fixture','out','capture']:parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists() and not args.capture.exists()
    fixture=load(args.fixture);rom=Path(fixture['research_ROM']);assert sha(rom.read_bytes())==fixture['research_ROM_sha256']
    arm=NdsImage.open(rom).read_file('/__arm9__.bin');contract=load('work/analysis/script_sources_v733/source_contract.json')
    core=CORE.read_bytes();assert sha(core)==CORE_SHA==contract['core_sha256']
    preferred=contract['interpreter_table']['source_VA']-contract['interpreter_table']['RVA'];targets=[]
    clean_arm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for offset,name in [(0x548A8,'modal_entry'),(0x54924,'modal_paint')]:
        word=struct.unpack_from('<I',arm,offset)[0]
        if offset==0x548A8:
            assert arm[offset:offset+4]==clean_arm[offset:offset+4]
        else:
            # The accepted alignment layer intentionally redirects this BL.
            # Its original R0/R1 setup and current typed-paper target are the ABI boundary.
            assert arm[offset-8:offset]==clean_arm[offset-8:offset]==bytes.fromhex('0700a0e10810a0e1')
            assert word==0xEBFEA145
            delta=(word&0xFFFFFF)<<2
            if delta&0x2000000:delta-=0x4000000
            assert 0x02000000+offset+8+delta==0x01FFCE40
        index=((word>>16)&0xFF0)|((word>>4)&15)
        address=struct.unpack_from('<Q',core,contract['interpreter_table']['file_offset']+index*8)[0]
        targets.append(dict(PC=0x02000000+offset,word=word,name=name,instruction_index=index,handler_RVA=address-preferred))
    contract['targets']=targets;args.out.mkdir(parents=True)
    contractpath=args.out/'source_contract.json';save(contractpath,contract)
    adapter=checked_text(textwrap.dedent(inspect.getsource(original.Observer.__init__)),{
        "    packet=read('work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json')\n    self.FE_bodies={r['current_native_macro_output_hex'] for block in packet['blocks'] if block['block']==120 for r in block['records'] if r['source_presentation_prefix_hex']=='fe'}":
        "    self.FE_bodies=set(EXPECTED_FE_BODIES)",
        "if target['name']=='modal_paint' and body.hex() in self.FE_bodies:":
        "if target['name']=='modal_paint' and frame>=3000:",
    })
    env={**original.__dict__,'EXPECTED_FE_BODIES':fixture['expected_FE_bodies_hex']}
    exec(compile(adapter,__file__+'::same-readonly-source-modal-observer','exec'),env)
    class Observer(original.Observer):__init__=env['__init__']
    save(args.out/'run_plan.json',dict(fixture=str(args.fixture),fixture_sha256=sha(args.fixture.read_bytes()),PID=os.getpid(),
        research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),frames=fixture['frames'],inputs=fixture['inputs'],inputs_sha256=fixture['inputs_sha256'],
        capture_folder=str(args.capture),source_owned_observer_adapter=adapter,read_only_PC_filters=targets,
        original_observer=str(Path(original.__file__)),original_observer_sha256=sha(Path(original.__file__).read_bytes()),
        no_savestate_battery_or_emulated_memory_override=True,source_content_fixture_not_natural_story_activation=True,
        guide_photos=False,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    observers=[]
    class Proxy:
        def __getattr__(self,name):return getattr(ct,name)
        def CDLL(self,path,*other,**kwargs):
            lib=ct.CDLL(path,*other,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer=Observer(lib,args.capture/'modal_observer',contractpath);observer.install();observers.append(observer)
                original_run=lib.retro_run;original_run.restype=None
                def run():observer.next_frame();original_run()
                lib.retro_run=run
            return lib
    old=harness.ct;harness.ct=Proxy()
    sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(args.capture),'--frames',str(fixture['frames']),
        '--inputs-json',fixture['inputs'],'--capture-every','120','--dump-ram']
    try:harness.main()
    finally:
        harness.ct=old
        for observer in observers:observer.close()
    for observer in observers:observer.save()
    reportpath=args.capture/'capture_report.json';observedpath=args.capture/'modal_observer/actual_modal_contexts.json'
    report,observed=load(reportpath),load(observedpath)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
    assert len(observers)==1 and not observed['errors'] and not observed['mismatches'] and observed['all_host_slots_restored_and_core_file_exact']
    save(args.out/'terminal.json',dict(terminal=True,frames=report['frames'],report=str(reportpath),report_sha256=sha(reportpath.read_bytes()),
        observer=str(observedpath),observer_sha256=sha(observedpath.read_bytes()),modal_paints=sum(r['kind']=='modal_paint' for r in observed['rows']),
        actual_source_content_cold_boot_not_natural_endgame=True,geometry_visual_andpixel_binding_pending=True,new_credit=0,new_registered_ROM=False))
    print('Source content geometry probe terminal;read-only callbacks restored. Bind observed descriptors andview captures before approving geometry.')
