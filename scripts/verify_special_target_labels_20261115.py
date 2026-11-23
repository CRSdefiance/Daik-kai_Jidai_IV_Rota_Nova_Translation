"""Match the original sea-inspection tooltips and their current glyphs."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R5, UC_ARM_REG_R8, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_special_target_labels_20261115 as stage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK
from scripts.record_navigation_v327 import dark_text
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_personal_gameplay_v841 import get_machine

base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'tooltip_gameplay_verification.json', ROOT / 'tooltip_comparison.png'
BOX = (88, 262, 222, 294)


def native_copy(arm, report, expected, cls):
    row = next(row for row in report['read_only_pause_RAM_snapshots'] if row['frame'] == 5700)
    raw = Path(row['path']).read_bytes()
    assert row['read_only_export'] and stage.digest(raw) == row['sha256']
    cpu, get = get_machine(arm, raw)
    fleet = get(0xCB1A8) + 4 + 39 * 132
    target = get(0x36C70, fleet + 12)
    assert target and get(0xAB128, target) == cls
    obj = get(0xABA00, target)
    label = stage.c_string(cpu, get(0x1FD74, obj), 'ascii')
    assert label['text'] == expected
    out = 0x02410040
    cpu.mem_write(out - 16, b'\xA5' * 288)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_R0, out)
    cpu.reg_write(UC_ARM_REG_R5, target)
    cpu.reg_write(UC_ARM_REG_R8, fleet)
    cpu.emu_start(BASE + 0x70424, BASE + 0x70498, count=200000)
    assert cpu.reg_read(UC_ARM_REG_PC) == BASE + 0x70498
    text = stage.c_string(cpu, out, 'ascii')
    assert text['text'] == f'Monster\n  {expected} class'
    assert bytes(cpu.mem_read(out - 16, 16)) == bytes(cpu.mem_read(out + 256, 16)) == b'\xA5' * 16
    return {'capture_RAM': row, 'original_mobile_type': cls, 'original_mobile': target,
            'class_object': obj, 'class_name': label, 'emulated_original_map_formatter': text}


def verify_label(font, im, text):
    category = dark_text(font, 'Monster', im, (92, 266, 142, 277))
    label = dark_text(font, text + ' class', im, (98, 278, 221, 289))
    assert category['bounds'] == [92, 266, 134, 277]
    assert label['bounds'] == [98, 278, 98 + 6 * len(text + ' class'), 289]
    assert category['color'] == label['color'] == (0, 8, 0)
    return [category, label]


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    info = base.load(stage.STORED)
    arms = [base.NdsImage.open(rom).read_file(stage.ARM) for rom in (stage.parent.ROM, stage.ROM)]
    assert base.digest(stage.ROM) == info['candidate_sha256']
    font = GameAsciiFont.from_arm9(arms[1])
    details, pictures, reports, evidence = {}, {}, {}, {}
    for case, text, cls, side in (('monster', 'Monster Fish', 34, 0),
                                  ('ghost_before', 'Ghost', 38, 0),
                                  ('ghost_after', 'Ghost Ship', 38, 1)):
        receipt = ROOT / (case if cls == 34 else case + '_settled') / 'terminal.json'
        terminal = base.load(receipt)
        path = Path(terminal['capture'])
        assert base.digest(path) == terminal['capture_sha256']
        report = base.load(path)
        assert report['ROM_sha256'] == terminal['candidate_sha256'] == info[('previous_sha256', 'candidate_sha256')[side]]
        final = 6300 if cls == 34 else 6750
        assert report['frames'] == final and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert terminal.get('settled_controller_schedule', False) == (cls == 38)
        fixture, = report['synthetic_condition_fixtures']
        assert terminal['fixture'] == fixture and fixture['frame'] == 4800 and fixture['all_other4MiB_bytes_exact']
        assert fixture['target_model_link_fixture'] == (cls == 38)
        assert fixture['original_class_ID'] == cls
        data = native_copy(arms[side], report, text, cls)
        pngs = shots(report)
        holds = {n: verify_label(font, captured(pngs[n]), text) for n in (5700, final)}
        details[case] = {'runtime_copy': data, 'panels': holds, 'terminal': terminal}
        pictures[case] = captured(pngs[5700])
        evidence.update({str(p): base.digest(p) for p in (path, receipt, Path(data['capture_RAM']['path']))})
        evidence.update({row['path']: row['PNG_sha256'] for row in pngs.values()})
        reports[case] = report
    a, b = (reports[case] for case in ('ghost_before', 'ghost_after'))
    assert a['scripted_input_schedule'] == b['scripted_input_schedule']
    assert a['battery_save_preloaded']['source_sha256'] == b['battery_save_preloaded']['source_sha256']
    assert a['core_DLL_sha256'] == b['core_DLL_sha256'] and a['core_options'] == b['core_options']
    assert a['synthetic_condition_fixtures'][0]['changes'] == b['synthetic_condition_fixtures'][0]['changes']
    before, after = shots(a), shots(b)
    assert before.keys() == after.keys()
    changes, exact = {}, []
    for frame in before:
        diff = ImageChops.difference(captured(before[frame]), captured(after[frame])).getbbox()
        if diff:
            assert BOX[0] <= diff[0] < diff[2] <= BOX[2] and BOX[1] <= diff[1] < diff[3] <= BOX[3], (frame, diff)
            changes[frame] = diff
        else:
            exact.append(frame)
    assert {5700, 6750} <= changes.keys()
    assert {4800, 5950, 6300} <= set(exact)
    status = dark_text(font, "You can't view that information!", captured(after[6300]), (12, 291, 250, 327))
    sheet = Image.new('RGB', (990, 146), '#263238')
    draw = ImageDraw.Draw(sheet)
    for col, (case, label) in enumerate((('monster', 'Monster Fish'), ('ghost_before', 'Ghost before'),
                                        ('ghost_after', 'Ghost Ship after'))):
        x = col * 330 + 4
        draw.text((x, 5), label, fill='white')
        crop = pictures[case].crop((87, 257, 247, 317))
        sheet.paste(crop.resize((320, 120), Image.Resampling.NEAREST), (x, 20))
    sheet.save(SHEET)
    base.save(OUTPUT, {'candidate_sha256': info['candidate_sha256'], 'cases': details, 'changed_frame_bounds': changes,
                       'identical_control_frames': exact, 'inspection_status': status,
                       'sheet_sha256': base.digest(SHEET), 'evidence': evidence,
                       'actual_selected_tooltips': True, 'disclosed_model_link_fixture': True,
                       'natural_special_target_spawn': False, 'hardware': False})
    print('Verified the complete Monster Fish and Ghost Ship labels and exact unaffected frames.')


if __name__ == '__main__':
    main()
