"""Walk all native SFX titles by ordinary title-menu inputs."""

from argparse import ArgumentParser
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import stage_sound_sirens_20261120 as stage


FIRST, STEP = 3680, 48
SELECT = tuple(FIRST + STEP * index for index in range(stage.COUNT))
WRAP = FIRST + STEP * stage.COUNT
END = WRAP + 480
FRAMES = (3000, *SELECT, WRAP, WRAP + 240, END)


def inputs():
    start = [(1601, 'START'), (2101, 'DOWN'), (2401, 'A'), (2801, 'A'), (3201, 'RIGHT')]
    navigation = [(frame + 1, 'DOWN') for frame in SELECT]
    play = (SELECT[stage.INDEX] - STEP//2, 'A')
    return [dict(start=frame, duration=8, buttons=[button]) for frame, button in sorted(
        [*start, *navigation, play, (WRAP + 1, 'B'), (WRAP + 241, 'B')])]


def main(side, out):
    assert not out.exists()
    proof = stage.batch.load(stage.PROOF)
    rom = stage.parent.ROM if side == 'current' else stage.ROM
    assert stage.parent.base.digest(rom) == proof['parent_sha256' if side == 'current' else 'candidate_sha256']
    out.mkdir(parents=True)
    schedule = out / 'inputs.json'
    stage.batch.write(schedule, inputs())
    sys.argv = [harness.__file__, '--rom', str(rom), '--out', str(out/'capture'), '--frames', str(END),
        '--inputs-json', str(schedule), '--press-start', '-1', '--capture-every', '999999',
        '--capture-at', *map(str, FRAMES), '--dump-ram']
    harness.main()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('side', choices=('current', 'revised'))
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    main(args.side, args.out)
