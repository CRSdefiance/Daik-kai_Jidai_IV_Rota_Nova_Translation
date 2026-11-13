"""Reconcile all Lil source positions with the 254 newly registered records."""

import re

from scripts.reconcile_lil278_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "ROOT = Path('work/story_source_coverage_20261110_SC2_v6')":
        "ROOT = Path('work/story_source_coverage_20261110_SC2_v7')",
    "PRIOR = Path('work/story_source_coverage_20261110_SC2_v5/coverage.json')":
        "PRIOR = Path('work/story_source_coverage_20261110_SC2_v6/coverage.json')",
    'lil278_B299_B311': 'lil254_B312_B319',
    'Lil_SC2_B299_B311_clean_20261110': 'Lil_SC2_B312_B319_clean_20261110',
    'all278_individual_five_gates_pass': 'all254_individual_five_gates_pass',
    'census:6205': 'census:6459',
    'all6720': 'all 6720',
})
counts = {'278': '254', '793': '515', '6205': '6459', '515': '261', '5927': '6205'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(counts) + r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda match: counts[match[0]], source)


if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
