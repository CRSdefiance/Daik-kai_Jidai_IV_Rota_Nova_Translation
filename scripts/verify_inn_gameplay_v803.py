"""Actual revised Inn stays:complete glyphs,controls,fees,calendar and returns."""

import inspect
import struct
from pathlib import Path
from types import FunctionType

from PIL import Image,ImageChops

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import inn_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts import verify_shared_newgame_v782 as startup
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_palace_gameplay_v797 import load as original_load
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import independent_font,models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read,save
from unicorn.arm_const import UC_ARM_REG_R0

ROOT=owned.ROOT
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    loader_source=inspect.getsource(original_load)
    marker="rep['read_only_pause_RAM_snapshots']";assert loader_source.count(marker)==1
    loader_source=loader_source.replace(marker,"rep.get('read_only_pause_RAM_snapshots',[])")
    loader_env={**original_load.__globals__};exec(compile(loader_source,__file__,'exec'),loader_env)
    load=loader_env['load']
    op,old,of,oram=load('inn_v801_context',8600)
    np,new,nf,nram=load('inn_v803_stays',8600)
    assert old['scripted_input_schedule']==new['scripted_input_schedule'] and old['core_options']==new['core_options']
    rom=NdsImage.open(new['ROM']);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    entries=owned.current_entries(common,arm);blocks=IlnkContainer.parse(common).blocks
    rows={r['message_id']:r for r in read('translations/inn_editorial_manuscript_v3.json')['records']}
    source=(ROOT/'effective_format_case.py').read_text(encoding='utf-8')
    env={**original.__dict__};exec(compile(source,str(ROOT/'effective_format_case.py'),'exec'),env)
    owner,printed,wrapped=[struct.unpack_from('<I',arm,n)[0] for n in (0x552A0,0x5444C,0x54450)]
    holds=[];outside=[]
    for frame,n in ((4800,1177),(5200,1178),(6200,1179),(7000,1180),(7400,1181)):
        raw=nram[frame];assert cstring(raw,owner+0x2030)==entries[n].text
        assert raw.count(blocks[entries[n].block])==1
        values=('３'.encode('cp932'),) if n==1180 else ()
        case=env['format_case'](prepared(arm),rows[n],values)
        assert cstring(raw,wrapped).hex()==case['formatted_hex'] and not case['findings']
        if n==1180:assert values[0] in cstring(raw,printed) and len(case['lines'])==1
        plane=raster(arm,bytes.fromhex(case['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
        assert plane==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
        b=Image.open(nf[frame]['path']).convert('RGB');a=Image.open(of[frame]['path']).convert('RGB')
        expected={(16+i%228,296+i//228) for i,p in enumerate(plane) if p==1}
        actual={(x,y) for y in range(294,366) for x in range(16,244) if b.getpixel((x,y))==(0,8,0)}
        assert expected==actual,(frame,n,len(expected-actual),len(actual-expected))
        diff=ImageChops.difference(a,b);diff.paste((0,0,0),(16,294,244,366))
        assert diff.getbbox() is None,(frame,diff.getbbox())
        outside.append(dict(frame=frame,whole_outside_dialogue_plane_exact=True))
        holds.append(dict(frame=frame,message_id=n,capture=nf[frame],lines=case['lines'],
            complete_independent_font_exact=True,complete_first_final_letters_and_visible_left_margin=True,
            native_resident_complete_block_exact=True,no_unexpected_dark_ink_on_blank_paper=True))
    changed={r['frame'] for r in holds};controls=[]
    for frame in sorted(nf):
        if frame in changed:continue
        a,b=[Image.open(fs[frame]['path']).convert('RGB') for fs in (of,nf)]
        assert a.tobytes()==b.tobytes(),frame
        controls.append(dict(frame=frame,whole_screen_exact=True))
    old_arm=NdsImage.open(old['ROM']).read_file('/__arm9__.bin')
    states=[]
    for frame in sorted(nram):
        left,right=oram[frame],nram[frame]
        assert state(old_arm,left)==state(arm,right)
        assert models(old_arm,left)==models(arm,right)
        assert persistent_objects(old_arm,left)==persistent_objects(arm,right)
        assert tasks(old_arm,left)==tasks(arm,right)
        u=machine(arm);u.mem_write(BASE,right);call(u,0xCB1B4,());cal=u.reg_read(UC_ARM_REG_R0)
        tick=struct.unpack('<I',u.mem_read(cal+8,4))[0]
        states.append(dict(frame=frame,financial_state=state(arm,right),calendar_tick=tick,
            original_models_actors_towns_items_goods_couriers_equal_baseline=True))
    at={r['frame']:r for r in states}
    assert [at[f]['financial_state']['cash'] for f in (4400,5600,8200,8600)]==[8371,8370,8367,8367]
    assert at[5600]['calendar_tick']-at[4400]['calendar_tick']==48
    assert at[8200]['calendar_tick']-at[5600]['calendar_tick']==144
    save(ROOT/'stay_gameplay_verification.json',dict(candidate=new['ROM'],candidate_sha256=new['ROM_sha256'],
        reports=[str(op),str(np)],actual_holds=holds,outside_body_comparisons=outside,control_frames=controls,
        native_state_pairs=states,one_night_cost1_and_three_nights_cost3=True,
        normal_menu_return_frames=[5600,8200],normal_town_return_frame=8600,
        donor_source_unchanged=True,source_input_schedule_exact=True,
        actual_insufficient_funds_reports_and_market_battle_rumors_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),optional_pause_RAM_loader_sha256=sha(loader_source.encode()),full_goal_complete=False))
    FunctionType(startup.main.__code__,{**startup.__dict__,'ROOT':ROOT,'REPORT':CAP/'inn_v803_newgame/capture_report.json',
        '__file__':str(Path(__file__).resolve())})()
    print(f'V803:five actual Inn holds,all complete fonts,{len(controls)} full-screen controls,{len(states)} complete object/state pairs,exact1+3-night fees/calendar and seven New Game frames pass.',flush=True)


if __name__=='__main__':main()
