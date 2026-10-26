"""Execute original choice getters, VM dispatch, geometry and centered painting."""

import copy
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.ship_advice_choice_centering import (
    CURRENT,
    END,
    PATH,
    START,
    apply_release,
    compile_object,
)
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine

ROOT = Path('work/choice_centering_20261022')
CONFIG = Path('translations/ship_advice_choice_centering_20261022_release_v1.json')
PARENT = Path('out/screenshot_text_repairs_20261022_candidate.nds')


def choice_vm(arm, object_bytes):
    cpu = machine(arm)
    text, owner, provider, result, cursor, rect = (0x02430020, 0x02431020, 0x02432020,
                                                 0x02433020, 0x02433120, 0x02434020)
    cpu.mem_write(text - 16, b'\xA5' * 96)
    cpu.mem_write(text, object_bytes)
    original = bytes(cpu.mem_read(text - 16, 96))
    cpu.mem_write(owner, struct.pack('<2I', 0, text))
    call(cpu, 0x2A3D8, (provider, owner))
    call(cpu, 0x2A3B8, (provider,))
    assert cpu.reg_read(UC_ARM_REG_R0) == 2
    labels, widths = [], []
    for index in (0, 1):
        call(cpu, 0x2A30C, (provider, index))
        pointer = cpu.reg_read(UC_ARM_REG_R0)
        label = bytes(cpu.mem_read(pointer, 32)).split(b'\0')[0]
        labels.append(label)
        call(cpu, 0xCF348, (pointer, 0, 0))
        widths.append(cpu.reg_read(UC_ARM_REG_R0))
    maximum = max(8, *widths)
    call(cpu, 0x52E40, (rect, provider, maximum, 2))
    geometry = list(struct.unpack('<4i', cpu.mem_read(rect, 16)))
    cases = []
    for selected in (0, 1, -1):
        cpu.mem_write(result - 16, b'\xA5' * 64)
        cpu.mem_write(cursor - 16, b'\xA5' * 64)
        seen = []

        def complete_modal(uc, address, size, unused, seen=seen, selected=selected):
            if address == 0x02051FC0:
                descriptor = uc.reg_read(UC_ARM_REG_R0)
                assert struct.unpack('<I', uc.mem_read(descriptor + 8, 4))[0] == text
                seen.append(address)
                # Only the modal input loop is bridged; getter, parsing and
                # native return/control flow execute without substitution.
                uc.reg_write(UC_ARM_REG_R0, selected & 0xFFFFFFFF)
                uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

        hook = cpu.hook_add(UC_HOOK_CODE, complete_modal)
        try:
            executed = call(cpu, 0x2A510, (result, owner, cursor, 0))
        finally:
            cpu.hook_del(hook)
        assert seen == [0x02051FC0] and {0x0202A510, 0x0202A1D8} <= executed
        state, selection = struct.unpack('<2I', cpu.mem_read(result, 8))
        assert state == (2 if selected >= 0 else 0)
        if selected >= 0:
            assert selection == selected
        assert struct.unpack('<I', cpu.mem_read(cursor, 4))[0] == len(object_bytes)
        assert bytes(cpu.mem_read(text - 16, 96)) == original
        assert bytes(cpu.mem_read(result - 16, 16)) == bytes(cpu.mem_read(result + 8, 16)) == b'\xA5' * 16
        assert bytes(cpu.mem_read(cursor - 16, 16)) == bytes(cpu.mem_read(cursor + 4, 16)) == b'\xA5' * 16
        cases.append({'modal_selection': selected, 'VM_state': state, 'next_command_delta': len(object_bytes),
                      'original_dispatch_ABI_and_guards_pass': True})
    return {'labels': [p.decode() for p in labels], 'native_width_units': widths,
            'native_menu_rectangle': geometry, 'minimum_width_units': maximum, 'VM_cases': cases}


