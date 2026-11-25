"""Compare the ordinary Ceuta departure and both live notice buffers."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from scripts import replay_departure_numerals_20261119 as replay
from scripts import stage_departure_numerals_20261119 as stage
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, render

base = stage.base
PROOF = stage.ROOT / 'ordinary_departure_verification.json'
PAGES = {50395: (85, 'Sailing days left: about ２０.', 'Sailing days left: about 20.'),
         52875: (86, ' １/２３\n  Sky: Sunny\n  Departed Ceuta.', ' 1/23\n  Sky: Sunny\n  Departed Ceuta.')}
CROP = (16, 296, 244, 344)


def compare_pages(old, new, rom, frames, evidence):
    arm = rom.read_file(stage.ARM)
    buffers = unpack_from('<2I', arm, 0x54890)
    raster, _, _ = font_tools(rom)
    font = rom.read_file('/GRP/KANJI.FNT')
    snapshots = [{r['frame']: r for r in report[key]} for report, key in (
        (old, 'read_only_pause_RAM_snapshots'), (new, 'read_only_capture_RAM_snapshots'))]
    output = Image.new('RGB', (1024, 2 * 224), '#263238')
    draw = ImageDraw.Draw(output)
    records = []
    for row, (frame, (message, previous, current)) in enumerate(PAGES.items()):
        pair = []
        for col, (label, text) in enumerate((('Previous', previous), ('Regular digits', current))):
            shot = frames[col][frame]
            path = shot['path']
            assert base.digest(path) == shot['PNG_sha256']
            with Image.open(path) as image:
                screen = image.convert('RGB')
            pair.append(screen)
            raw = text.encode('cp932')
            snapshot = snapshots[col][frame]
            ram = Path(snapshot['path']).read_bytes()
            assert snapshot['read_only_export'] and len(ram) == snapshot['bytes'] == 0x400000
            assert base.digest(snapshot['path']) == snapshot['sha256']
            for pointer in buffers:
                at = pointer - stage.BASE
                assert ram[at:at + len(raw) + 1] == raw + b'\0', (frame, col, ram[at:at+64])
            plane, _ = render(raster, arm, font, raw)
            actual = screen.crop(CROP)
            assert bytes(px == (0, 8, 0) for px in actual.get_flattened_data()) == bytes(px == 1 for px in plane)
            x, y = 512 * col, 224 * row
            draw.text((x + 5, y + 4), f'{label}  /  COMMON {message}', fill='white')
            crop = screen.crop((0, 284, 256, 384)).resize((512, 200), Image.Resampling.NEAREST)
            output.paste(crop, (x, y + 18))
            evidence.update({path: shot['PNG_sha256'], snapshot['path']: snapshot['sha256']})
        bounds = ImageChops.difference(*pair).getbbox()
        x, y, right, lower = bounds
        assert CROP[0] <= x < right <= CROP[2] and CROP[1] <= y < lower <= CROP[1] + 12
        records.append(dict(message_ID=message, frame=frame, observed=current, current_hex=current.encode('ascii').hex(),
            previous_hex=previous.encode('cp932').hex(), exact_live_buffer_and_pixels=True, changed_pixels=bounds,
            current_capture=frames[1][frame], previous_capture=frames[0][frame]))
    path = stage.ROOT / 'departure_digit_comparison.png'
    assert not path.exists()
    output.save(path)
    sheet = dict(path=str(path), sha256=base.digest(path))
    return records, sheet


def main():
    assert not PROOF.exists()
    report = replay.CAPTURE / 'capture_report.json'
    old, new, stage_proof, inputs = map(base.load, (replay.SOURCE, report, stage.PROOF, replay.INPUT))
    assert new['ROM_sha256'] == stage_proof['candidate_sha256'] == base.digest(stage.ROM)
    assert old['ROM_sha256'] == base.load(replay.ordinary.active.RELEASE)['candidate_sha256']
    assert new['frames'] == replay.END and new['scripted_input_schedule'] == inputs
    assert inputs == [r for r in old['scripted_input_schedule'] if r['start'] + r['duration'] <= replay.END]
    for dossier in (old, new):
        assert dossier['cold_boot'] and not dossier['savestate_loaded'] and not dossier['callback_errors']
        assert not any(value for key, value in dossier.items() if key.startswith('synthetic_'))
    donors = [dossier['battery_save_preloaded'] for dossier in (old, new)]
    assert donors[0]['source_sha256'] == donors[1]['source_sha256'] == base.digest(donors[1]['source'])
    assert all(d['copied_byte_exact_before_cold_boot'] for d in donors)
    assert old['core_DLL_sha256'] == new['core_DLL_sha256'] and old['core_options'] == new['core_options']
    frames = [{r['frame']: r for r in dossier['frames_captured']} for dossier in (old, new)]
    changed = [n for n in replay.FRAMES if frames[0][n]['framebuffer_sha256'] != frames[1][n]['framebuffer_sha256']]
    assert changed == list(PAGES)
    evidence = {str(p): base.digest(p) for p in (report, replay.SOURCE, replay.INPUT, stage.PROOF, Path(__file__))}
    for frame in set(replay.FRAMES) - set(changed):
        for current in frames:
            shot = current[frame]
            assert base.digest(shot['path']) == shot['PNG_sha256']
            evidence[shot['path']] = shot['PNG_sha256']
    records, sheet = compare_pages(old, new, base.NdsImage.open(stage.ROM), frames, evidence)
    assert dict(start=52876, duration=8, buttons=['A']) in inputs
    base.save(PROOF, dict(candidate_sha256=stage_proof['candidate_sha256'], predecessor_sha256=stage_proof['predecessor_sha256'],
        comparison_capture_sha256=old['ROM_sha256'], panels=records, ordinary_existing_save=True, hardware=False,
        exact_other_frames=sorted(set(replay.FRAMES) - set(changed)), dismissal_input=52876,
        later_sailing_and_fog_frame=53165, sheets=[sheet], evidence=evidence))
    print('Both game-generated notices match the native raster. Six other held frames match pixel for pixel.')


if __name__ == '__main__':
    main()
