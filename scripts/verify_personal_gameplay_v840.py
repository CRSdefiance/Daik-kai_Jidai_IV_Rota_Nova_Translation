"""Bind actual Deck comments to native selection, complete fonts and visible RGB."""

import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.personal_chatter_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v712 import load
from scripts.native_call_abi_v764 import call
from scripts.native_deck_elapsed_fixture_v839 import assign
from scripts.native_machine_scoped_v764 import machine
from scripts.personal_chatter_layout_v837 import compiled, layout
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels
from scripts.verify_full_fleet_battle_v652 import fleet_models
from scripts.verify_village_wrap_v608 import read, save

BASE = 0x02000000
ROOT = Path('work/analysis/personal_chatter_v840')
ROM = Path('out/all_routes_combined_v838_candidate.nds')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
CASES = {'Rafael': ('personal_activity_v839_838_Rafael_later',16900),
         'Charles': ('personal_cabin_v840_838_Charles_after',5400)}


def get_machine(arm, raw):
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    def get(at, *args):
        call(cpu, at, args)
        return cpu.reg_read(UC_ARM_REG_R0)
    return cpu, get


def rtti(raw, vtable):
    ti = struct.unpack_from('<I',raw,vtable-BASE-4)[0]
    name = struct.unpack_from('<I',raw,ti-BASE+4)[0]
    return raw[name-BASE:name-BASE+64].split(b'\0')[0].decode('ascii')


def actual_view(raw):
    matches, at = [], raw.find(struct.pack('<I',0x021314E8))
    while at >= 0:
        parent = at - 0x2194
        if parent >= 0 and at + 0x104 < len(raw):
            if struct.unpack_from('<I',raw,parent)[0] == 0x02130EF0 and struct.unpack_from('<I',raw,at+0x100)[0] == 3:
                resource = struct.unpack_from('<I',raw,at+0x50)[0]
                if BASE <= resource < BASE+len(raw)-20:
                    h = struct.unpack_from('<5I',raw,resource-BASE)
                    if h[:3] == (4,63,96) and (resource+h[4]) & 0xFFFFFFFF == BASE+at+0x104:
                        matches.append((BASE+at,BASE+parent,resource,h))
        at = raw.find(struct.pack('<I',0x021314E8),at+4)
    assert len(matches) == 1, matches
    view,parent,resource,h = matches[0]
    assert rtti(raw,0x021314E8) == '18CDeckPersonnelView'
    assert rtti(raw,0x02130EF0) == '13CDeckLookView'
    return view,parent,resource,h


def projected(rom,raw,view,old_crop=False):
    cpu = machine(rom.read_file('/__arm9__.bin'))
    cpu.mem_write(BASE,raw)
    ov = loadOverlayTable(rom.rom.arm9OverlayTable,lambda oid,fid:rom.rom.files[fid])[0]
    cpu.mem_write(ov.ramAddress,bytes(ov.data))
    renderer = 0x02468000
    cpu.mem_write(renderer,struct.pack('<I',0x0215FA94))
    cpu.mem_write(renderer+0x100,bytes(8))
    if old_crop:
        cpu.mem_write(BASE+0x1147B8,struct.pack('<2I',144,24))
    commands = []
    def blit(u,pc,size,unused):
        sp=u.reg_read(UC_ARM_REG_SP)
        sizep,dest=struct.unpack('<2I',u.mem_read(sp,8))
        commands.append({'image':u.reg_read(UC_ARM_REG_R1),'layer':u.reg_read(UC_ARM_REG_R0),
            'flags':u.reg_read(UC_ARM_REG_R2),
            'source_origin':list(struct.unpack('<2i',u.mem_read(u.reg_read(UC_ARM_REG_R3),8))),
            'size':list(struct.unpack('<2i',u.mem_read(sizep,8))),
            'destination':list(struct.unpack('<2i',u.mem_read(dest,8)))})
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    hook=cpu.hook_add(UC_HOOK_CODE,blit,begin=0x01FF92D8,end=0x01FF92D8)
    try:
        call(cpu,0x14BE8,(view,renderer),instruction_limit=3000000)
    finally:
        cpu.hook_del(hook)
    return commands


