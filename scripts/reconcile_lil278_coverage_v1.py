"""Extend the exact Lil source census by the 278 registered source positions."""

import re

from scripts.reconcile_lil361_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "ROOT = Path('work/story_source_coverage_20261110_SC2_v5')":
        "ROOT = Path('work/story_source_coverage_20261110_SC2_v6')",
    "PRIOR = Path('work/story_source_coverage_20261110_SC2_v4/coverage.json')":
        "PRIOR = Path('work/story_source_coverage_20261110_SC2_v5/coverage.json')",
    'lil361_B283_B298': 'lil278_B299_B311',
    'Lil_SC2_B283_B298_clean_20261110': 'Lil_SC2_B299_B311_clean_20261110',
    'all361_individual_five_gates_pass': 'all278_individual_five_gates_pass',
})
counts = {'361': '278', '1154': '793', '5927': '6205', '793': '515', '5566': '5927'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(counts) + r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda match: counts[match[0]], source)

if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
