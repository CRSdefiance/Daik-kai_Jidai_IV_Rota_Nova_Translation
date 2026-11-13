"""Bounded source-guarded live contact pilot; inspect native predicate/roll trace."""
import ctypes as ct
import json
import struct
import time
from collections import Counter
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_lookout_contact_v1798b import ROM,apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lookout_navigation_v1800')
RUN=Path('work/analysis/observed_lookout_v1799')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/observed_lookout_v1799_1775')
BASE=0x02000000


def append(command):
    with(RUN/'navigation.jsonl').open('a',encoding='utf-8')as f:f.write(json.dumps(command)+'\n')


if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    pid=read(RUN/'run_plan.json')['PID'];kernel=ct.WinDLL('kernel32',use_last_error=True)
    kernel.OpenProcess.argtypes=[ct.c_uint,ct.c_int,ct.c_uint];kernel.OpenProcess.restype=ct.c_void_p
    kernel.GetExitCodeProcess.argtypes=[ct.c_void_p,ct.POINTER(ct.c_uint)];kernel.CloseHandle.argtypes=[ct.c_void_p]
    handle=kernel.OpenProcess(0x1000,0,pid);assert handle
    def alive():
        code=ct.c_uint();assert kernel.GetExitCodeProcess(handle,ct.byref(code));return code.value==259
    def snapshot(frame):
        path=CAP/f'frame_{frame:06d}_arm9_ram.bin';photo=CAP/f'frame_{frame:06d}_navigation.png';deadline=time.monotonic()+60
        while True:
            assert alive(),'Original emulator is terminal;do notrestart from observation timeout'
            try:
                raw=path.read_bytes();assert len(raw)==0x400000
                image=Image.open(photo).convert('RGB');image.load();assert image.size==(256,384)
                progress=read(RUN/'live_observer_progress.json');assert not progress['errors']and not progress['mismatches']
                return raw,photo,image,progress
            except (OSError,ValueError,AssertionError):
                if time.monotonic()>deadline:raise TimeoutError('Keep the same emulator;requested pause not observed:'+str(frame))
                time.sleep(.05)
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');owner=struct.unpack_from('<I',arm,0x552A0)[0]
    observations=[];frame=5503;reason='bounded_contact_pilot';first=True
    try:
        for cycle in range(401):
            raw,photo,image,progress=snapshot(frame)
            cpu,get=get_machine(arm,raw);root=get(0xCB1A8)
            template=raw[owner-BASE+0x2030:owner-BASE+0x2130].split(b'\0')[0]
            paper=sum(1 for y in range(298,360,4)for x in range(18,242,4)
                if(lambda c:c[0]>170 and c[1]>145 and c[0]>c[2]+20)(image.getpixel((x,y))))>450
            counts=dict(Counter(r['kind']for r in progress['rows']))
            context=list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))
            row={'cycle':cycle,'frame':frame,'RAM_sha256':sha(raw),'capture':str(photo),'capture_sha256':sha(photo.read_bytes()),
                'template_hex':template.hex(),'paper_navigation_heuristic_only':paper,'source_battle_context':context,
                'observer_counts':counts,'native_Lookout_Aim':get(0x8235C,root+0x2090,7,6,0)}
            observations.append(row)
            if counts.get('shot_announcement',0):
                reason='original_shot_announcement_boundary_observed';holds=[]
                for gap in(300,30):
                    append({'until':frame+gap,'duration':1});frame+=gap
                    data,picture,_,_=snapshot(frame)
                    holds.append({'frame':frame,'RAM_sha256':sha(data),'capture':str(picture),'capture_sha256':sha(picture.read_bytes())})
                row['full_hold_candidates']=holds;break
            if paper:reason='other_original_modal_observed';break
            if context!=[0,1,8]:reason='original_battle_context_changed';break
            if cycle==400:break
            request={'lookout_contact':'qualify'if first else'maintain'}
            try:_,receipt=apply_fixture(arm,raw,request)
            except AssertionError as error:
                row['precondition_rejection']=str(error);reason='source_health_contact_or_staffing_precondition_rejected';break
            row['fixture_preflight']=receipt
            command={'until':frame+(10 if first else 2),'duration':8 if first else 1,'battle_fixture':request}
            if first:command['buttons']=['B']
            append(command);frame=command['until'];first=False
            if cycle%20==0:print({'cycle':cycle,'frame':frame,'observed_original_checks':counts},flush=True)
            save(ROOT/'live_navigation_progress.json',{'observations':observations,'last_requested_frame':frame,
                'PID':pid,'same_process_confirmed_live':alive(),'commands_are_not_execution_receipts':True})
        save(ROOT/'bounded_result.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'PID':pid,
            'observations':observations,'paused_frame':frame,'reason':reason,'emulator_left_paused_not_terminal':True,
            'no_native_RNG_message_result_or_live_contact_cursor_override':True,
            'synthetic_survival_and_contact_fixtures_disclosed':True,'no_editorial_completion_credit':True,
            'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
        print({'paused':frame,'reason':reason,'native_predicate_counts':observations[-1]['observer_counts']},flush=True)
    finally:kernel.CloseHandle(handle)
