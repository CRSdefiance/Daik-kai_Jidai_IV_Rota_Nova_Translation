"""Verify complete relationship lettering, substitutions and the chart return."""

from pathlib import Path
from struct import pack, unpack_from

from PIL import Image, ImageChops, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R6, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_forces_relationships_20261115 as replay
from scripts import stage_forces_relationships_20261115 as stage
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.probe_button_prompt_native import STACK
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_personal_gameplay_v841 import get_machine


base = stage.base
OUTPUT = stage.ROOT / 'forces_verification.json'
SHEET = stage.ROOT / 'forces_relationships.png'
NATIVE_SHEET = stage.ROOT / 'forces_relationship_name_matrix.png'
BOX = (0, 180, 256, 192)
LIVES = (13580, 14380, 15180)
NAMES = ('Z', 'FIONA', '100% Company', 'Castor Trading Co.')
COLORS = ((0, 255, 0), (213, 64, 16), (255, 0, 255))
STYLES = (3, 4, 6)
HEADER, VIEW = 0x02450000, 0x02460000


def font_points(font, text, x, y):
    return {(x + i * 6 + px, y + py) for i, character in enumerate(text)
            for glyph in (font.decode(character),) for px in range(6) for py in range(11) if glyph.getpixel((px, py))}


def native_name_matrix(arm, raw, font):
    sheet = Image.new('RGB', (1080, 3 * 96), '#273034')
    captions = ImageDraw.Draw(sheet)
    proof = []
    for row, typ in enumerate(stage.LABELS):
        raw, _ = replay.set_relationship(arm, raw, dict(mode=typ.kind))
        for col, name in enumerate(NAMES):
            cpu, get = get_machine(arm, raw)
            pool = get(0xCB160)
            player, other = pool + 4, pool + 4 + 9 * 76
            name_pointer = get(0x3CF9C, player)
            assert 0 < len(name) <= 18
            value = name.encode('ascii') + b'\0'
            cpu.mem_write(name_pointer, value)
            width, height = 256, 192
            header = pack('<5I', 4, width // 4, height, 20, 20)
            size = width * height // 2
            cpu.mem_write(HEADER - 16, b'\xA5' * 16 + header + bytes(size) + b'\xA5' * 16)
            get(0xD3D80, VIEW)
            cpu.mem_write(STACK, pack('<4I', width, height, 0, 0))
            get(0xD3AFC, VIEW, HEADER, 0, 0)
            get(0xD5160, STACK + 0x27C, VIEW, 1)
            text = typ.english % name
            origin = width - len(text) * 6, 180
            seen = []

            def draw(u, pc, size, _):
                context = u.reg_read(UC_ARM_REG_R0)
                ptr = u.reg_read(UC_ARM_REG_R1)
                assert context == STACK + 0x27C
                assert bytes(u.mem_read(ptr, len(text) + 1)) == text.encode('ascii') + b'\0'
                assert unpack_from('<2I', u.mem_read(context + 0x24, 8)) == origin
                assert unpack_from('<I', u.mem_read(context + 0x30, 4))[0] == STYLES[row]
                seen.append(ptr)

            handle = cpu.hook_add(UC_HOOK_CODE, draw, begin=0x020D5404, end=0x020D5404)
            cpu.reg_write(UC_ARM_REG_R6, other)
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            try:
                cpu.emu_start(0x0208D2F8, 0x0208D400, count=200000)
            finally:
                cpu.hook_del(handle)
            assert len(seen) == 1
            assert cpu.reg_read(UC_ARM_REG_PC) == 0x0208D400 and cpu.reg_read(UC_ARM_REG_SP) == STACK
            assert bytes(cpu.mem_read(HEADER, 20)) == header and bytes(cpu.mem_read(name_pointer, len(value))) == value
            assert bytes(cpu.mem_read(HEADER - 16, 16)) == bytes(cpu.mem_read(HEADER + 20 + size, 16)) == b'\xA5' * 16
            pixels = bytes(n for b in cpu.mem_read(HEADER + 20, size) for n in (b & 15, b >> 4))
            expected = font_points(font, text, origin[0], origin[1] + 1)
            assert all(0 <= x < 256 and 180 <= y < 192 for x, y in expected)
            found = {(k % width, k // width) for k, v in enumerate(pixels) if v}
            assert found == expected and set(pixels) == {0, STYLES[row]}
            x, y = col * 270 + 6, row * 96
            captions.text((x, y + 4), f'{typ.kind} with {name}', fill='white')
            panel = Image.frombytes('L', (width, height), pixels).crop(BOX).point(lambda p: 240 if p else 34)
            sheet.paste(panel.resize((256, 24), Image.Resampling.NEAREST), (x, y + 25))
            proof.append(dict(kind=typ.kind, name=name, full_text=text, origin=list(origin),
                glyph_pixels=len(found), name_bytes=len(name), screen_right_edge=256,
                exact_complete_native_plane=True, unchanged_header_and_adjacent_guards=True,
                original_C_format_and_renderer=True))
    sheet.save(NATIVE_SHEET)
    return proof


def verify():
    staged = base.load(stage.STORED)
    roots = replay.ROOT / 'previous/capture', stage.ROOT / 'revised/capture'
    reports = [base.load(path / 'capture_report.json') for path in roots]
    evidence = {str(path): base.digest(path) for path in (stage.STORED, replay.REFERENCE, Path(__file__),
                 *(p / 'capture_report.json' for p in roots))}
    pre, post = reports
    assert [report['ROM_sha256'] for report in reports] == [staged['previous_sha256'], staged['candidate_sha256']]
    assert pre['scripted_input_schedule'] == post['scripted_input_schedule'] and pre['core_options'] == post['core_options']
    for report in reports:
        assert report['frames'] == 16400 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not any(value for key, value in report.items() if key.startswith('synthetic_')
                       and key != 'synthetic_condition_fixtures')
        rows = report['synthetic_condition_fixtures']
        assert [(r['frame'], r['mode']) for r in rows] == list(replay.PAUSES)
        assert [len(r['changes']) for r in rows] == [1, 1, 2, 1]
        assert [r['expected_state'] for r in rows] == [2, 3, 4, 1]
        donor = report['battery_save_preloaded']
        assert base.digest(donor['source']) == donor['source_sha256']

    ordinary_path = replay.ROOT / 'ordinary/terminal.json'
    ordinary = base.load(ordinary_path)
    assert ordinary['ROM_sha256'] == staged['previous_sha256']
    assert any(r['PC'] == 0x0208D31C and r['registers'][9] == 9 for r in ordinary['caption_calls'])
    assert not any(r['PC'] == 0x0203D7B4 for r in ordinary['caption_calls'])
    evidence[str(ordinary_path)] = base.digest(ordinary_path)
    arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    previous, revised = map(shots, reports)
    rows, equal = [], []
    sheet = Image.new('RGB', (1070, 3 * 87), '#283238')
    draw = ImageDraw.Draw(sheet)
    native_seed = None
    for frame in replay.FRAMES:
        a, b = map(captured, (previous[frame], revised[frame]))
        evidence.update({r['path']: r['PNG_sha256'] for r in (previous[frame], revised[frame])})
        diff = ImageChops.difference(a, b).getbbox()
        if frame not in LIVES:
            assert diff is None, (frame, diff)
            equal.append(frame)
        if frame not in (*LIVES, 13280, 15980):
            continue
        snapshot, = [r for r in post['read_only_capture_RAM_snapshots'] if r['frame'] == frame]
        assert snapshot['read_only_export'] and base.digest(snapshot['path']) == snapshot['sha256']
        evidence[snapshot['path']] = snapshot['sha256']
        raw = Path(snapshot['path']).read_bytes()
        if frame == 13280:
            native_seed = raw
            continue
        cpu, get = get_machine(arm, raw)
        pool = get(0xCB160)
        assert get(0x397D8, pool) == 0
        other = pool + 4 + 9 * 76
        if frame == 15980:
            assert get(0x3C858, other) == 1
            continue
        i = LIVES.index(frame)
        assert get(0x3C858, other) == i + 2
        assert bytes(cpu.mem_read(get(0x3CF9C, pool + 4), 11)) == b'Castor Co.\0'
        text = stage.LABELS[i].english % 'Castor Co.'
        assert diff and diff[1] >= 180 and diff[3] <= 192
        origin = (256 - len(text) * 6, 181)
        ink = font_mask(b, font, text, *origin, BOX, COLORS[i])
        rows.append(dict(frame=frame, format_id=stage.LABELS[i].id, original_state=i + 2,
                         exact_full_text=text, complete_glyph_pixels=ink, changed_bounds=list(diff)))
        for column, (name, image) in enumerate((('Previous', a), ('Revised', b))):
            x, y = column * 535 + 6, i * 87
            draw.text((x, y + 4), f'{name} {stage.LABELS[i].kind}', fill='white')
            sheet.paste(image.crop((0, 160, 256, 194)).resize((512, 68), Image.Resampling.NEAREST), (x, y + 19))
    market = captured(revised[16400])
    assert font_mask(market, font, 'Market Info', 95, 303, (88, 302, 167, 315), (8, 8, 8)) == 136
    assert native_seed is not None
    native = native_name_matrix(arm, native_seed, font)
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=staged['candidate_sha256'], previous_sha256=staged['previous_sha256'],
        actual_relationship_frames=rows, exact_control_frames=equal, native_name_matrix=native,
        original_return_to_market_menu=16400, fixtures_only_relationship_model_bytes=True,
        ordinary_relationship_acquisition=False, hardware=False, complete_sheet=str(SHEET),
        sheet_sha256=base.digest(SHEET), name_matrix_sheet=str(NATIVE_SHEET),
        name_matrix_sheet_sha256=base.digest(NATIVE_SHEET), evidence=evidence))
    print('Three complete gameplay labels and 12 original formatted names pass. Neutral and return controls match.')


if __name__ == '__main__':
    verify()
