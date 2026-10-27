"""Ordinary controls for all four original Gallery carousels; copied save fixture."""

import json
from pathlib import Path

OUT = Path('work/analysis/gallery_v522')


def main():
    events = []
    captures = [2400, 2800]
    routes = []

    def event(start, buttons=None, touch=None):
        row = {'start': start, 'duration': 8, 'buttons': buttons or []}
        if touch is not None:
            row['touch'] = touch
        events.append(row)

    event(1601, ['START'])
    event(2001, touch=[128, 148])
    event(2201, ['A'])
    event(2401, touch=[128, 126])
    event(2601, ['A'])
    first = 3200
    for route, name, count, touch in [
        (0, 'Rafael', 46, [84, 50]),
        (1, 'Hodram', 41, [170, 50]),
        (2, 'Lil', 39, [84, 130]),
        (3, 'Maria', 38, [170, 130]),
    ]:
        event(first - 399, touch=touch)
        event(first - 199, ['A'])
        frames = [first + n * 200 for n in range(count)]
        for frame in frames[1:]:
            event(frame - 199, ['RIGHT'])
        wrap = frames[-1] + 200
        event(wrap - 199, ['RIGHT'])
        captures.extend(frames + [wrap])
        routes.append({'route': route, 'captain': name, 'count': count,
                       'frames': frames, 'wrap_frame': wrap})
        if route != 3:
            event(wrap + 1, ['B'])
            captures.append(wrap + 200)
            first = wrap + 800
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'inputs.json').write_text(json.dumps(events, indent=2) + '\n')
    (OUT / 'run_plan.json').write_text(json.dumps({
        'input_schedule': str(OUT / 'inputs.json'), 'capture_frames': captures,
        'routes': routes, 'final_frame': routes[-1]['wrap_frame'] + 200,
        'synthetic_gallery_access_only': True, 'ordinary_carousel_controls': True,
    }, indent=2) + '\n')
    print(f'All164 Gallery positions and four wrap checks scheduled; final frame {routes[-1]["wrap_frame"] + 200}.')


if __name__ == '__main__':
    main()
