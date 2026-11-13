"""Complete six-label Help states and unchanged non-Help native footer rasters."""

import json
import struct
from itertools import pairwise
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_R0, UC_ARM_REG_R12

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.help_footer_release_v2 import PREDICATE, TABLE, transform
from dk4tool.rom.nds import NdsImage
from scripts.execute_sailing_footer_v317 import execute
from scripts.probe_button_prompt_native import call, machine
from scripts.probe_scene_caption_raster import expected_pixels

ROOT = Path('work/analysis/help_footer_v452')
POINTERS = (0x0211B574, 0x0211B53C, 0x0211B524, 0x0211B4FC, 0x0211B58C, 0x0211B51C)
LABELS = ('Prev', 'Next', 'Index', 'First', 'Quit', 'Select')


def main():
    arm = NdsImage.open('out/all_routes_combined_v449_candidate.nds').read_file('/__arm9__.bin')
    target, transformation = transform(arm)
    assert target == (ROOT / 'research_arm9.bin').read_bytes()
    cpu = machine(target)
    scopes = []
    for table in (TABLE, TABLE + 24):
        for caller in (0x020CA92C, 0x020CA930, 0x020CA934, 0x020CA94C, 0x020CA968,
                       0x020CA984, 0x020CA9A0, 0x020CA9BC, 0x020CA9C0):
            cpu.reg_write(UC_ARM_REG_R12, table)
            call(cpu, PREDICATE - 0x02000000, (123, 0, 0, caller))
            expected = table == TABLE and caller in range(0x020CA930, 0x020CA9BD, 28)
            assert bool(cpu.reg_read(UC_ARM_REG_CPSR) & 0x40000000) == expected
            assert cpu.reg_read(UC_ARM_REG_R0) == 123
            scopes.append({'descriptor': table, 'caller': caller, 'matched': expected, 'ABI_pass': True})
    cases = []
    for mask in range(64):
        pointers = [p if mask & (1 << i) else 0 for i, p in enumerate(POINTERS)]
        contract = bytearray(target)
        struct.pack_into('<6I', contract, TABLE - 0x02000000, *pointers)
        labels = [label for i, label in enumerate(LABELS) if mask & (1 << i)]
        consumed = ''.join(reversed(labels))
        for mode, copied in ((4, False), (16, False), (4, True), (16, True)):
            advance = 5 if not copied or mask & 12 else 6
            result = execute(bytes(contract), 'unused', footer_table=TABLE - 0x02000000, mode=mode, footer_copy=copied)
            assert [r['text'] for r in result['footer_draws']] == list(reversed(labels))
            assert result['pixels'] == expected_pixels(target, consumed, 0, 0, mode, advance=advance)
            placements = []
            for slot, label in enumerate(LABELS):
                x, width, source_x = result['footer_metadata'][slot * 3:slot * 3 + 3]
                if not pointers[slot]:
                    assert x == -1
                    continue
                assert width == len(label) * advance
                assert 0 <= x and x + 14 + width + 2 <= 256
                placements.append({'label': label, 'button_left': x, 'caption_width': width,
                                   'caption_buffer_x': source_x, 'button_right': x + 14 + width + 2})
            for a, b in pairwise(placements):
                assert a['button_right'] <= b['button_left']
            assert result['stack_and_registers_preserved']
            cases.append({'mask': mask, 'mode': mode, 'copied_actual_descriptor': copied, 'placements': placements,
                          'complete_native_glyph_and_pixel_masks_exact': True, 'pixel_sha256': sha(result['pixels'])})
    unchanged = []
    for table in (0x12EC10, 0x12EC28, 0x12EC3C, 0x119134, 0x11914C):
        for mode in (4, 16):
            a, b = [execute(raw, 'unused', footer_table=table, mode=mode) for raw in (arm, target)]
            for key in ('pixels', 'footer_metadata', 'footer_draws', 'footer_labels', 'glyph_events'):
                assert a[key] == b[key], (table, mode, key)
            unchanged.append({'table': table, 'mode': mode, 'full_native_pixels_metadata_glyphs_exact': True})
    proof = {'source_arm9_sha256': sha(arm), 'target_arm9_sha256': sha(target), 'transform': transformation,
             'all256_original_and_copied_Help_footer_native_cases': cases,
             'all18_exact_caller_descriptor_scope_cases': scopes,
             'all10_non_Help_Golden_Route_sailing_cases_exact': unchanged,
             'source_font_shapes_palettes_and_button_borders_unchanged': True,
             'actual_Help_buttons_navigation_and_display_pending': True,
             'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('256 complete original/copied Help footer states;18 exact scope cases;10 unchanged other footer cases pass.')


if __name__ == '__main__':
    main()
