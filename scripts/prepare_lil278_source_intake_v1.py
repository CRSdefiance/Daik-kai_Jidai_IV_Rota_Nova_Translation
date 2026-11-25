"""Select the next thirteen complete Lil exchanges from the reconciled clean census."""
from pathlib import Path

from scripts import prepare_lil269_source_intake_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    '1423': '793',
    '5297': '5927',
    '269': '278',
    'len(selected) == 40': 'len(selected) == 13',
    'complete_exchanges=40': 'complete_exchanges=13',
})
census = Path('work/story_source_coverage_20261110_SC2_v5/coverage.json')
env = {**previous.env, 'ROOT': Path('work/Lil278_B299_B311_clean_20261110'),
    'CENSUS': census, 'PACKET': census.with_name('residual_clean_source_packet.json'),
    'RELEASE': Path('work/lil361_B283_B298_release_v1/registered_release_verification.json'),
    'BLOCKS': list(range(299, 312)), '__file__': __file__}
exec(compile(source, __file__, 'exec'), env)

if __name__ == '__main__':
    env['main']()