def hold(rom,raw,image,row,slot):
    arm=rom.read_file('/__arm9__.bin')
    view,parent,resource,h=actual_view(raw)
    cpu,get=get_machine(arm,raw)
    controller=get(0xCB1A8)+struct.unpack_from('<I',arm,0x13C90)[0]
    actor=get(0x82BC4,controller,slot)
    assert actor == row['actor_ID']
    state=struct.unpack_from('<I',raw,parent-BASE+0x3A0)[0]
    assert state in (0,1)
    selected=[]
    def numeric(u,pc,size,unused):
        selected.append(u.reg_read(UC_ARM_REG_R0))
        u.reg_write(UC_ARM_REG_R0,0x02450000)
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    hook=cpu.hook_add(UC_HOOK_CODE,numeric,begin=BASE+0x5528C,end=BASE+0x5528C)
    try:
        # Numeric-selection proof only. No text is supplied or rendered here.
        call(cpu,0x12104,(actor,state))
    finally:
        cpu.hook_del(hook)
    assert selected == [row['message_id']]
    lines=layout(row['english'])
    events=[dict(kind='ascii',code=ord(c),style=15,x=x*6,y=60+y*12)
            for y,line in enumerate(lines) for x,c in enumerate(line)]
    pixels=expected_pixels(arm,rom.read_file('/GRP/KANJI.FNT'),events,4,background=0)
    expected=b''.join(pixels[y*128:y*128+126] for y in range(60,96))
    address=(resource+h[4])&0xFFFFFFFF
    actual=raw[address-BASE+60*126:address-BASE+96*126]
    assert expected == actual
    indices=bytes(n for b in actual for n in (b&15,b>>4))
    assert not any(indices[y*252+x] for y in range(36) for x in range(216,252))
    palette=(resource+h[3])&0xFFFFFFFF
    assert struct.unpack_from('<H',raw,palette-BASE+30)[0] == 0x8020
    mask=bytes(bool(indices[y*252+x]) for y in range(36) for x in range(216))
    rgb=list(image.convert('RGB').crop((16,112,232,148)).get_flattened_data())
    assert mask == bytes(c==(0,8,0) for c in rgb)
    new,old=projected(rom,raw,view),projected(rom,raw,view,True)
    assert new[:-1] == old[:-1]
    assert new[-1] == {**old[-1],'size':[216,36]}
    assert new[-1]['source_origin']==[0,60] and new[-1]['destination']==[16,112]
    assert old[-1]['size']==[144,24]
    lost=sum(bool(indices[y*252+x]) for y in range(36) for x in range(216) if x>=144 or y>=24)
    return {'message_id':row['message_id'],'actor_ID':actor,'assigned_room_slot':slot,
        'source_role_type':get(0x81F54,controller,actor),'original_parent_activity_state':state,
        'actual_view':view,'actual_parent':parent,'identity_from_unique_native_RTTI_geometry_not_text':True,
        'native_original12104_numeric_selection':selected,
        'numeric_probe_does_not_supply_or_render_text':True,'complete_English':row['english'],'visible_lines':lines,
        'full252x36_bitmap_body_matches_independent_complete_words':True,
        'whole216x36_actual_RGB_ink_and_blank_plane_matches':True,
        'uniform_x16_line_starts_complete_leading_and_trailing_letters':True,
        'native_parent_projection':new,'all_other_parent_draw_commands_palettes_and_frame_preserved':True,
        'ink_pixels_original_crop_would_drop':lost,'no_text_selector_role_or_code_override_in_actual_run':True}


def model_state(arm,raw):
    cpu,get=get_machine(arm,raw)
    controller=get(0xCB1A8)+0x2090
    company=get(0x397D8,get(0xCB160))
    force=get(0xCB160)+4+company*0x4C
    calendar=get(0xCB1B4)
    actors=get(0xCB184)
    owned=[n for n in range(4,25) if get(0x7E958,actors+4+n*32)==company]
    return {'funds':get(0x3CCC8,force),'calendar_tick':struct.unpack('<I',cpu.mem_read(calendar+8,4))[0],
        'all31_original_occupant_bytes':bytes(cpu.mem_read(controller+6,31)).hex(),
        'actual_owned_companion32_byte_records':{str(n):sha(bytes(cpu.mem_read(actors+4+n*32,32))) for n in owned},
        'five_ship_and_flagship_models':fleet_models(arm,raw)}


