"""Select the next eight complete Lil exchanges from the reconciled clean census."""

from pathlib import Path

from scripts import prepare_lil278_source_intake_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous.source, {
    '793': '515',
    '5927': '6205',
    '278': '254',
    'len(selected) == 13': 'len(selected) == 8',
    'complete_exchanges=13': 'complete_exchanges=8',
})
census = Path('work/story_source_coverage_20261110_SC2_v6/coverage.json')
env = {**previous.env, 'ROOT': Path('work/Lil254_B312_B319_clean_20261110'),
       'CENSUS': census, 'PACKET': census.with_name('residual_clean_source_packet.json'),
       'RELEASE': Path('work/lil278_B299_B311_release_v1/registered_release_verification.json'),
       'BLOCKS': list(range(312, 320)), '__file__': __file__}
exec(compile(source, __file__, 'exec'), env)

if __name__ == '__main__':
    env['main']()
