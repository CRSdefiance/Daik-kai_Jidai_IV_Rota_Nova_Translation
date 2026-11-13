"""Native complete Tavern addresses, printf, word wrapping and untouched siblings."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.tavern_address_release import apply_release
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_remaining_common_layout import warm_copy
from scripts.verify_common_alignment_native_v257 import raster

ROOT = Path('work/analysis/tavern_addresses_v413')
ROM = Path('out/all_routes_combined_v408_candidate.nds')


def wrap(arm, text, parent, message):
    u = machine(arm)
    u.mem_write(0x02387A20, bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48]))
    source, output = 0x0242C020, 0x0242D020
    u.mem_write(source - 16, b'\xA5' * 16 + text + b'\0' + b'\xA5' * 16)
    u.mem_write(output - 16, b'\xA5' * 288)
    u.mem_write(STACK + 0x264, struct.pack('<I', parent))
    u.mem_write(STACK + 0x274, struct.pack('<I', message))
    call(u, 0x01FFCF3C - 0x02000000, (output, source, 0))
    result = bytes(u.mem_read(output, 256)).split(b'\0', 1)[0]
    assert bytes(u.mem_read(source, len(text) + 1)) == text + b'\0'
    assert bytes(u.mem_read(output - 16, 16)) == bytes(u.mem_read(output + 256, 16)) == b'\xA5' * 16
    return result


def main():
    r = NdsImage.open(ROM)
    common, arm = r.read_file('/COMMON/MESFILE.DK4'), r.read_file('/__arm9__.bin')
    target, mapped, change = apply_release(common, arm, 'translations/tavern_addresses_v1.json')
    entries = common_message_entries(target, mapped, clean=False)
    copies = [warm_copy(mapped, target, n, entries[n].text, cold_cache=cold)
              for n in [864, 865, 866, 867, 869, 870, 871, 872, 873, 874] for cold in (False, True)]
    u = machine(mapped)
    for n in range(8):
        actual = bytes(u.mem_read(0x02143BD0 + n * 8, 8)).split(b'\0', 1)[0]
        assert actual == (b'Sir' if n % 2 == 0 else b"Ma'am")
    out, fmt, addr, item, region = [STACK + n for n in (0x1000, 0x2000, 0x2100, 0x2200, 0x2300)]
    font = GameAsciiFont.from_arm9(mapped)
    cases = []
    for gender in ['Sir', "Ma'am"]:
        for name in ['Blue Oak Shield', 'Minotaur Axe', 'Golden Cutlass']:
            for area in ['N. Sea', 'Mediterranean', 'East Asia']:
                text = entries[870].text.rstrip()
                u.mem_write(out - 16, b'\xA5' * 544)
                for p, value in [(fmt, text), (addr, gender.encode()), (item, name.encode()), (region, area.encode())]:
                    u.mem_write(p, value + b'\0')
                u.mem_write(STACK, struct.pack('<I', region))
                call(u, 0xD7720, (out, fmt, addr, item))
                expected = text.replace(b'%s', gender.encode(), 1).replace(b'%s', name.encode(), 1).replace(b'%s', area.encode(), 1)
                assert bytes(u.mem_read(out, len(expected) + 1)) == expected + b'\0'
                assert bytes(u.mem_read(out - 16, 16)) == b'\xA5' * 16
                assert bytes(u.mem_read(out + len(expected) + 1, 527 - len(expected))) == b'\xA5' * (527 - len(expected))
                formatted = wrap(mapped, expected, 0x02054014, 870)
                assert b' '.join(formatted.split()) == expected
                pixels = raster(mapped, formatted, 0x01FFCE40 - 0x02000000,
                                size=(228, 64), instruction_limit=300000)
                ink = sum(sum(bool(p) for p in font.decode(c).get_flattened_data())
                          for c in expected.decode() if c != ' ')
                assert sum(bool(p) for p in pixels) == ink
                if name == 'Blue Oak Shield' and area == 'N. Sea':
                    Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in pixels)).save(ROOT / f'clue_{gender.replace(chr(39), "")}_native.png')
                cases.append({'address': gender, 'item': name, 'region': area,
                              'complete_native_text': expected.decode(), 'word_wrapped': formatted.decode(),
                              'all_native_glyph_pixels': ink})
    related = []
    for n in [871, 873]:
        for address_text in ['Sir', "Ma'am", '旦那', '姉さん']:
            first = b'Bergstrom' if n == 871 else address_text.encode('cp932')
            u.mem_write(fmt, entries[n].text.rstrip() + b'\0')
            u.mem_write(addr, first + b'\0')
            u.mem_write(item, address_text.encode('cp932') + b'\0')
            call(u, 0xD7720, (out, fmt, addr, item))
            expected = entries[n].text.rstrip().replace(b'%s', first, 1)
            assert bytes(u.mem_read(out, len(expected) + 1)) == expected + b'\0'
            if address_text in ['Sir', "Ma'am"]:
                value = wrap(mapped, expected, 0x02054014, n)
                assert b' '.join(value.split()) == expected
            related.append({'id': n, 'address': address_text, 'complete_output': expected.decode('cp932')})
    scope = []
    raw = b'Sir, here is a treasure clue with a sufficiently long complete sentence.'
    for parent in [0x02054014, 0x02054044]:
        for n in [819, 820, 821, 822, 869, 870, 871, 872, 873, 874, 321, 327]:
            a, b = wrap(arm, raw, parent, n), wrap(mapped, raw, parent, n)
            if parent != 0x02054014 or n not in range(870, 874):
                assert a == b
            assert b' '.join(a.split()) == b' '.join(b.split())
            scope.append({'parent': parent, 'message': n, 'exact_passthrough': a == b})
    proof = {'source_candidate': str(ROM), 'source_candidate_sha256': sha(ROM.read_bytes()),
             'target_common_sha256': sha(target), 'target_arm9_sha256': sha(mapped),
             'native_cold_warm_neighbor_copies': copies, 'male_female_clue_printf_wrap_raster_cases': cases,
             'all_eight_actual_address_slots_English': True, 'applause_and_encouragement_printf_cases': related,
             'scope_and_existing_rumors_and_equipment_passthrough': scope,
             'change': change, 'actual_release_display_pending': True, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'{len(copies)} native copies, {len(cases)} male/female clue rasters and {len(scope)} scope cases pass.')


if __name__ == '__main__':
    main()
