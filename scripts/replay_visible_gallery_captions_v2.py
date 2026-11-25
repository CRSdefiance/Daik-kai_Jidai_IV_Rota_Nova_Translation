"""Verify all four Gallery routes and add a focused Maria wrap for the moved captions."""

import argparse
from inspect import getsource
from types import FunctionType

from PIL import Image, ImageChops

from scripts import replay_visible_gallery_captions_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, stage, review = prior.base, prior.stage, prior.review
ROOT, ROM = stage.ROOT, stage.ROM
LIVE = ROOT / 'gallery_caption_gameplay_verification_v2.json'
FOUR_ROUTES = ROOT / 'gallery_four_route_comparison.json'
OLD_ORIGIN, ORIGIN = 262, 263


def caption(font, text, image):
    x0 = 128 - len(text) * 5 // 2
    expected = {(x0 + i*5 + x, ORIGIN+y) for i, char in enumerate(text) for x in range(6) for y in range(11)
                if font.decode(char).getpixel((x, y))}
    actual = {(x, y) for x in range(32, 224) for y in range(261, 277)
              if image.getpixel((x, y)) == (230, 230, 230)}
    assert expected == actual, text
    return dict(English=text, origin=[x0, ORIGIN], complete_ink_pixels=len(expected),
                bounds=[x0, ORIGIN, x0 + (len(text)-1)*5+6, ORIGIN+11])


def observed_schedule():
    inputs, frames, end, selected, donor = prior.schedule()
    # The prepared Gallery state enters Maria at position 1, as observed in
    # the current complete frame. The retained direction events are unchanged.
    current = {frame: (route, (index+1) % 38 if route == 3 else index)
               for frame, (route, index) in selected.items()}
    return inputs, frames, end, current, donor


def four_routes():
    source = checked_text(getsource(prior.compare), {
        "262 <= delta[1] < delta[3] <= 273": "263 <= delta[1] < delta[3] <= 274",
        "len(selected) == 10 and len(revised) == 7": "len(selected) == 10 and len(revised) == 5",
        'Ten original Gallery positions and seven revised captions matched; arrows and return screens are exact.':
            'Ten original Gallery positions and five revised captions matched; arrows and return screens are exact.',
    })
    env = vars(prior) | dict(schedule=observed_schedule, compact_caption=caption, LIVE=FOUR_ROUTES, __file__=__file__)
    exec(compile(source, __file__ + '::observed-start-positions-and-current-font', 'exec'), env)
    env['compare']()


def maria_schedule():
    old = base.load(prior.OLD_REPORT)
    events = list(old['scripted_input_schedule'][:5])
    events.extend((dict(start=2801, duration=8, buttons=[], touch=[170, 130]),
                   dict(start=3001, duration=8, buttons=['A'])))
    events.extend(dict(start=3201 + 200*i, duration=8, buttons=['LEFT']) for i in range(7))
    events.extend(dict(start=n, duration=8, buttons=['B']) for n in (4801, 5201, 5601))
    return events, [2400, 2800, *range(3200, 4800, 200), 5200, 5600, 6000], 6000, {}, old['battery_save_preloaded']


def capture_maria(side):
    source = checked_text(getsource(prior.capture), {
        "ROOT / f'gallery_{side}'": "ROOT / f'maria_{side}'",
    })
    env = vars(prior) | dict(schedule=maria_schedule, __file__=__file__)
    exec(compile(source, __file__ + '::ordinary-Maria-wrap', 'exec'), env)
    env['capture'](side)


def compare_maria():
    prior_evidence = base.load(FOUR_ROUTES)
    proof = base.load(stage.PROOF)
    assert prior_evidence['candidate_sha256'] == proof['candidate_sha256'] == base.digest(ROM)
    assert prior_evidence['parent_sha256'] == proof['parent_sha256']
    events, frames, end, _, donor = maria_schedule()
    runs, evidence = [], []
    for side, digest in (('parent', proof['parent_sha256']), ('revised', proof['candidate_sha256'])):
        folder = ROOT / f'maria_{side}'
        receipt_path = folder / 'terminal.json'
        report_path = folder / 'capture/capture_report.json'
        receipt, report = map(base.load, (receipt_path, report_path))
        assert base.digest(report_path) == receipt['report_sha256']
        assert receipt['candidate_sha256'] == report['ROM_sha256'] == digest
        assert report['frames'] == end and report['scripted_input_schedule'] == events
        assert receipt['original_donor_sha256'] == donor['source_sha256']
        cases = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_cold_boot.png')}
        assert set(frames) <= cases.keys()
        runs.append(cases)
        evidence.extend((receipt_path, report_path))
    draft = [row for row in base.load(review.OUTPUT)['records'] if row['route'] == 3]
    font = stage.GameAsciiFont.from_arm9(base.NdsImage.open(ROM).read_file(stage.ARM))
    matches, revisions, exact = [], [], []
    for frame in frames:
        pics = [run[frame] for run in runs]
        assert all(base.digest(p['path']) == p['PNG_sha256'] for p in pics)
        a, b = [Image.open(p['path']).convert('RGB') for p in pics]
        delta = ImageChops.difference(a, b).getbbox()
        if 3200 <= frame < 4800:
            possible = []
            for row in draft:
                try:
                    old = caption(font, row['current_English'], a)
                except AssertionError:
                    continue
                possible.append((row, old))
            assert len(possible) == 1
            row, old = possible[0]
            new = caption(font, row['english'], b)
            matches.append(dict(id=row['id'], frame=frame, original_image=row['original_scene_image'],
                                before=old, after=new, changed_rectangle=delta))
            if row['decision'] == 'revision':
                assert delta and 32 <= delta[0] < delta[2] <= 224 and 263 <= delta[1] < delta[3] <= 274
                revisions.append(row['id'])
                continue
        assert not delta and pics[0]['framebuffer_sha256'] == pics[1]['framebuffer_sha256']
        exact.append(frame)
    assert set(revisions) == {'SCENE_CAPTION_ROUTE_3_33', 'SCENE_CAPTION_ROUTE_3_37'}
    base.save(LIVE, prior_evidence | dict(selected_captions=prior_evidence['selected_captions'] + matches,
        observed_revision_ids=prior_evidence['observed_revision_ids'] + revisions,
        exact_frame_matches_by_replay={'four_routes': prior_evidence['exact_frame_matches'], 'Maria': exact},
        evidence=prior_evidence['evidence'] | {str(p): base.digest(p) for p in (*evidence, FOUR_ROUTES, __file__)}))
    print('Seven revised captions passed the original Gallery. Complete photos, arrows and return screens match.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('four-routes', 'parent', 'revised', 'compare'))
    action = parser.parse_args().action
    if action == 'four-routes':
        four_routes()
    elif action == 'compare':
        compare_maria()
    else:
        capture_maria(action)
