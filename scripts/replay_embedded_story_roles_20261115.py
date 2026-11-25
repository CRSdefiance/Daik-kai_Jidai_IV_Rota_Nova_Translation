"""Replay original Hodram excerpts in an initialized opening on both ROMs."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import pack_into, unpack_from
import sys

from PIL import Image, ImageChops, ImageDraw

from scripts import headless_desmume_v193 as emulator
from scripts import replay_tavern_toast_startup_20261114 as boot
from scripts import stage_embedded_story_roles_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_london_stockholm_dialogue_20261115 import BODY, native_hold


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'gameplay_verification.json', ROOT / 'gameplay_comparison.png'
BEFORE = ROOT.with_name('embedded_story_roles_20261115_v1') / 'before'
INPUTS = Path('out/hodram_opening_wraps_20261114_v2/inputs.json')
EXCERPTS = ((86, 1280, 1548), (142, 2698, 3126))
HOST = 42
HOLDS = tuple(range(3900, 9600, 300))
FRAMES = (2200, 2800, *HOLDS, 9900, 10200)
END = 10201


def replay(side):
    staged = base.load(stage.STORED)
    rom, expected = (stage.parent.ROM, staged['previous_sha256']) if side == 'before' else (
        stage.ROM, staged['candidate_sha256'])
    assert base.digest(rom) == expected
    image, clean = map(base.NdsImage.open, (rom, stage.CLEAN))
    arm = image.read_file(stage.ARM)
    archive = image.read_file(stage.FILE)
    bank = stage.IlnkContainer.parse(archive)
    original = bank.blocks[HOST]
    clean_host = stage.IlnkContainer.parse(clean.read_file(stage.FILE)).blocks[HOST]
    end = 8 + unpack_from('<H', original, 4)[0]
    clean_end = 8 + unpack_from('<H', clean_host, 4)[0]
    footer = original[end - 6:end]
    assert footer == clean_host[clean_end - 6:clean_end] == bytes.fromhex('00c200000000')
    assert original[8:42] == clean_host[8:42]
    inventory, _, _ = stage.scoped_inventory()
    selected, refs = [], []
    for block, start, stop in EXCERPTS:
        scene = bank.blocks[block]
        commands, speeches = stage.raw_speeches(arm, scene, inventory)
        assert {start, stop} <= {r['offset'] for r in commands}
        excerpt = [c for c in commands if start <= c['offset'] < stop]
        assert all(c['word'] == 0x4000 for c in excerpt)
        assert scene[start:stop] == b''.join(bytes.fromhex(c['whole_command_hex']) for c in excerpt)
        selected.extend(excerpt)
        refs.extend([dict(block=block, **r) for r in speeches if start <= r['offset'] - 5 < stop])
    fixture = bytearray(original[:42] + b''.join(bytes.fromhex(r['whole_command_hex']) for r in selected) + footer)
    pack_into('<H', fixture, 4, len(fixture) - 8)
    bank.blocks[HOST] = bytes(fixture) + bytes(-len(fixture) % 4)
    _, shown = stage.raw_speeches(arm, bank.blocks[HOST], inventory)
    assert [r['raw_hex'] for r in shown] == [r['raw_hex'] for r in refs] and len(shown) == len(HOLDS) == 19
    image.replace_file(stage.FILE, bank.to_bytes())
    folder = BEFORE if side == 'before' else ROOT / side
    folder.mkdir()
    target = folder / 'initialized_Hodram_RESEARCH_ONLY.nds'
    image.save(target)
    image.replace_file(stage.FILE, archive)
    assert bytes(image.rom.save()) == rom.read_bytes()
    schedule = [r for r in base.load(INPUTS) if r['start'] <= 2200]
    schedule.extend(dict(start=n + 100, duration=5, buttons=['A']) for n in HOLDS)
    inputs = folder / 'inputs.json'
    base.save(inputs, schedule)
    original_argv = sys.argv
    try:
        sys.argv = [emulator.__file__, '--rom', str(target), '--out', str(folder / 'capture'), '--frames', str(END),
                    '--inputs-json', str(inputs), '--press-start', '-1', '--capture-every', '999999',
                    '--capture-at', *map(str, FRAMES)]
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
        speeches=refs, original_excerpt_commands=selected, inverse_exact=True))


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
    paths = [BEFORE / 'replay.json', ROOT / 'after/replay.json']
    a, b = map(base.load, paths)
    evidence = {str(p): base.digest(p) for p in paths}
    for row in (a, b):
        assert base.digest(row['report']) == row['report_sha256']
        assert base.digest(row['fixture_path']) == row['fixture_sha256'] and row['inverse_exact']
        evidence[row['report']] = row['report_sha256']
    old, new = (base.load(r['report']) for r in (a, b))
    assert all(old[k] == new[k] for k in ('scripted_input_schedule', 'core_DLL_sha256', 'core_options'))
    before, after = map(shots, (old, new))
    assert set(before) == set(after) and set(FRAMES) <= before.keys()
    image = base.NdsImage.open(stage.ROM)
    raster, _, _ = stage.font_tools(image)
    arm, kanji = (image.read_file(p) for p in (stage.ARM, '/GRP/KANJI.FNT'))
    draft = base.load(stage.MANUSCRIPT)
    reviewed = {(row['block'], row['current_reference']['record_index']): row
                for row in draft['records'] if row['decision'] == 'revision'}
    target = {}
    for frame, prior, current in zip(HOLDS, a['speeches'], b['speeches'], strict=True):
        key = current['block'], current['record_index']
        assert key == (prior['block'], prior['record_index'])
        if key in reviewed:
            row = reviewed[key]
            assert current['raw_hex'] == row['target_hex'] and prior['raw_hex'] == row['current_reference']['raw_hex']
            target[frame] = row
        else:
            assert current == prior
    assert len(target) == 8
    observed, controls, panels = [], [], []
    for frame in FRAMES:
        first, last = (captured(shot[frame]) for shot in (before, after))
        evidence.update({shot[frame]['path']: shot[frame]['PNG_sha256'] for shot in (before, after)})
        diff = ImageChops.difference(first, last).getbbox()
        if frame in target:
            row = target[frame]
            assert diff and BODY[0] <= diff[0] < diff[2] <= BODY[2] and BODY[1] <= diff[1] < diff[3] <= BODY[3], (frame, diff)
            planes = []
            for screen, tokenized in ((first, row['current_reference']['raw_hex']), (last, row['target_hex'])):
                body = bytes.fromhex(tokenized)[1:].replace(b'FI', b'Hodram')
                pixels, _ = stage.render_portrait(raster, arm, kanji, body)
                planes.append((stage.digest(pixels), native_hold(screen, pixels)))
            assert planes[1][0] == next(page['page_sha256'] for page in row['native_pages']
                                        if page['example'] == ('Hodram' if row['FI_offsets'] else 'stored'))
            observed.append(dict(frame=frame, id=row['id'], substitution='Hodram' if row['FI_offsets'] else None,
                                 body_ink_pixels=planes[1][1], changed_bounds=diff))
            panels.append((row['id'], first, last))
        else:
            assert diff is None, (frame, diff)
            controls.append(frame)
    sheet = Image.new('RGB', (1024, 192 * len(panels)), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (ident, first, last) in enumerate(panels):
        for j, (label, screen) in enumerate(zip(('Before', 'Revised'), (first, last), strict=True)):
            x, y = j * 512, i * 192
            draw.text((x + 4, y + 2), f'{ident} / {label}', fill='white')
            sheet.paste(screen.crop((0, 274, 256, 360)).resize((512, 172), Image.Resampling.NEAREST), (x, y + 18))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=b['candidate_sha256'], previous_sha256=a['candidate_sha256'],
        initialized_story=True, natural_event_activation=False, hardware=False, held_panels=observed,
        exact_control_frames=controls, sheet_sha256=base.digest(SHEET), evidence=evidence))
    print(f'Verified {len(observed)} complete revised holds and {len(controls)} unchanged frames.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('before', 'after', 'startup', 'verify'))
    args = parser.parse_args()
    if args.case in ('before', 'after'):
        replay(args.case)
    else:
        {'startup': startup, 'verify': verify}[args.case]()
