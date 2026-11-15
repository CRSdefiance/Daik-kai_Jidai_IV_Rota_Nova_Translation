"""Retain the original RAM-size guard while adding the Maria route checks."""

from inspect import getsource

from scripts import verify_crew_equipment_advice_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    source = checked_text(getsource(previous.verify_live), {
        '"        check_maria_snapshot(raw)"':
            '"        assert len(raw) == 0x400000\\n        check_maria_snapshot(raw)"',
    })
    env = vars(previous) | globals()
    exec(compile(source, __file__ + '::retained-ram-size-guard', 'exec'), env)
    env['verify_live']()


if __name__ == '__main__':
    main()
