"""Initialize the shark exchange before the daily random-event gates."""

import argparse
import inspect
from pathlib import Path
from types import FunctionType

from dk4tool.rom.nds import NdsImage
from scripts import replay_shark_encounter_v1 as previous


ENTRY, CONTINUE = 0x30E54, 0x30E58
OUT = Path('out/shark_encounter_replay_20261111_v2')


def fixture_controller(rom):
    arm, clean = (NdsImage.open(path).read_file(previous.ARM) for path in (rom, previous.CLEAN))
    assert arm[ENTRY - 4:CONTINUE + 4] == clean[ENTRY - 4:CONTINUE + 4]
    env = vars(previous) | {'ENTRY': ENTRY, 'CONTINUE': CONTINUE}
    return FunctionType(previous.fixture_controller.__code__, env)(rom)


def replay(choice):
    # The ROM, donor, and ordinary inputs stay the same as the first replay.
    # Keep its failed activation evidence and write this run to a new directory.
    env = vars(previous) | {'fixture_controller': fixture_controller}
    code = inspect.getsource(previous.replay)
    original = "out = stage.ROOT / choice"
    assert code.count(original) == 1
    env['OUT'] = OUT
    exec(compile(code.replace(original, "out = OUT / choice\n    out.parent.mkdir(exist_ok=True)"),
                 __file__ + '::same-cold-boot-and-choice-inputs', 'exec'), env)
    env['replay'](choice)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('choice', choices=('raise', 'kill'))
    replay(parser.parse_args().choice)
