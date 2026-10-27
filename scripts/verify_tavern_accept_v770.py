"""Actual ordinary round payment,captain,barkeep,patron and treasure tip."""

import re
import struct
from pathlib import Path

from PIL import Image,ImageChops

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.probe_tavern_continuation_layout_v768 import format_case
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_market_gameplay_v753 import snapshot,state
from scripts.verify_port_gameplay_v762 import capture,cstring
from scripts.verify_shipyard_gameplay_v760 import models,independent_font
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_release_v770')
BODY=(16,294,244,366)


def main():
    pa,old,old_arm,before=capture('tavern_round_v770_accept_v767')
    pb,new,arm,after=capture('tavern_round_v770_accept_v770')
    assert old['frames']==new['frames']==8201
    assert old['scripted_input_schedule']==new['scripted_input_schedule'] and old['core_options']==new['core_options']
    assert set(before)==set(after)
    rom=NdsImage.open(new['ROM']);common=rom.read_file('/COMMON/MESFILE.DK4')
    entries=common_message_entries(common,arm,clean=False);blocks=IlnkContainer.parse(common).blocks
    doc={r['message_id']:r for r in read('translations/tavern_continuation_editorial_manuscript_v3.json')['records']}
    p,w,owner=[struct.unpack_from('<I',arm,at)[0] for at in(0x5444C,0x54450,0x552A0)]
    scenes=[];controls=[];states=[]
    for frame in sorted(after):
        a,b=[Image.open(rows[frame]['path']).convert('RGB') for rows in(before,after)]
        diff=ImageChops.difference(a,b)
        if frame not in(5000,5200,5400,5800,6200,6600):
            assert diff.getbbox() is None,(frame,diff.getbbox())
            controls.append(frame);continue
        raw=snapshot(new,frame)
        template=cstring(raw,owner+0x2030)
        selected=[n for n in (852,865,872,874,870) if entries[n].text==template];assert len(selected)==1
        n=selected[0];assert raw.count(blocks[entries[n].block])==1
        printf=cstring(raw,p)
        m=re.fullmatch(b'(.*?)'.join(re.escape(part) for part in template.split(b'%s')),printf);assert m
        u=machine(arm);u.mem_write(BASE,raw)
        native=format_case(u,doc[n],m.groups())
        assert not native['findings'] and bytes.fromhex(native['formatted_hex'])==cstring(raw,w)
        plane=raster(arm,bytes.fromhex(native['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
        assert plane==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),native['lines'])
        expected={(16+i%228,296+i//228) for i,v in enumerate(plane) if v==1}
        actual={(x,y) for y in range(BODY[1],BODY[3]) for x in range(BODY[0],BODY[2]) if b.getpixel((x,y))==(0,8,0)}
        assert expected==actual,(frame,len(expected-actual),len(actual-expected))
        previous={(x,y) for y in range(BODY[1],BODY[3]) for x in range(BODY[0],BODY[2]) if a.getpixel((x,y))==(0,8,0)}
        shadows={(x+1,y+1) for x,y in expected|previous}
        unexpected=[(x,y) for y in range(BODY[1],BODY[3]) for x in range(BODY[0],BODY[2]) if(x,y) not in expected|previous|shadows and a.getpixel((x,y))!=b.getpixel((x,y))]
        assert not unexpected,(frame,unexpected[:10])
        diff.paste((0,0,0),BODY);assert diff.getbbox() is None,(frame,diff.getbbox())
        scenes.append({'frame':frame,'message_id':n,'arguments_cp932':[s.decode('cp932') for s in m.groups()],
            'lines':native['lines'],'capture':after[frame],'full_independent_font_plane_and_blank_paper_cells_exact':True,
            'all_pixels_outside_text_plane_including_YesNo_buttons_exact':True})
    for frame in new['exact_requested_capture_frames']:
        if frame<3200:continue
        x,y=snapshot(old,frame),snapshot(new,frame)
        assert state(old_arm,x)==state(arm,y),(frame,'native state')
        assert models(old_arm,x)==models(arm,y),(frame,'models')
        assert persistent_objects(old_arm,x)==persistent_objects(arm,y),(frame,'persistent objects')
        states.append(frame)
    pc,start_old,_,start_before=capture('port_services_v762_newgame_762')
    pd,start_new,_,start_after=capture('tavern_round_v770_newgame_v770')
    assert start_old['scripted_input_schedule']==start_new['scripted_input_schedule']
    assert start_new['frames']==4000 and not start_new.get('battery_save_preloaded')
    assert set(start_before)==set(start_after)=={1,60,180,1600,2000,3200,4000}
    assert all(Path(start_before[f]['path']).read_bytes()==Path(start_after[f]['path']).read_bytes() for f in start_after)
    cash_before=state(arm,snapshot(new,3200))['cash']
    cash_after=state(arm,snapshot(new,6600))['cash']
    cost=int(next(r['arguments_cp932'][0] for r in scenes if r['message_id']==852))
    assert cash_before-cash_after==cost==314
    assert state(arm,snapshot(new,7800))['cash']==cash_after-5
    save(ROOT/'accept_gameplay_verification.json',{'candidate':new['ROM'],'candidate_sha256':new['ROM_sha256'],
        'six_actual_round_path_holds':scenes,'whole_screen_controls':controls,'paired_native_state_object_frames':states,
        'all7_New_Game_frames_byte_identical':True,'capture_reports':[str(pa),str(pb),str(pc),str(pd)],
        'ordinary_inputs_only_no_RAM_fixture_or_savestate':True,'other27_messages_native_source_font_coverage_with_family_sampling':True,
        'native_payment_receipt':{'cash_before':cash_before,'cash_after_round':cash_after,'displayed_cost':cost,'subsequent_ordinary_drink_charge':5},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Six actual round-path holds,payment/native models,full unchanged controls and seven New Game frames pass.',flush=True)


if __name__=='__main__':main()
