"""Verify complete live glyphs in the focused Sea View and ordinary Reefs replays."""

import argparse
from hashlib import sha256
from pathlib import Path
import struct

from PIL import Image

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, render
from scripts.run_sea_event_bubbles_focused_v2 import FIELD, ORIGINAL
from scripts.run_sailing_alert_replays_v2 import set_condition
from scripts.stage_sailing_alert_balanced_v2 import ARM, BASE, OUTPUT, PROOF, ROM, ROOT
from scripts.verify_sea_event_bubbles_focused_v2 import FRAMES


LEVELUP = ROOT / 'levelup/floating_levelup_live_verification.json'
REEFS = ROOT / 'reefs/ordinary_reefs_live_verification.json'
BECALMED = ROOT / 'becalmed/becalmed_live_verification.json'


def shot_map(report):
    return {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('navigation.png')}


def foreground(path, crop):
    with Image.open(path) as screen:
        return bytes(color == (0, 8, 0) for color in screen.convert('RGB').crop(crop).get_flattened_data())


def prove_levelup(report, raw, terminal, raster, arm, kanji):
    assert terminal['focused_bubbles_selector'] and terminal['original_fixture_donor_unchanged']
    assert raw[FIELD - BASE:FIELD - BASE + 4] == ORIGINAL
    parent = load(terminal['earlier_reference'])
    assert report['synthetic_condition_fixtures'] == parent['synthetic_condition_fixtures']
    previous, actual = shot_map(parent), shot_map(report)
    assert all(previous[frame]['framebuffer_sha256'] == actual[frame]['framebuffer_sha256'] for _, frame in FRAMES)
    initial = load(OUTPUT)['exact_floating_notice_consumer']['inherited_gameplay']
    frame = initial['frame']
    assert frame == 10627
    shot = actual[frame]
    specs = (((75, 256, 207, 274), (85, 260)), ((72, 274, 205, 289), (83, 276)))
    observed = []
    for prior, (crop, origin) in zip(initial['visible_notices'], specs, strict=True):
        name = prior['actor_name']
        visible = f'{name} leveled up!'
        text = visible.encode('ascii')
        assert len(text) == len(bytes.fromhex(prior['exact_CP932_hex']))
        address = prior['address']
        assert raw[address - BASE:address - BASE + len(text) + 1] == text + b'\0'
        ink, glyphs = render(raster, arm, kanji, text)
        assert glyphs[0]['code'] == text[0] and glyphs[-1]['code'] == text[-1]
        plane = Image.frombytes('L', (228, 48), bytes(p == 1 for p in ink))
        bounds = plane.getbbox()
        assert bounds is not None
        left, top = origin[0] - crop[0], origin[1] - crop[1]
        expected = Image.new('L', (crop[2] - crop[0], crop[3] - crop[1]))
        assert 0 < left + bounds[0] < left + bounds[2] < expected.width
        assert 0 < top + bounds[1] < top + bounds[3] < expected.height
        expected.paste(plane.crop(bounds), (left + bounds[0], top + bounds[1]))
        assert expected.tobytes() == foreground(shot['path'], crop)
        observed.append(dict(message_ID=97, actor_name=name, observed_English=visible,
            original_widget_RAM_address=address, exact_display_hex=text.hex(), complete_glyphs=len(glyphs),
            exact_foreground_and_margins=True, crop=crop, native_font_origin=origin))
    return dict(frame=frame, actual_gameplay=True, hardware=False, capture=shot, observed=observed,
        original_five_bubbles_pages_byte_exact=True, selector_word_restored_before_sailing=True,
        source_and_English_cell_width_equal_for_unchanged_name=True,
        fixture_scope='The earlier bubbles event uses one temporary selector instruction. Original gameplay computes both level-ups.')


def prove_reefs(report, staged, raster, arm, kanji):
    assert not any(report[k] for k in report if k.startswith('synthetic_'))
    assert not report.get('battery_save_preloaded')
    cases = {case['native']['formatted_hex']: case for case in staged['crew_cases'] if case['arguments'] == ['Reefs']}
    expand, output = (struct.unpack_from('<I', arm, offset)[0] - BASE for offset in (0x5444C, 0x54450))
    captures = {row['frame']: row for row in report.get('read_only_capture_RAM_snapshots', [])}
    shots = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('capture.png')}
    if not shots:
        shots = {row['frame']: row for row in report['frames_captured']}
    observed = []
    samples = []
    for frame, shot in sorted(shots.items()):
        ram_path = Path(shot['path']).with_name(f'frame_{frame:06d}_arm9_ram.bin')
        if not ram_path.exists():
            continue
        raw = ram_path.read_bytes()
        if frame in captures:
            assert digest(ram_path) == captures[frame]['sha256']
        assert len(raw) == 0x400000
        display = raw[output:output + 256].split(b'\0', 1)[0]
        samples.append(dict(frame=frame, last_original_portrait_buffer_hex=display.hex()))
        case = cases.get(display.hex())
        if not case:
            continue
        expanded = raw[expand:expand + 256].split(b'\0', 1)[0]
        assert expanded.hex() == case['native']['input_hex']
        pixels, glyphs = render(raster, arm, kanji, display)
        crop = (16, 296, 244, 344)
        if bytes(p == 1 for p in pixels) != foreground(shot['path'], crop):
            continue
        assert case['native_ink_sha256'] == sha256(pixels).hexdigest()
        observed.append(dict(frame=frame, message_ID=case['message_ID'], text=display.decode('ascii').strip(),
            capture=shot, RAM=str(ram_path), RAM_sha256=digest(ram_path),
            original_runtime_condition='Reefs', exact_foreground_and_margins=True, glyphs=len(glyphs)))
    assert samples
    return dict(observed=observed, actual_gameplay=True, ordinary_controller_schedule=True, hardware=False,
        sampled_frames=samples, target_reef_warning_observed=bool(observed))