def paint(arm, text, style):
    width, height = 48, 20
    cpu = machine(arm)
    cpu.mem_write(POOL, bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48]))
    header, view, context, string = 0x02450000, 0x02453000, 0x02454000, 0x02455000
    size = width * height // 2
    raw_header = struct.pack('<5I', 4, width // 4, height, 0x02452000 - header, 20)
    cpu.mem_write(header - 16, b'\xA5' * (size + 52))
    cpu.mem_write(header, raw_header + bytes(size))
    call(cpu, 0xD3D80, (view,))
    cpu.mem_write(STACK, struct.pack('<4I', width, height, 0, 0))
    call(cpu, 0xD3AFC, (view, header, 0, 0))
    metrics = struct.unpack_from('<I', arm, 0xD5088)[0]
    cpu.mem_write(metrics + 4, struct.pack('<2I', 6, 12))
    call(cpu, 0xD5160, (context, view, style))
    cpu.mem_write(string - 16, b'\xA5' * 96)
    cpu.mem_write(string, text + b'\0')
    original = bytes(cpu.mem_read(string - 16, 96))
    # The native menu constructor sets alignment mode zero and enables D5340.
    cpu.mem_write(context + 0x18, struct.pack('<I', 0))
    call(cpu, 0xD5340, (context, string))
    pixels = bytes(n for b in cpu.mem_read(header + 20, size) for n in (b & 15, b >> 4))
    x, y = (width - len(text) * 6) // 2, 4
    expected = bytearray(width * height)
    font = GameAsciiFont.from_arm9(arm)
    for index, character in enumerate(text.decode()):
        glyph = font.decode(character)
        for yy in range(11):
            for xx in range(6):
                if glyph.getpixel((xx, yy)):
                    expected[(y + yy) * width + x + index * 6 + xx] = style
    assert pixels == bytes(expected)
    assert bytes(cpu.mem_read(string - 16, 96)) == original
    assert bytes(cpu.mem_read(header, 20)) == raw_header
    assert bytes(cpu.mem_read(header - 16, 16)) == bytes(cpu.mem_read(header + 20 + size, 16)) == b'\xA5' * 16
    visible = text.rstrip(b' ')
    visible_center_twice = 2 * x + len(visible) * 6
    return pixels, {'text': text.decode(), 'native_origin': [x, y],
                    'visible_cell_center_twice': visible_center_twice,
                    'independent_complete_native_pixels_match': True, 'style': style}


def main():
    ROOT.mkdir(exist_ok=True)
    config = json.loads(CONFIG.read_text())
    manuscript = json.loads(Path(config['manuscript']).read_text())
    replacement = compile_object(CURRENT, manuscript)
    parent = NdsImage.open(PARENT)
    arm = parent.read_file('/__arm9__.bin')
    before = choice_vm(arm, CURRENT)
    after = choice_vm(arm, replacement)
    assert before['labels'] == ['Yes ', 'No      '] and after['labels'] == ['Yes', 'No']
    assert before['native_menu_rectangle'] == after['native_menu_rectangle']
    assert before['minimum_width_units'] == after['minimum_width_units'] == 8
    assert before['VM_cases'] == after['VM_cases']
    sheet = Image.new('RGB', (480, 264), '#333333')
    draw = ImageDraw.Draw(sheet)
    cases = []
    for column, (title, labels) in enumerate((('Before', before['labels']), ('After', after['labels']))):
        draw.text((column * 240 + 12, 8), title, fill='white')
        for row, label in enumerate(labels):
            pixels, proof = paint(arm, label.encode(), 1)
            paint(arm, label.encode(), 15)
            panel = Image.new('RGB', (48, 20))
            background = (0, 168, 176) if row == 0 else (204, 198, 180)
            panel.putdata([(8, 8, 8) if p else background for p in pixels])
            sheet.paste(panel.resize((192, 80), Image.Resampling.NEAREST), (column * 240 + 24, 36 + row * 88))
            draw.text((column * 240 + 12, 224 + row * 16), f'{label!r}: x={proof["native_origin"][0]}', fill='white')
            cases.append({'version': title, **proof})
    assert [c['visible_cell_center_twice'] for c in cases if c['version'] == 'After'] == [48, 48]
    negatives = []
    for kind in ('opcode', 'different_label', 'unreviewed'):
        raw, doc = CURRENT, copy.deepcopy(manuscript)
        if kind == 'opcode':
            raw = b'\x01' + raw[1:]
        elif kind == 'different_label':
            doc['records'][1]['english'] = 'Nope{PAD}'
        else:
            doc['records'][0]['review']['formatting'] = False
        try:
            compile_object(raw, doc)
        except ValueError:
            negatives.append(kind)
        else:
            raise AssertionError(f'Invalid compiler input accepted: {kind}')
    source_sc0 = parent.read_file(PATH)
    apply_release(parent, NdsImage.open('out/raphael_natural_v2_accepted_base.nds'), CONFIG)
    old, new = IlnkContainer.parse(source_sc0), IlnkContainer.parse(parent.read_file(PATH))
    for index, (a, b) in enumerate(zip(old.blocks, new.blocks, strict=True)):
        assert len(a) == len(b)
        if index == 177:
            assert a[:START] == b[:START] and a[END:] == b[END:]
            assert len(a.split(b'\0')) == len(b.split(b'\0'))
        else:
            assert a == b
    candidate = Path('out/screenshot_text_repairs_20261022_centered_candidate.nds')
    if candidate.exists():
        saved = NdsImage.open(candidate)
        assert list(parent.iter_files()) == list(saved.iter_files())
        assert dict(parent.iter_components()) == dict(saved.iter_components())
    sheet.save(ROOT / 'native_choice_before_after.png')
    (ROOT / 'native_choice_proof.json').write_text(json.dumps({
        'scope': 'Original choice getters, geometry, complete centered native pixel planes, and VM dispatch. Modal input loop is bridged; full original scene not exercised.',
        'before': before, 'after': after, 'native_pixel_cases': cases,
        'two_foreground_styles_tested_per_case': True, 'compiler_negatives_rejected': negatives,
        'all_other_blocks_and_bytes_and_record_numbering_preserved': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'config_sha256': sha(CONFIG.read_bytes()),
        'ARM9_sha256': sha(arm), 'source_SC0_sha256': sha(source_sc0),
        'target_SC0_sha256': sha(parent.read_file(PATH)), 'full_scene_and_hardware_verified': False,
    }, indent=2) + '\n', encoding='utf-8')
    print('PASS: both labels centered; native rectangle exact; Yes/No/cancel VM returns and next-command positions exact; full native pixels and three rejection cases pass.')


if __name__ == '__main__':
    main()
