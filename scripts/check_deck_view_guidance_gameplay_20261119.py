"""Verify both Deck View help versions and unchanged Filter interaction in DeSmuME."""

from pathlib import Path
from json import loads
from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_deck_view_guidance_20261119 as replay
from scripts import stage_deck_view_guidance_20261119 as stage
from scripts.verify_deck_filter_release_v263 import ink

base = stage.base
PROOF = stage.ROOT / 'ordinary_gameplay.json'
HELP_INK = (230, 230, 230)
MENU_INK = (8, 8, 8)
# These are pauses in the recorded Lisbon navigation journal.
DECK_FRAME = 20400
MENU_FRAMES = (22064, 22032)
FRAMES = (16800, 17200, 17600, 18000, 18400, 18800, 19200, 19600, 20000, DECK_FRAME,
          20800, 21200, 21600, 22000, 22032, 22064, 22096, 22400, 22800)


def opened(shot, evidence):
    assert base.digest(shot['path']) == shot['PNG_sha256']
    evidence[shot['path']] = shot['PNG_sha256']
    with Image.open(shot['path']) as frame:
        return frame.convert('RGB')


def pixels(image, rectangle, color):
    left, top, right, bottom = rectangle
    return {(x, y) for y in range(top, bottom) for x in range(left, right) if image.getpixel((x, y)) == color}


def help_mask(image, font, rows, key):
    expected = set()
    wording = []
    for row, top in zip(rows[2:], stage.ORIGINS, strict=True):
        for n, text in enumerate(row[key].split('\n')):
            y = top + n * 16
            glyphs = ink(font, text[1:] if n else text, 0, y)
            assert all(0 <= x < 256 and 30 <= dy < 128 for x, dy in glyphs)
            expected |= glyphs
            wording.append(text.strip())
    assert len(wording) == 6 and expected == pixels(image, (0, 30, 256, 140), HELP_INK)
    return dict(complete_help_pixels=len(expected), rows=wording)


def filter_labels(image, font):
    spans = []
    for label in ('Unassigned', 'All'):
        shape = ink(font, label, 0, 0)
        left_edge = min(gx for gx, _ in shape)
        matches = []
        for y in range(270, 307):
            actual = pixels(image, (88, y, 167, y + 11), MENU_INK)
            if len(actual) != len(shape):
                continue
            x = min(px for px, _ in actual) - left_edge
            if {(px - x, py - y) for px, py in actual} == shape:
                matches.append((x, y, actual))
        (x, y, matched), = matches
        assert matched and len(matched) == len(shape)
        spans.append(dict(text=label, origin=[x, y], complete_pixels=len(matched)))
    assert spans[1]['origin'][1] - spans[0]['origin'][1] == 20
    return spans


def live_strings(report, rows, key, frame, evidence):
    shot, = (r for r in report['read_only_pause_RAM_snapshots'] if r['frame'] == frame)
    wram = Path(shot['path']).read_bytes()
    assert shot['read_only_export'] and len(wram) == shot['bytes'] == 0x400000
    assert base.digest(shot['path']) == shot['sha256']
    evidence[shot['path']] = shot['sha256']
    for row in rows:
        at = row['target_pointer'] - stage.BASE
        wanted = row[key].encode('ascii') + b'\0'
        assert unpack_from('<I', wram, row['field'])[0] == row['target_pointer']
        assert wram[at:at + len(wanted)] == wanted


