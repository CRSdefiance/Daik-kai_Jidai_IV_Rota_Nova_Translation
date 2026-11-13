"""Complete Cook15 native body fonts,including the separate Sera selection."""

import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.personal_chatter_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.work_comments_layout_v843 import compiled, layout, serialize
from scripts.prepare_work_comments_v842 import snapshot, machine_at
from scripts.prepare_cooking_prose_v848 import ROM
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels
from scripts.verify_village_wrap_v608 import read, save


ROOT = Path('work/analysis/cooking_comments_v849')
MANUSCRIPT = Path('translations/cooking_comments_editorial_manuscript_v1.json')
BASE, VIEW, TEXT = 0x02000000, 0x0218DF2C, 0x02450000

def execute(rom, raw, actor, role, number, text, expected_lines=None):
    arm = rom.read_file('/__arm9__.bin')
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    overlays = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.rom.files[fid])
    assert list(overlays) == [0]
    overlay = overlays[0]
    assert overlay.ramAddress == 0x01FFA000 and len(overlay.data) == 6208
    cpu.mem_write(overlay.ramAddress, bytes(overlay.data))
    resource = struct.unpack('<I', cpu.mem_read(VIEW + 0x50, 4))[0]
    header = bytes(cpu.mem_read(resource, 20))
    kind, pitch, height, palette, offset = struct.unpack('<5I', header)
    assert (kind, pitch, height) == (4, 63, 96)
    pixels = (resource + offset) & 0xFFFFFFFF
    size = pitch * height * 2
    assert pixels == VIEW + 0x104 and pixels + size == resource
    prefix = bytes(cpu.mem_read(pixels - 16, 16))
    suffix = bytes(cpu.mem_read(pixels + size, 32))
    cpu.mem_write(pixels, b'\x99' * size)
    cpu.mem_write(TEXT - 16, b'\xa5' * (len(text) + 33))
    cpu.mem_write(TEXT, text + b'\0')
    events, selected, geometry, trace, returned = [], [], [], set(), []
    def observer(u, pc, instruction_size, unused):
        trace.add(pc)
        if pc == BASE + 0x5528C:
            selected.append(u.reg_read(UC_ARM_REG_R0))
            assert selected[-1] == number
            u.reg_write(UC_ARM_REG_R0, TEXT)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif pc == BASE + 0x154CC:
            context, pointer = u.reg_read(UC_ARM_REG_R0), u.reg_read(UC_ARM_REG_R1)
            fields = list(struct.unpack('<12I', u.mem_read(context, 48)))
            assert fields[1:5] == [0, 0, 252, 96] and fields[9:11] == [0, 60]
            assert bytes(u.mem_read(pointer, len(text) + 1)) == text + b'\0'
            geometry.append({'context_fields': fields, 'expanded_text': pointer, 'text_hex': text.hex()})
        elif pc == BASE + 0x154D0:
            returned.append(u.reg_read(UC_ARM_REG_R0) - geometry[-1]['expanded_text'])
        elif pc in (BASE + 0xD16B4, 0x01FF83AC):
            sp = u.reg_read(UC_ARM_REG_SP)
            code, style = struct.unpack('<2I', u.mem_read(sp, 8))
            events.append({'kind': 'ascii' if pc == BASE + 0xD16B4 else 'cp932',
                           'code': code, 'style': style,
                           'x': u.reg_read(UC_ARM_REG_R2), 'y': u.reg_read(UC_ARM_REG_R3),
                           **({'font_flags': struct.unpack('<I', u.mem_read(u.reg_read(UC_ARM_REG_R0) + 12, 4))[0]} if pc == 0x01FF83AC else {})})
    # Only boundary/body hooks are needed;avoid one Python callback per glyph
    # blitter instruction while still proving the exact overlay clear entry.
    points = (BASE + 0x5528C, BASE + 0x154CC, BASE + 0x154D0,
              BASE + 0xD16B4, 0x01FF83AC, 0x01FFB2DC)
    handles = [cpu.hook_add(UC_HOOK_CODE, observer, begin=p, end=p) for p in points]
    try:
        # Cook15 and its assigned actor are declared isolated CPU fixtures.
        # State0 executes the ordinary original working-comment selector.
        call(cpu, 0x15334, (VIEW, role, 0, actor), instruction_limit=2000000)
    finally:
        for h in handles:
            cpu.hook_del(h)
    assert selected == [number] and len(geometry) == 1
    assert bytes(cpu.mem_read(TEXT, len(text) + 1)) == text + b'\0'
    assert bytes(cpu.mem_read(TEXT - 16, 16)) == bytes(cpu.mem_read(TEXT + len(text) + 1, 16)) == b'\xa5' * 16
    assert bytes(cpu.mem_read(pixels - 16, 16)) == prefix
    assert bytes(cpu.mem_read(pixels + size, 32)) == suffix
    assert bytes(cpu.mem_read(resource, 20)) == header and 0x01FFB2DC in trace
    actual = bytes(cpu.mem_read(pixels, size))
    expected = expected_pixels(arm, rom.read_file('/GRP/KANJI.FNT'), events, 4, background=0)
    cropped = b''.join(expected[y * 128:y * 128 + 126] for y in range(96))
    assert actual == cropped, ('independent whole canvas', actor, len(actual))
    body = [e for e in events if e['y'] >= 60]
    assert all(e['kind'] == 'ascii' and e['style'] == 15 for e in body)
    assert all(0 <= e['x'] and e['x'] + 6 <= 252 and 60 <= e['y'] and e['y'] + 11 <= 96 for e in body)
    points_by_line = {}
    for e in body:
        points_by_line.setdefault(e['y'], []).append(e)
    requests = []
    for y, row in sorted(points_by_line.items()):
        requests.append(''.join(chr(e['code']) for e in row))
    lines = [line.rstrip(' ') for line in requests]
    if expected_lines is not None:
        # Native glyph requests can include duplicate blank cells from paired
        # ASCII painting. Prove the final complete visible text independently
        # from the authored words and generated coordinates,not that trace.
        semantic_events = [e for e in events if e['y'] < 60]
        semantic_events += [dict(kind='ascii',code=ord(char),style=15,x=x*6,y=60+y*12)
                            for y,line in enumerate(expected_lines) for x,char in enumerate(line)]
        semantic = expected_pixels(arm,rom.read_file('/GRP/KANJI.FNT'),semantic_events,4,background=0)
        semantic = b''.join(semantic[y*128:y*128+126] for y in range(96))
        assert actual == semantic, ('independent complete words/coordinates',actor,expected_lines)
        lines = expected_lines
    indices = bytes(n for b in actual for n in (b & 15, b >> 4))
    return {'actor_ID': actor, 'message_id': number, 'text_hex': text.hex(), 'generated_native_lines': lines,
            'native_glyph_request_lines_including_trailing_blank_cells': requests,
            'native_text_bytes_consumed': returned[0], 'complete_native_copy_macro_draw_and_ABI': returned == [len(text)],
            'full252x96_native_and_independent_canvas_equal': True,
            'bitmap_and_input_guards_exact': True,
            'independent_authored_words_at_x0_12px_rows_match_every_pixel': expected_lines is not None,
            'body_origin': [0, 60], 'body_bounds': [0, 60, 252, 96],
            'overlay_sha256': sha(bytes(overlay.data)), 'font_events': events,
            'canvas_sha256': sha(actual)}, indices


