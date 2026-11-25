"""Trace shared lookups during unmodified title and Rafael opening playback."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from scripts import observe_online_gallery_common_v1 as observer
from scripts import observe_setup_save_common_v1 as setup
from scripts import register_barmaid_town_labels_20261115 as current


base = current.base
ROOT = Path('work/opening_scene_label_playback_20261115_v1')
TITLE = Path('work/analysis/opening_composition_v646/full_composition_results.json')
ROUTES = Path('work/analysis/route_opening_movies_v647/run_configs.json')
ASSETS = (4, 5, 10, 22, 23, 24, 46, 48, 72, 73, 76, 82, 148, 149, 150,
          151, 155, 156, 157, 158, 160, 162, 163, 164, 168, 169)


def title_frames():
    rows = base.load(TITLE)['cases']
    frames = {}
    for row in rows:
        if row['source_movie'] != '/FLS/M28.fls':
            continue
        assert row['whole49152_RGB_pixels_exact_without_exclusions']
        for binding in row['source_VRAM_bindings']:
            for index in binding['source_equivalence_candidates']:
                frames.setdefault(index, row['display_frame'])
    return {index: frames[index] for index in ASSETS}


def schedule(case):
    if case == 'title':
        return [], sorted(set(title_frames().values())), 7400, TITLE, None
    config = base.load(ROUTES)[case]
    inputs = Path(config['inputs'])
    assert base.digest(inputs) == config['inputs_sha256']
    return base.load(inputs), [2550, 2908, 3000, 3141, 3220], config['frames'], inputs, None


def main(case):
    replay = FunctionType(observer.main.__code__, vars(observer) | dict(
        ROOT=ROOT, parent=current, observer=setup.scoped_observer, get_schedule=schedule,
        FOCUS=set(range(3570, 3607)), __file__=__file__))
    replay(case)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('title', 'rafael'))
    main(parser.parse_args().case)