def main():
    assert not PROOF.exists()
    directories = [replay.LISBON_ROOT / name for name in ('parent', 'revised')]
    paths = [folder / 'capture/capture_report.json' for folder in directories]
    reports = [base.load(p) for p in paths]
    stored = base.load(stage.PROOF)
    original = base.load(replay.LISBON)
    prefix = original['scripted_input_schedule']
    commands = [loads(line) for line in replay.JOURNAL.read_text(encoding='utf-8').splitlines()]
    assert commands[-1] == {'stop': True}
    candidates = [stage.parent.ROM, stage.ROM]
    hashes = [stored['predecessor_sha256'], stored['candidate_sha256']]
    for report, root, candidate, sha in zip(reports, directories, candidates, hashes, strict=True):
        assert base.digest(candidate) == report['ROM_sha256'] == sha and report['frames'] == FRAMES[-1]
        assert report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and not any(v for k, v in report.items() if k.startswith('synthetic_'))
        donor = report['battery_save_preloaded']
        assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
        assert original['battery_save_preloaded']['source_sha256'] == donor['source_sha256']
        assert prefix == base.load(root / 'inputs.json')
        journal = base.load(root / 'capture/navigation_command_journal.json')
        assert journal['ROM_sha256'] == sha and journal['last_command_frame'] == FRAMES[-1]
        recorded = journal['commands_received']
        assert [r['command'] for r in recorded] == commands and all(r['validation_passed'] for r in recorded)
        tail = []
        for entry in recorded[:-1]:
            cmd = entry['command']
            if cmd.get('buttons') or cmd.get('touch'):
                add = dict(start=entry['frame']+1, duration=cmd['duration'], buttons=cmd['buttons'])
                if 'touch' in cmd:
                    add['touch'] = cmd['touch']
                tail.append(add)
        assert report['scripted_input_schedule'] == prefix + tail
    assert reports[0]['core_options'] == reports[1]['core_options'] and reports[0]['core_DLL_sha256'] == reports[1]['core_DLL_sha256']
    evidence = {str(p): base.digest(p) for p in (*paths, replay.LISBON, replay.JOURNAL, stage.PROOF, Path(__file__),
        *(folder/'capture/navigation_command_journal.json' for folder in directories))}
    by_frame = [{r['frame']: r for r in record['frames_captured'] if r['path'].endswith('_navigation.png')} for record in reports]
    shots = [[opened(report[n], evidence) for n in FRAMES] for report in by_frame]
    before, after = ({n: img for n, img in zip(FRAMES, pair, strict=True)} for pair in shots)
    changed = {}
    for n in FRAMES:
        bounds = ImageChops.difference(before[n], after[n]).getbbox()
        if bounds:
            assert 0 <= bounds[0] < bounds[2] <= 256 and 49 <= bounds[1] < bounds[3] <= 128
            changed[n] = bounds
    assert all(n in changed for n in (DECK_FRAME, *MENU_FRAMES))
    font = GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.ARM))
    rows = stored['records']
    old_help = help_mask(before[DECK_FRAME], font, rows, 'current_Compiled')
    new_help = help_mask(after[DECK_FRAME], font, rows, 'compiled')
    labels = []
    for selected, n in enumerate(MENU_FRAMES):
        assert help_mask(after[n], font, rows, 'compiled') == new_help
        options = filter_labels(after[n], font)
        assert filter_labels(before[n], font) == options
        for index, option in enumerate(options):
            x, y = option['origin']
            color = (0, 165, 172) if index == selected else (205, 198, 180)
            assert after[n].getpixel((x, y - 2)) == color
        labels.append(dict(frame=n, options=options, highlighted=options[selected]['text']))
    assert reports[0]['scripted_input_schedule'][-2:] == [dict(start=22097, duration=8, buttons=['A']),
        dict(start=22401, duration=8, buttons=['B'])]
    assert help_mask(after[22800], font, rows, 'compiled') == new_help
    for report, key in zip(reports, ('current_Compiled', 'compiled'), strict=True):
        live_strings(report, rows, key, MENU_FRAMES[0], evidence)

    comparison = Image.new('RGB', (1024, 496), '#263238')
    text = ImageDraw.Draw(comparison)
    for col, (label, image) in enumerate((('Previous', before[DECK_FRAME]), ('Revised', after[DECK_FRAME]))):
        x = col * 512
        text.text((x + 5, 4), label, fill='white')
        comparison.paste(image.crop((0, 0, 256, 128)).resize((512, 256), Image.Resampling.NEAREST), (x, 20))
    for col, n in enumerate(MENU_FRAMES):
        x = col * 512
        text.text((x + 5, 283), ('Filter / Unassigned', 'Filter / All')[col], fill='white')
        comparison.paste(after[n].crop((0, 252, 256, 348)).resize((512, 192), Image.Resampling.NEAREST), (x, 300))
    path = stage.ROOT / 'deck_help_gameplay.png'
    comparison.save(path)
    base.save(PROOF, dict(candidate_sha256=hashes[1], predecessor_sha256=hashes[0], ordinary_existing_save=True, hardware=False,
        previous_help=old_help, revised_help=new_help, filter_labels=labels, held_changed_frames=changed,
        unrelated_pixels_and_filter_transitions_preserved=True, exact_live_strings=True,
        sheets=[dict(path=str(path), sha256=base.digest(path))], evidence=evidence))
    print('Ordinary Deck View verified all six revised rows and both complete Filter labels.')


if __name__ == '__main__':
    main()
