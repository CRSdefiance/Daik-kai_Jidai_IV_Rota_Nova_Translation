"""Match the Lisbon rumor's full live buffers and glyphs, including its return."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType

from PIL import ImageChops

from scripts import check_rafael_sail_controls_replay_20261119 as portrait_sheet
from scripts import replay_twisted_horn_rumor_20261119 as replay
from scripts import stage_twisted_horn_rumor_20261119 as stage

base = stage.base
FRAME = 56980
CROP = (16, 296, 244, 360)
PROOF = stage.ROOT / 'ordinary_lisbon_verification.json'


def verify_hold(report, frames, raw, rows, arm, font, raster, snapshot_key, evidence):
    capture = frames[FRAME]
    screen = portrait_sheet.deck.captured(capture)
    snapshot, = (s for s in report[snapshot_key] if s['frame'] == FRAME)
    data = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and len(data) == snapshot['bytes'] == 0x400000
    assert base.digest(snapshot['path']) == snapshot['sha256']
    wrapped = '\n'.join(rows).encode('ascii')
    for offset, text in ((0x5444C, raw), (0x54450, wrapped)):
        pointer = unpack_from('<I', arm, offset)[0] - 0x02000000
        assert data[pointer:pointer + len(text) + 1] == text + b'\0'
    rendered, _ = stage.golden.fleet.portrait.render_portrait(raster, arm, font, wrapped)
    pixels = screen.crop(CROP).get_flattened_data()
    assert bytes(color == (0, 8, 0) for color in pixels) == bytes(pixel == 1 for pixel in rendered)
    evidence[capture['path']] = capture['PNG_sha256']
    evidence[snapshot['path']] = snapshot['sha256']
    return screen, capture


def main():
    assert not PROOF.exists()
    manifest = replay.CAPTURE / 'capture_report.json'
    old, new, proof, inputs = map(base.load, (replay.SOURCE, manifest, stage.PROOF, replay.INPUT))
    assert proof['candidate_sha256'] == new['ROM_sha256'] == base.digest(stage.ROM)
    assert proof['predecessor_sha256'] == base.digest(stage.parent.ROM)
    assert old['ROM_sha256'] == base.digest(replay.previous.ordinary.active.ROM)
    assert new['frames'] == replay.END and new['scripted_input_schedule'] == inputs
    assert inputs == [r for r in old['scripted_input_schedule'] if r['start'] + r['duration'] <= replay.END]
    assert dict(start=56981, duration=8, buttons=['A']) in inputs
    assert dict(start=57461, duration=8, buttons=['B']) in inputs
    for record in (old, new):
        assert record['cold_boot'] and not record['savestate_loaded'] and not record['callback_errors']
        assert not any(value for key, value in record.items() if key.startswith('synthetic_'))
    assert old['core_DLL_sha256'] == new['core_DLL_sha256'] and old['core_options'] == new['core_options']
    donors = [r['battery_save_preloaded'] for r in (old, new)]
    assert all(d['copied_byte_exact_before_cold_boot'] and base.digest(d['source']) == d['source_sha256'] for d in donors)
    assert donors[0]['source_sha256'] == donors[1]['source_sha256']
    frames = [{s['frame']: s for s in r['frames_captured']} for r in (old, new)]
    changed = [n for n in replay.FRAMES if frames[0][n]['framebuffer_sha256'] != frames[1][n]['framebuffer_sha256']]
    assert changed == [FRAME], changed
    evidence = {str(p): base.digest(p) for p in (replay.SOURCE, manifest, stage.PROOF, replay.INPUT, Path(__file__))}
    unchanged = sorted(set(replay.FRAMES) - {FRAME})
    for number in unchanged:
        for capture in (r[number] for r in frames):
            assert base.digest(capture['path']) == capture['PNG_sha256']
            evidence[capture['path']] = capture['PNG_sha256']
    rom = base.NdsImage.open(stage.ROM)
    arm, font = (rom.read_file(p) for p in (stage.ARM, '/GRP/KANJI.FNT'))
    raster, _, _ = stage.golden.fleet.portrait.font_tools(rom)
    pair, holds = [], []
    for dossier, pictures, key, label, snapshot_key in (
        (old, frames[0], 'current_hex', 'Previous', 'read_only_pause_RAM_snapshots'),
        (new, frames[1], 'staged_hex', 'Revised', 'read_only_capture_RAM_snapshots'),
    ):
        rows = proof['previous_lines' if label == 'Previous' else 'revised_lines']
        image, hold = verify_hold(dossier, pictures, bytes.fromhex(proof['record'][key]), rows, arm, font,
                                  raster, snapshot_key, evidence)
        pair.append((label, image))
        holds.append(hold)
    bounds = ImageChops.difference(pair[0][1], pair[1][1]).getbbox()
    x, y, right, bottom = bounds
    assert CROP[0] <= x < right <= CROP[2] and CROP[1] <= y < bottom <= CROP[3]
    scope = vars(portrait_sheet) | {'ROOT': stage.ROOT}
    sample = FunctionType(portrait_sheet.sheet.__code__, scope)(pair)
    base.save(PROOF, dict(candidate_sha256=proof['candidate_sha256'], predecessor_sha256=proof['predecessor_sha256'],
        ordinary_gameplay=True, hardware=False, message_ID=stage.ID, held_frames=holds, changed_pixel_bounds=bounds,
        live_expanded_and_wrapped_bytes_verified=True, full_native_glyph_masks_equal=True,
        unchanged_frames=unchanged, purchase_prompt_frame=57220, item_list_frame=57460, equipped_item_frame=58660,
        sheets=[sample], evidence=evidence))
    print('Ordinary Lisbon verified the complete rumor, the next two purchase screens, and the equipped Sextant.')


if __name__ == '__main__':
    main()
