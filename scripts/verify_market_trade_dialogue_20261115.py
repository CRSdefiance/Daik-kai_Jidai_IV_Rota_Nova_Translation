"""Verify the full Investment and Palace pages and the menu transitions."""

from collections import Counter

from PIL import Image, ImageChops, ImageDraw

from scripts import replay_market_trade_dialogue_20261115 as replay
from scripts import stage_market_trade_dialogue_20261115 as stage
from scripts.verify_captain_biographies_v1 import captured, shots


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'gameplay_verification.json', ROOT / 'market_trade_replay.png'
BODY = (16, 294, 244, 360)


def read_case(mode, side, expected_sha):
    root = ROOT if side == 'after' else ROOT.with_name('market_trade_dialogue_20261115_v1')
    path = root / f'{mode}_{side}' / 'capture/capture_report.json'
    report = base.load(path)
    events, donor, history = replay.schedule(mode)
    assert report['ROM_sha256'] == expected_sha and report['frames'] == 5601
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    assert report['scripted_input_schedule'] == events
    assert report['battery_save_preloaded']['source_sha256'] == base.digest(donor) == replay.DONOR_SHA
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    rows = shots(report)
    dependencies = {str(p): base.digest(p) for p in (path, history)}
    frames = {}
    for n in replay.FRAMES:
        row = rows[n]
        dependencies[row['path']] = row['PNG_sha256']
        frames[n] = captured(row)
    return report, frames, dependencies


def make_sheet(gallery):
    sheet = Image.new('RGB', (1040, 230 * len(gallery)), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (label, before, after) in enumerate(gallery):
        for column, (side, screen) in enumerate((('Previous', before), ('Current', after))):
            x, y = column * 520 + 4, i * 230
            draw.text((x, y + 4), f'{label} {side}', fill='white')
            sheet.paste(screen.crop((0, 280, 256, 384)).resize((512, 208), Image.Resampling.NEAREST), (x, y + 18))
    sheet.save(SHEET)


def verify_mode(before, after, mode, records, render):
    assert all(before[0][k] == after[0][k] for k in ('core_options', 'core_DLL_sha256'))
    ids = [761] if mode == 'palace' else [762, 763]
    expected = {}
    for n in ids:
        case, = [case for case in records[n]['layout_cases'] if case['arguments'] in ([], ['Palace'])]
        plane = render(bytes.fromhex(case['formatted_hex']))
        expected[n] = {(16 + j % 228, 296 + j // 228) for j, ink in enumerate(plane) if ink == 1}
        assert expected[n]
    holds, controls = [], []
    for frame in after[1]:
        old, new = (run[1][frame] for run in (before, after))
        diff = ImageChops.difference(old, new).getbbox()
        pixels = {(x, y) for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2])
                  if new.getpixel((x, y)) == (0, 8, 0)}
        found = next((n for n, mask in expected.items() if pixels == mask), None)
        if found is not None:
            holds.append(dict(message_ID=found, frame=frame, complete_ink_pixels=len(pixels), changed_bounds=diff))
        if diff is None:
            controls.append(frame)
        else:
            assert found in (762, 763) and mode == 'investment', (mode, frame, diff, found)
            assert BODY[0] <= diff[0] < diff[2] <= BODY[2] and BODY[1] <= diff[1] < diff[3] <= BODY[3]
    assert holds and Counter(r['message_ID'] for r in holds).most_common(1)[0][1] >= 2
    assert (5400 in controls and 5600 in controls), (mode, controls)
    return holds, controls


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    staged, draft = map(base.load, (stage.STORED, stage.MANUSCRIPT))
    assert base.digest(stage.ROM) == staged['candidate_sha256']
    image = base.NdsImage.open(stage.ROM)
    arm, kanji = [image.read_file(path) for path in (stage.ARM, '/GRP/KANJI.FNT')]
    raster, _, _ = stage.font_tools(image)
    records = {row['message_ID']: row for row in draft['records']}
    evidence, game, gallery = {}, {}, []
    for mode in ('investment', 'palace'):
        old, new = (read_case(mode, side, staged['candidate_sha256' if side == 'after' else 'previous_sha256'])
                    for side in ('before', 'after'))
        evidence.update(old[2] | new[2])
        holds, controls = verify_mode(old, new, mode, records,
            lambda body: stage.render_portrait(raster, arm, kanji, body)[0])
        frame = holds[0]['frame']
        gallery.append((str(holds[0]['message_ID']), old[1][frame], new[1][frame]))
        game[mode] = dict(complete_holds=holds, whole_frame_controls=controls)
    make_sheet(gallery)
    live = {row['message_ID'] for row in game['investment']['complete_holds']}
    base.save(OUTPUT, dict(candidate_sha256=staged['candidate_sha256'], previous_sha256=staged['previous_sha256'],
        ordinary_saved_game=True, modes=game, offline_only_revisions=sorted(set(stage.encoded_changes()) - live),
        hardware=False, evidence=evidence, sheet_sha256=base.digest(SHEET)))
    print('Verified ordinary gameplay in the Market contract refusal and Investment transition.')


if __name__ == '__main__':
    main()
