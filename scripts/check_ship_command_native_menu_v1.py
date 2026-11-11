"""Check the real ship-menu table getters, geometry, glyphs and input guards."""

import inspect
import struct
from pathlib import Path
from types import SimpleNamespace

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.ship_command_label_v1 import BASE, OLD_POINTER, NEW_POINTER, TABLE, TEXT
from dk4tool.rom.nds import NdsImage
from scripts import native_menu_backing_surface_v4080 as backing
from scripts import verify_ship_advice_choice_centering_20261022 as original
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.native_call_abi_v764 import call
from scripts.prepare_ship_command_research_v1 import PROOF, ROM, WORK
from scripts.source_locked_derivation_v5118 import checked_text


def provider(arm, expected_pointer):
    cpu = original.machine(arm)
    descriptor = 0x02431020
    rectangle = 0x02432020
    captured = []

    def boundary(u, pc, size, _):
        raw = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 20))
        captured.append(raw)
        u.reg_write(UC_ARM_REG_R0, 1)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    hook = cpu.hook_add(UC_HOOK_CODE, boundary, begin=BASE+0x51FC0, end=BASE+0x51FC0)
    call(cpu, 0x51E7C, (BASE+TABLE, 2, 0, 0))
    cpu.hook_del(hook)
    assert cpu.reg_read(UC_ARM_REG_R0) == 1 and len(captured) == 1
    vtable, table, count, flag, cursor = struct.unpack('<5I', captured[0])
    assert (vtable, table, count, flag, cursor) == (0x02140970, BASE+TABLE, 2, 0, 0)
    cpu.mem_write(descriptor-16, b'\xA5'*52)
    cpu.mem_write(descriptor, captured[0])
    cpu.mem_write(rectangle-16, b'\xA5'*48)

    def method(slot):
        return struct.unpack('<I', cpu.mem_read(vtable+slot, 4))[0]-BASE

    call(cpu, method(0), (descriptor,))
    assert cpu.reg_read(UC_ARM_REG_R0) == 2
    options = []
    for index in range(count):
        call(cpu, method(4), (descriptor, index))
        pointer = cpu.reg_read(UC_ARM_REG_R0)
        raw = bytes(cpu.mem_read(pointer, 24)).split(b'\0', 1)[0]
        if index == 1:
            assert pointer == expected_pointer
        call(cpu, 0xCF348, (pointer, 0, 0))
        options.append(dict(index=index, pointer=pointer, terminated_hex=(raw+b'\0').hex(),
            text=raw.decode('cp932'), width_units=cpu.reg_read(UC_ARM_REG_R0)))
    units = max(8, *(r['width_units'] for r in options))
    call(cpu, method(0x2C), (rectangle, descriptor, units, count))
    box = struct.unpack('<4i', cpu.mem_read(rectangle, 16))
    assert 0 <= box[0] < box[2] <= 256 and 0 <= box[1] < box[3] <= 192
    assert bytes(cpu.mem_read(descriptor-16, 52)) == b'\xA5'*16 + captured[0] + b'\xA5'*16
    assert bytes(cpu.mem_read(rectangle-16, 16)) == bytes(cpu.mem_read(rectangle+16, 16)) == b'\xA5'*16
    return dict(options=options, descriptor_hex=captured[0].hex(), minimum_width_units=units,
        modal_rectangle=box, zero_flag_original_constructor_style=True, complete_native_getters_measurement_andgeometry_ABI=True)


def main():
    root = WORK / 'native_menu'
    assert not root.exists()
    research = load(PROOF)
    assert digest(ROM) == research['ROM_sha256'] and digest(research['parent']) == research['parent_sha256']
    arm, parent = (NdsImage.open(path).read_file('/__arm9__.bin') for path in (ROM, research['parent']))
    before, after = provider(parent, OLD_POINTER), provider(arm, NEW_POINTER)
    assert before['options'][0] == after['options'][0]
    assert [r['text'] for r in before['options']] == ['Assign', '船を捨てる']
    assert [r['text'] for r in after['options']] == ['Assign', TEXT[:-1].decode('ascii')]
    assert after['options'][1]['width_units'] == len(TEXT)-1
    assert before['modal_rectangle'][1::2] == after['modal_rectangle'][1::2]

    paint_source = checked_text(inspect.getsource(backing.paint), {
        "'expected[(y+yy)*backing_width+x+index*6+xx]'": "'expected[(y+yy+1)*backing_width+x+index*6+xx]'",
    })
    sections = MainCodeFile(arm, BASE).sections
    owners = [*sections, SimpleNamespace(ramAddress=POOL, data=bytes(sections[3].data[:-48]))]
    executed = set()

    def machine(source):
        assert source == arm
        cpu = original.machine(source)

        def verify_code(u, pc, size, _):
            hits = [s for s in owners if s.ramAddress <= pc and pc+size <= s.ramAddress+len(s.data)]
            assert len(hits) == 1, hex(pc)
            hit = hits[0]
            at = pc-hit.ramAddress
            assert bytes(u.mem_read(pc, size)) == bytes(hit.data[at:at+size]), hex(pc)
            executed.add(pc)

        cpu.hook_add(UC_HOOK_CODE, verify_code)
        return cpu

    proxy = SimpleNamespace(**{**vars(original), 'machine': machine})
    env = {**vars(backing), 'original': proxy}
    exec(compile(paint_source, __file__, 'exec'), env)
    root.mkdir()
    width = after['minimum_width_units']*6
    sheet = Image.new('RGB', (420, 225), '#263238')
    draw = ImageDraw.Draw(sheet)
    results = []
    for option in after['options']:
        for style in (1, 15):
            data, proof = env['paint'](arm, option['text'].encode('ascii'), style, width, (0, option['index']*12))
            assert proof['independent_complete_native_pixels_match'] and proof['visible_cell_center_twice'] == width
            assert proof['storage_padding_all_blank'] and proof['extra_flush_stays_within_physical_backing']
            position = len(results)*55
            color = (244, 235, 205) if style == 1 else (0, 165, 170)
            tile = Image.new('RGB', (width, 12))
            tile.putdata([(0, 8, 0) if value else color for value in data])
            draw.text((5, position+3), f"{option['text']}  /  native style {style}", fill='white')
            sheet.paste(tile.resize((width*3, 36), Image.Resampling.NEAREST), (5, position+17))
            path = root / f"O{option['index']}_S{style}.bin"
            path.write_bytes(data)
            results.append(dict(option=option['index'], plane=str(path), plane_sha256=digest(path), **proof))
    path = root / 'native_ship_menu.png'
    sheet.save(path)
    save(root / 'native_ship_menu.json', dict(parent=before, research=after, captions=results,
        original_static_menu_table_getters_and_original_geometry_executed=True,
        complete_english_planes_centering_leading_trailing_glyphs_bounds_andguards_pass=True,
        no_dialogue_wrapping_or_pagination_in_this_single_row_caption_consumer=True,
        modal_UI_loop_return_is_explicit_offline_ABI_boundary=True,
        native_geometry_measured_in_initialized_static_machine=True,
        foreground_painter_executed_addresses=sorted(executed),
        sheet=str(path), sheet_sha256=digest(path), directly_viewed=False,
        actual_gameplay_and_registered_release_pending=True, new_credit=0,
        evidence={str(p):digest(p) for p in [PROOF, Path(backing.__file__), Path(original.__file__), Path(__file__)]}))
    print(f"Ship menu geometry {before['modal_rectangle']} -> {after['modal_rectangle']}. Four complete caption planes.")


if __name__ == '__main__':
    main()
