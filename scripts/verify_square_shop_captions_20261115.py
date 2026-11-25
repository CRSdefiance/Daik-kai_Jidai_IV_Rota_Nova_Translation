"""Verify complete Square menu captions, original substitutions and live navigation."""

from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.category_dialogue_lookup import BASE, OUTER, TABLE
from scripts import replay_square_shop_captions_20261115 as live
from scripts import stage_square_shop_captions_20261115 as stage
from scripts.probe_button_prompt_native import call
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_category_lookup_v754 import UI_RETURNS, cpu_for, getter, string
from scripts.verify_square_caption_cells_v483 import native


base = stage.base
REPORT = stage.ROOT / 'caption_verification.json'
SHEET = stage.ROOT / 'square_shop_captions.png'
GAME_SHEET = stage.ROOT / 'lisbon_square_comparison.png'
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')


def expected_pixels(font, text):
    return {(5 * col + x, y + 1) for col, char in enumerate(text)
            for glyph in (font.decode(char),) for y in range(11) for x in range(6)
            if glyph.getpixel((x, y))}


def square_pointer(cpu, number):
    call(cpu, OUTER - BASE, (number & 0xFFFFFFFF,))
    return cpu.reg_read(UC_ARM_REG_R0)


def caption(cpu, pointer):
    scratch = 0x02455000
    cpu.mem_write(scratch, bytes(12) + b'\xA5' * 128)
    call(cpu, 0xABFCC, (scratch, BASE + stage.FORMAT_SLOT, pointer))
    assert cpu.reg_read(UC_ARM_REG_R0) == scratch + 12
    assert bytes(cpu.mem_read(scratch + 8, 4)) == b'\x01\0\0\0'
    result = bytes(cpu.mem_read(scratch + 12, 128))
    text, rest = result.split(b'\0', 1)
    assert rest == b'\xA5' * len(rest)
    return text.decode('ascii')


