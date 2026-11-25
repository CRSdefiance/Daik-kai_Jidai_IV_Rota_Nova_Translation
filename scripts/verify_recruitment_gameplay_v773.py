"""Actual ordinary recruiting glyphs,charge,crew flow and New Game controls."""

import re
import struct
from pathlib import Path

from PIL import Image,ImageChops

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import recruitment_editorial_runtime as runtime
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import probe_recruitment_layout_v771 as layout
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.prepare_recruitment_release_v773 import ROOT,MANUSCRIPT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_market_gameplay_v753 import snapshot,state
from scripts.verify_port_gameplay_v762 import capture,cstring
from scripts.verify_shipyard_gameplay_v760 import models,independent_font
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import save,read

BODY=(16,294,244,366)


def main():
    pa,old,old_arm,before=capture('recruitment_v773_return_v770')
    pb,new,arm,after=capture('recruitment_v773_return_v773')
    assert old['frames']==new['frames']==8801
    assert old['scripted_input_schedule']==new['scripted_input_schedule'] and old['core_options']==new['core_options']
    assert set(before)==set(after)
    rom=NdsImage.open(new['ROM']);common=rom.read_file('/COMMON/MESFILE.DK4')
    entries=common_message_entries(common,arm,clean=False);blocks=IlnkContainer.parse(common).blocks
    doc={r['message_id']:r for r in read(MANUSCRIPT)['records']}
    env=dict(layout.__dict__);env['runtime']=runtime
    from types import FunctionType
    formatter=FunctionType(layout.formatter.__code__,env)()[0]
    p,w,owner=[struct.unpack_from('<I',arm,at)[0] for at in(0x5444C,0x54450,0x552A0)]
    scenes=[];controls=[];states=[]
    for frame in sorted(after):
        a,b=[Image.open(rows[frame]['path']).convert('RGB') for rows in(before,after)]
        diff=ImageChops.difference(a,b)
        if frame not in(5000,5200,5400,5600,5800,6000,6200,6400):
            assert diff.getbbox() is None,(frame,diff.getbbox())
            controls.append(frame);continue
        raw=snapshot(new,frame);template=cstring(raw,owner+0x2030)
        selected=[n for n in doc if entries[n].text==template];assert len(selected)==1,(frame,template)
        n=selected[0];assert raw.count(blocks[entries[n].block])==1
        printf=cstring(raw,p)
        match=re.fullmatch(b'(.*?)'.join(re.escape(part) for part in template.split(b'%s')),printf);assert match,(frame,template,printf)
        u=machine(arm);u.mem_write(BASE,raw)
        native=formatter(u,doc[n],match.groups())
        assert not native['findings'] and bytes.fromhex(native['formatted_hex'])==cstring(raw,w)
        plane=raster(arm,bytes.fromhex(native['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
        assert plane==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),native['lines'])
        expected={(16+i%228,296+i//228) for i,v in enumerate(plane) if v==1}
        actual={(x,y) for y in range(BODY[1],BODY[3]) for x in range(BODY[0],BODY[2]) if b.getpixel((x,y))==(0,8,0)}
        assert expected==actual,(frame,len(expected-actual),len(actual-expected))
        previous={(x,y) for y in range(BODY[1],BODY[3]) for x in range(BODY[0],BODY[2]) if a.getpixel((x,y))==(0,8,0)}
        shadows={(x+1,y+1) for x,y in expected|previous}
        unexpected=[(x,y) for y in range(BODY[1],BODY[3]) for x in range(BODY[0],BODY[2])
            if(x,y) not in expected|previous|shadows and a.getpixel((x,y))!=b.getpixel((x,y))]
        assert not unexpected,(frame,unexpected[:10])
        diff.paste((0,0,0),BODY);assert diff.getbbox() is None,(frame,diff.getbbox())
        scenes.append({'frame':frame,'message_id':n,'source_arguments_hex':[s.hex() for s in match.groups()],
            'lines':native['lines'],'capture':after[frame],'complete_independent_font_and_blank_paper_cells_exact':True,
            'all_other_pixels_including_controls_portraits_and_advance_exact':True})
    assert {r['message_id'] for r in scenes}=={890,897,904,907}
    for frame in new['exact_requested_capture_frames']:
        if frame<3200:continue
        x,y=snapshot(old,frame),snapshot(new,frame)
        assert state(old_arm,x)==state(arm,y),(frame,'state')
        assert models(old_arm,x)==models(arm,y),(frame,'models')
        assert persistent_objects(old_arm,x)==persistent_objects(arm,y),(frame,'persistent')
        states.append(frame)
    start=state(arm,snapshot(new,3200));charged=state(arm,snapshot(new,5400))
    cost=next(r for r in scenes if r['message_id']==890)['source_arguments_hex'][0]
    amount=int(bytes.fromhex(cost).decode('cp932'))
    assert start['cash']-charged['cash']==amount
    pc,start_old,_,start_before=capture('tavern_round_v770_newgame_v770')
    pd,start_new,_,start_after=capture('recruitment_v773_newgame_v773')
    assert start_old['scripted_input_schedule']==start_new['scripted_input_schedule']
    assert start_new['frames']==4000 and not start_new.get('battery_save_preloaded')
    assert set(start_before)==set(start_after)=={1,60,180,1600,2000,3200,4000}
    assert all(Path(start_before[f]['path']).read_bytes()==Path(start_after[f]['path']).read_bytes() for f in start_after)
    save(ROOT/'recruitment_gameplay_verification.json',{'candidate':new['ROM'],'candidate_sha256':new['ROM_sha256'],
        'actual_cost_invitation_crowd_count_holds':scenes,'whole_screen_controls':controls,
        'paired_native_state_model_frames':states,'source_cost':amount,'cash_before':start['cash'],'cash_after':charged['cash'],
        'source34_volunteers_unassigned_and_native_Assign_Sailors_flow':True,'ordinary_return_frame':8800,
        'all7_New_Game_frames_byte_identical':True,'capture_reports':[str(pa),str(pb),str(pc),str(pd)],
        'no_RAM_fixture_or_savestate_in_these_runs':True,'condition_rumor_actual_scenes_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(f'Eight actual holds across890/897/907/904,{amount} gold charged,ordinary crew flow/return and7 New Game controls pass. Condition rumors pending.',flush=True)


if __name__=='__main__':main()
