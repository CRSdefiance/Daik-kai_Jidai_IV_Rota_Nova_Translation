"""Compare the original Istanbul Recruit Crew path on the two exact ROMs."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack_from
from subprocess import run
import sys
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from scripts import check_tavern_round_digits_20261120 as tavern
from scripts import replay_damaged_save_digits_20261120 as boot
from scripts import stage_recruit_crew_20261120 as stage
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, glyph_codes
from scripts.stage_mutiny_review_v1 import render_portrait
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_london_stockholm_dialogue_20261115 import native_hold


base, ROOT, parent = stage.base, stage.ROOT, stage.parent
HISTORY = Path('work/emulation_v193/recruitment_v773_return_v773/capture_report.json')
BEFORE_REPLAY = ROOT.with_name('recruit_crew_20261120') / 'before'
FRAMES = (3200, 4600, 5000, 5400, 5800, 6200, 6600, 7000, 7400, 7800, 8200, 8800)
PAIRED = {5000: (890, 1573), 6200: (904, 34), 6600: (1042, 51), 7000: (1042, 51)}
RESULT, SHEET = ROOT / 'gameplay.json', ROOT / 'recruit_crew_comparison.png'


def replay(side):
    staged = base.load(stage.PROOF)
    if side == 'startup':
        history = base.load(parent.STARTUP_CAPTURE)
        source = history['battery_save_preloaded']
        launch = FunctionType(boot.replay.__code__, vars(boot) | {'stage': stage})
        assert base.digest(stage.ROM) == staged['candidate_sha256']
        assert base.digest(source['source']) == source['source_sha256']
        launch(stage.ROM, history, source['source'], side)
        return

    history = base.load(HISTORY)
    source = history['battery_save_preloaded']
    assert base.digest(HISTORY) and base.digest(source['source']) == source['source_sha256']
    assert history['cold_boot'] and not history['savestate_loaded'] and not history['callback_errors']
    assert not any(v for k, v in history.items() if k.startswith('synthetic_'))
    rom = parent.stage.ROOT / 'clean_rebuilt.nds' if side == 'before' else stage.ROM
    assert base.digest(rom) == staged['parent_sha256' if side == 'before' else 'candidate_sha256']
    folder = BEFORE_REPLAY if side == 'before' else ROOT / side
    folder.mkdir()
    plan = folder / 'inputs.json'
    base.save(plan, history['scripted_input_schedule'])
    run([sys.executable, '-B', '-m', 'scripts.headless_desmume_v193', '--rom', str(rom), '--out', str(folder / 'capture'),
         '--frames', str(history['frames']), '--inputs-json', str(plan), '--battery-save', source['source'], '--press-start', '-1',
         '--capture-every', '999999', '--touchscreen', '--dump-capture-ram', '--capture-at', *map(str, FRAMES)], check=True)
    assert base.digest(source['source']) == source['source_sha256']


def verify():
    assert not RESULT.exists() and not SHEET.exists()
    staged, native, history = map(base.load, (stage.PROOF, stage.NATIVE, HISTORY))
    paths = [folder / 'capture/capture_report.json' for folder in (BEFORE_REPLAY, ROOT / 'after')]
    reports = [base.load(p) for p in paths]
    images = [base.NdsImage.open(p) for p in (parent.ROM, stage.ROM)]
    arms = [rom.read_file(stage.ARM) for rom in images]
    fonts = [rom.read_file('/GRP/KANJI.FNT') for rom in images]
    assert fonts[0] == fonts[1]
    tables = [stage.catalogue(arm, image.read_file(stage.COMMON)) for arm, image in zip(arms, images, strict=True)]
    for report, sha in zip(reports, (staged['parent_sha256'], staged['candidate_sha256']), strict=True):
        assert report['ROM_sha256'] == sha and report['cold_boot'] and not report['savestate_loaded']
        assert report['battery_save_preloaded']['source_sha256'] == history['battery_save_preloaded']['source_sha256']
        assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        assert report['frames'] == history['frames'] and report['scripted_input_schedule'] == history['scripted_input_schedule']
        assert not report['callback_errors'] and not any(v for k, v in report.items() if k.startswith('synthetic_'))
        assert report['exact_requested_capture_frames'] == list(FRAMES)

    proof = {str(p): base.digest(p) for p in (*paths, HISTORY, stage.NATIVE)}
    frames = [shots(r) for r in reports]
    pairs = []
    addresses = [unpack_from('<I', arms[1], at)[0] - stage.BASE for at in (0x5444C, 0x54450)]
    painter, _, _ = font_tools(images[1])
    sheet = Image.new('RGB', (1024, 840), '#263238')
    labels = ImageDraw.Draw(sheet)
    for n in FRAMES:
        selected = [r[n] for r in frames]
        pictures = [captured(row) for row in selected]
        difference = ImageChops.difference(*pictures).getbbox()
        proof.update({r['path']: r['PNG_sha256'] for r in selected})
        if n not in PAIRED:
            assert difference is None, (n, difference)
            continue
        assert difference and 16 <= difference[0] < difference[2] <= 244 and 295 <= difference[1] < difference[3] <= 360
        key, value = PAIRED[n]
        rows = []
        for side, (report, arm, picture) in enumerate(zip(reports, arms, pictures, strict=True)):
            snap, raw = tavern.capture_ram(report, n)
            para, wrapped = (raw[a:a+256].split(b'\0', 1)[0] for a in addresses)
            token = str(value)
            if side == 0:
                token = token.translate(str.maketrans('0123456789', '０１２３４５６７８９'))
            assert para == tables[side][key].text % token.encode('cp932'), (n, key, para)
            assert b' '.join(wrapped.split()) == para.strip()
            plane, glyphs = render_portrait(painter, arm, fonts[side], wrapped.replace(b'\r', b''))
            count = native_hold(picture, plane)
            codes = [g['code'] for g in glyphs]
            assert codes == glyph_codes(wrapped)
            assert all(c < 128 for c in codes) if side else any(c >= 128 for c in codes)
            proof[snap['path']] = snap['sha256']
            rows.append(dict(paragraph_hex=para.hex(), rendered_hex=wrapped.hex(), complete_ink=count))
            x, y = side * 512, len(pairs) * 210
            labels.text((x + 4, y + 3), f'{"Previous" if side == 0 else "Revised"} / frame {n} / {key}', fill='white')
            sheet.paste(picture.crop((0, 275, 256, 372)).resize((512, 194), Image.Resampling.NEAREST), (x, y + 15))
        pairs.append(dict(frame=n, message_ID=key, number=value, displays=rows, changes_within_body=True))
    for report, arm in zip(reports, arms, strict=True):
        for frame, expected in ((3200, 8371), (5400, 6798), (8800, 6798)):
            snap, raw = tavern.capture_ram(report, frame)
            assert tavern.wallet(arm, raw) == expected
            proof[snap['path']] = snap['sha256']
    sheet.save(SHEET)
    sheets = {r['path']: r['sha256'] for r in native['sheets']}
    sheets[str(SHEET)] = base.digest(SHEET)
    base.save(RESULT, dict(candidate_sha256=staged['candidate_sha256'], parent_sha256=staged['parent_sha256'],
        ordinary_Istanbul_recruitment=True, charge=1573, volunteers=34, spare_berths=51,
        full_recruitment_and_return_observed=True, shortfall_branch_offline_only=True, hardware=False,
        matching_control_frames=[n for n in FRAMES if n not in PAIRED], paired_pages=pairs, sheets=sheets, evidence=proof))
    print('Verified the gold quote, headcount, spare berths, actual charge and return on both ROMs.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('before', 'after', 'startup', 'verify'))
    action = parser.parse_args().action
    verify() if action == 'verify' else replay(action)
