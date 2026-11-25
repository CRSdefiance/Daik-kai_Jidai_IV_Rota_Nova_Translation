"""Verify all five bubbles encounter panels and restore the test selectors."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from scripts import replay_bubble_portrait_wraps_20261120 as replay
from scripts import replay_bubble_portrait_anchored_20261120 as anchored
from scripts import replay_bubble_portrait_compatible_20261120 as fixture
from scripts import stage_bubble_portrait_wraps_20261120 as stage
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.verify_sea_event_bubbles_focused_v2 import FIELD, FOCUSED, ORIGINAL, RETURN


base = stage.base
PROOF, SHEET = (stage.ROOT / p for p in ('focused_gameplay.json', 'bubbles_gameplay.png'))
FRAMES = ((461, 9627), (463, 9827), (469, 10027), (470, 10227), (478, 10427))


def main():
    assert not PROOF.exists() and not SHEET.exists()
    staged = base.load(stage.PROOF)
    scope = base.load(fixture.PROOF)
    terminal_path = fixture.LIVE / 'terminal.json'
    terminal = base.load(terminal_path)
    rom_hash = base.digest(fixture.ROM)
    assert rom_hash == terminal['candidate_sha256'] == scope['candidate_sha256']
    assert base.digest(stage.ROM) == scope['staged_current_ROM_sha256'] == staged['candidate_sha256']
    assert base.digest(stage.PROOF) == scope['staged_proof_sha256']
    assert base.digest(terminal['report']) == terminal['report_sha256']
    assert base.digest(terminal['commands']) == terminal['commands_sha256']
    report, end_ram = checked_report(terminal['report'], rom_hash, RETURN)
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    assert not any(report[k] for k in report if k.startswith('synthetic_') and k != 'synthetic_condition_fixtures')
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('navigation.png')}
    saved = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}
    image = base.NdsImage.open(stage.ROM)
    arm = base.NdsImage.open(fixture.ROM).read_file(stage.ARM)
    current_arm = image.read_file(stage.ARM)

    def snapshot(frame):
        row = saved[frame]
        assert row['read_only_export'] and base.digest(row['path']) == row['sha256']
        return Path(row['path']).read_bytes()

    fixtures = []
    for frame, mode in ((8327, 'choose-bubbles'), (9627, 'restore-selection')):
        _, record = fixture.set_condition(arm, snapshot(frame), {'mode': mode})
        fixtures.append(record | {'frame': frame})
    assert report['synthetic_condition_fixtures'] == fixtures
    assert snapshot(RETURN) == end_ram
    off = FIELD - replay.prior.BASE
    assert end_ram[off:off + 4] == ORIGINAL
    assert end_ram[replay.TABLE:replay.TABLE + 32] == arm[replay.TABLE:replay.TABLE + 32]

    expand, output = (unpack_from('<I', arm, offset)[0] - replay.prior.BASE for offset in (0x5444C, 0x54450))
    crop = (16, 296, 244, 360)
    raster, _, _ = stage.font_tools(image)
    kanji = image.read_file('/GRP/KANJI.FNT')
    rows = {row['message_ID']: row for row in staged['records']}
    panels = []
    sheet = Image.new('RGB', (768, 432), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (message, frame) in enumerate((*FRAMES, (None, RETURN))):
        shot = frames[frame]
        assert base.digest(shot['path']) == shot['PNG_sha256']
        with Image.open(shot['path']) as opened:
            screen = opened.convert('RGB')
        x, y = i % 3 * 256, i // 3 * 216
        draw.text((x + 4, y + 4), f'{frame}  {message if message else "Sailing return"}', fill='white')
        sheet.paste(screen.crop((0, 192, 256, 384)), (x, y + 22))
        if message is None:
            continue
        ram = snapshot(frame)
        plain, text = (ram[at:at + 256].split(b'\0')[0] for at in (expand, output))
        row = rows[message]
        assert plain.hex() == row['staged_hex'] and text.hex() == row['display_hex'], (message, plain, text)
        assert ram[off:off + 4] == (FOCUSED if frame == 9627 else ORIGINAL)
        assert scope['exact_visible_records'][str(message)] == plain.hex()
        ink, glyphs = stage.render_portrait(raster, current_arm, kanji, text)
        pixels = screen.crop(crop)
        assert bytes(p == (0, 8, 0) for p in pixels.get_flattened_data()) == bytes(v == 1 for v in ink)
        panels.append(dict(message_ID=message, frame=frame, capture=shot, glyph_count=len(glyphs), exact_native_ink=True))
    assert frames[RETURN]['framebuffer_sha256'] != frames[FRAMES[-1][1]]['framebuffer_sha256']
    sheet.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=staged['candidate_sha256'], compatible_test_ROM_sha256=rom_hash,
        exact_glyph_panels=panels, fixtures=fixtures,
        selector_and_table_restored=True, return_to_sailing=frames[RETURN], actual_emulator=True,
        natural_random_selection=False, late_danger_variants_observed=False, hardware=False,
        sheet={'path': str(SHEET), 'sha256': base.digest(SHEET)},
        initial_unanchored_replay=str(replay.LIVE / 'capture/capture_report.json'),
        current_anchored_replay=str(anchored.LIVE / 'capture/capture_report.json'),
        evidence={str(p): base.digest(p) for p in (
            terminal_path, terminal['report'], terminal['commands'], stage.PROOF, fixture.PROOF,
            replay.LIVE / 'capture/capture_report.json', anchored.LIVE / 'capture/capture_report.json')}))
    print('Verified all five live glyph masks and the return to sailing after restoring the test inputs.')


if __name__ == '__main__':
    main()
