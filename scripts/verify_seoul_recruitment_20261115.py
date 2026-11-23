"""Verify the full ordinary Seoul recruitment and its transition back to the Square."""

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_historical_story_wraps_20261111 as pixels
from scripts import replay_seoul_recruitment_20261115 as replay
from scripts import stage_seoul_recruitment_20261115 as stage
from scripts.checkpoint_amsterdam_square_current_20261114 import body_mask
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'gameplay_verification.json', ROOT / 'gameplay_comparison.png'
FRAMES = (*range(4750, 11551, 400), *range(12039, 12680, 320), *range(13319, 17480, 320))
RETURNS = (12999, 17799, 18119, 19079, 21319)
HEADER = {3: 'Maria Li', 10: 'Xien Yan', 12: 'Yukihisa Shiraki', 25: 'Yifa Sol'}
BODY = (16, 296, 232, 360)
SAMPLE = (18, 37, 41, 49, 101, 124, 135)


def active_run(case, sha):
    folder = ROOT / case
    paths = [folder / part for part in ('capture/capture_report.json', 'requests.json', 'terminal.json')]
    report, trace, terminal = map(base.load, paths)
    inputs, holds, end, _, donor = replay.schedule(case)
    assert report['ROM_sha256'] == terminal['ROM_sha256'] == sha and report['frames'] == end
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['scripted_input_schedule'] == inputs and not any(v for k, v in report.items() if k.startswith('synthetic_'))
    save = report['battery_save_preloaded']
    assert save['copied_byte_exact_before_cold_boot'] and save['source_sha256'] == donor['source_sha256'] == base.digest(save['source'])
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
    assert trace['source_requests'] == terminal['target_COMMON_calls']
    assert [row['message_ID'] for row in trace['source_requests'][::2]] == [341, 658, 726, 658, 658]
    assert all(row['frame'] >= 17577 for row in trace['source_requests'])
    assert all(base.digest(p) == digest for p, digest in terminal['evidence'].items())
    rows = shots(report)
    assert set(holds) <= rows.keys()
    return report, trace['source_requests'], rows, {str(p): base.digest(p) for p in paths} | terminal['evidence']


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    staged, draft = map(base.load, (stage.STORED, stage.MANUSCRIPT))
    assert base.digest(stage.ROM) == staged['candidate_sha256'] == draft['candidate_sha256']
    assert base.digest(stage.MANUSCRIPT) == staged['manuscript_sha256']
    a = active_run('parent', staged['previous_sha256'])
    b = active_run('staged', staged['candidate_sha256'])
    assert a[1] == b[1] and a[2].keys() == b[2].keys()
    assert all(a[0][k] == b[0][k] for k in ('core_DLL_sha256', 'core_options', 'scripted_input_schedule'))
    x = base.NdsImage.open(stage.ROM)
    arm, kanji = (x.read_file(p) for p in (stage.ARM, '/GRP/KANJI.FNT'))
    font = GameAsciiFont.from_arm9(arm)
    _, paint = stage.prior.precedent.planners(arm)
    evidence = a[3] | b[3]
    comparisons, shown = [], {}
    for f, row in zip(FRAMES, draft['records'], strict=True):
        n = row['source_reference']['record_index']
        before, after = [captured(run[2][f]) for run in (a, b)]
        for run in (a, b):
            image = run[2][f]
            evidence[image['path']] = image['PNG_sha256']
        expected_name = HEADER[row['source_reference']['selector']]
        try:
            headers = [complete_mask(font, expected_name, im, 16, 277, (98, 97, 98)) for im in (before, after)]
        except ValueError as error:
            raise AssertionError((f, n, expected_name)) from error
        assert headers[0] == headers[1]
        diff = ImageChops.difference(before, after)
        if row['decision'] == 'retention':
            raw = bytes.fromhex(row['current_reference']['raw_hex'])[1:]
            old, = paint(arm, kanji, stage.prior_story.expand_bytes(raw))['pages']
            pages = (old, old)
            assert diff.getbbox() is None
        else:
            pages = [side['pages'][0] for side in (row['before_native'], row['after_native'])]
            assert diff.crop(BODY).getbbox()
            diff.paste((0, 0, 0), BODY)
            diff.paste((0, 0, 0), (226, 359, 247, 380))
            assert diff.getbbox() is None, (f, n, diff.getbbox())
        for im, page in zip((before, after), pages, strict=True):
            native = pixels.prior.masks(bytes.fromhex(page['native_plane_hex']))
            actual = pixels.body_masks(im)
            assert actual == native, (f, n, list(map(len, actual)), list(map(len, native)))
        comparisons.append(dict(id=row['id'], frame=f, body_pixels_exact_both_sides=True,
            nameplate=expected_name, complete_nameplate_pixels=headers[0][0], decision=row['decision']))
        if n in SAMPLE:
            shown[n] = before, after
    assert len(comparisons) == 35 and tuple(shown) == SAMPLE
    joined = None
    for f in RETURNS:
        old, new = [captured(run[2][f]) for run in (a, b)]
        assert ImageChops.difference(old, new).getbbox() is None
        if f == 17799:
            joined = body_mask(new, font, ('Yifa Sol joined!',))
        evidence.update({run[2][f]['path']: run[2][f]['PNG_sha256'] for run in (a, b)})
    sheet = Image.new('RGB', (1024, 228 * len(shown)), '#252830')
    draw = ImageDraw.Draw(sheet)
    for i, (n, screens) in enumerate(shown.items()):
        for j, screen in enumerate(screens):
            x, y = 512 * j, 228 * i
            draw.text((x + 5, y + 3), f'B140 R{n} ' + ('before' if j == 0 else 'after'), fill='white')
            sheet.paste(screen.crop((0, 270, 256, 376)).resize((512, 212), Image.Resampling.NEAREST), (x, y + 16))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=staged['candidate_sha256'], observed_panels=comparisons,
        returned_control_frames=list(RETURNS), recruitment_notice=joined,
        original_post_event_square_requests=b[1], ordinary_saved_game_entry=True,
        hardware=False, sheet_sha256=base.digest(SHEET), evidence=evidence))
    print('Verified all 35 held panels, complete names, and five recruitment and Square transition controls.')


if __name__ == '__main__':
    main()
