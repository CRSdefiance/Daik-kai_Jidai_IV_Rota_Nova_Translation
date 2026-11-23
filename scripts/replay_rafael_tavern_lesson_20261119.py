"""Cold-boot Rafael's ordinary Lisbon save and observe the Tavern recruitment lesson."""

from argparse import ArgumentParser
from inspect import getsource

from scripts import replay_rafael_deck_after_trade_20261119 as original
from scripts import review_rafael_tavern_lesson_20261119 as staged
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = staged.ROOT.parent
ACTION_KEYS = (
    (16020, 'X'), (16920, 'B'), (17220, 'B'),
    *( (frame, 'A') for frame in range(18120, 19700, 220) ),
    (19900, 'DOWN'), (20120, 'DOWN'), (20340, 'A'), (20560, 'A'), (20780, 'A'),
    (21000, 'A'), (21220, 'A'), (21440, 'Y'), (21660, 'A'), (21900, 'X'),
    (22140, 'A'), (22380, 'A'), (22620, 'A'), (22900, 'B'), (23140, 'B'),
    *( (frame, 'A') for frame in range(23400, 30401, 230) ),
)
TOUCHES = ((16320, [95, 110]), (16620, [95, 110]), (17520, [80, 29]), (17820, [80, 29]))
TAIL = sorted([dict(start=f, duration=8, buttons=[key]) for f, key in ACTION_KEYS] +
              [dict(start=f, duration=8, buttons=[], touch=xy) for f, xy in TOUCHES], key=lambda r: r['start'])
FRAMES = (15961, *(r['start'] + 185 for r in TAIL), 30610)
END = 30611


def capture(case):
    source = checked_text(getsource(original.capture), {
        'rom, proof = parent.ROM, parent.RELEASE': 'rom, proof = staged.parent.ROM, staged.parent.RELEASE',
        'rom, proof = build.ROM, build.PROOF': 'rom, proof = staged.ROM, staged.PROOF',
        "base.load(INPUTS) + [dict(start=f,duration=8,buttons=['A']) for f in AFTER]":
            "base.load(INPUTS) + [dict(start=f,duration=8,buttons=['A']) for f in AFTER if f <= 15701] + TAIL",
    })
    tail, frames = TAIL, FRAMES
    if case == 'followthrough_v3':
        keys = ((22620, 'B'), *((f, 'A') for f in range(22900, 30401, 230)))
        tail = [r for r in TAIL if r['start'] <= 22380] + [dict(start=f, duration=8, buttons=[key]) for f, key in keys]
        frames = (15961, *(r['start'] + 185 for r in tail), 30610)
    env = vars(original) | dict(staged=staged, ROOT=ROOT, TAIL=tail, FRAMES=frames, END=END)
    exec(compile(source, __file__ + '::capture', 'exec'), env)
    env['capture'](case)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('current', 'tavern_final_v3', 'followthrough_v3'))
    capture(parser.parse_args().case)
