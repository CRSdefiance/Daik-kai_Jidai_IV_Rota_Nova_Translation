"""Execute original scene selection, centering, wrapper and complete font pixels.

Route/index/owner view are explicit caller fixtures. No game unlock, GPU or
interactive navigation claim is made by this isolated native test.
"""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.prepare_artwork_name_captions_v283 import NAMES, read
from scripts.prepare_artwork_name_captions_v283 import ROOT as PRIOR
from scripts.probe_button_prompt_native import STACK, machine
from scripts.research_online_loader_v190 import resource_call as call

ROOT = Path('work/analysis/artwork_caption_selector_v284')
TABLES = {0: 0x115CAC, 1: 0x115A04, 2: 0x115968, 3: 0x115834}
COUNTS = {0: 46, 1: 41, 2: 39, 3: 38}
HEADER, OWNER, FRAME, STOP = 0x02450000, 0x02470000, 0x02440000, BASE + 0x4300C


def execute(arm, row, mode, *, gallery=False):
    cpu = machine(arm)
    if gallery:
        rom = NdsImage.open('out/all_routes_combined_v275_candidate.nds').rom
        overlays = loadOverlayTable(rom.arm9OverlayTable, lambda _, file_id: rom.files[file_id])
        assert len(overlays) == 1
        overlay = overlays[0]
        assert overlay.ramAddress == 0x01FFA000 and len(overlay.data) == 6208 and overlay.bssSize == 32
        cpu.mem_write(overlay.ramAddress, bytes(overlay.data) + bytes(overlay.bssSize))
    cpu.mem_write(POOL, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    size = 256 * 192 * (2 if mode == 16 else 1) // (1 if mode == 16 else 2)
    header = struct.pack('<5I', mode, 256 // (1 if mode == 16 else 4), 192,
                         0x0247F000 - HEADER, 20)
    cpu.mem_write(HEADER - 16, b'\xA5' * (size + 52))
    cpu.mem_write(HEADER, header + (b'\xA5' * size if gallery else bytes(size)))
    view = OWNER + 0x6028
    call(cpu, 0xD3D80, (view,))
    cpu.mem_write(STACK, struct.pack('<4I', 256, 192, 0, 0))
    call(cpu, 0xD3AFC, (view, HEADER, 0, 0))
    metrics = struct.unpack_from('<I', arm, 0xD5088)[0]
    cpu.mem_write(metrics + 4, struct.pack('<2I', 6, 16))
    table, index = (0x115678 if gallery else TABLES[row['route_index']]), row['index']
    assert 0 <= index < (4 if gallery else COUNTS[row['route_index']])
    frame = OWNER - 0xA4 if gallery else FRAME
    cpu.mem_write(frame + 0x50, struct.pack('<I', 70))
    registers = {UC_ARM_REG_R4: 2, UC_ARM_REG_R5: 0, UC_ARM_REG_R6: 1,
                 UC_ARM_REG_R7: index, UC_ARM_REG_R8: BASE + table,
                 UC_ARM_REG_R10: OWNER, UC_ARM_REG_R11: frame}
    for register, value in {**registers, UC_ARM_REG_SP: STACK}.items():
        cpu.reg_write(register, value)
    events, draws, executed = [], [], set()

    def observe(uc, address, size, _):
        executed.add(address)
        if address == BASE + 0xD5404:
            context, pointer = uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)
            raw = bytes(uc.mem_read(pointer, 256)).split(b'\0', 1)[0]
            draws.append({'pointer': pointer, 'text': raw.decode('ascii'),
                          'origin': list(struct.unpack('<2I', uc.mem_read(context + 36, 8))),
                          'tracking': struct.unpack('<i', uc.mem_read(context + 28, 4))[0]})
        elif address == BASE + 0xD16B4:
            code, style = struct.unpack('<2I', uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 8))
            events.append((code, style, uc.reg_read(UC_ARM_REG_R2), uc.reg_read(UC_ARM_REG_R3)))

    cpu.hook_add(UC_HOOK_CODE, observe)
    stop = STOP
    if gallery:
        cpu.emu_start(BASE + 0x42C2C, BASE + 0x42CE4, count=1000)
        assert cpu.reg_read(UC_ARM_REG_PC) == BASE + 0x42CE4
        cpu.mem_write(frame + 0x1C, struct.pack('<I', index))
        registers = {reg: cpu.reg_read(reg) for reg in registers}
        stop = BASE + 0x42FD0
    cpu.emu_start(BASE + (0x42F70 if gallery else 0x42FD0), stop, count=1000000)
    assert cpu.reg_read(UC_ARM_REG_PC) == stop and cpu.reg_read(UC_ARM_REG_SP) == STACK
    assert all(cpu.reg_read(reg) == value for reg, value in registers.items())
    text = row['english']
    for before, after in NAMES.items():
        text = text.replace(before, after)
    x = 8 if gallery else 128 - len(text) * 5 // 2
    selected = struct.unpack('<I', cpu.mem_read(BASE + table + index * 4, 4))[0]
    if gallery:
        text += ' ' if len(text) % 2 else ''
        expected_draws = [
            {'pointer': struct.unpack_from('<I', arm, 0x432C8)[0], 'text': 'Event Scenes',
             'origin': [92, 2], 'tracking': 0},
            {'pointer': selected, 'text': text, 'origin': [8, 20], 'tracking': 0}]
    else:
        expected_draws = [{'pointer': selected, 'text': text, 'origin': [x, 70], 'tracking': -1}]
    assert draws == expected_draws, (draws, expected_draws)
    assert [(c, xx, yy) for c, _, xx, yy in events if c != 32] == [
        (ord(c), draw['origin'][0] + n * (6 + draw['tracking']), draw['origin'][1])
        for draw in expected_draws for n, c in enumerate(draw['text']) if c != ' ']
    assert {BASE + p for p in (0x42F70 if gallery else 0x42FD0, 0x456A0, 0xD5160, 0xD5404, 0xD5140)} <= executed
    if gallery:
        assert BASE + 0xD393C in executed
        assert any(0x01FFA000 <= p < 0x01FFB840 for p in executed)
    expected = bytearray(256 * 192)
    font = GameAsciiFont.from_arm9(arm)
    for code, style, xx, yy in events:
        assert 0 <= xx <= 250 and 0 <= yy <= 181
        glyph = font.decode(chr(code))
        for gy in range(11):
            for gx in range(6):
                if glyph.getpixel((gx, gy)):
                    expected[(yy + gy) * 256 + xx + gx] = style
    raw = bytes(cpu.mem_read(HEADER + 20, size))
    if mode == 4:
        pixels = bytes(n for b in raw for n in (b & 15, b >> 4))
        assert pixels == expected
    else:
        palette = struct.unpack_from('<I', arm, 0xD181C)[0] - BASE
        colors = struct.unpack_from('<16H', arm, palette)
        wanted = b''.join(struct.pack('<H', colors[n] if n else 0) for n in expected)
        assert raw == wanted
    assert bytes(cpu.mem_read(HEADER, 20)) == header
    assert bytes(cpu.mem_read(HEADER - 16, 16)) == bytes(cpu.mem_read(HEADER + 20 + size, 16)) == b'\xA5' * 16
    return {'id': row['id'], 'mode': mode, 'selected_text': text,
            'selected_pointer': selected, 'origin': [x, 20 if gallery else 70],
            'native_draws': draws,
            'native_bitmap_clear_and_original_overlay_executed': gallery,
            'native_wrapper_context_renderer_cleanup_executed': True,
            'complete_independent_pixels_and_visible_letters_exact': True,
            'stack_registers_header_and_buffer_guards_preserved': True,
            'pixels_sha256': sha(raw)}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source = (PRIOR / 'proposed_arm9_research_only.bin').read_bytes()
    assert sha(source) == read(PRIOR / 'native_proof.json')['target_arm9_sha256']
    rows = read('translations/scene_caption_manuscript_v2.json')['records']
    cases = [execute(source, row, mode) for row in rows for mode in (4, 16)]
    proof = {'format': 'dk4-native-artwork-caption-selector-v284',
             'target_arm9_sha256': sha(source), 'all164_captions_native_cases': cases,
             'native_selection_strlen_centering_wrapper_real_context_font_and_cleanup_pass': True,
             'external_draw_contract_bridges_used': False,
             'route_index_owner_view_and_font_metrics_are_caller_fixtures': True,
             'actual_unlock_input_GPU_and_live_scene_composition_pending': True,
             'full_registered_release_integration_pending': True,
             'playable_ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} complete native selector/wrapper/font cases pass; live scene navigation remains pending.')


if __name__ == '__main__':
    main()
