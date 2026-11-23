"""Reach the original relaxed Square giveaway confirmation with a supplied voice."""

from argparse import ArgumentParser
from inspect import getsource
from types import SimpleNamespace

from scripts import register_port_fleet_wrap_20261123 as parent
from scripts import replay_square_sample_voice_20261123 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def replay(side):
    from scripts import stage_cabin_square_wrap_20261123 as stage

    stage.ROOT.mkdir(parents=True, exist_ok=True)
    settings = SimpleNamespace(ROOT=stage.ROOT, ROM=stage.ROM, PROOF=stage.PROOF,
        parent=parent, base=stage.base, CLEAN=stage.CLEAN, ARM=stage.ARM)
    code = checked_text(getsource(previous.replay), {
        'assigned[:off] + b"\\x05" + assigned[off+1:]':
            'assigned[:off] + bytes((6,)) + assigned[off+1:]',
        'get(0x7E988, (actor,)) == 5': 'get(0x7E988, (actor,)) == 6',
        'get(0x53F4C, (actor, 0x021184C0)) == 663': 'get(0x53F4C, (actor, 0x021184C0)) == 664',
        'get(0x53F4C, (actor, 0x021184A0)) == 671': 'get(0x53F4C, (actor, 0x021184A0)) == 672',
        'dict(address=addr, before=7, after=5)': 'dict(address=addr, before=7, after=6)',
        'supplied_voice_style=5, original_confirmation=663, original_announcement=671':
            'supplied_voice_style=6, original_confirmation=664, original_announcement=672',
    })
    scope = vars(previous) | dict(stage=settings)
    exec(compile(code, __file__ + "::queued_square_voice", "exec"), scope)
    scope["replay"](side)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("side", choices=("old", "new"))
    replay(parser.parse_args().side)
