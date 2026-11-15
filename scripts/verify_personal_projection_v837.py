"""Native Deck parent crop, original frame/headers and complete visible words."""

import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_dialogue_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.audit_item_runtime_storage_v785 import census
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.personal_chatter_layout_v837 import compiled, layout, serialize
from scripts.probe_personal_fonts_v836 import CAP, VIEW, execute
from scripts.prepare_personal_chatter_v835 import ROM
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/personal_chatter_v837')
MANUSCRIPT = Path('translations/personal_chatter_editorial_manuscript_v2.json')
BASE, FIELD, TABLE = 0x02000000, 0x1147B8, 0x114718


def changed_arm(arm):
    assert struct.unpack_from('<7I', arm, TABLE + 5 * 28) == (0xFFFFFFFF, 16, 112, 0, 60, 144, 24)
    out = bytearray(arm)
    struct.pack_into('<2I', out, FIELD, 216, 36)
    restored = bytearray(out)
    restored[FIELD:FIELD + 8] = arm[FIELD:FIELD + 8]
    assert bytes(restored) == arm
    return bytes(out)


def composition(rom, raw, text, target, *, actor=4, state=1, forced_mode=None):
    arm = rom.read_file('/__arm9__.bin')
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.rom.files[fid])[0]
    assert overlay.ramAddress == 0x01FFA000 and len(overlay.data) == 6208
    cpu.mem_write(overlay.ramAddress, bytes(overlay.data))
    if target:
        cpu.mem_write(BASE + FIELD, changed_arm(arm)[FIELD:FIELD + 8])
    renderer = 0x02468000
    cpu.mem_write(renderer, struct.pack('<I', 0x0215FA94))
    cpu.mem_write(renderer + 0x100, bytes(8))
    draws, selected = [], []
    entries = current_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm) if text is None else None
    def hook(u, pc, size, unused):
        if pc == BASE + 0x5528C:
            selected.append(u.reg_read(UC_ARM_REG_R0))
            payload = entries[selected[-1]].text if entries is not None else text
            u.mem_write(0x02450000, payload + b'\0')
            u.reg_write(UC_ARM_REG_R0, 0x02450000)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif pc == 0x01FF92D8:
            sp = u.reg_read(UC_ARM_REG_SP)
            sizep, destination = struct.unpack('<2I', u.mem_read(sp, 8))
            draws.append({'image': u.reg_read(UC_ARM_REG_R1), 'layer': u.reg_read(UC_ARM_REG_R0),
                          'flags': u.reg_read(UC_ARM_REG_R2),
                          'source_origin': list(struct.unpack('<2i', u.mem_read(u.reg_read(UC_ARM_REG_R3), 8))),
                          'size': list(struct.unpack('<2i', u.mem_read(sizep, 8))),
                          'destination': list(struct.unpack('<2i', u.mem_read(destination, 8)))})
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
    hooks = [cpu.hook_add(UC_HOOK_CODE, hook, begin=p, end=p) for p in (BASE + 0x5528C, 0x01FF92D8)]
    try:
        # Original entry resolves the real flagship/room type and sets view mode3.
        # Actor/state preview and room14 are controlled selection inputs here.
        call(cpu, 0x15948, (VIEW, 14, state, actor), instruction_limit=2000000)
        assert struct.unpack('<I', cpu.mem_read(VIEW + 0x100, 4))[0] == 3
        if forced_mode is not None:
            cpu.mem_write(VIEW + 0x100, struct.pack('<I', forced_mode))
        call(cpu, 0x14BE8, (VIEW, renderer), instruction_limit=3000000)
    finally:
        for h in hooks:
            cpu.hook_del(h)
    vt = struct.unpack('<I', cpu.mem_read(VIEW, 4))[0]
    offset = struct.unpack('<i', cpu.mem_read(vt - 16, 4))[0]
    bounds = list(struct.unpack('<4i', cpu.mem_read(VIEW + offset + 0x20, 16)))
    assert bounds == [0, 0, 256, 192]
    resource = struct.unpack('<I', cpu.mem_read(VIEW + 0x50, 4))[0]
    header = bytes(cpu.mem_read(resource, 20))
    palette = (resource + struct.unpack_from('<I', header, 12)[0]) & 0xFFFFFFFF
    return {'draws': draws, 'selected_IDs': selected, 'captured_parent_bounds': bounds,
            'canvas_resource': resource, 'canvas_header_hex': header.hex(),
            'canvas_palette': palette, 'canvas_palette32_sha256': sha(bytes(cpu.mem_read(palette, 32))),
            'original_full_selection_and_parent_complete_ABI': True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    source = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert source[TABLE:TABLE + 168] == arm[TABLE:TABLE + 168]
    new = changed_arm(arm)
    (ROOT / 'ARM9_PARENT_CROP_RESEARCH_ONLY.bin').write_bytes(new)
    incoming = census(rom, [(BASE + TABLE, BASE + TABLE + 168)], [])
    assert incoming == [['absolute', 'section0', BASE + 0x14F44, BASE + TABLE, False]], incoming
    report = read(CAP / 'capture_report.json')
    snapshot = next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame'] == 15200)
    raw = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and sha(raw) == snapshot['sha256']
    doc = read(MANUSCRIPT)
    text = compiled(next(r for r in doc['records'] if r['message_id'] == 1365))
    old, target = [composition(rom, raw, text, flag) for flag in (False, True)]
    assert old['selected_IDs'] == target['selected_IDs'] == [1365]
    assert old['draws'][:-1] == target['draws'][:-1]
    assert old['draws'][-1] == {**target['draws'][-1], 'size': [144, 24]}
    assert target['draws'][-1]['size'] == [216, 36]
    assert target['draws'][-1]['source_origin'] == [0, 60] and target['draws'][-1]['destination'] == [16, 112]
    assert old['canvas_header_hex'] == target['canvas_header_hex']
    assert old['canvas_palette32_sha256'] == target['canvas_palette32_sha256']
    # State3 alone refers to this descriptor. Probe the other parent branches
    # as explicit view-state controls,not claimed ordinary UI activations.
    controls = []
    for mode in (0, 1, 2, 4):
        a, b = [composition(rom, raw, text, flag, forced_mode=mode) for flag in (False, True)]
        assert a == b
        controls.append({'forced_native_view_mode': mode, 'all_original_parent_draws_palette_bounds_exact': True})
    # A genuinely assigned current captain provides the established work-caption
    # control through the original selector,without inventing a message number.
    control_a, control_b = [composition(rom, raw, None, flag, actor=0, state=0) for flag in (False, True)]
    assert control_a['selected_IDs'] == control_b['selected_IDs'] and len(control_a['selected_IDs']) == 1
    assert control_a['draws'][:-1] == control_b['draws'][:-1]
    cases = []
    for row in doc['records']:
        lines = layout(row['english'])
        case, plane = execute(rom, raw, row['actor_ID'], compiled(row), lines)
        assert case['complete_native_copy_macro_draw_and_ABI']
        assert all(not plane[y * 252 + x] for y in range(60, 96) for x in range(216, 252))
        missing_old = sum(bool(plane[y * 252 + x]) for y in range(60, 96) for x in range(252)
                          if x >= 144 or y >= 84)
        path = ROOT / f'ID{row["message_id"]}_complete_visible_native_ink.png'
        image = Image.frombytes('L', (252, 96), bytes(0 if p else 255 for p in plane))
        image.save(path)
        cases.append({**case, 'generated_visible_lines': lines, 'visible_source_crop': [0, 60, 216, 36],
                      'screen_rectangle': [16, 112, 232, 148], 'all_body_ink_inside_actual_parent_crop': True,
                      'ink_pixels_old144x24_crop_would_drop': missing_old,
                      'preview': str(path), 'preview_sha256': sha(path.read_bytes())})
    parities = []
    for first in (1, 2, 3, 4, 15, 16, 25, 26, 33, 34, 35, 36):
        for second in (1, 2, 15, 16, 35, 36):
            for third in (7, 8):
                lines = ['A' * first, 'B' * second, 'C' * third]
                c, plane = execute(rom, raw, 4, serialize(lines), lines)
                assert c['complete_native_copy_macro_draw_and_ABI']
                assert all(not plane[y * 252 + x] for y in range(60, 96) for x in range(216, 252))
                parities.append([first, second, third])
    sheet = Image.new('RGB', (3 * 514, 9 * 231), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, c in enumerate(cases):
        x, y = i % 3 * 514, i // 3 * 231
        draw.text((x + 5, y + 5), f'ID{c["message_id"]}: visible216x36 crop; native ink', fill='white')
        with Image.open(c['preview']) as im:
            sheet.paste(im.resize((504, 192), Image.Resampling.NEAREST), (x + 5, y + 28))
    path = ROOT / 'all25_visible_crop_native_ink_2x.png'
    sheet.save(path)
    save(ROOT / 'native_projection_and_font_proof.json', {
        'current_ROM': str(ROM), 'current_ROM_sha256': sha(ROM.read_bytes()),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'source_ARM9_sha256': sha(arm), 'proposed_parent_ARM9_sha256': sha(new),
        'exact_owned_parent_data_fields': [FIELD, FIELD + 4], 'source_values': [144, 24], 'target_values': [216, 36],
        'all_other_ARM9_bytes_and_executable_code_exact': True,
        'descriptor_incoming_reference_census': incoming, 'original_parent': old, 'proposed_parent': target,
        'other_parent_modes_unchanged': controls, 'original_assigned_captain_source_control': {'before': control_a, 'after': control_b},
        'original_paper_frame_rectangle': [4, 100, 252, 188], 'new_text_rectangle': [16, 112, 232, 148],
        'new_area_avoids_right_corner_x236_and_bottom_corner_y172': True,
        'all_frame_portrait_header_draws_destinations_palettes_unchanged': True,
        'source_canvas_and_screen_dimensions_unchanged': True,
        'all25_compiled_visible_word_and_native_font_cases': cases,
        'all144_visible_width_phase_cases': parities,
        'native_bitmap_and_CPU_geometry_proof_only_GPU_submission_intercepted': True,
        'room_actor_state_preview_and_renderer_origin_are_declared_fixture_inputs': True,
        'original_first144x24_projection_preserved_expansion_only': True,
        'remaining_other_work_caption_editorial_content_not_certified': True,
        'review_sheet': str(path), 'review_sheet_sha256': sha(path.read_bytes()), 'visual_review_pending': True,
        'actual_RGB_activity_samples_registration_ROM_patch_and_completion_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'layout_sha256': sha(Path('scripts/personal_chatter_layout_v837.py').read_bytes()), 'full_goal_complete': False})
    print('V837:original parent crop144x24 proved;216x36 expansion preserves frame/header/palette/other modes. All25 complete visible fonts and144 width-phase cases pass.',flush=True)


if __name__ == '__main__':
    main()
