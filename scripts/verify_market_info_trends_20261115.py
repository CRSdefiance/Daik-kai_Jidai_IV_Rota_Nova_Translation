"""Verify the full trend label and its ordinary no-trend control."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import observe_market_info_trends_20261115 as replay
from scripts import stage_market_info_trends_20261115 as stage
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_personal_gameplay_v841 import get_machine


base = stage.base
OUTPUT = stage.ROOT / 'market_info_verification.json'
SHEET = stage.ROOT / 'market_info_trends.png'
BOX = (78, 208, 118, 224)


def main():
    staged = base.load(stage.STORED)
    evidence = {str(path): base.digest(path) for path in (stage.STORED, replay.REFERENCE, Path(__file__))}
    head = {}
    for version, path, sha in (
        ('previous', replay.ROOT, staged['previous_sha256']),
        ('revised', stage.ROOT, staged['candidate_sha256']),
    ):
        for mode in ('control', 'trend'):
            report_path = path / mode / 'capture/capture_report.json'
            report = base.load(report_path)
            assert report['ROM_sha256'] == sha and report['cold_boot'] and not report['savestate_loaded']
            assert not report['callback_errors'] and not any(
                value for key, value in report.items()
                if key.startswith('synthetic_') and key != 'synthetic_condition_fixtures')
            expected = [row for row in base.load(replay.REFERENCE)['scripted_input_schedule'] if row['start'] <= 12301]
            if version == 'revised' and mode == 'trend':
                expected.append(dict(start=12701, duration=8, buttons=['B']))
                assert report['frames'] == 13000
            else:
                assert report['frames'] == 12600
            assert report['scripted_input_schedule'] == expected
            donor = report['battery_save_preloaded']
            assert base.digest(donor['source']) == donor['source_sha256']
            snapshots = report.get('synthetic_condition_fixtures', [])
            assert len(snapshots) == int(mode == 'trend')
            if snapshots:
                sample, = snapshots
                start = sample['municipal_product_slot']
                assert sample['frame'] == 12280 and sample['town'] == 11 and sample['goods'] == 'Olive Oil'
                assert sample['changes'] == [dict(address=start, before=125, after=14),
                    dict(address=start + 1, before=0, after=22)]
            screen = shots(report)
            head[version, mode] = report, screen
            evidence[str(report_path)] = base.digest(report_path)
            evidence.update({row['path']: row['PNG_sha256'] for row in screen.values()})

    def frame(version, mode, n):
        return captured(head[version, mode][1][n])

    prior_control = frame('previous', 'control', 12600)
    prior_trend = frame('previous', 'trend', 12600)
    revised_control = frame('revised', 'control', 12600)
    revised_trend = frame('revised', 'trend', 12600)
    assert ImageChops.difference(prior_control, revised_control).getbbox() is None
    assert all(ImageChops.difference(frame('previous', 'control', 12280), frame(v, m, 12280)).getbbox() is None
               for v, m in head)
    assert ImageChops.difference(prior_control, prior_trend).getbbox() == BOX
    assert ImageChops.difference(revised_control, revised_trend).getbbox() == BOX
    assert ImageChops.difference(prior_trend, revised_trend).getbbox() == (80, 210, 116, 222)
    arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    ink = font_mask(revised_trend, font, stage.ENGLISH, 80, 211, BOX, (230, 230, 230))
    assert ink == 74
    assert (0, 8, 0) not in revised_trend.crop(BOX).get_flattened_data()
    snap, = [row for row in head['revised', 'trend'][0]['read_only_pause_RAM_snapshots'] if row['frame'] == 12600]
    assert snap['read_only_export'] and base.digest(snap['path']) == snap['sha256']
    evidence[snap['path']] = snap['sha256']
    cpu, get = get_machine(arm, Path(snap['path']).read_bytes())
    assert get(0xB65E4) == 11
    assert get(0xB31E0, get(0xB6618), 14) == 22
    assert bytes(cpu.mem_read(0x02000000 + stage.OFFSET, stage.SLOT)) == bytes.fromhex(staged['changed_slot']['target_hex'])
    exit_screen = frame('revised', 'trend', 13000)
    assert exit_screen.crop((0, 192, 256, 384)).tobytes() != revised_trend.crop((0, 192, 256, 384)).tobytes()
    assert exit_screen.crop((35, 2, 240, 15)).tobytes() != revised_trend.crop((35, 2, 240, 15)).tobytes()
    chart = font_mask(exit_screen, font, 'Forces', 125, 371, (123, 368, 162, 382), (230, 230, 230))
    assert chart == 67
    sheet = Image.new('RGB', (930, 160), '#283238')
    draw = ImageDraw.Draw(sheet)
    for i, (caption, screen) in enumerate((('No trend', prior_control), ('Previous', prior_trend), ('Revised', revised_trend))):
        x = 310 * i
        draw.text((x + 8, 4), caption, fill='white')
        sheet.paste(screen.crop((0, 191, 128, 238)).resize((256, 94), Image.Resampling.NEAREST), (x + 8, 25))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=staged['candidate_sha256'], previous_sha256=staged['previous_sha256'],
        active_trend_actual_gameplay=True, natural_trend_acquisition=False, port_index=11,
        original_counter=22, original_product=14, fixture_scope='Two bytes in one local trend slot',
        displayed_label=stage.ENGLISH, native_screen_extent=list(BOX), complete_glyph_pixels=ink,
        complete_leading_trailing_letters=True, complete_blank_and_shadow_checks=True, native_pages=1,
        outside_heading_pixels_exact=True, no_trend_frame_pixel_identical=True, pre_report_frame_pixel_identical=True,
        B_return_to_chart_frame=13000, complete_Forces_footer_pixels=chart, hardware=False,
        sheet=str(SHEET), sheet_sha256=base.digest(SHEET), evidence=evidence))
    print('Trends has all 74 font pixels, the no-trend control is exact, and B returns to the route chart.')


if __name__ == '__main__':
    main()
