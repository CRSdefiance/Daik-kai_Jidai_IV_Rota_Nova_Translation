"""Native status providers, compact consumer selection and complete label rasters."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R4,
    UC_ARM_REG_R6,
    UC_ARM_REG_R8,
    UC_ARM_REG_R10,
    UC_ARM_REG_SP,
)

from dk4tool.patch.city_status_labels import NAMES, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_sailing_footer_v317 import execute
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_scene_caption_raster import expected_pixels

ROOT = Path('work/analysis/city_status_v437')
PARENT = Path('out/all_routes_combined_v436_candidate.nds')
OBJECT, POINTER, LENGTH = 0x02460000, 0x02460100, 0x02460104


def main():
    parent = NdsImage.open(PARENT)
    arm, storage = transform(parent.read_file('/__arm9__.bin'))
    assert arm == (ROOT / 'research_arm9.bin').read_bytes()
    u = machine(arm)
    providers, selections, rasters = [], [], []
    for status in range(256):
        data = bytearray(b'\xA5' * 0x80)
        data[0x6A] = status
        u.mem_write(OBJECT, bytes(data))
        before = bytes(u.mem_read(OBJECT, 0x80))
        call(u, 0xB2D58, (OBJECT,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        full = bytes(u.mem_read(pointer, 64)).split(b'\0')[0].decode('ascii')
        assert full == NAMES[status] if status < 13 else full == 'Normal'
        call(u, 0xB16D8, (OBJECT, POINTER, LENGTH))
        selected, length = struct.unpack('<2I', u.mem_read(POINTER, 8))
        compact = bytes(u.mem_read(selected, 64)).split(b'\0')[0].decode('ascii')
        assert compact == ('Shortage' if len(full) >= 8 else full)
        assert length == len(compact)
        assert bytes(u.mem_read(OBJECT, 0x80)) == before
        if status >= 13:
            continue
        providers.append({'status': status, 'full': full, 'pointer': pointer,
                          'compact': compact, 'actual_compact_length': length})
        # Execute both direct compact-paint selection fragments using the same
        # original getter. Stop before the context/bitmap painter calls.
        for start, stop, object_reg, text_reg in [
                (0x0208D858, 0x0208D870, UC_ARM_REG_R10, UC_ARM_REG_R6),
                (0x020B61EC, 0x020B6204, UC_ARM_REG_R8, UC_ARM_REG_R4)]:
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(object_reg, OBJECT)
            u.emu_start(start, stop, count=1000)
            assert u.reg_read(UC_ARM_REG_PC) == stop
            text = bytes(u.mem_read(u.reg_read(text_reg), 64)).split(b'\0')[0].decode('ascii')
            assert text == compact
            assert bytes(u.mem_read(OBJECT, 0x80)) == before
            selections.append({'status': status, 'consumer_fragment': start,
                               'selected_complete_English': text})
        for text, origin in [(full, [0, 0]), (compact, [56, 44])]:
            result = execute(arm, text, x=origin[0], y=origin[1], tracking=0,
                             mode=4, clear=9, buffered_context=True, surface_size=(256, 192))
            reference = text + (' ' if len(text) % 2 else '')
            assert result['pixels'] == expected_pixels(arm, reference, *origin, 4, advance=6)
            assert result['final_x'] == origin[0] + len(text) * 6
            if origin[0]:
                assert result['final_x'] <= 104
            rasters.append({'status': status, 'text': text, 'origin': origin,
                            'complete_first_internal_final_pixels_exact': True,
                            'final_x': result['final_x']})
    proof = {'format': 'dk4-city-status-native-v437', 'parent': str(PARENT),
             'parent_sha256': sha(PARENT.read_bytes()), 'target_ARM9_sha256': sha(arm),
             'storage': storage, 'all256_full_and_compact_getters_pass': True,
             'providers': providers, '26_actual_compact_selector_fragment_cases': selections,
             '26_complete_native_painter_cases': rasters,
             'scope': 'Original providers/selectors and glyph painter with explicit isolated city byte/context/bitmap inputs. No genuine status event, complete live widget/notice composition or all caller geometry is credited.',
             'actual_cold_boot_and_integrated_release_pending': True,
             'all18_plaques_fully_completed': False, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'provider_cases': 256, 'compact_selector_cases': len(selections),
                      'complete_native_rasters': len(rasters), 'no_growth': True}))


if __name__ == '__main__':
    main()
