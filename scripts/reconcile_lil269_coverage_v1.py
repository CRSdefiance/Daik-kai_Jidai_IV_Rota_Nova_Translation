"""Extend exact SC2 credit and preserve the complete earlier partially credited context."""
import re
from scripts.reconcile_lil382_coverage_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "ROOT = Path('work/story_source_coverage_20261110_SC2_v3')": "ROOT = Path('work/story_source_coverage_20261110_SC2_v4')",
    "PRIOR = Path('work/story_source_coverage_20261109_SC2_v2/coverage.json')":
        "PRIOR = Path('work/story_source_coverage_20261110_SC2_v3/coverage.json')",
    'lil382_residual_A': 'lil269_B243_B282',
    'all382_individual_five_gates_pass': 'all269_individual_five_gates_pass',
    'Lil_SC2_residual_A_382_clean_20261110': 'Lil_SC2_B243_B282_clean_20261110',
    "for r in g['records']]": "for r in g.get('complete_clean_context_records',g['records'])]",
})
counts = {'382': '269', '1805': '1423', '5297': '5566', '1423': '1154', '4915': '5297'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(sorted(counts, key=len, reverse=True)) + r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda m: counts[m[0]], source)
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-exact-source-position-census-complete-context-preserved', 'exec'), globals())
