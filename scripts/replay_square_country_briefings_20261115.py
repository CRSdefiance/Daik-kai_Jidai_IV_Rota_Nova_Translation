"""Replay ordinary Amsterdam Square and the cumulative startup controls."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import observe_amsterdam_square_current_20261114 as amsterdam
from scripts import replay_refit_help_startup_20261115 as startup
from scripts import stage_square_country_briefings_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


def main(case):
    if case == 'startup':
        FunctionType(startup.main.__code__, vars(startup) | dict(stage=stage))()
        return
    receipt = stage.base.load(stage.STORED)
    source = checked_text(getsource(amsterdam.playback.main), {
        '    rom = parent.ROM\n    release = base.load(parent.RELEASE)': '    rom = STAGE_ROM\n    release = STAGE_RECEIPT',
        '    installed = []': "    argv.append('--touchscreen')\n    installed = []",
    })
    scope = vars(amsterdam.playback) | dict(
        ROOT=stage.ROOT / 'amsterdam', STAGE_ROM=stage.ROM, STAGE_RECEIPT=receipt,
        FOCUS={136, *stage.NUMBERS}, observer=amsterdam.trace.scoped_observer, get_schedule=amsterdam.schedule,
        __file__=__file__,
    )
    exec(compile(source, __file__ + '::ordinary-amsterdam', 'exec'), scope)
    scope['main']('square')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('startup', 'amsterdam'))
    main(parser.parse_args().case)
