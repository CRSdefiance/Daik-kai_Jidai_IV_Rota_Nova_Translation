"""Verify the revised Cheese panel and earlier exit from the Price Info modal."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_price_info_wraps_20261115 as replay
from scripts import stage_price_info_wraps_20261115 as stage
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_trade_good_descriptions_v1 import exact_title, preserved_outside_focus


base = stage.base
OUTPUT = stage.ROOT / 'gameplay_verification.json'
PAPER = (16, 296, 244, 360)
CHEESE_FOCUS = (144, 286, 172, 314)


def screen_pixels(image):
    return sha256(bytes(pixel == (0, 8, 0) for pixel in image.crop(PAPER).get_flattened_data())).hexdigest()


def main():
    assert not OUTPUT.exists()
    staged = base.load(stage.STORED)
    evidence = {str(path): base.digest(path) for path in (replay.OLD_INPUTS, replay.DONOR_PLAN, Path(__file__))}
    donor = base.load(replay.DONOR_PLAN)['source_save']
    assert base.digest(donor['source']) == donor['source_sha256']
    evidence[donor['source']] = donor['source_sha256']
    images, reports = {}, {}
    for case, key in (('parent', 'previous_sha256'), ('revised', 'candidate_sha256')):
        folder = stage.ROOT / case
        plan = folder / 'inputs.json'
        path = folder / 'capture/capture_report.json'
        report = base.load(path)
        reports[case] = report
        assert report['ROM_sha256'] == staged[key] and report['frames'] == 18201
        assert report['scripted_input_schedule'] == base.load(plan)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
        assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        assert report['battery_save_preloaded']['source_sha256'] == donor['source_sha256']
        evidence.update({str(p): base.digest(p) for p in (plan, path)})
        frames = shots(report)
        images[case] = {frame: captured(frames[frame]) for frame in replay.historical.FRAMES}
        for frame in replay.historical.FRAMES:
            evidence[frames[frame]['path']] = frames[frame]['PNG_sha256']

    old, new = images['parent'], images['revised']
    assert all(reports['parent'][key] == reports['revised'][key] for key in ('core_DLL_sha256', 'core_options'))
    assert reports['revised']['scripted_input_schedule'] == [
        row for row in reports['parent']['scripted_input_schedule'] if row['start'] != 15401]
    arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    row = next(row for row in base.load(stage.MANUSCRIPT)['records'] if row['message_id'] == 145)
    page, = row['pages']
    assert screen_pixels(new[15000]) == page['pixel_sha256']
    template = bytes.fromhex(row['staged_hex']) + b'\0'
    assert screen_pixels(old[15000]) != page['pixel_sha256']
    for case, frames, payload in (('parent', (15000, 15400), bytes.fromhex(row['exact_current_hex']) + b'\0'),
                                  ('revised', (15000,), template)):
        snaps = {s['frame']: s for s in reports[case]['read_only_capture_RAM_snapshots']}
        for frame in frames:
            snapshot = snaps[frame]
            raw = Path(snapshot['path']).read_bytes()
            assert len(raw) == 0x400000 and snapshot['read_only_export']
            assert sha256(raw).hexdigest() == snapshot['sha256']
            evidence[snapshot['path']] = snapshot['sha256']
            for addr in unpack_from('<2I', arm, 0x54890):
                offset = addr - 0x02000000
                assert raw[offset:offset + len(payload)] == payload
    title = exact_title(font, 'Cheese', new[14600])
    assert title == exact_title(font, 'Cheese', new[15400]) == exact_title(font, 'Cheese', old[15800])
    blink = preserved_outside_focus(new[14600], new[15400], CHEESE_FOCUS)
    exact_holds = [frame for frame in replay.historical.FRAMES if ImageChops.difference(old[frame], new[frame]).getbbox() is None]
    assert 13400 in exact_holds and 17000 in exact_holds and 18200 in exact_holds

    sheet = Image.new('RGB', (1060, 350), '#242a31')
    draw = ImageDraw.Draw(sheet)
    for index, (source, frame, label) in enumerate(((old, 15000, 'Previous page 1'),
            (old, 15400, 'Previous page 2'), (new, 15000, 'Revised page'),
            (new, 15400, 'Back at the list'))):
        x, y = index % 2 * 530, index // 2 * 175
        draw.text((x + 8, y + 6), label, fill='white')
        panel = source[frame].crop((0, 293, 256, 365)).resize((512, 144), Image.Resampling.NEAREST)
        sheet.paste(panel, (x + 8, y + 25))
    path = stage.ROOT / 'price_info_before_after.png'
    sheet.save(path)
    base.save(OUTPUT, dict(candidate_sha256=staged['candidate_sha256'], previous_sha256=staged['previous_sha256'],
        complete_page=page, cheese_title=title, original_list_return_cursor_blink=blink,
        parent_pages_observed=2, revised_pages_observed=1, exact_control_frames=exact_holds,
        scope='Ordinary Lisbon Market inputs using the existing copied test save.',
        hardware=False, screenshot=str(path), screenshot_sha256=base.digest(path), evidence=evidence))
    print(f'Cheese displays one complete page and returns after one advance. {len(exact_holds)} surrounding holds match.')


if __name__ == '__main__':
    main()