def prepare_model(arm,raw,actor,role,ui_raw):
    assert raw[0x12104:0x12920]==arm[0x12104:0x12920]
    assert raw[0x15334:0x154E8]==arm[0x15334:0x154E8]
    assert raw[0x53914:0x53A00]==arm[0x53914:0x53A00]
    cpu,get=machine_at(arm,raw)
    actors=get(0xCB184);hero=get(0x7F244)
    obj=actors+struct.unpack_from('<I',arm,0x1229C)[0] if actor==hero else actors+4+actor*32
    condition,mood=get(0x7E100,obj),get(0x7E0B4,obj)
    assert condition==0 and mood in (1,2,3),(actor,hero,condition,mood)
    controller=get(0xCB1A8)+0x2090
    model=get(0x82E04,controller)
    assert all(not VIEW<=p<VIEW+0x30E4 for p in (actors,obj,controller,model))
    # Copy one genuine initialized CabinInfoView into the CPU-only UI fixture.
    # The captured real captain and actor models are not replaced.
    lo=VIEW-BASE
    cpu.mem_write(VIEW,ui_raw[lo:lo+0x30E4])
    old_type=get(0x132C0,model,18)
    before_occupants=[get(0x82BC4,controller,n) for n in range(31)]
    cpu.mem_write(model+0x1E+18,bytes([role]))
    assert get(0x132C0,model,18)==role
    for slot,occupant in enumerate(before_occupants):
        if occupant==actor:get(0x82BA8,controller,slot)
    get(0x82BB8,controller,18,actor)
    assert get(0x81F54,controller,actor)==role
    return bytes(cpu.mem_read(BASE,len(raw))),{'actor_ID':actor,'actual_captain_ID':hero,
        'source_condition':condition,'source_mood':mood,'original_slot18_type':old_type,
        'declared_CPU_role_fixture':role,'declared_CPU_assignment_slot':18,
        'genuine_body_widget_clone_bytes':0x30E4,'actor_and_captain_records_not_replaced':True,
        'no_live_RAM_or_ROM_changes':True}


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin')
    assert read(ROM.with_suffix('.manifest.json'))['candidate_sha256']==sha(ROM.read_bytes())
    doc=read(MANUSCRIPT)
    ui,ui_receipt=snapshot('personal_cabin_v840_838_Charles_after',4600)
    npc,npc_receipt=snapshot('personal_cabin_v840_838_Charles_after',3200)
    representatives={0:4,1:16,2:9,3:7,4:5,5:6,6:14,7:23}
    heroes={0:('personal_activity_v839_838_Rafael_later',3200),
        1:('personal_cabin_v840_838_Charles_after',3200),
        2:('ceremony_Lil_approach_v825',23000),3:('ceremony_Maria_approach_v825',26000)}
    cases=[]
    for row in doc['records']:
        if row['fixed_actor_ID'] is not None:
            actor=row['fixed_actor_ID'];source,receipt=npc,npc_receipt
        elif row['protagonist_ID'] is None:
            actor=representatives[row['voice_class']];source,receipt=npc,npc_receipt
        else:
            actor=row['protagonist_ID'];source,receipt=snapshot(*heroes[actor])
        prepared,fixture=prepare_model(arm,source,actor,row['role_ID'],ui)
        case,plane=execute(rom,prepared,actor,row['role_ID'],row['message_id'],compiled(row),layout(row['english']))
        assert case['complete_native_copy_macro_draw_and_ABI']
        assert not any(plane[y*252+x] for y in range(60,96) for x in range(216,252))
        image=Image.frombytes('L',(252,96),bytes(0 if v else 255 for v in plane))
        path=ROOT/f'ID{row["message_id"]}_complete_native_ink.png';image.save(path)
        case.update(source_snapshot=receipt,isolated_CPU_fixture=fixture,
            all_body_ink_inside_registered216x36_crop=True,preview=str(path),preview_sha256=sha(path.read_bytes()),
            native_ink_only_not_actual_RGB_scene_or_earned_assignment=True)
        cases.append(case)
        print(row['message_id'],case['generated_native_lines'],flush=True)
    sheet=Image.new('RGB',(3*514,5*231),'#263238');draw=ImageDraw.Draw(sheet)
    for i,case in enumerate(cases):
        x,y=i%3*514,i//3*231
        draw.text((x+5,y+5),f"ID{case['message_id']} native complete words;actual scene pending",fill='white')
        with Image.open(case['preview']) as im:sheet.paste(im.resize((504,192),Image.Resampling.NEAREST),(x+5,y+28))
    path=ROOT/'all13_native_ink_masks_2x.png';sheet.save(path)
    save(ROOT/'native_font_proof.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'cases':cases,'all13_source_numeric_selection_complete_ABI_words_and_visible_ink_pass':True,
        'genuine_initialized_body_widget_source':ui_receipt,
        'four_original_actual_captain_states_used_no_captain_ID_substitution':True,
        'role_assignments_and_UI_clone_are_CPU_only_formatting_fixtures':True,
        'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),'visual_review_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),
        'layout_producer_sha256':sha(Path('scripts/work_comments_layout_v843.py').read_bytes()),
        'registered_repack_original_copy_actual_RGB_and_gameplay_pending':True,'full_goal_complete':False})
    print('All24 original work selectors,complete native/independent body words and216x36 bounds pass;visual review and actual release remain.',flush=True)


if __name__=='__main__':main()

