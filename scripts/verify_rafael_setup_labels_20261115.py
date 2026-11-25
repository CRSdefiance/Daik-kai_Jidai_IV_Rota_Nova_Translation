"""Check all date values and the earlier/later original editor frames."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import pack, unpack_from

from PIL import Image, ImageChops, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_rafael_setup_labels_20261115 as replay
from scripts import stage_rafael_setup_labels_20261115 as stage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_plaque_release_v247 import find_mask


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'setup_gameplay.json', ROOT / 'setup_gameplay.png'
NATIVE = ROOT / 'all_date_format_cases.json'
PARENT_EVIDENCE = ROOT.with_name('rafael_setup_labels_20261115_v1')
HEAD = (12, 197, 145, 214)
DATE = (86, 307, 169, 323)
MONTH = (33, 221, 145, 261)
EDIT_FIELDS = {frame: row[5] for frame, row in zip((2591, 2991, 3391, 3791, 4191), stage.HEADINGS, strict=True)}


def native_dates():
    assert not NATIVE.exists()
    source, image = map(base.NdsImage.open, (stage.CLEAN, stage.ROM))
    old, arm = (i.read_file(stage.ARM) for i in (source, image))
    staged = base.load(stage.STORED)
    assert base.digest(stage.ROM) == staged['candidate_sha256']
    assert all(old[lo:hi] == arm[lo:hi] for lo, hi in ((0x9E680, 0x9E6A0), (0xCD084, 0xCD0A0)))
    pointer, = unpack_from('<I', arm, 0x9E6F0)
    assert pointer == BASE + 0x1502BC
    font = GameAsciiFont.from_arm9(arm)
    cpu = machine(arm)
    previous = base.load(stage.parent.RELEASE)
    runtime = RegisteredRuntime(stage.parent.RELEASE, previous['own_registered_startup'], captain=3)
    cpu.mem_write(BASE, runtime.raw)
    for row in staged['fields']:
        reference = row['registered_reference']
        off, size = reference['ARM9_offset'], reference['allocation']
        assert runtime.raw[off:off + size].hex() == row['current_reference']['raw_hex']
        cpu.mem_write(BASE + off, bytes.fromhex(reference['raw_hex']))
    surface, view, context = 0x02450000, 0x02454000, STACK + 0x20
    width, height = 116, 12
    size = width * height // 2
    header = pack('<5I', 4, width // 4, height, 0x02453000 - surface, 20)
    metrics, = unpack_from('<I', arm, 0xD5088)
    cpu.mem_write(metrics + 4, pack('<2I', 6, 16))
    lengths, cases = [], []
    for month in range(1, 13):
        call(cpu, 0xCD084, (month - 1,))
        days = cpu.reg_read(UC_ARM_REG_R0)
        assert days in (28, 29, 30, 31)
        lengths.append(days)
        for day in range(1, days + 1):
            cpu.mem_write(surface - 16, b'\xA5' * 16 + header + bytes(size) + b'\xA5' * 16)
            call(cpu, 0xD3D80, (view,))
            cpu.mem_write(STACK, pack('<4I', width, height, 0, 0))
            call(cpu, 0xD3AFC, (view, surface, 0, 0))
            call(cpu, 0xD5160, (context, view, 1))
            call(cpu, 0xD5200, (context, pointer, month, day))
            raw = bytes(cpu.mem_read(surface + len(header), size))
            actual = bytes(n for packed in raw for n in (packed & 15, packed >> 4))
            assert bytes(cpu.mem_read(surface - 16, 16 + len(header))) == b'\xA5' * 16 + header
            assert bytes(cpu.mem_read(surface + len(header) + size, 16)) == b'\xA5' * 16
            text = f'{month}/{day}'
            expected = bytearray(width * height)
            for i, ch in enumerate(text):
                glyph = font.decode(ch)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected[(y+1) * width + i * 6 + x] = 1
            assert actual == expected, text
            cases.append(dict(month=month, day=day, rendered=text, pixels=sum(expected)))
    assert lengths == [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    base.save(NATIVE, dict(candidate_sha256=staged['candidate_sha256'], ARM9_sha256=stage.digest(arm),
        formatter=BASE + 0xD5200, native_calendar_month_days=lengths, cases=cases,
        supported_dates_checked=len(cases), both_printf_arguments_preserved_in_source_order=True,
        complete_native_ink_blank_fields_and_canaries=True, initialized_parent_snapshot=runtime.receipt()['snapshot']))
    print(len(cases), 'valid native date strings verified.')


def gameplay():
    assert not OUTPUT.exists() and not SHEET.exists()
    staged = base.load(stage.STORED)
    before, after = {}, {}
    traces, evidence = [], {}
    events, frames, end, _, _ = replay.schedule(None)
    arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    for dest, side, sha in ((before, 'before', staged['previous_sha256']), (after, 'after', staged['candidate_sha256'])):
        folder = (PARENT_EVIDENCE if side == 'before' else ROOT) / side
        terminal, report = map(base.load, (folder / 'terminal.json', folder / 'capture/capture_report.json'))
        assert terminal['ROM_sha256'] == report['ROM_sha256'] == sha
        assert report['cold_boot'] and not (report['savestate_loaded'] or report.get('battery_save_preloaded'))
        assert not report['callback_errors'] and report['scripted_input_schedule'] == events and report['frames'] == end
        assert all(not value for key, value in report.items() if key.startswith('synthetic_'))
        assert all(base.digest(p) == digest for p, digest in terminal['evidence'].items())
        traces.append(terminal['target_COMMON_calls'])
        evidence.update(terminal['evidence'])
        evidence[str(folder / 'terminal.json')] = base.digest(folder / 'terminal.json')
        by_frame = shots(report)
        for frame in frames:
            row = by_frame[frame]
            evidence[row['path']] = row['PNG_sha256']
            dest[frame] = captured(row)
    assert traces[0] == traces[1] and {row['message_ID'] for row in traces[1]} == {120}

    headings, calendar, dates = [], [], []
    for n, img in after.items():
        # Any shape/color changes must stay in the changed text areas. This
        # keeps untouched screen text, portraits, calendar icons, cell focus,
        # confirmation, and footer controls covered by the complete RGB check.
        compare = before[n].copy()
        for zone in (HEAD, DATE, MONTH):
            compare.paste(img.crop(zone), zone)
        assert ImageChops.difference(compare, img).getbbox() is None, n
        if n in EDIT_FIELDS:
            headings.append(dict(frame=n, **find_mask(font, EDIT_FIELDS[n].ljust(16), img, HEAD)))
        if n in (4591, 4991, 5391):
            calendar.append(dict(frame=n, **find_mask(font, 'Month', img, (34, 222, 86, 245))))
        if n in (2200, 4191, 5791, 6191, 6591):
            target = '3/5' if n <= 4191 else '4/13'
            dates.append(dict(frame=n, **find_mask(font, target.ljust(12), img, DATE)))
    assert len(headings) == 5 and len(calendar) == 3 and len(dates) == 5
    assert not obsolete_month_suffix(after, font)
    ink, bounds = complete_mask(font, 'Everything correct?', after[6191], 16, 333, (0, 8, 0))
    confirm = dict(text='Everything correct?', ink_pixels=ink, bounds=bounds)
    displayed = (2200, 2591, 2991, 3391, 3791, 4191, 4591, 4991, 5391, 5791, 6191, 6591)
    sheet = Image.new('RGB', (4 * 390, 6 * 231), '#263238')
    draw = ImageDraw.Draw(sheet)
    for n, frame in enumerate(displayed):
        for side, pick in enumerate((before, after)):
            x = (n % 2 * 2 + side) * 390
            y = n // 2 * 231
            draw.text((x + 6, y + 5), f'{frame}  {("Before", "After")[side]}', fill='white')
            panel = pick[frame].crop((0, 192, 256, 384)).resize((288, 216), Image.Resampling.NEAREST)
            sheet.paste(panel, (x + 6, y + 15))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=staged['candidate_sha256'], exact_outside_edit_regions_every_sample=True,
        input_schedule=events, heading_masks=headings, calendar_heading_masks=calendar, date_masks=dates,
        confirm_mask=confirm, common_requests=traces[1], no_legacy_SETUP_100_to_107_calls=True,
        sheet=str(SHEET), sheet_sha256=base.digest(SHEET), evidence=evidence,
        ordinary_cold_boot=True, hardware=False))
    print('All five headings, three calendar states, both dates, and confirmation passed.')


def obsolete_month_suffix(frames, font):
    for frame in (4591, 4991, 5391):
        region = (126, 242, 156, 261)
        try:
            find_mask(font, 'M', frames[frame], region)
        except ValueError:
            continue
        return True
    return False


def startup_mask(old, new):
    changed = [n for n in (1600, 2200, 3340, 4000, 16000, 31000)
               if old[n]['framebuffer_sha256'] != new[n]['framebuffer_sha256']]
    assert changed == [3340]
    before, after = captured(old[3340]), captured(new[3340])
    assert ImageChops.difference(before, after).getbbox() == (89, 309, 147, 319)
    font = GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.ARM))
    rendered = find_mask(font, '6/7'.ljust(12), after, DATE)
    return dict(frame=3340, exact_change_bounds=[89, 309, 147, 319], complete_Maria_date_mask=rendered,
                previous=old[3340], revised=new[3340])


def startup_proof():
    previous = base.load(stage.parent.RELEASE)
    receipt = base.load(previous['own_registered_startup'])
    prior = Path(receipt['read_only_snapshot']['path']).parent.parent
    oracle = replay.boot.startup.boot.startup_check
    source = checked_text(getsource(oracle.verify_startup), {
        "BIOGRAPHIES / 'own_startup/capture/capture_report.json'": "PRIOR / 'capture/capture_report.json'",
        "    assert all(old[n]['framebuffer_sha256'] == new[n]['framebuffer_sha256'] for n in frames)":
            '    date_hold = startup_mask(old, new)',
        'exact_matching_frames=[new[n] for n in frames], complete_deployed_payload_exact=True,':
            'exact_matching_frames=[new[n] for n in frames if n != 3340], date_only_hold=date_hold, complete_deployed_payload_exact=True,',
        'matched all six holds and 24 protected name getters.':
            'matched five complete holds, the changed birthday field, and 24 protected name getters.',
    })
    namespace = vars(oracle) | dict(ROOT=ROOT, BOOT=replay.STARTUP, ROM=stage.ROM, PROOF=ROOT / 'startup_input.json',
        PRIOR=prior, BIOGRAPHIES=prior.parent, startup_mask=startup_mask, __file__=__file__)
    exec(compile(source, __file__ + '::startup-birthday-mask', 'exec'), namespace)
    namespace['verify_startup']()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('check', choices=('dates', 'gameplay', 'startup'))
    checks = {'dates': native_dates, 'gameplay': gameplay, 'startup': startup_proof}
    checks[parser.parse_args().check]()
