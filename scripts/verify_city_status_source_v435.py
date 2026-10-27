"""Execute original town-status getters; isolated supplied byte, not live events."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROM = Path('out/all_routes_combined_v434_candidate.nds')
ROOT = Path('work/analysis/city_help_v435')
OBJECT = 0x02460020


def main():
    current = NdsImage.open(ROM)
    clean = NdsImage.open('work/clean.nds')
    arm = current.read_file('/__arm9__.bin')
    original = clean.read_file('/__arm9__.bin')
    assert arm[0xB2D58:0xB2D94] == original[0xB2D58:0xB2D94]
    assert arm[0xB2E04:0xB2E0C] == original[0xB2E04:0xB2E0C]
    table = struct.unpack_from('<13I', arm, 0x156430)
    fallback = struct.unpack_from('<I', arm, 0xB2D90)[0]
    assert table == struct.unpack_from('<13I', original, 0x156430)
    u = machine(arm)
    rows = []
    for status in range(256):
        data = bytearray(b'\xA5' * 0x80)
        data[0x6A] = status
        u.mem_write(OBJECT - 16, b'\xA5' * 16 + data + b'\xA5' * 16)
        before = bytes(u.mem_read(OBJECT - 16, 0xA0))
        call(u, 0xB2D58, (OBJECT,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        assert pointer == (table[status] if status < 13 else fallback)
        assert bytes(u.mem_read(OBJECT - 16, 0xA0)) == before
        if status < 13:
            raw = bytes(u.mem_read(pointer, 64)).split(b'\0')[0]
            rows.append({'status': status, 'pointer': pointer,
                         'source_table_field': 0x02156430 + status * 4,
                         'current_text': raw.decode('cp932'), 'current_hex': raw.hex(),
                         'natural_English_candidate': ['War', 'Plague', 'Famine', 'Boom', 'Slump',
                                                      'Seasoning Shortage', 'Spice Shortage', 'Luxury Shortage',
                                                      'Alcohol Shortage', 'Fiber Shortage', 'Dye Shortage',
                                                      'Ore Shortage', 'Normal'][status]})
    assert rows[-1]['current_text'] == 'Normal'
    assert all(any(ord(c) > 127 for c in row['current_text']) for row in rows[:-1])
    proof = {'format': 'dk4-town-status-source-v435', 'candidate': str(ROM),
             'candidate_sha256': sha(ROM.read_bytes()), 'native_status_cases': 256,
             'active_table_and_getter_code_clean_exact': True, 'status_rows': rows,
             '12_active_Japanese_status_labels_confirmed': True,
             'scope': 'Original full status getter with supplied isolated city byte6A; complete pointers/strings and ABI/input guards. No genuine city condition, complete painter, layout or gameplay event is credited.',
             'no_live_RAM_ROM_or_save_changes': True,
             'source_owned_storage_layout_and_release_fix_pending': True,
             'all18_plaques_fully_completed': False, 'full_goal_complete': False}
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / 'status_source_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'native_status_cases': 256, 'active_untranslated_status_labels': 12,
                      'source_input_and_ABI_guards_pass': True, 'ROM_changed': False}))


if __name__ == '__main__':
    main()
