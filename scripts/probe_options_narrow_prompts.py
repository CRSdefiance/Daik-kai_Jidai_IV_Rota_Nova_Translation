"""Research complete narrow-English Options confirmations in current native path."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.probe_common_tribute_modal_pixels import verify as pixels

PROMPTS = {'sailing': (0x13880C, 56, 'Sailing Help is %s. Change to %s?', 0x3FCD0, 0x3FD44, 2),
           'reports': (0x138844, 52, 'Reports are %s. Change to %s?', 0x3FD54, 0x3FDC8, 1)}


def prepare(source):
    if sha(source) != '1b5e9c5bec1418770c138256ecdd7d2c74d0f0db67fda6330a10f70ae68a82ec':
        raise ValueError('Exact complete V143 ARM9 required')
    saved = bytearray(source)
    for offset, capacity, text, _, _, _ in PROMPTS.values():
        raw = text.encode('ascii') + b'\0'
        if len(raw) > capacity:
            raise ValueError('Complete natural Options prompt exceeds source allocation')
        saved[offset:offset + capacity] = raw.ljust(capacity, b'\0')
    return bytes(saved)


def execute(source, kind, flags):
    _, _, text, start, literal, mask = PROMPTS[kind]
    machine = machine_for(source)
    resident = MainCodeFile(source, BASE).sections[1]
    machine.mem_map(0x01FF8000, 0x8000)
    machine.mem_write(resident.ramAddress, bytes(resident.data))
    preferences = struct.unpack_from('<I', source, literal)[0]
    machine.mem_write(preferences + 0x3E, bytes((flags,)))
    formatted, expanded = struct.unpack_from('<2I', source, 0x54890)
    for buffer in (formatted, expanded):
        machine.mem_write(buffer - 32, b'\xa5' * 320)
    expected = text.replace('%s', 'On' if flags & mask else 'Off', 1).replace(
        '%s', 'Off' if flags & mask else 'On', 1).encode('ascii')
    machine.emu_start(BASE + start, BASE + 0x5479C, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != BASE + 0x5479C or machine.reg_read(UC_ARM_REG_SP) != STACK - 8 - 24 - 200:
        raise ValueError('Actual Options caller/formatter fails to reach native widget construction')
    for buffer in (formatted, expanded):
        if bytes(machine.mem_read(buffer - 32, 320)) != b'\xa5' * 32 + expected + b'\0' + b'\xa5' * (287 - len(expected)):
            raise ValueError('Options native formatting loses full prose, state order or buffer guards')
    if bytes(machine.mem_read(preferences + 0x3E, 1)) != bytes((flags,)):
        raise ValueError('Options preparation changes preference before user response')
    return {'kind': kind, 'flags': flags, 'complete_prepared_text': expected.decode('ascii'),
            'current_and_proposed_state_order_preserved': True, 'preference_unchanged': True}


def respond(source, kind, flags, accepted):
    _, _, _, _, literal, mask = PROMPTS[kind]
    machine = machine_for(source)
    preferences = struct.unpack_from('<I', source, literal)[0]
    dirty = struct.unpack_from('<I', source, literal + 12)[0]
    machine.mem_write(preferences + 0x3E, bytes((flags,)))
    machine.mem_write(dirty + 0x64, struct.pack('<I', 0x12345678))
    machine.mem_write(STACK, struct.pack('<2I', 0x87654321, STOP))
    machine.reg_write(UC_ARM_REG_R0, int(accepted))
    machine.reg_write(UC_ARM_REG_R4, int(bool(flags & mask)))
    start = 0x3FD0C if kind == 'sailing' else 0x3FD90
    machine.emu_start(BASE + start, STOP, count=1000)
    expected = flags ^ mask if accepted else flags
    if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 8
            or bytes(machine.mem_read(preferences + 0x3E, 1)) != bytes((expected,))
            or struct.unpack('<I', machine.mem_read(dirty + 0x64, 4))[0] != (1 if accepted else 0x12345678)):
        raise ValueError('Native Options response changes wrong preference or cancellation state')
    return {'kind': kind, 'flags': flags, 'accepted': accepted, 'result_flags': expected,
            'unrelated_bits_and_cancel_behavior_preserved': True}


def main():
    rom = NdsImage.open('out/all_routes_combined_v143_candidate.nds')
    source, font = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    research = prepare(source)
    renderer = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    if (MainCodeFile(source, BASE).sections[1].data[:6944] != MainCodeFile(renderer, BASE).sections[1].data
            or any(source[a:b] != renderer[a:b] for a, b in ((0x548A8, 0x54988),
                                                           (0xD1500, 0xD5B00), (0x125A60, 0x125E75)))):
        raise ValueError('Current Options raster differs from pinned unchanged V142 renderer')
    cases = [execute(research, kind, flags) for kind in PROMPTS for flags in (0, 1, 2, 3, 255)]
    responses = [respond(research, kind, flags, accepted) for kind in PROMPTS
                 for flags in (0, 1, 2, 3, 255) for accepted in (False, True)]
    unique = list(dict.fromkeys(c['complete_prepared_text'] for c in cases))
    rendered = []
    for text in unique:
        for mode in (4, 16):
            native = pixels(renderer, font, text, mode)
            if len({e['y'] for e in native['glyph_events']}) != 1:
                raise ValueError('Complete Options prompt unexpectedly wraps')
            rendered.append({'text': text, 'mode': mode, 'pixels_sha256': sha(native['pixels']),
                             'single_row_complete_native_glyphs_and_pixels': True})
    report = {'status': 'pass-research-narrow-options-native-preparation-and-pixels',
              'source_sha256': sha(source), 'research_sha256': sha(research),
              'cases': cases, 'native_pixels': rendered, 'native_responses': responses,
              'limitations': 'Actual Options state selection, varargs wrapper, formatter and original macros execute together. Unchanged shared renderer is a separate invocation; full widget/choice/input, physical routing and cold-boot gameplay remain pending. Source warning about old ASCII corruption is not revoked by this research proof.'}
    Path('work/analysis/options_narrow_prompts_arm9.bin').write_bytes(research)
    Path('work/analysis/options_narrow_prompts_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} actual Options preparations and {len(rendered)} native pixel cases preserve narrow English and state order.')


if __name__ == '__main__':
    main()