def audit(source, previous, target):
    old_cpu, new_cpu = map(cpu_for, (previous, target))
    font = GameAsciiFont.from_arm9(target)
    assert font.glyphs == GameAsciiFont.from_arm9(previous).glyphs
    assert source[stage.FORMAT_SLOT:stage.FORMAT_SLOT + 5] == b'%s\x93\x58\0'
    for start, end in ((TABLE, TABLE + 72), (0x5FCA0, 0x5FDE8), (0x5FC40, 0x5FC5C)):
        assert previous[start:end] == target[start:end]
    controls = []
    for return_pc in (*UI_RETURNS, 0x0205FC48):
        for ident in (*range(18), -1, -2, -3, 18, 19, 255):
            a, b = (getter(cpu, ident, return_pc) for cpu in (old_cpu, new_cpu))
            assert a == b
            if 0 <= ident < 18:
                assert string(old_cpu, a) == string(new_cpu, b)
            controls.append(dict(category=ident, original_return_pc=return_pc, exact_result=b))
    for ident in (*range(18, 256), -1, -2, -3):
        assert square_pointer(old_cpu, ident) == square_pointer(new_cpu, ident)

    sheet = Image.new('RGB', (768, 252), '#263238')
    drawing = ImageDraw.Draw(sheet)
    rows = []
    for ident, (source_text, old_name, note) in enumerate(stage.CAPTIONS):
        new_name = stage.EXPANSIONS.get(ident, old_name)
        table_entry = TABLE + 4 * ident
        clean_offset = unpack_from('<I', source, table_entry)[0] - BASE
        clean_bytes = source[clean_offset:source.index(0, clean_offset) + 1]
        assert clean_bytes == source_text.encode('cp932') + b'\0'
        old_ptr, new_ptr = (square_pointer(cpu, ident) for cpu in (old_cpu, new_cpu))
        assert string(old_cpu, old_ptr) == old_name and string(new_cpu, new_ptr) == new_name
        before, after = (caption(cpu, pointer) for cpu, pointer in ((old_cpu, old_ptr), (new_cpu, new_ptr)))
        assert (before, after) == (old_name + ' Shop', new_name + ' Shop')
        original, old_context, _ = native(previous, before)
        plane, context, _ = native(target, after)
        expected = expected_pixels(font, after)
        assert all(0 <= x < 64 and 0 <= y < 12 for x, y in expected)
        expected_old = expected_pixels(font, before)
        assert original == bytes(int((i % 64, i // 64) in expected_old) for i in range(768)), before
        assert plane == bytes(int((i % 64, i // 64) in expected) for i in range(768)), after
        if before == after:
            assert original == plane and old_context == context
        image = Image.frombytes('L', (64, 12), bytes(value * 230 for value in plane))
        x, y = (ident % 3) * 256, (ident // 3) * 42
        drawing.text((x + 4, y + 10), f'{ident:02d}', fill='white')
        sheet.paste(image.resize((192, 36), Image.Resampling.NEAREST), (x + 39, y + 3))
        rows.append(dict(id=f'SQUARE_SHOP_CAPTION_{ident}', category=ident, Japanese=source_text + '屋',
            english=after, previous=before, speaker='Square shop menu',
            context='A selectable retail shop caption assembled from the stock product category and the original shop suffix.',
            source_meaning=note, localization_note=note, decision='revision' if before != after else 'retention',
            source_reference=dict(file_path=stage.ARM, table_entry=table_entry, string_offset=clean_offset,
                                  category_hex=clean_bytes.hex(), format_offset=stage.FORMAT_SLOT,
                                  format_hex=source[stage.FORMAT_SLOT:stage.FORMAT_SLOT + 5].hex()),
            current_reference=dict(file_path=stage.ARM, table_entry=table_entry, previous_pointer=old_ptr,
                                   deployed_pointer=new_ptr, format_offset=stage.FORMAT_SLOT,
                                   previous_hex=(old_name.encode() + b'\0').hex(),
                                   deployed_hex=(new_name.encode() + b'\0').hex(),
                                   consumer=BASE + 0x5FDA8, format_hex=target[stage.FORMAT_SLOT:stage.FORMAT_SLOT + 8].hex()),
            native_display=dict(single_line=True, width=64, height=12, ink_pixels=len(expected),
                                first_and_last_glyphs_complete=True, native_plane_hex=plane.hex()),
            review=dict.fromkeys(GATES, True)))

    for long_text in ('Seasonings Shop', 'Precious Metals Shop'):
        assert max(x for x, _ in expected_pixels(font, long_text)) >= 64
    sheet.save(SHEET)
    return rows, controls


def gameplay_pair(staged, previous, focused):
    cases, evidence = [], {}
    suffix = live.TREND_SUFFIX if focused else '_ordinary'
    for side, digest in (('parent', previous), ('candidate', staged)):
        path = stage.ROOT / (side + suffix) / 'capture/capture_report.json'
        report = base.load(path)
        assert report['ROM_sha256'] == digest and report['frames'] == live.END
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not any(value for key, value in report.items()
                       if key.startswith('synthetic_') and key != 'synthetic_condition_fixtures')
        fixture = report.get('synthetic_condition_fixtures', [])
        assert len(fixture) == int(focused)
        if focused:
            snapshot, = (row for row in report['read_only_pause_RAM_snapshots'] if row['frame'] == live.PAUSE)
            assert snapshot['read_only_export'] and base.digest(snapshot['path']) == snapshot['sha256']
            rom = stage.ROM if side == 'candidate' else stage.parent.ROM
            arm = base.NdsImage.open(rom).read_file(stage.ARM)
            _, expected = live.trend(arm, (path.parent / 'frame_003720_arm9_ram.bin').read_bytes(), live.FOCUSED)
            assert fixture == [expected | {'frame': live.PAUSE}]
            evidence[snapshot['path']] = snapshot['sha256']
        assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        donor = report['battery_save_preloaded']
        assert base.digest(donor['source']) == donor['source_sha256']
        evidence[str(path)] = base.digest(path)
        cases.append(report)
    old, new = cases
    assert all(old[key] == new[key] for key in ('scripted_input_schedule', 'core_DLL_sha256', 'core_options'))
    assert old['battery_save_preloaded']['source_sha256'] == new['battery_save_preloaded']['source_sha256']
    a, b = map(shots, cases)
    return a, b, evidence


def caption_box(index):
    top = 214 + index * 32
    return (120, top, 184, top + 12)


def live_caption(font, image, index, name):
    box = caption_box(index)
    left, top, right, bottom = box
    ink = {(x - left, y - top) for y in range(top, bottom) for x in range(left, right)
           if image.getpixel((x, y)) == (230, 230, 230)}
    assert ink == expected_pixels(font, name), (name, box)
    return dict(text=name, box=box, ink_pixels=len(ink))


def gameplay(staged, previous):
    groups = {}
    evidence = {}
    font = GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.ARM))
    for focused in (False, True):
        old, new, dependencies = gameplay_pair(staged, previous, focused)
        evidence.update(dependencies)
        changes, same = [], []
        for frame in live.FRAMES:
            parent, candidate = (captured(shot[frame]) for shot in (old, new))
            assert parent.size == candidate.size == (256, 384)
            diff = ImageChops.difference(parent, candidate)
            bounds = diff.getbbox()
            if focused and frame >= 4350:
                assert bounds
                for index in (1, 2, 3):
                    diff.paste((0, 0, 0), caption_box(index))
                assert diff.getbbox() is None, (frame, diff.getbbox())
                changes.append(dict(frame=frame, bounds=bounds))
            else:
                assert bounds is None, (frame, bounds)
                same.append(frame)
            evidence.update({shot[frame]['path']: shot[frame]['PNG_sha256'] for shot in (old, new)})
        groups[focused] = (old, new, changes, same)
    _, ordinary, _, exact = groups[False]
    ordinary_labels = ('Cond. Shop', 'Treats Shop', 'Fiber Shop', 'Crafts Shop')
    holds = [live_caption(font, captured(ordinary[4750]), i, label) for i, label in enumerate(ordinary_labels)]

    old, new, changes, focused_controls = groups[True]
    before_labels = ('Cond. Shop', 'Med Shop', 'Goods Shop', 'Goods Shop')
    after_labels = ('Cond. Shop', 'Medicine Shop', 'Sundries Shop', 'Sundries Shop')
    full_holds = []
    for frame in (4750, 5550, 6350, 7150):
        for shots_by_frame, names in ((old, before_labels), (new, after_labels)):
            frame_image = captured(shots_by_frame[frame])
            full_holds.extend(dict(frame=frame, label=live_caption(font, frame_image, i, name))
                              for i, name in enumerate(names))
    comparison = Image.new('RGB', (1024, 384), '#263238')
    drawing = ImageDraw.Draw(comparison)
    for i, (name, run) in enumerate((('Previous', old), ('Revised', new))):
        x = 512 * i
        drawing.text((x + 5, 3), name + ' / Lisbon trend test', fill='white')
        excerpt = captured(run[4750]).crop((0, 194, 256, 375))
        comparison.paste(excerpt.resize((512, 362), Image.Resampling.NEAREST), (x, 19))
    comparison.save(GAME_SHEET)
    return dict(ordinary_saved_lisbon=True, exact_frames=exact, complete_live_captions=holds,
                focused_trend_fixture_fields=4, focused_changed_frames=changes, focused_control_frames=focused_controls,
                focused_full_label_masks=full_holds, hardware=False, earned_trend=False,
                sheet_sha256=base.digest(GAME_SHEET), evidence=evidence)


def main():
    staged = base.load(stage.STORED)
    assert base.digest(stage.ROM) == staged['candidate_sha256']
    assert base.digest(stage.parent.ROM) == staged['previous_sha256']
    source, previous, target = (base.NdsImage.open(path).read_file(stage.ARM)
                                for path in (stage.CLEAN, stage.parent.ROM, stage.ROM))
    rows, controls = audit(source, previous, target)
    game = gameplay(staged['candidate_sha256'], staged['previous_sha256'])
    report = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=list(GATES), candidate_sha256=staged['candidate_sha256'], records=rows, gameplay=game,
        category_getter_controls=controls, square_sentinel_controls=241,
        native_sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)))
    validate_natural_dialogue_batch(report)
    base.save(REPORT, report)
    print('Verified 18 full Square planes, 144 shared getter controls and 22 Lisbon frame pairs.')


if __name__ == '__main__':
    main()
