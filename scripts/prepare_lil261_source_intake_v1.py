"""Select the thirteen remaining Lil exchanges from the exact clean census."""

from pathlib import Path

from scripts import prepare_lil254_source_intake_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous.source, {
    '515': '261',
    '6205': '6459',
    '254': '261',
    'len(selected) == 8': 'len(selected) == 13',
    'complete_exchanges=8': 'complete_exchanges=13',
})
census = Path('work/story_source_coverage_20261110_SC2_v7/coverage.json')
env = {**previous.env, 'ROOT': Path('work/Lil261_B323_B335_clean_20261110'),
       'CENSUS': census, 'PACKET': census.with_name('residual_clean_source_packet.json'),
       'RELEASE': Path('work/lil254_B312_B319_release_v1/registered_release_verification.json'),
       'BLOCKS': list(range(323, 336)), '__file__': __file__}
exec(compile(source, __file__, 'exec'), env)

if __name__ == '__main__':
    env['main']()
