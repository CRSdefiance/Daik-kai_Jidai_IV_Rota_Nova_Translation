"""Native paired-character names through actual raw-image ASCII raster."""

import argparse
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R5,
    UC_ARM_REG_R10,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--persistent', action='store_true', help='Verify the separately reserved SDK-loaded name section.')
    parser.add_argument('--residual-names', action='store_true', help='Verify Vels and Akaboo on complete V149 research.')
    parser.add_argument('--fidelity-names', action='store_true', help='Verify source-faithful names on staged V153 research.')
    parser.add_argument('--inherited-initials', action='store_true', help='Verify five preserved full-width F initials on exact saved V154.')
    args = parser.parse_args()
    source_path = 'persistent_name_section_arm9.bin' if args.persistent else 'joint_square_shopkeeper_research_arm9.bin'
    proof_path = 'persistent_name_section_proof.json' if args.persistent else 'joint_square_shopkeeper_native_proof.json'
    if args.residual_names:
        source_path, proof_path = 'residual_character_names_arm9.bin', 'residual_character_names_proof.json'
    if args.fidelity_names:
        source_path, proof_path = 'ordinary_name_fidelity_research_arm9.bin', 'ordinary_name_fidelity_plan.json'
    if args.inherited_initials:
        source = NdsImage.open('out/all_routes_combined_v154_candidate.nds').read_file('/__arm9__.bin')
        parent = json.loads(Path('work/analysis/ordinary_name_v154_saved_proof.json').read_text(encoding='utf-8'))
    else:
        source = Path('work/analysis', source_path).read_bytes()
        parent = json.loads(Path('work/analysis', proof_path).read_text(encoding='utf-8'))
    identity = ('target_arm9_sha256' if args.fidelity_names or args.inherited_initials else
                'research_sha256' if args.persistent or args.residual_names else 'research_arm9_sha256')
    if sha(source) != parent[identity]:
        raise ValueError('Exact combined shopkeeper research required')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    if source[0xD6D0:0xD79C] != clean[0xD6D0:0xD79C]:
        raise ValueError('Original paired-name bitmap/getter/caller changed')
    cases, rasters, panels = [], [], []
    expected_names = {61: 'Vels', 77: 'Akaboo'} if args.residual_names else dict.fromkeys(range(82, 92), 'Square Shopkeeper')
    if args.fidelity_names:
        expected_names = {row['index']: row['english'] for row in parent['records']}
    if args.inherited_initials:
        expected_names = {20: 'Ｆernando', 35: 'Ｆernan', 178: 'Ｆollower', 186: 'Ｆrancisca', 194: 'Ｆaticia'}
    kanji = NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT') if args.inherited_initials else None
    for index, expected_name in expected_names.items():
        machine = machine_for(source)
        machine.mem_map(0x01FF0000, 0x10000)

        def cache(uc, address, size, _):
            if address in (BASE + 0xA34, BASE + 0xA38, BASE + 0xA3C):
                uc.reg_write(UC_ARM_REG_PC, address + 4)

        hook = machine.hook_add(UC_HOOK_CODE, cache)
        machine.emu_start(BASE + 0x9E0, STOP, count=100000)
        machine.hook_del(hook)
        machine.emu_start(BASE + 0x88C, BASE + 0x8AC, count=3000000)
        if args.fidelity_names or args.inherited_initials:
            machine.emu_start(BASE + 0x8E4, BASE + 0x8E8, count=10000)
        if kanji is not None:
            machine.mem_write(struct.unpack_from('<I', source, 0xD19B8)[0], kanji)
        machine.reg_write(UC_ARM_REG_SP, STACK)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.emu_start(BASE + 0x10DD0C, STOP, count=10000)
        image_header = struct.unpack_from('<I', source, 0xD898)[0]
        image_words = struct.unpack('<5I', machine.mem_read(image_header, 20))
        image_format, pitch, image_height, _, pixel_delta = image_words
        if (image_format, pitch, image_height) != (4, 116, 96):
            raise ValueError(f'Native raw name-image header differs: {image_words}')
        pixels = image_header + pixel_delta
        pixel_size = pitch * image_height * 2
        machine.mem_write(pixels, bytes(pixel_size))
        machine.mem_write(pixels - 32, b'\xA5' * 32)
        machine.mem_write(pixels + pixel_size, b'\xA5' * 32)
        header_before = bytes(machine.mem_read(image_header, 20))
        selected = ordinary_getter(source, index, machine)
        root = struct.unpack_from('<I', source, 0xCB18C)[0]
        actor = root + 4 + index * 32
        dialog = 0x02440000
        machine.mem_write(dialog + 0x34, struct.pack('<2I', actor, actor))
        machine.mem_write(dialog + 0x1E4, source[0xD3C00:0xD3C04])
        font = struct.unpack_from('<I', source, 0xD5088)[0]
        machine.mem_write(font + 4, struct.pack('<2I', 6, 12))
        machine.reg_write(UC_ARM_REG_SP, STACK)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.reg_write(UC_ARM_REG_R5, 0)
        machine.reg_write(UC_ARM_REG_R10, dialog)
        clear_calls = []

        def clear(uc, address, size, _, calls=clear_calls):
            if address == BASE + 0xD393C:
                calls.append(uc.reg_read(UC_ARM_REG_R0))
                uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

        hook = machine.hook_add(UC_HOOK_CODE, clear)
        machine.emu_start(BASE + 0xD6D0, BASE + 0xD73C, count=10000)
        machine.hook_del(hook)
        bitmap = bytes(machine.mem_read(dialog + 0x1E4, 0x30))
        mode, width, height = [struct.unpack_from('<I', bitmap, p)[0] for p in (0x14, 0x28, 0x2C)]
        if (mode, width, height) != (5, 256, 24):
            raise ValueError('Actual paired-name bitmap geometry differs')
        context = STACK + 0x78
        expected = bytearray(pixel_size)
        all_events = []
        for row, end in ((0, 0xD73C), (1, 0xD798)):
            if row:
                # Follow the actual given-name branch (alternate surname branch excluded).
                machine.emu_start(BASE + 0xD748, BASE + 0xD758, count=10)
                machine.emu_start(BASE + 0xD780, BASE + end, count=10000)
            pointer = machine.reg_read(UC_ARM_REG_R1)
            text = bytes(machine.mem_read(pointer, 128)).split(b'\0', 1)[0].decode('cp932')
            x, y = struct.unpack('<2I', machine.mem_read(context + 0x24, 8))
            if (machine.reg_read(UC_ARM_REG_PC) != BASE + end or pointer != selected
                    or text != expected_name or (x, y) != (0, row * 12)):
                raise ValueError(f'Native paired-name preparation differs: {index=}, {row=}, {pointer=}, {selected=}, {text=}, {x=}, {y=}')
            cases.append({'index': index, 'row': row, 'text': text, 'pointer': pointer,
                          'x': x, 'y': y, 'bitmap_width': width, 'bitmap_height': height,
                          'bitmap_mode': mode, 'ascii_advance_contract': 6,
                          'complete_text_width': len(text.encode('cp932')) * 6,
                          'bitmap_clear_contract_calls': clear_calls})
            events = []

            def glyph(uc, address, size, _, events=events):
                if address in (BASE + 0xD16B4, 0x01FF83AC):
                    code, style = struct.unpack('<2I', uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 8))
                    # Incoming R2/R3 are absolute raw-image pixel origins.
                    events.append({'kind': 'ascii' if address == BASE + 0xD16B4 else 'cp932',
                                   'code': code, 'style': style,
                                   'x': uc.reg_read(UC_ARM_REG_R2), 'y': uc.reg_read(UC_ARM_REG_R3)})
                    if address == 0x01FF83AC:
                        events[-1]['font_flags'] = struct.unpack('<I', uc.mem_read(uc.reg_read(UC_ARM_REG_R0) + 12, 4))[0]

            def raster_write(uc, access, address, size, value, _, pixels=pixels, pixel_size=pixel_size, font=font):
                if not ((pixels <= address and address + size <= pixels + pixel_size)
                        or (STACK - 0x10000 <= address and address + size <= STACK + 0x200)
                        or (kanji is not None and address == font + 12 and size == 4)):
                    raise ValueError('Native name raster writes outside pixels/stack context')

            hook = machine.hook_add(UC_HOOK_CODE, glyph)
            write_hook = machine.hook_add(UC_HOOK_MEM_WRITE, raster_write)
            machine.emu_start(BASE + end, BASE + end + 4, count=100000)
            machine.hook_del(hook)
            machine.hook_del(write_hook)
            expected_codes = [int.from_bytes(c.encode('cp932'), 'big') for c in text] + ([32] if len(text.encode('cp932')) % 2 else [])
            if [e['code'] for e in events] != expected_codes:
                raise ValueError(f'Native glyph dispatch differs: {events}; context={bytes(machine.mem_read(context, 0x48)).hex()}')
            if kanji is not None:
                all_events.extend(events)
                oracle = expected_pixels(source, kanji, all_events, 4)
                for py in range(24):
                    expected[py * pitch * 2:py * pitch * 2 + 128] = oracle[py * 128:py * 128 + 128]
            else:
                font_masks = GameAsciiFont.from_arm9(source)
                for event in events:
                    mask = font_masks.decode(chr(event['code']))
                    for gy in range(11):
                        for gx in range(6):
                            value = event['style'] if mask.getpixel((gx, gy)) else 0
                            px, py = event['x'] + gx, event['y'] + gy
                            offset = py * pitch * 2 + px // 2
                            shift = 4 * (px % 2)
                            expected[offset] = (expected[offset] & ~(15 << shift)) | (value << shift)
            actual = bytes(machine.mem_read(pixels, pixel_size))
            if actual != expected:
                raise ValueError('Native name raster differs from independent ASCII pixels')
            if (bytes(machine.mem_read(image_header, 20)) != header_before
                    or bytes(machine.mem_read(pixels - 32, 32)) != b'\xA5' * 32
                    or bytes(machine.mem_read(pixels + pixel_size, 32)) != b'\xA5' * 32
                    or bytes(machine.mem_read(dialog + 0x1E4, 0x30)) != bitmap):
                raise ValueError('Native name draw alters header/descriptor/pixel guards')
            rasters.append({'index': index, 'row': row, 'glyph_events': events,
                            'raw_image_width': pitch * 4, 'raw_image_height': image_height,
                            'pixels_sha256': sha(actual), 'independent_pixels_match': True,
                            'header_descriptor_and_pixel_guards_preserved': True})
            if row == 1:
                panel = Image.new('RGB', (256, 24), 'white')
                for py in range(24):
                    for px in range(256):
                        value = (actual[py * pitch * 2 + px // 2] >> (4 * (px % 2))) & 15
                        if value:
                            panel.putpixel((px, py), (25, 25, 25))
                panels.append((index, panel))
    sheet = Image.new('RGB', (800, len(panels) * 100), (235, 235, 235))
    draw = ImageDraw.Draw(sheet)
    for number, (index, panel) in enumerate(panels):
        draw.text((12, number * 100 + 4), f'Ordinary name {index}: native rows y0 / y12', fill='black')
        sheet.paste(panel.resize((768, 72), Image.Resampling.NEAREST), (12, number * 100 + 22))
    output = Path('work/qa/persistent_square_shopkeeper_native' if args.persistent else 'work/qa/square_shopkeeper_native')
    if args.residual_names:
        output = Path('work/qa/residual_character_names_native')
    if args.fidelity_names:
        output = Path('work/qa/ordinary_name_fidelity_native')
    if args.inherited_initials:
        output = Path('work/qa/ordinary_name_inherited_initials_native')
    output.mkdir(parents=True, exist_ok=True)
    sheet.save(output / 'native_sheet.png')
    result = {'status': 'pass-native-paired-name-connected-raw-image-pixels',
              'research_sha256': sha(source), 'cases': cases, 'rasters': rasters, 'candidate_changed': False,
              'separately_reserved_persistent_names': args.persistent or args.residual_names,
              'limits': ['Characters assigned to paired-dialogue fields are fixtures; actual scene eligibility remains open.',
                         'Actual native raw-image initializer/bitmap/context/getter/virtual caller and ASCII raster execute; clear is contracted against initially zero pixels.',
                         'Mode five selects a direct raw image; actual scene eligibility and physical composition remain unverified.',
                         'Second-row given-name branch is selected explicitly; surname branch is outside this label check.']}
    report_path = ('persistent_square_shopkeeper_paired_name_context_proof.json' if args.persistent
                   else 'square_shopkeeper_paired_name_context_proof.json')
    if args.residual_names:
        report_path = 'residual_character_names_paired_pixels_proof.json'
    if args.fidelity_names:
        report_path = 'ordinary_name_fidelity_paired_pixels_proof.json'
    if args.inherited_initials:
        report_path = 'ordinary_name_inherited_initials_pixels_proof.json'
    Path('work/analysis', report_path).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(rasters)} connected native name rasters match independent pixels; full glyphs, descriptors and buffer guards preserved.')


if __name__ == '__main__':
    main()
