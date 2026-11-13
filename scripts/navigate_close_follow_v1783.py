"""Bounded source-coordinate follow;leave any selected original message paused."""
import json
import struct
import time
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_close_follow_v1781 import apply_fixture,INITIAL,FOLLOW,ROM
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/close_follow_navigation_v1783')
RUN=Path('work/analysis/close_follow_v1782_openWaterReady8')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/close_follow_v1782_1775_openWaterReady8')

def append(command):
    with (RUN/'navigation.jsonl').open('a',encoding='utf-8')as f:f.write(json.dumps(command)+'\n')

def snapshot(frame):
    raw_path=CAP/f'frame_{frame:06d}_arm9_ram.bin';photo=CAP/f'frame_{frame:06d}_navigation.png'
    deadline=time.monotonic()+60
    while True:
        try:
            raw=raw_path.read_bytes();assert len(raw)==0x400000
            image=Image.open(photo);image.load();assert image.size==(256,384)
            return raw,photo
        except (OSError,AssertionError):
            if time.monotonic()>deadline:raise TimeoutError('Observation timeout only;do not infer terminal orrestart:'+str(frame))
            time.sleep(.05)

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');owner=struct.unpack_from('<I',arm,0x552A0)[0]
    initial,_=snapshot(5100);baseline=cstring(initial,owner+0x2030);frame=5100;observations=[]
    for step in range(151):
        raw,photo=snapshot(frame);cpu,get=get_machine(arm,raw);root=get(0xCB1A8);enemy=root+4+8*132
        template=cstring(raw,owner+0x2030);seen=bool(cpu.mem_read(enemy+0x50,1)[0]&4)
        observations.append({'frame':frame,'RAM_sha256':sha(raw),'capture':str(photo),'capture_sha256':sha(photo.read_bytes()),
            'template_hex':template.hex(),'enemy8_seen':seen,
            'own_point':list(struct.unpack('<2i',cpu.mem_read(root+4+132+0x34,8))),
            'enemy8_point':list(struct.unpack('<2i',cpu.mem_read(enemy+0x34,8))),
            'original_loaded_groups_hex':bytes(cpu.mem_read(root+0x2080,16)).hex()})
        if seen or template!=baseline:
            selected_frame=frame;holds=[]
            for jump in (300,30):
                append({'until':frame+jump,'duration':1});frame+=jump
                data,picture=snapshot(frame)
                holds.append({'frame':frame,'capture':str(picture),'capture_sha256':sha(picture.read_bytes()),'RAM_sha256':sha(data)})
            save(ROOT/'selected_original_event_hold_ready.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
                'baseline_template_hex':baseline.hex(),'selection_frame':selected_frame,'selected_template_hex':template.hex(),
                'enemy8_seen_at_selection':seen,'observations':observations,'holds':holds,'paused_frame':frame,
                'normal_input_B_only_to_close_Info_no_message_dismissal_yet':True,
                'source_selected_event_not_yet_verified_as_target':True,'emulator_left_paused_not_terminal':True,
                'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
            print({'original_event_selected_at':selected_frame,'seen':seen,'template':template.decode('cp932'),'paused':frame},flush=True)
            break
        if step==150:
            save(ROOT/'bounded_follow_terminal_request.json',{'observations':observations,'last_frame':frame,
                'reason':'150-frame limit without original selection','no_target_credit':True,'full_goal_complete':False})
            append({'stop':True});print({'bounded_limit':frame,'no_target_credit':True},flush=True);break
        request=INITIAL if step==0 else FOLLOW
        try:_,preflight=apply_fixture(arm,raw,request)
        except AssertionError as error:
            save(ROOT/'bounded_follow_terminal_request.json',{'observations':observations,'last_frame':frame,
                'reason':'source precondition refuses next fixture','details':str(error),'no_target_credit':True,'full_goal_complete':False})
            append({'stop':True});print({'safe_stop':frame,'reason':str(error)},flush=True);break
        observations[-1]['proposed_fixture_preflight']=preflight
        command={'until':frame+1,'duration':8 if step==0 else 1,'battle_fixture':request}
        if step==0:command['buttons']=['B']
        append(command);frame+=1
        if step%20==0:print({'following_frame':frame,'source_target':preflight['target_original_virtual_position'],'native_known_town':115},flush=True)
