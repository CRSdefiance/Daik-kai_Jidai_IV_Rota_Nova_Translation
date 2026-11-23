"""Play the ordinary Lisbon departure and choose Rafael's question about the wind."""

from argparse import ArgumentParser
from inspect import getsource

from scripts import replay_rafael_tavern_lesson_20261119 as tavern
from scripts import review_rafael_voyage_ceuta_20261119 as staged
from scripts.source_locked_derivation_v5118 import checked_text

KEYS = ((22620, 'B'), *((f, 'A') for f in range(22900, 31680, 230)), (31735, 'DOWN'), (31845, 'A'),
        *((f, 'A') for f in range(32075, 34200, 230)))
TAIL = [r for r in tavern.TAIL if r['start'] <= 22380] + [dict(start=f, duration=8, buttons=[key]) for f, key in KEYS]
FRAMES = (22805, 29295, *[f+165 for f, _ in KEYS if 22900 <= f < 31700], 31708, 31800, 32005,
          *[f+175 for f, _ in KEYS if f >= 32075], 34420)
END = 34421


def capture(case):
    selected = (staged.parent.ROM, staged.parent.RELEASE) if case == 'current' else (staged.ROM, staged.PROOF)
    source = checked_text(getsource(tavern.original.capture), {
        'rom, proof = parent.ROM, parent.RELEASE': 'rom, proof = selected',
        'rom, proof = build.ROM, build.PROOF': 'rom, proof = selected',
        "base.load(INPUTS) + [dict(start=f,duration=8,buttons=['A']) for f in AFTER]":
            "base.load(INPUTS) + [dict(start=f,duration=8,buttons=['A']) for f in AFTER if f <= 15701] + TAIL",
    })
    scope = vars(tavern.original) | dict(selected=selected, ROOT=staged.ROOT, TAIL=TAIL, FRAMES=FRAMES, END=END)
    exec(compile(source, __file__+'::capture', 'exec'), scope)
    scope['capture'](case)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('current', 'revised_v3'))
    capture(parser.parse_args().case)
