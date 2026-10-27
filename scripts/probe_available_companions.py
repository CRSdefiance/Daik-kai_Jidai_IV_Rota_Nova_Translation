"""Research full empty-companion-list English with preserved adjacent Options."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R4,
    UC_ARM_REG_R10,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.inventory_arm9_text import components
from scripts.probe_common_tribute_modal_pixels import verify as pixels
from scripts.probe_options_narrow_prompts import execute as options
from scripts.probe_options_narrow_prompts import respond

SOURCE = '5939d4730b0a30ae68f9dc4c98b9170a807b3f54d1af4670607148005b6d9ab8'
ENGLISH = 'No companions are available!'
OWNERS = [(0x13880C, 56, 0x3FD4C), (0x138844, 52, 0x3FDD0),
          (0x138878, 8, 0x408CC), (0x138880, 20, 0x40BF0)]


def prepare(image):
    source = image.read_file('/__arm9__.bin')
    if sha(source) != SOURCE:
        raise ValueError('Exact complete V146 ARM9 required')
    start, end = 0x13880C, 0x138894
    refs = []
    for name, _, raw in components(image):
        for p in range(len(raw) - 3):
            target = struct.unpack_from('<I', raw, p)[0] - BASE
            if start <= target < end:
                refs.append((name, p, target))
    expected = [('arm9', field, at) for at, _, field in OWNERS]
    if refs != expected:
        raise ValueError('Complete companion/Options pool reference grammar differs')
    saved, packed, moves = bytearray(source), bytearray(), []
    for at, capacity, field in OWNERS:
        original = source[at:at + capacity]
        raw = original.split(b'\0', 1)[0] + b'\0'
        if any(original[len(raw):]):
            raise ValueError('Complete companion/Options owner padding is not zero')
        if at == 0x138880:
            raw = ENGLISH.encode('ascii') + b'\0'
        new = start + len(packed)
        packed.extend(raw)
        packed.extend(b'\0' * (-len(packed) % 4))
        moves.append({'old_offset': at, 'new_offset': new, 'field_offset': field,
                      'source_capacity': capacity, 'original_allocation_hex': original.hex(),
                      'complete_text': raw[:-1].decode('cp932')})
        struct.pack_into('<I', saved, field, BASE + new)
    if len(packed) > end - start:
        raise ValueError('Full companion message does not fit complete owned pool')
    saved[start:end] = packed.ljust(end - start, b'\0')
    restored = bytearray(saved)
    restored[start:end] = source[start:end]
    for _, _, field in OWNERS:
        restored[field:field + 4] = source[field:field + 4]
    if bytes(restored) != source:
        raise ValueError('Companion research changes unrelated bytes')
    return bytes(saved), {'source_span': [start, end], 'used_aligned_bytes': len(packed),
                          'owned_bytes': end - start, 'moves': moves, 'references': refs,
                          'all_other_arm9_bytes_preserved': True}


def empty_branch(source):
    machine = machine_for(source)
    resident = MainCodeFile(source, BASE).sections[1]
    machine.mem_map(0x01FF8000, 0x8000)
    machine.mem_write(resident.ramAddress, bytes(resident.data))
    frame = STACK - 36 - 0x344
    machine.reg_write(UC_ARM_REG_SP, frame)
    machine.reg_write(UC_ARM_REG_R10, 0)
    expected = ENGLISH.encode('ascii') + b'\0'
    buffers = struct.unpack_from('<2I', source, 0x54890)
    for buffer in buffers:
        machine.mem_write(buffer - 32, b'\xA5' * 320)
    machine.emu_start(BASE + 0x40B1C, BASE + 0x5479C, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != BASE + 0x5479C or machine.reg_read(UC_ARM_REG_SP) != frame - 24 - 200:
        raise ValueError('Actual empty-companion branch fails to reach modal construction')
    for buffer in buffers:
        if bytes(machine.mem_read(buffer - 32, 320)) != b'\xA5' * 32 + expected + b'\xA5' * (288 - len(expected)):
            raise ValueError('Companion native format/macros lose complete sentence or guards')
    machine.reg_write(UC_ARM_REG_SP, frame)
    machine.mem_write(frame + 0x344, struct.pack('<9I', *range(8), STOP))
    machine.emu_start(BASE + 0x40BD4, STOP, count=100)
    if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK
            or machine.reg_read(UC_ARM_REG_R0) != 0):
        raise ValueError('Companion empty-list return result/frame differs')
    positive = machine_for(source)
    positive.reg_write(UC_ARM_REG_R10, 1)
    positive.emu_start(BASE + 0x40B1C, BASE + 0x40B24, count=10)
    if positive.reg_read(UC_ARM_REG_PC) != BASE + 0x40B24:
        raise ValueError('Nonempty list enters companion-error branch')
    return {'complete_text': ENGLISH, 'native_zero_count_branch_formatter_and_macros_verified': True,
            'native_empty_return_zero_and_stack_preserved': True, 'positive_count_bypasses_error': True,
            'limits': 'Filtered list count supplied as a fixture; actual enumeration/backend and modal widgets/dismissal remain unexecuted.'}


def parenthesized_format(source, name):
    machine = machine_for(source)
    pointer, context = 0x02410000, 0x02411000
    raw = name.encode('cp932')
    machine.mem_write(pointer, raw + b'\0')
    machine.reg_write(UC_ARM_REG_R0, pointer)
    machine.reg_write(UC_ARM_REG_R4, context)
    buffer = struct.unpack_from('<I', source, 0xD529C)[0]
    machine.mem_write(buffer - 32, b'\xA5' * 1088)
    machine.emu_start(BASE + 0x408AC, BASE + 0xD5404, count=100000)
    selected = machine.reg_read(UC_ARM_REG_R1)
    expected = ('（' + name + '）').encode('cp932') + b'\0'
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0xD5404
            or machine.reg_read(UC_ARM_REG_R0) != context
            or selected != buffer
            or bytes(machine.mem_read(buffer - 32, 1088)) != b'\xA5' * 32 + expected + b'\xA5' * (1056 - len(expected))):
        raise ValueError('Native relocated neighboring format loses complete parenthesized name')
    return {'name': name, 'complete_prepared_text': expected[:-1].decode('cp932'),
            'actual_neighboring_literal_varargs_and_formatter_preserved': True}


def main():
    image = NdsImage.open('out/all_routes_combined_v146_candidate.nds')
    source = image.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x40A84, 0x40BF4), (0x40888, 0x408D0), (0x3FCD0, 0x3FD4C), (0x3FD54, 0x3FDD0)]
    if any(source[a:b] != clean[a:b] for a, b in spans):
        raise ValueError('Original companion/Options consumer code differs')
    research, allocation = prepare(image)
    native = empty_branch(research)
    inherited_options = [options(research, kind, flags) for kind in ('sailing', 'reports') for flags in (0, 1, 2, 3, 255)]
    responses = [respond(research, kind, flags, accepted) for kind in ('sailing', 'reports')
                 for flags in (0, 1, 2, 3, 255) for accepted in (False, True)]
    parenthesized = [parenthesized_format(research, name) for name in ('', 'A', 'Even', 'Fleet', '海', 'Indigo海')]
    renderer = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    if (MainCodeFile(source, BASE).sections[1].data[:6944] != MainCodeFile(renderer, BASE).sections[1].data
            or any(source[a:b] != renderer[a:b] for a, b in ((0x548A8, 0x54988), (0xD1500, 0xD5B00), (0x125A60, 0x125E75)))):
        raise ValueError('Companion current modal raster differs from pinned unchanged renderer')
    destination = Path('work/qa/available_companions_native')
    destination.mkdir(parents=True, exist_ok=True)
    rasters = []
    for mode in (4, 16):
        raster = pixels(renderer, image.read_file('/GRP/KANJI.FNT'), ENGLISH, mode)
        if len({event['y'] for event in raster['glyph_events']}) != 1:
            raise ValueError('Complete companion sentence unexpectedly wraps')
        rasters.append({'mode': mode, 'pixels_sha256': sha(raster['pixels']), 'single_row_complete_glyphs_and_independent_pixels': True})
        if mode == 16:
            panel = Image.new('RGB', (256, 192))
            panel.putdata([(255, 255, 255) if c == 9 else (128, 128, 128) if c == 14
                           else (0, 0, 0) for c in struct.unpack('<49152H', raster['pixels'])])
            panel.crop((0, 0, 256, 96)).resize((1024, 384), Image.Resampling.NEAREST).save(destination / 'native_sheet.png')
    row = {'id': 'NO_AVAILABLE_COMPANIONS', 'offset': 0x138880, 'capacity': 20,
           'source_hex': clean[0x138880:0x138894].hex().upper(), 'japanese': '仲間がいません！',
           'english': ENGLISH + '{PAD}', 'speaker': 'Companion selection error',
           'context': '40A84 constructs a filtered companion list; zero count at 40B1C branches to 40BCC and modal 5473C, returning zero after dismissal. Availability wording avoids claiming that unavailable companions do not exist.',
           'source_meaning': 'There are no companions to select.',
           'localization_note': 'Complete natural American English preserves the source warning and its empty eligible-list context. No abbreviations or authored breaks; full sentence fits one native row. Neighboring complete Options prompts and parenthesized format bytes are retained. Physical gameplay remains pending.',
           'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False}}
    document = {'format': 'dk4-arm9-prompt-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
                'target_locale': 'en-US', 'encoder': 'dialogue-fixed-v1', 'review_gates': list(row['review']), 'records': [row]}
    Path('translations/available_companions_manuscript_v1.json').write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report = {'status': 'pass-research-native-companion-message-options-preserved-review-pending',
              'source_arm9_sha256': sha(source), 'research_arm9_sha256': sha(research),
              'allocation': allocation, 'native_empty_branch': native,
              'inherited_options_cases': inherited_options, 'native_options_response_cases': responses,
              'native_parenthesized_format_cases': parenthesized,
              'pixel_cases': rasters, 'consumer_locks': [{'start': a, 'end': b, 'sha256': sha(source[a:b])} for a, b in spans],
              'candidate_changed': False, 'runtime_verified': False,
              'limits': ['Native preparation and raster are separate executions.', native['limits'],
                         'Full Options/parenthesized-format physical presentation and gameplay remain pending.']}
    Path('work/analysis/available_companions_arm9.bin').write_bytes(research)
    Path('work/analysis/available_companions_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f"Full companion prose fits {allocation['used_aligned_bytes']}/{allocation['owned_bytes']} bytes; native empty branch, 10 inherited Options, 20 responses and two pixel cases pass.")


if __name__ == '__main__':
    main()
