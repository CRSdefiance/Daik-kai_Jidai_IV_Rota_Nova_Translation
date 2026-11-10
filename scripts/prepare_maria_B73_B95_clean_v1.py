"""Select328 disjoint clean objects in21 complete exchanges before current English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(Path('scripts/prepare_maria_B51_B57_clean_v1.py').read_text(encoding='utf-8'), {
    'work/Maria_B51_B57_clean_20261109': 'work/Maria_B73_B95_clean_20261109',
    'work/story_source_coverage_20261109_SC3_v3': 'work/story_source_coverage_20261109_SC3_v6',
    "51<=g['block']<=57": "73<=g['block']<=95",
    'list(range(51,58))': '[73,74,75,76,77,78,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95]',
    '==310': '==328', "'records':310": "'records':328", 'source_objects=310': 'source_objects=328',
    "'complete_exchanges':7": "'complete_exchanges':21", 'complete_exchanges=7': 'complete_exchanges=21',
    "'B50_separate_registered_integration_in_progress_not_restarted':True": "'Maria303_registered_integration_preserved_not_restarted':True",
    'Prepared310 clean-only objects/seven complete exchanges': 'Prepared328 clean-only objects/21 complete exchanges',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-exact-disjoint-clean-intake328-before-current-English', 'exec'), globals())
