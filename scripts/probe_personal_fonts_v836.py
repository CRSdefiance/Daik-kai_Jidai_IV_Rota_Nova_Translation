"""Original actor/expander/bitmap/font execution with complete independent pixels."""

import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_dialogue_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.personal_chatter_layout_v836 import compiled, layout, serialize
from scripts.prepare_personal_chatter_v835 import ROM, MANUSCRIPT
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/personal_chatter_v836')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/personal_chatter_v835_Rafael_context')
BASE, VIEW, TEXT = 0x02000000, 0x0218DF2C, 0x02450000


def execute(rom, raw, actor, text, expected_lines=None):
    arm = rom.read_file('/__arm9__.bin')
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    overlays = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.rom.files[fid])
    assert list(overlays) == [0]
    overlay = overlays[0]
    assert overlay.ramAddress == 0x01FFA000 and len(overlay.data) == 6208
    cpu.mem_write(overlay.ramAddress, bytes(overlay.data))
    resource = struct.unpack('<I', cpu.mem_read(VIEW + 0x50, 4))[0]
    header = bytes(cpu.mem_read(resource, 20))
    kind, pitch, height, palette, offset = struct.unpack('<5I', header)
    assert (kind, pitch, height) == (4, 63, 96)
    pixels = (resource + offset) & 0xFFFFFFFF
    size = pitch * height * 2
    assert pixels == VIEW + 0x104 and pixels + size == resource
    prefix = bytes(cpu.mem_read(pixels - 16, 16))
    suffix = bytes(cpu.mem_read(pixels + size, 32))
    cpu.mem_write(pixels, b'\x99' * size)
    cpu.mem_write(TEXT - 16, b'\xa5' * (len(text) + 33))
    cpu.mem_write(TEXT, text + b'\0')
    events, selected, geometry, trace, returned = [], [], [], set(), []
    def observer(u, pc, instruction_size, unused):
        trace.add(pc)
        if pc == BASE + 0x5528C:
            selected.append(u.reg_read(UC_ARM_REG_R0))
            assert selected[-1] == 1361 + actor
            u.reg_write(UC_ARM_REG_R0, TEXT)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif pc == BASE + 0x154CC:
            context, pointer = u.reg_read(UC_ARM_REG_R0), u.reg_read(UC_ARM_REG_R1)
            fields = list(struct.unpack('<12I', u.mem_read(context, 48)))
            assert fields[1:5] == [0, 0, 252, 96] and fields[9:11] == [0, 60]
            assert bytes(u.mem_read(pointer, len(text) + 1)) == text + b'\0'
            geometry.append({'context_fields': fields, 'expanded_text': pointer, 'text_hex': text.hex()})
        elif pc == BASE + 0x154D0:
            returned.append(u.reg_read(UC_ARM_REG_R0) - geometry[-1]['expanded_text'])
        elif pc in (BASE + 0xD16B4, 0x01FF83AC):
            sp = u.reg_read(UC_ARM_REG_SP)
            code, style = struct.unpack('<2I', u.mem_read(sp, 8))
            events.append({'kind': 'ascii' if pc == BASE + 0xD16B4 else 'cp932',
                           'code': code, 'style': style,
                           'x': u.reg_read(UC_ARM_REG_R2), 'y': u.reg_read(UC_ARM_REG_R3),
                           **({'font_flags': struct.unpack('<I', u.mem_read(u.reg_read(UC_ARM_REG_R0) + 12, 4))[0]} if pc == 0x01FF83AC else {})})
    # Only boundary/body hooks are needed;avoid one Python callback per glyph
    # blitter instruction while still proving the exact overlay clear entry.
    points = (BASE + 0x5528C, BASE + 0x154CC, BASE + 0x154D0,
              BASE + 0xD16B4, 0x01FF83AC, 0x01FFB2DC)
    handles = [cpu.hook_add(UC_HOOK_CODE, observer, begin=p, end=p) for p in points]
    try:
        # Room-type5 is a declared header fixture,not a live actor assignment.
        # State1 executes the original activity selector in the captured context.
        call(cpu, 0x15334, (VIEW, 5, 1, actor), instruction_limit=2000000)
    finally:
        for h in handles:
            cpu.hook_del(h)
    assert selected == [1361 + actor] and len(geometry) == 1
    assert bytes(cpu.mem_read(TEXT, len(text) + 1)) == text + b'\0'
    assert bytes(cpu.mem_read(TEXT - 16, 16)) == bytes(cpu.mem_read(TEXT + len(text) + 1, 16)) == b'\xa5' * 16
    assert bytes(cpu.mem_read(pixels - 16, 16)) == prefix
    assert bytes(cpu.mem_read(pixels + size, 32)) == suffix
    assert bytes(cpu.mem_read(resource, 20)) == header and 0x01FFB2DC in trace
    actual = bytes(cpu.mem_read(pixels, size))
    expected = expected_pixels(arm, rom.read_file('/GRP/KANJI.FNT'), events, 4, background=0)
    cropped = b''.join(expected[y * 128:y * 128 + 126] for y in range(96))
    assert actual == cropped, ('independent whole canvas', actor, len(actual))
    body = [e for e in events if e['y'] >= 60]
    assert all(e['kind'] == 'ascii' and e['style'] == 15 for e in body)
    assert all(0 <= e['x'] and e['x'] + 6 <= 252 and 60 <= e['y'] and e['y'] + 11 <= 96 for e in body)
    points_by_line = {}
    for e in body:
        points_by_line.setdefault(e['y'], []).append(e)
    requests = []
    for y, row in sorted(points_by_line.items()):
        requests.append(''.join(chr(e['code']) for e in row))
    lines = [line.rstrip(' ') for line in requests]
    if expected_lines is not None:
        # Native glyph requests can include duplicate blank cells from paired
        # ASCII painting. Prove the final complete visible text independently
        # from the authored words and generated coordinates,not that trace.
        semantic_events = [e for e in events if e['y'] < 60]
        semantic_events += [dict(kind='ascii',code=ord(char),style=15,x=x*6,y=60+y*12)
                            for y,line in enumerate(expected_lines) for x,char in enumerate(line)]
        semantic = expected_pixels(arm,rom.read_file('/GRP/KANJI.FNT'),semantic_events,4,background=0)
        semantic = b''.join(semantic[y*128:y*128+126] for y in range(96))
        assert actual == semantic, ('independent complete words/coordinates',actor,expected_lines)
        lines = expected_lines
    indices = bytes(n for b in actual for n in (b & 15, b >> 4))
    return {'actor_ID': actor, 'message_id': 1361 + actor, 'text_hex': text.hex(), 'generated_native_lines': lines,
            'native_glyph_request_lines_including_trailing_blank_cells': requests,
            'native_text_bytes_consumed': returned[0], 'complete_native_copy_macro_draw_and_ABI': returned == [len(text)],
            'full252x96_native_and_independent_canvas_equal': True,
            'bitmap_and_input_guards_exact': True,
            'independent_authored_words_at_x0_12px_rows_match_every_pixel': expected_lines is not None,
            'body_origin': [0, 60], 'body_bounds': [0, 60, 252, 96],
            'overlay_sha256': sha(bytes(overlay.data)), 'font_events': events,
            'canvas_sha256': sha(actual)}, indices


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(ROM)
    assert read(ROM.with_suffix('.manifest.json'))['candidate_sha256'] == sha(ROM.read_bytes())
    report = read(CAP / 'capture_report.json')
    source_snapshot = next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame'] == 15200)
    raw = Path(source_snapshot['path']).read_bytes()
    assert source_snapshot['read_only_export'] and sha(raw) == source_snapshot['sha256']
    assert struct.unpack_from('<I', raw, VIEW - BASE)[0] == 0x021314E8
    doc = read(MANUSCRIPT)
    before = current_entries(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'))
    cases, baseline = [], []
    for row in doc['records']:
        n, actor = row['message_id'], row['actor_ID']
        old, _ = execute(rom, raw, actor, before[n].text)
        baseline.append(old)
        case, plane = execute(rom, raw, actor, compiled(row), layout(row['english']))
        assert case['complete_native_copy_macro_draw_and_ABI']
        assert case['generated_native_lines'] == layout(row['english'])
        assert ' '.join(case['generated_native_lines']) == row['english']
        image = Image.frombytes('L', (252, 96), bytes(0 if v else 255 for v in plane))
        path = ROOT / f'ID{n}_complete_native_ink_mask.png'
        image.save(path)
        case.update(preview=str(path), preview_sha256=sha(path.read_bytes()),
                    preview_is_ink_mask_only_palette_parent_GPU_and_actual_UI_not_verified=True)
        cases.append(case)
        print(n,case['generated_native_lines'],flush=True)
    boundary = []
    for text in (b'A', b'A' * 41, b'A' * 42, b'A' * 43, b'A' * 84, b'A' * 126, b'A' * 127):
        case, _ = execute(rom, raw, 4, text)
        assert case['native_text_bytes_consumed'] == min(len(text), 126)
        assert case['complete_native_copy_macro_draw_and_ABI'] == (len(text) <= 126)
        boundary.append({k: v for k, v in case.items() if k not in ('font_events',)})
    phase_cases = []
    for first in (1, 2, 3, 4, 15, 16, 25, 26, 39, 40, 41, 42):
        for second in (1, 2, 15, 16, 41, 42):
            for third in (7, 8):
                lines = ['A' * first, 'B' * second, 'C' * third]
                case, _ = execute(rom, raw, 4, serialize(lines), lines)
                assert case['complete_native_copy_macro_draw_and_ABI']
                phase_cases.append({'line_lengths': [first, second, third], 'wire_hex': serialize(lines).hex(),
                                    'all_three_complete_rows_and_letters_at_x0_match_independent_pixels': True})
    sheet = Image.new('RGB', (3 * 514, 9 * 231), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, case in enumerate(cases):
        x, y = i % 3 * 514, i // 3 * 231
        draw.text((x + 5, y + 5), f'ID{case["message_id"]}: native ink; palette/UI pending', fill='white')
        with Image.open(case['preview']) as im:
            sheet.paste(im.resize((504, 192), Image.Resampling.NEAREST), (x + 5, y + 28))
    path = ROOT / 'all25_native_ink_masks_2x.png'
    sheet.save(path)
    save(ROOT / 'native_font_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'manuscript': str(MANUSCRIPT),
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'actual_snapshot': source_snapshot,
        'cases': cases, 'all25_current_wording_baselines': baseline, 'original_native_width_height_boundaries': boundary,
        'all144_three_row_parity_and_edge_cases': phase_cases,
        'generated_pre_LF_phase_spaces_keep_complete_letters_without_visible_indent': True,
        'native_view_geometry': [252, 96], 'native_comment_rectangle': [0, 60, 252, 96],
        'original_overlay0_was_required_for_actual_bitmap_clear_and_paint': True,
        'whole_25_generated_strings_and_words_preserved': True,
        'common_lookup_is_explicit_injected_provider_after_original_ID_selection': True,
        'roomtype5_header_is_declared_native_probe_fixture_not_live_assignment': True,
        'no_ROM_or_live_RAM_change': True, 'native_font_and_wrap_scope_only_actual_UI_and_integration_pending': True,
        'review_sheet': str(path), 'review_sheet_sha256': sha(path.read_bytes()), 'visual_review_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'layout_producer_sha256': sha(Path('scripts/personal_chatter_layout_v836.py').read_bytes()),
        'full_goal_complete': False})
    print('All25 complete native/independent canvas cases and original width/height boundaries pass;visual review and actual UI pending.',flush=True)


if __name__ == '__main__':
    main()
