"""Extend exact SC2 source credit while preserving complete prior context."""
import re
from scripts.reconcile_lil269_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "ROOT = Path('work/story_source_coverage_20261110_SC2_v4')": "ROOT = Path('work/story_source_coverage_20261110_SC2_v5')",
    "PRIOR = Path('work/story_source_coverage_20261110_SC2_v3/coverage.json')": "PRIOR = Path('work/story_source_coverage_20261110_SC2_v4/coverage.json')",
    'lil269_B243_B282': 'lil361_B283_B298',
    'all269_individual_five_gates_pass': 'all361_individual_five_gates_pass',
    'Lil_SC2_B243_B282_clean_20261110': 'Lil_SC2_B283_B298_clean_20261110',
})
counts = {'269': '361', '1423': '1154', '5566': '5927', '1154': '793', '5297': '5566'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(sorted(counts, key=len, reverse=True)) + r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda m: counts[m[0]], source)

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-exact-source-position-census-andcomplete-context-preservation', 'exec'), globals())
