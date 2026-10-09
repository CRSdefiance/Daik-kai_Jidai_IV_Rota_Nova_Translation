"""Actual fleet-array/virtual getter and two display preparations; raster pending."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, machine_for
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels


def execute(source, kind, name, *, raster=False, kanji_font=b'',
            captain_index=None, current_character=0):
    machine = machine_for(source)
    root = struct.unpack_from('<I', source, 0xCB1B0)[0]
    fleet = root + 4
    dialog, captain, vtable, callback, text = (0x02420000, 0x02424000,
                                              0x02425000, 0x02426000, 0x02427000)
    # Execute the actual constructor prefix that owns both fleet virtual tables.
    machine.reg_write(UC_ARM_REG_R0, fleet)
    machine.emu_start(BASE + 0xCBA3C, BASE + 0xCBA58, count=20)
    if struct.unpack('<I', machine.mem_read(fleet, 4))[0] != BASE + 0x134EE0:
        raise ValueError('Actual fleet constructor selects another name vtable')
    if captain_index is not None:
        from scripts.probe_fleet_captain_names import setup

        name = setup(source, machine, fleet, captain_index, current_character, name or '')
    bitmap_bytes, events, executed = 96 * 72, [], set()
    if raster:
        resident = MainCodeFile(source, BASE).sections[1]
        machine.mem_map(0x01FF8000, 0x8000)
        machine.mem_write(resident.ramAddress, bytes(resident.data))
        font_pointer = struct.unpack_from('<I', source, 0xD19B8)[0]
        machine.mem_write(font_pointer, kanji_font)
        font = struct.unpack_from('<I', source, 0xD5088)[0]
        machine.mem_write(font + 4, struct.pack('<2I', 6, 12))
        machine.mem_write(dialog + 0x10, source[0xD3C00:0xD3C04])
        machine.reg_write(UC_ARM_REG_R4, dialog)
        machine.reg_write(UC_ARM_REG_SP, STACK)
        machine.emu_start(BASE + 0x87680, BASE + 0x876EC, count=10000)
        if struct.unpack('<2I', machine.mem_read(dialog + 0x38, 8)) != (192, 72):
            raise ValueError('Native fleet bitmap geometry differs')
        machine.mem_write(dialog + 0x74, b'\x99' * bitmap_bytes)
        machine.mem_write(dialog + 0x54, b'\xA5' * 32)
    machine.mem_write(dialog + 0x1B88, struct.pack('<I', 0))
    machine.mem_write(captain, struct.pack('<I', vtable))
    machine.mem_write(vtable + 0x20, struct.pack('<I', callback))
    machine.mem_write(text, (name or '').encode('cp932') + b'\0')
    ring = struct.unpack_from('<I', source, 0x36B48)[0]
    machine.mem_write(ring + 8, struct.pack('<I', 0))
    frame = STACK - 0x4C - (12 if kind == 'fixed' else 20)
    machine.reg_write(UC_ARM_REG_SP, frame)
    machine.reg_write(UC_ARM_REG_R5, dialog)
    contracts = []

    def code(uc, address, size, _):
        executed.add(address)
        if raster and address in (BASE + 0xD16B4, 0x01FF83AC):
            sp = uc.reg_read(UC_ARM_REG_SP)
            glyph, style = struct.unpack('<2I', uc.mem_read(sp, 8))
            events.append({'kind': 'ascii' if address == BASE + 0xD16B4 else 'cp932',
                           'code': glyph, 'style': style,
                           'x': uc.reg_read(UC_ARM_REG_R2), 'y': uc.reg_read(UC_ARM_REG_R3)})
            if address == 0x01FF83AC:
                events[-1]['font_flags'] = struct.unpack('<I', uc.mem_read(uc.reg_read(UC_ARM_REG_R0) + 12, 4))[0]
        fixture_addresses = (BASE + 0x352F4, BASE + 0xD393C)
        if captain_index is None:
            fixture_addresses += (BASE + 0x3697C, callback)
        if address in fixture_addresses:
            contracts.append(address)
            result = (captain if name is not None else 0) if address == BASE + 0x3697C else (
                text if address == callback else 0)
            uc.reg_write(UC_ARM_REG_R0, result)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    machine.hook_add(UC_HOOK_CODE, code)
    # Actual container indexing selects the object before text-context setup.
    machine.emu_start(BASE + (0x3757C if kind == 'fixed' else 0x37CCC),
                      BASE + (0x375B0 if kind == 'fixed' else 0x37CF0), count=1000)
    if machine.reg_read(UC_ARM_REG_R4) != fleet:
        raise ValueError('Actual display caller fails to select fleet array object')
    # Preparation-only mode deliberately skips context setup; raster mode executes it.
    machine.emu_start(BASE + ((0x375B0 if kind == 'fixed' else 0x37CF0) if raster
                             else (0x375C0 if kind == 'fixed' else 0x37D08)),
                      BASE + 0xD5404, count=100000)
    expected = 'Unidentified fleet' if name is None else 'Pirate ' + name
    selected = machine.reg_read(UC_ARM_REG_R1)
    raw = bytes(machine.mem_read(selected, 128)).split(b'\0', 1)[0]
    x, y = struct.unpack('<2i', machine.mem_read(frame + 0x24, 8))
    wanted_x = 42 if kind == 'fixed' else (192 - len(expected.encode('cp932')) * 6) // 2
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0xD5404
            or machine.reg_read(UC_ARM_REG_R0) != frame
            or machine.reg_read(UC_ARM_REG_SP) != frame
            or raw != expected.encode('cp932') or (x, y) != (wanted_x, 0)):
        raise ValueError('Native fleet display loses full text or placement')
    result = {'caller': kind, 'name_fixture': name, 'complete_text': expected,
            'x': x, 'y': y, 'center_uses_cp932_byte_length': kind == 'centered',
            'actual_constructor_vtable_root_index_getter_and_formatter_verified': True,
            'contracts': contracts}
    if captain_index is not None:
        needed = {BASE + 0x3697C}
        if captain_index != 208:
            needed |= {BASE + 0x7F244, BASE + (0x1371C if captain_index == current_character else 0x7EB0C)}
        if not needed <= executed:
            raise ValueError('Native captain selector and selected name getter did not execute')
        result.update({'captain_index_fixture': captain_index,
                       'current_character_fixture': current_character,
                       'native_captain_selector_and_name_dispatch_verified': True})
    if raster:
        descriptor_before = bytes(machine.mem_read(dialog + 0x1B74, 64))
        machine.emu_start(BASE + 0xD5404, BASE + (0x375F4 if kind == 'fixed' else 0x37D50), count=1000000)
        actual = bytes(machine.mem_read(dialog + 0x74, bitmap_bytes))
        padded = bytearray(b'\x99' * (128 * 192))
        for row in range(72):
            padded[row * 128:row * 128 + 96] = actual[row * 96:(row + 1) * 96]
        if bytes(padded) != expected_pixels(source, kanji_font, events, 4, background=9):
            raise ValueError('Fleet native pixels differ from independent font decode')
        codes = []
        raw_expected = expected.encode('cp932')
        index = 0
        while index < len(raw_expected):
            first = raw_expected[index]
            paired = 0x81 <= first <= 0x9F or 0xE0 <= first <= 0xFC
            codes.append((first << 8 | raw_expected[index + 1]) if paired else first)
            index += 2 if paired else 1
        content = [event for event in events if event['code'] != 32]
        if ([event['code'] for event in content] != [code for code in codes if code != 32]
                or any(e['x'] < 0 or e['x'] + (12 if e['kind'] == 'cp932' else 6) > 192
                       or e['y'] != 0 for e in content)
                or machine.reg_read(UC_ARM_REG_SP) != frame
                or bytes(machine.mem_read(dialog + 0x54, 32)) != b'\xA5' * 32
                or bytes(machine.mem_read(dialog + 0x1B74, 64)) != descriptor_before):
            raise ValueError('Fleet native rendering drops glyphs or exceeds its bitmap')
        if not {BASE + 0xD5160, BASE + 0xD5404, BASE + 0xD16B4, BASE + 0xE2A5C} <= executed:
            raise ValueError('Actual text context/glyph-copy bodies did not execute')
        result.update({'bitmap_width': 192, 'bitmap_height': 72,
                       'native_pixels_sha256': sha(actual), 'glyph_events': events,
                       'full_glyph_order_bounds_and_independent_pixels_verified': True})
        return result, actual
    return result


def main():
    source = Path('work/analysis/fleet_name_relocated_arm9.bin').read_bytes()
    proof = json.loads(Path('work/analysis/fleet_name_relocation_proof.json').read_text(encoding='utf-8'))
    parent = NdsImage.open('out/all_routes_combined_v147_candidate.nds').read_file('/__arm9__.bin')
    spans = [(0x37568, 0x375F4), (0x37CB8, 0x37D50), (0xCBA3C, 0xCBA80),
             (0xCB1A8, 0xCB1B4), (0x36A60, 0x36A6C), (0x134EE0, 0x134EF0),
             (0xCED28, 0xCED50)]
    if sha(source) != proof['research_arm9_sha256'] or any(source[a:b] != parent[a:b] for a, b in spans):
        raise ValueError('Exact fleet research and inherited display consumers required')
    cases = [execute(source, kind, name) for kind in ('fixed', 'centered')
             for name in (None, '', 'A', 'Even', 'Fleet', '海', 'Indigo海')]
    result = {'status': 'pass-native-fleet-display-preparation-raster-pending',
              'research_arm9_sha256': sha(source), 'cases': cases,
              'consumer_locks': [{'start': a, 'end': b, 'sha256': sha(source[a:b])} for a, b in spans],
              'limits': ['Fleet index zero, no affiliation, and captain/name virtual resolution are fixtures.',
                         'Constructor executes only its vtable-owning prefix.',
                         'Fixed caller bitmap clear is contracted; text-context setup is skipped.',
                         'These cases stop at D5404: no rendering/geometry/font/input proof is claimed.',
                         'Other virtual name consumers and valid dynamic name bounds remain open.']}
    Path('work/analysis/fleet_name_display_callers_proof.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    font = NdsImage.open('out/all_routes_combined_v147_candidate.nds').read_file('/GRP/KANJI.FNT')
    rasters = [execute(source, kind, name, raster=True, kanji_font=font)
               for kind in ('fixed', 'centered') for name in (None, '', 'A', 'Even', 'Fleet', '海', 'Indigo海')]
    panels = []
    for record, pixels in rasters:
        panel = Image.new('RGB', (192, 72))
        panel.putdata([(255, 255, 255) if ((pixels[(y * 192 + x) // 2] >> ((x % 2) * 4)) & 15) == 1
                       else (170, 170, 170) if ((pixels[(y * 192 + x) // 2] >> ((x % 2) * 4)) & 15) == 15
                       else (0, 0, 0) for y in range(72) for x in range(192)])
        enlarged = panel.resize((768, 288), Image.Resampling.NEAREST)
        labeled = Image.new('RGB', (768, 320), 'white')
        labeled.paste(enlarged, (0, 32))
        ImageDraw.Draw(labeled).text((8, 8), record['caller'] + ' / ' + repr(record['name_fixture']), fill='black')
        panels.append(labeled)
    sheet = Image.new('RGB', (1536, 320 * 7), 'white')
    for index, panel in enumerate(panels):
        sheet.paste(panel, ((index // 7) * 768, (index % 7) * 320))
    destination = Path('work/qa/fleet_name_native')
    destination.mkdir(parents=True, exist_ok=True)
    sheet.save(destination / 'native_sheet.png')
    raster_report = {'status': 'pass-connected-fleet-native-pixels-visual-review-pending',
                     'research_arm9_sha256': sha(source), 'cases': [r for r, _ in rasters],
                     'native_sheet_sha256': sha((destination / 'native_sheet.png').read_bytes()),
                     'geometry': {'width': 192, 'height': 72, 'mode': 4, 'halfword_pitch': 48},
                     'consumer_locks': result['consumer_locks'] + [
                         {'start': a, 'end': b, 'sha256': sha(source[a:b])}
                         for a, b in ((0x87644, 0x87710), (0xD3AFC, 0xD3B34),
                                      (0xD3E88, 0xD3EF8), (0xD1964, 0xD198C))],
                     'limits': ['Successful outer parent initialization and default bitmap vtable are fixtures.',
                                'Actual bitmap resource setup, text context, virtual getter, formatter and glyph-copy/painter bodies execute.',
                                'Bitmap clear remains a background fixture; physical composition/input, name bounds and other consumers remain pending.']}
    Path('work/analysis/fleet_name_connected_pixels_proof.json').write_text(json.dumps(raster_report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} actual fleet display preparations and {len(rasters)} connected native rasters preserve complete English/CP932 and match independent pixels; visual review pending.')


if __name__ == '__main__':
    main()