def main():
    rom=NdsImage.open(ROM);digest=sha(ROM.read_bytes())
    arm=rom.read_file('/__arm9__.bin')
    entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    manuscript=read('translations/personal_chatter_editorial_manuscript_v3.json')
    rows={r['message_id']:r for r in manuscript['records']}
    reports,shots,receipts,ram={},{},{},{}
    for case,(folder,frames) in CASES.items():
        report,images,receipt=load(CAP/folder,digest,frames)
        reports[case],shots[case],receipts[case]=report,images,receipt
        data={}
        for record in report.get('read_only_capture_RAM_snapshots',[])+report.get('read_only_pause_RAM_snapshots',[]):
            raw=Path(record['path']).read_bytes()
            assert record['read_only_export'] and len(raw)==0x400000 and sha(raw)==record['sha256']
            assert record['frame'] not in data or data[record['frame']]==raw
            data[record['frame']]=raw
        ram[case]=data
        donor=report['battery_save_preloaded']
        assert donor['source']!=donor['destination'] and donor['copied_byte_exact_before_cold_boot']
        assert sha(Path(donor['source']).read_bytes())==donor['source_sha256']
    fixtures=reports['Rafael']['synthetic_Deck_elapsed_counter_fixtures']
    assert len(fixtures)==3
    for fixture in fixtures:
        after,replay=assign(arm,ram['Rafael'][fixture['frame']],{'elapsed_ticks':961})
        assert replay=={k:v for k,v in fixture.items() if k!='frame'}
        assert sha(after)==fixture['after_RAM_sha256']
    assert reports['Rafael']['controlled_Deck_elapsed_adapter']['original_harness_file_unchanged']
    assert not any(v for k,v in reports['Rafael'].items() if k.startswith('synthetic_') and k!='synthetic_Deck_elapsed_counter_fixtures')
    assert not any(v for k,v in reports['Charles'].items() if k.startswith('synthetic_'))
    assert rows[1379]['english'].startswith('If I mix') and len(layout(rows[1379]['english'])[0])%2==1
    cases=[]
    for case,frame,number,slot in [('Rafael',10220,1367,1),('Rafael',10240,1367,1),
        ('Rafael',14500,1365,12),('Rafael',14700,1365,12),('Rafael',15500,1366,12),
        ('Rafael',15700,1366,12),('Charles',4600,1379,12),('Charles',4800,1379,12)]:
        assert entries[number].text==compiled(rows[number])
        item=hold(rom,ram[case][frame],shots[case][frame],rows[number],slot)
        item.update(case=case,frame=frame)
        cases.append(item)
    controls=[]
    for case,before,after in [('Rafael',13300,16900),('Charles',3800,5400)]:
        a,b=model_state(arm,ram[case][before]),model_state(arm,ram[case][after])
        assert a==b,(case,a,b)
        controls.append({'case':case,'before_frame':before,'normal_town_return_frame':after,
                         'complete_scoped_state_before_and_after':a,'all_equal':True})
    sheet=Image.new('RGB',(4*256,2*410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,item in enumerate(cases):
        x,y=i%4*256,i//4*410
        draw.text((x+4,y+4),f"{item['case']} {item['frame']} ID{item['message_id']}",fill='white')
        sheet.paste(shots[item['case']][item['frame']],(x,y+24))
    path=ROOT/'actual8_complete_personal_comment_holds.png';sheet.save(path)
    save(ROOT/'actual_gameplay_verification.json',{'candidate':str(ROM),'candidate_sha256':digest,
        'terminal_capture_receipts':receipts,'actual_complete_dialogue_holds':cases,
        'all3_elapsed_fixtures_replay_exactly_and_all_original_donors_preserved':True,
        'normal_Cabin_assignments_do_not_require_elapsed_or_role_fixtures':True,
        'original_timing_fixture_only_used_for_the_separate_Julio_animation_sample':True,
        'no_new_fixture_of_any_kind_in_Charles_run':True,'scoped_normal_return_state_controls':controls,
        'whole_game_PRNG_or_unobserved_state_parity_not_claimed':True,
        'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),'visual_review_pending':True,
        'scope':'Eight actual complete bitmap/RGB holds across four revised IDs. Janus/Claudio ordinary real Cabin assignments;Julio original timed activity with only two cooldown counters;Charles genuine owned companion and normal Cabin assignment,odd first-row phase. Normal cancel/town return preserves scoped funds,calendar,31 roles,owned companion records and five-ship models. Other21 comments have full source/native-font proof,not individual actual visits. No earned travel,fleet,acquisition,full-playthrough or hardware claim.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Eight actual complete native/RGB holds and both normal return state controls pass;visual sheet review pending.',flush=True)


if __name__=='__main__':
    main()