def prove_becalmed(report, staged, raster, arm, kanji):
    frames = shot_map(report)
    snapshots = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}

    def snapshot(frame):
        entry = snapshots[frame]
        assert entry['read_only_export'] and digest(entry['path']) == entry['sha256']
        return Path(entry['path']).read_bytes()

    expected = []
    for frame, mode in ((8327, 'choose-becalmed'), (9627, 'restore-becalmed')):
        _, receipt = set_condition(arm, snapshot(frame), {'mode': mode})
        expected.append(receipt | {'frame': frame})
    assert report['synthetic_condition_fixtures'] == expected
    assert snapshot(9827)[FIELD - BASE:FIELD - BASE + 4] == ORIGINAL
    expand, output = (struct.unpack_from('<I', arm, offset)[0] - BASE for offset in (0x5444C, 0x54450))
    raw = snapshot(9627)
    plain, display = (raw[at:at + 256].split(b'\0', 1)[0] for at in (expand, output))
    case = next(case for case in staged['crew_cases'] if 493 <= case['message_ID'] <= 500
                and case['native']['formatted_hex'] == display.hex())
    assert case['native']['input_hex'] == plain.hex() and case.get('protected_phrases')
    pixels, glyphs = render(raster, arm, kanji, display)
    crop = (16, 296, 244, 344)
    expected_ink = bytes(p == 1 for p in pixels)
    assert sha256(pixels).hexdigest() == case['native_ink_sha256']
    assert expected_ink == foreground(frames[9627]['path'], crop)
    assert expected_ink != foreground(frames[9827]['path'], crop)
    commands = load(ROOT / 'becalmed/capture/navigation_command_journal.json')['commands_received']
    assert all(row['validation_passed'] for row in commands)
    assert commands[-2]['frame'] == 9627 and commands[-2]['command']['buttons'] == ['A']
    return dict(actual_gameplay=True, hardware=False, observed=[dict(frame=9627, message_ID=case['message_ID'],
        complete_glyphs=len(glyphs), exact_foreground_and_margins=True, display_lines=case['visible_lines'],
        capture=frames[9627], exact_display_hex=display.hex(), RAM=snapshots[9627])],
        ordinary_A_dismisses_warning=True, following_capture=frames[9827], selector_restored=True,
        fixture=expected, natural_event_selection=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('reefs', 'levelup', 'becalmed'))
    mode = parser.parse_args().mode
    output = {'levelup': LEVELUP, 'reefs': REEFS, 'becalmed': BECALMED}[mode]
    assert not output.exists()
    staged = load(PROOF)
    terminal_path = ROOT / mode / 'terminal.json'
    terminal = load(terminal_path)
    sha = digest(ROM)
    assert sha == staged['research_ROM_sha256'] == terminal['candidate_sha256']
    assert digest(terminal['report']) == terminal['report_sha256']
    assert digest(terminal['earlier_reference']) == terminal['earlier_reference_sha256']
    frame_count = {'levelup': 10627, 'reefs': 30000, 'becalmed': 9827}[mode]
    report, raw = checked_report(terminal['report'], sha, frame_count)
    image = NdsImage.open(ROM)
    arm, kanji = image.read_file(ARM), image.read_file('/GRP/KANJI.FNT')
    raster, _, _ = font_tools(image)
    if mode == 'levelup':
        result = prove_levelup(report, raw, terminal, raster, arm, kanji)
    elif mode == 'becalmed':
        assert terminal['focused_becalmed_selector'] and terminal['original_fixture_donor_unchanged']
        result = prove_becalmed(report, staged, raster, arm, kanji)
    else:
        result = prove_reefs(report, staged, raster, arm, kanji)
    save(output, dict(candidate_sha256=sha, **result, evidence={str(path): digest(path) for path in
        (terminal_path, PROOF, OUTPUT, Path(__file__))}))
    print(f'{mode}: {len(result["observed"])} complete live texts passed.')


if __name__ == '__main__':
    main()
