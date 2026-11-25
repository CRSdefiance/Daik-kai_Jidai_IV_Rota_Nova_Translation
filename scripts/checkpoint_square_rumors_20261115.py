"""Bind both displayed rumors to the actual cache and verify their full panels."""

from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from scripts import replay_square_rumors_20261115 as replay
from scripts.checkpoint_town_market_wraps_20261115 import mask
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask


base, stage = replay.base, replay.stage
OUTPUT = stage.ROOT / 'gameplay_verification.json'
SHEET = stage.ROOT / 'gameplay_lower_screens.png'
REGIONS = (0, 20)
DISPLAY, RETURN = 5900, (6050, 6150, 6250, 6400)


def snapshot(report, key, frame, evidence):
    row = next(r for r in report[key] if r['frame'] == frame)
    data = Path(row['path']).read_bytes()
    assert row['read_only_export'] and len(data) == row['bytes'] == 0x400000
    assert sha256(data).hexdigest() == row['sha256']
    evidence[row['path']] = row['sha256']
    return data


def main():
    proof, review = map(base.load, (stage.STORED, stage.MANUSCRIPT))
    assert base.digest(stage.ROM) == proof['candidate_sha256'] == review['candidate_sha256']
    image = base.NdsImage.open(stage.ROM)
    arm, raw_common = image.read_file(stage.ARM), image.read_file(stage.COMMON)
    font, blocks = GameAsciiFont.from_arm9(arm), IlnkContainer.parse(raw_common).blocks
    applied = {row['message_ID']: row for row in review['records']}
    evidence = {str(p): base.digest(p) for p in (Path(__file__), Path(replay.__file__), stage.STORED, stage.MANUSCRIPT)}
    complete, transitions = [], []
    collage = Image.new('RGB', (512, 5 * 212), 'white')
    labels = ImageDraw.Draw(collage)
    for column, region in enumerate(REGIONS):
        historical, current_input, donor = replay.history(region)
        root = stage.ROOT / f'region{region}'
        terminal_path = root / 'terminal.json'
        terminal = base.load(terminal_path)
        report_path = Path(terminal['report'])
        report = base.load(report_path)
        assert terminal['report_sha256'] == base.digest(report_path)
        assert terminal['history_sha256'] == base.digest(historical)
        assert terminal['original_save_unchanged'] and terminal['donor_sha256'] == base.digest(donor)
        assert report['ROM_sha256'] == proof['candidate_sha256'] and report['frames'] == current_input['frames']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['scripted_input_schedule'] == current_input['scripted_input_schedule']
        save = report['battery_save_preloaded']
        assert save['copied_byte_exact_before_cold_boot'] and save['source_sha256'] == base.digest(donor)
        assert not any(value for key, value in report.items() if key.startswith('synthetic_') and key != replay.FIXTURE_RECEIPT)
        used, = report[replay.FIXTURE_RECEIPT]
        before = snapshot(report, 'read_only_pause_RAM_snapshots', 5800, evidence)
        modified, expected = replay.region_fixture(region)(arm, before, True)
        assert used == expected | {'frame': 5800}
        assert sum(a != b for a, b in zip(before, modified, strict=True)) == len(used['changes']) == 5
        journal_path = report_path.with_name('navigation_command_journal.json')
        journal = base.load(journal_path)['commands_received']
        assert [row['frame'] for row in journal] == [5800, report['frames']]
        assert [row['command'] for row in journal] == [{'until': report['frames'], 'missionary_fixture': True}, {'stop': True}]
        assert all(row['validation_passed'] for row in journal)
        after = snapshot(report, 'read_only_capture_RAM_snapshots', DISPLAY, evidence)
        n = used['expected_native_rumor_message']
        row = applied[n]
        block = blocks[row['staged_reference']['block']]
        cache_at = after.find(block)
        assert cache_at >= 0 and after.find(block, cache_at + 1) < 0
        captured_frames = shots(report)
        panels = {frame: captured(captured_frames[frame]) for frame in (DISPLAY, *RETURN)}
        image_at_display = panels[DISPLAY]
        lines = row['visible_lines']
        ink = {(x, y) for x in range(16, 244) for y in range(294, 360)
               if image_at_display.getpixel((x, y)) == (0, 8, 0)}
        assert ink == mask(font, lines), n
        count, bounds = complete_mask(font, 'Shopkeeper', image_at_display, 16, 277, (98, 97, 98))
        assert count == 135
        complete.append(dict(message_ID=n, region_fixture=region, frame=DISPLAY, visible_lines=lines, complete_body_pixels=len(ink),
            complete_nameplate_pixels=count, nameplate_bounds=bounds, unique_COMMON_block_ram_address=0x02000000 + cache_at,
            COMMON_block_sha256=sha256(block).hexdigest(), fixture_bytes=len(used['changes'])))
        for i, (frame, panel) in enumerate(panels.items()):
            x, y = 256 * column, 212 * i
            labels.text((x + 5, y + 4), f'Region {region}, frame {frame}', fill='black')
            collage.paste(panel.crop((0, 192, 256, 384)), (x, y + 20))
            shot = captured_frames[frame]
            evidence[shot['path']] = shot['PNG_sha256']
            if frame in RETURN:
                transitions.append(dict(region_fixture=region, frame=frame, compared_in_readable_sheet=True,
                                        capture_sha256=shot['PNG_sha256']))
        evidence.update({str(p): base.digest(p) for p in (historical, terminal_path, report_path, journal_path)})

    if not SHEET.exists():
        collage.save(SHEET)
    with Image.open(SHEET) as recorded:
        assert ImageChops.difference(collage, recorded.convert('RGB')).getbbox() is None
    evidence[str(SHEET)] = base.digest(SHEET)
    data = dict(candidate_sha256=proof['candidate_sha256'], complete_holds=complete, transitions=transitions,
        observed_changed_keys=[709, 729], offline_only_changed_keys=sorted(set(stage.PROSE) - {709, 729}),
        actual_emulator=True, natural_regional_travel_or_selection=False, hardware=False,
        sheet_sha256=evidence[str(SHEET)], evidence=evidence)
    if OUTPUT.exists():
        assert base.load(OUTPUT) == data
    else:
        base.save(OUTPUT, data)
    print('Two complete rumor panels, two Shopkeeper nameplates, and both original cache loads verified.')


if __name__ == '__main__':
    main()
