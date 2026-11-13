"""Check the unguarded327 source format at long-name and short-name boundaries."""

import json
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.rom.nds import NdsImage
from scripts.execute_modal_v365 import execute
from scripts.probe_button_prompt_native import STACK, call, machine

ROOT = Path('work/analysis/equipment_wrap_v365')


def main():
    arm = (ROOT / 'research_arm9.bin').read_bytes()
    original = NdsImage.open('out/all_routes_combined_v360_candidate.nds')
    geometry = json.loads(Path('work/analysis/equipment_confirmation_v362/actual_geometry.json').read_text())
    uc = machine(arm)
    rows = []
    actors = ['Rafael Castor', 'Hodram Joakim Bergstrom', 'Lil Argot',
              'Camille Marinus Overijssel', 'Maria Huamei Li']
    for actor in actors:
        for item in ['Travels of Marco Polo', 'Red-Haired Pirate Sword', "Saladin's Silver Armor", 'Sextant']:
            raw = f'{actor} equipped {item}.'.encode()
            uc.mem_write(STACK + 0x100, raw + b'\0')
            call(uc, 0x01FFCA00 - 0x02000000, (STACK + 0x100, STACK + 0x300))
            count = uc.reg_read(UC_ARM_REG_R0)
            assert count > 0
            layout = bytes(uc.mem_read(STACK + 0x300, count)).decode()
            assert ' '.join(layout.split()) == raw.decode()
            for mode in (4, 16):
                native = execute(original.read_file('/__arm9__.bin'), layout,
                                 modal=True, mode=mode, modal_guarded=True,
                                 kanji_font=original.read_file('/GRP/KANJI.FNT'), confirmation_contract=geometry)
                events = [g for g in native['glyph_events'] if g['code'] != 32]
                assert [g['code'] for g in events] == [ord(c) for c in raw.decode() if c != ' ']
                assert all(0 <= g['x'] and g['x'] + 6 <= 228 and g['y'] // 12 * 16 + 11 <= 48 for g in events)
                cursor = 0
                for word in raw.decode().split():
                    assert len({g['y'] for g in events[cursor:cursor + len(word)]}) == 1
                    cursor += len(word)
            rows.append({'actor': actor, 'item': item, 'layout': layout})
    (ROOT / 'unguarded_proof.json').write_text(json.dumps({'cases': rows, 'native_cases': len(rows) * 2,
        'unguarded_equipment_message': 327, 'full_goal_complete': False}, indent=2) + '\n')
    print(f'{len(rows)*2} native unguarded duplicate boundary cases retain all letters and whole words.')


if __name__ == '__main__':
    main()
