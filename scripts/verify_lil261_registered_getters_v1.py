"""Run both original getters for the protected names in Lil261's own startup."""

import sys

from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_lil361_startup_v1 import source as previous


if __name__ == '__main__':
    source = checked_text(previous, {
        'scripts.build_registered_lil361_v1': 'scripts.build_registered_lil261_v1',
        'all12 protected names from the Lil361 cumulative candidate own startup':
            'all12 protected names from the Lil261 cumulative candidate own startup',
    })
    assert not sys.argv[1:]
    sys.argv.append('--getters')
    exec(compile(source, __file__, 'exec'), globals())
