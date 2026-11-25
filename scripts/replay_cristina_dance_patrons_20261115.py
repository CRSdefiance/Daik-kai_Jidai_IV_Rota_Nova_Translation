"""Replay the patron panels with the original scene controls on a Rafael cold boot."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import pack_into, unpack_from
import sys

from PIL import Image, ImageChops, ImageDraw

from scripts import headless_desmume_v193 as emulator
from scripts import replay_tavern_toast_startup_20261114 as boot
from scripts import stage_cristina_dance_patrons_20261115 as stage
from scripts.replay_ritual_officiant_labels_20261115 import INPUTS as RAFAEL_INPUTS
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_london_stockholm_dialogue_20261115 import BODY, native_hold


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'gameplay_verification.json', ROOT / 'gameplay_comparison.png'
FILE, HOST, FIRST, STOP = '/data/SC0.DK4', 44, 422, 776
HOLDS = tuple(range(3900, 6200, 300))
FRAMES = (2200, 2800, *HOLDS, 6550, 6900)
END = 6901


def replay(side):
    staged = base.load(stage.STORED)
    rom, expected = (stage.parent.ROM, staged['previous_sha256']) if side == 'before' else (
        stage.ROM, staged['candidate_sha256'])
    assert base.digest(rom) == expected
    image, clean = map(base.NdsImage.open, (rom, stage.CLEAN))
    archive = image.read_file(FILE)
    bank = stage.IlnkContainer.parse(archive)
    clean_host = stage.IlnkContainer.parse(clean.read_file(FILE)).blocks[HOST]
    original = bank.blocks[HOST]
    assert original[8:40] == clean_host[8:40]
    end = 8 + unpack_from('<H', original, 4)[0]
    assert original[end - 4:end] == bytes(4)
    scene = bank.blocks[stage.BLOCKS[0]]
    inventory, _, _ = stage.scoped_inventory()
    commands, _ = stage.raw_speeches(image.read_file(stage.ARM), scene, inventory)
    assert {FIRST, STOP} <= {r['offset'] for r in commands}
    excerpt = scene[FIRST:STOP]
    selected = [r for r in commands if FIRST <= r['offset'] < STOP]
    assert excerpt == b''.join(bytes.fromhex(r['whole_command_hex']) for r in selected)
    fixture = bytearray(original[:40] + excerpt + bytes(4))
    pack_into('<H', fixture, 4, len(fixture) - 8)
    bank.blocks[HOST] = bytes(fixture) + bytes(-len(fixture) % 4)
    _, shown = stage.raw_speeches(image.read_file(stage.ARM), bank.blocks[HOST], inventory)
    assert [r['selector'] for r in shown] == [5, 254, 254, 0, 5, 254, 254, 7]
    image.replace_file(FILE, bank.to_bytes())
    folder = ROOT / side
    folder.mkdir()
    target = folder / 'initialized_Rafael_RESEARCH_ONLY.nds'
    image.save(target)
    image.replace_file(FILE, archive)
    assert bytes(image.rom.save()) == rom.read_bytes()
    source = base.load(RAFAEL_INPUTS)
    schedule = [r for r in source if r['start'] <= 2200]
    schedule.extend(dict(start=n, duration=5, buttons=['A']) for n in range(4000, 6400, 300))
    inputs = folder / 'inputs.json'
    base.save(inputs, schedule)
    original_argv = sys.argv
    try:
        sys.argv = [emulator.__file__, '--rom', str(target), '--out', str(folder / 'capture'), '--frames', str(END),
                    '--inputs-json', str(inputs), '--capture-every', '999999', '--capture-at', *map(str, FRAMES)]
        emulator.main()
    finally:
        sys.argv = original_argv
    path = folder / 'capture/capture_report.json'
    report = base.load(path)
    assert report['ROM_sha256'] == base.digest(target) and report['scripted_input_schedule'] == schedule
    assert report['frames'] == END and report['cold_boot'] and not report['savestate_loaded']
    assert not report.get('battery_save_preloaded') and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    base.save(folder / 'replay.json', dict(candidate_sha256=expected, fixture_path=str(target),
        fixture_sha256=report['ROM_sha256'], report=str(path), report_sha256=base.digest(path),
        speech_raw_hex=[r['raw_hex'] for r in shown], original_excerpt_commands=selected, inverse_exact=True))


def startup():
    receipt = base.load(stage.parent.RELEASE)
    prior = Path(base.load(receipt['own_registered_startup'])['read_only_snapshot']['path']).parent.parent
    source = checked_text(getsource(boot.main), {
        '    prior = stage.parent.stage.ROOT/"startup_retry"': '    prior = PRIOR_CAPTURE',
    })
    scope = vars(boot) | dict(stage=stage, PRIOR_CAPTURE=prior)
    exec(compile(source, __file__ + '::cumulative-startup', 'exec'), scope)
    scope['main']()


def verify():
    assert not OUTPUT.exists() and not SHEET.exists()
    prior, current = [ROOT / side / 'replay.json' for side in ('before', 'after')]
    a, b = map(base.load, (prior, current))
    evidence = {str(p): base.digest(p) for p in (prior, current)}
    for row in (a, b):
        assert base.digest(row['report']) == row['report_sha256']
        assert base.digest(row['fixture_path']) == row['fixture_sha256'] and row['inverse_exact']
        evidence[row['report']] = row['report_sha256']
    old, new = (base.load(r['report']) for r in (a, b))
    assert all(old[k] == new[k] for k in ('scripted_input_schedule', 'core_DLL_sha256', 'core_options'))
    before, after = map(shots, (old, new))
    assert set(before) == set(after)
    changed = {4500: 1, 4800: 2, 6000: 5}
    image = base.NdsImage.open(stage.ROM)
    raster, _, _ = stage.font_tools(image)
    arm, kanji = (image.read_file(p) for p in (stage.ARM, '/GRP/KANJI.FNT'))
    data = base.load(stage.MANUSCRIPT)
    rows = [r for r in data['records'] if r['route'] == 0 and r['decision'] == 'revision']
    pages = {n: stage.render_portrait(raster, arm, kanji, bytes.fromhex(b['speech_raw_hex'][offset])[1:])[0]
             for n, offset in changed.items()}
    assert [stage.digest(page) for page in pages.values()] == [r['page_sha256'] for r in rows]
    observed, controls, panels = [], [], []
    for frame in FRAMES:
        first, last = (captured(shot[frame]) for shot in (before, after))
        evidence.update({shot[frame]['path']: shot[frame]['PNG_sha256'] for shot in (before, after)})
        diff = ImageChops.difference(first, last).getbbox()
        if frame in changed:
            assert diff and BODY[0] <= diff[0] < diff[2] <= BODY[2] and BODY[1] <= diff[1] < diff[3] <= BODY[3]
            ink = native_hold(last, pages[frame])
            observed.append(dict(frame=frame, body_ink_pixels=ink, changed_bounds=diff))
            panels.append((first, last))
        else:
            assert diff is None, (frame, diff)
            controls.append(frame)
    assert len(observed) == 3 and {5100, 5400, 5700, 6900} <= set(controls)
    sheet = Image.new('RGB', (1024, 230 * len(panels)), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (row, pair) in enumerate(zip(rows, panels, strict=True)):
        for j, (label, screen) in enumerate(zip(('Before', 'Revised'), pair, strict=True)):
            x, y = j * 512, i * 230
            draw.text((x + 4, y + 3), f"{row['speaker']} / {label}", fill='white')
            sheet.paste(screen.crop((0, 274, 256, 378)).resize((512, 208), Image.Resampling.NEAREST), (x, y + 18))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=b['candidate_sha256'], previous_sha256=a['candidate_sha256'],
        initialized_story=True, natural_event_activation=False, hardware=False, held_panels=observed,
        exact_control_frames=controls, sheet_sha256=base.digest(SHEET), evidence=evidence))
    print(f'Verified three Rafael patron holds and {len(controls)} unchanged frames.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('before', 'after', 'startup', 'verify'))
    case = parser.parse_args().case
    if case in ('before', 'after'):
        replay(case)
    else:
        {'startup': startup, 'verify': verify}[case]()
