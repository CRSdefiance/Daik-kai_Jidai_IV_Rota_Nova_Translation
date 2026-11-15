"""Compile chooser rows with native ASCII pair-phase padding before each LF."""

import argparse
import inspect
from types import FunctionType

from scripts import stage_captain_biographies_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_sera_assignment_review_v1 import ROOT as PARENT_ROOT


ROOT = previous.ROOT.with_name('captain_biographies_20261111_v2')
ROM = ROOT / previous.ROM.name
PROOF = ROOT / previous.PROOF.name
PRIOR = PARENT_ROOT / 'own_startup'
DECISIONS = previous.DECISIONS | {'Maria': (
    "Defying the isolation law, a Ming admiral leads her own fleet to protect people from wokou raids.",
    *previous.DECISIONS['Maria'][1:3],
    ('isolation law', *previous.DECISIONS['Maria'][3][1:]),
)}


def encode_rows(lines):
    # An LF following an odd-length ASCII row can consume the next glyph.
    # A trailing blank completes that pair without indenting the next row.
    stored = [line + ' ' * (len(line) % 2) for line in lines[:-1]] + [lines[-1]]
    assert all(len(row) % 2 == 0 and 16 + len(row) * 6 <= 256 for row in stored[:-1])
    assert tuple(row.rstrip() for row in stored) == tuple(lines)
    return '\n'.join(stored).encode('ascii') + b'\0'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('stage', 'candidate', 'startup'))
    action = parser.parse_args().action
    env = {**vars(previous), **globals(), '__file__': __file__, '__name__': 'captain_biographies_v2'}
    source = checked_text(inspect.getsource(previous.rebuild), {
        "payload = '\\n'.join(lines).encode('ascii') + b'\\0'": 'payload = encode_rows(lines)',
    })
    exec(compile(source, __file__ + '::chooser-pair-phase', 'exec'), env)
    fn = previous.stage if action == 'stage' else previous.replay
    FunctionType(fn.__code__, env)(*(() if action == 'stage' else (action,)))


if __name__ == '__main__':
    main()
