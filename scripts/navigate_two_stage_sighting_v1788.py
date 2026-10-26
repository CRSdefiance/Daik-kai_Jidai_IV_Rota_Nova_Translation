"""Let the original loader admit fleet8,then approach without touching its flags."""
import json
import struct
import time
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_two_stage_sighting_v1786b import apply_fixture,ROM
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/two_stage_navigation_v1788')
RUN=Path('work/analysis/two_stage_sighting_v1787_twoStageReady8')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/two_stage_sighting_v1787_1775_twoStageReady8')

def append(command):
    with (RUN/'navigation.jsonl').open('a',encoding='utf-8')as f:f.write(json.dumps(command)+'\n')

def snapshot(frame):
    raw_path=CAP/f'frame_{frame:06d}_arm9_ram.bin';photo=CAP/f'frame_{frame:06d}_navigation.png';deadline=time.monotonic()+60
    while True:
        try:
            data=raw_path.read_bytes();assert len(data)==0x400000
            image=Image.open(photo);image.load();assert image.size==(256,384)
            return data,photo
        except (OSError,AssertionError):
            if time.monotonic()>deadline:raise TimeoutError('Observation timeout only;keep the same emulator:'+str(frame))
            time.sleep(.05)

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');owner=struct.unpack_from('<I',arm,0x552A0)[0]
    first,_=snapshot(5100);baseline=cstring(first,owner+0x2030);frame=5100;rows=[];previous=None;close=False;loaded_streak=0
    for step in range(81):
        raw,photo=snapshot(frame);cpu,get=get_machine(arm,raw);root=get(0xCB1A8);own,enemy=root+4+132,root+4+8*132
        point=list(struct.unpack('<2i',cpu.mem_read(own+0x34,8)));target=list(struct.unpack('<2i',cpu.mem_read(enemy+0x34,8)))
        groups=bytes(cpu.mem_read(root+0x2080,16));template=cstring(raw,owner+0x2030);seen=bool(cpu.mem_read(enemy+0x50,1)[0]&4)
        row={'frame':frame,'own_point':point,'original_target':target,'groups_hex':groups.hex(),'enemy8_seen':seen,
            'template_hex':template.hex(),'RAM_sha256':sha(raw),'capture':str(photo),'capture_sha256':sha(photo.read_bytes())};rows.append(row)
        if seen or template!=baseline:
            holds=[];selection=frame
            for gap in (300,30):
                append({'until':frame+gap,'duration':1});frame+=gap;data,picture=snapshot(frame)
                holds.append({'frame':frame,'capture':str(picture),'capture_sha256':sha(picture.read_bytes()),'RAM_sha256':sha(data)})
            save(ROOT/'selected_original_event_hold_ready.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
                'observations':rows,'selected_template_hex':template.hex(),'selection_frame':selection,'holds':holds,
                'paused_frame':frame,'native_loading_before_close_observed':close,
                'no_message_dismissal_or_target_credit_yet':True,'emulator_left_paused_not_terminal':True,
                'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
            print({'original_selection':selection,'template':template.decode('cp932'),'paused':frame,'native_loaded_before_close':close},flush=True);break
        if step==80:
            save(ROOT/'bounded_stop.json',{'observations':rows,'reason':'80-step limit without selection','last_frame':frame,'no_target_credit':True})
            append({'stop':True});print({'bounded_stop':frame},flush=True);break
        loaded_streak=loaded_streak+1 if 8 in groups[::4] else 0
        if loaded_streak>=2 and previous is not None:
            own_move=[point[i]-previous['fixture_point'][i]for i in range(2)]
            enemy_move=[target[i]-previous['target'][i]for i in range(2)]
            compensation=[enemy_move[i]-own_move[i]for i in range(2)]
            assert max(map(abs,compensation))<=32
            proposed=[target[i]+compensation[i]for i in range(2)];context='closeLoaded8';close=True
            row['source_observed_relative_motion_compensation']=compensation
        else:
            assert not close,'Do not restore visibility orforce a previously unloaded group'
            proposed=[target[0]-200,target[1]];context='loadReady8'if step==0 else'holdLoadReady8'
        request={'sighting_context':context,'own_point':proposed}
        try:_,preflight=apply_fixture(arm,raw,request)
        except AssertionError as error:
            save(ROOT/'bounded_stop.json',{'observations':rows,'reason':'source precondition rejected next location','details':str(error),'last_frame':frame,'no_target_credit':True})
            append({'stop':True});print({'safe_stop':frame,'reason':str(error)},flush=True);break
        row['fixture_preflight']=preflight
        previous={'fixture_point':proposed,'target':target}
        command={'until':frame+1,'duration':1,'battle_fixture':request}
        if step<8:command['buttons']=['B']
        append(command);frame+=1
        if step%10==0:print({'frame':frame,'stage':context,'target_loaded':8 in groups[::4]},flush=True)
