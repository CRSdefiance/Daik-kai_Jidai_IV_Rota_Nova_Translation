"""Select303 disjoint clean objects in ten complete exchanges before current English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/prepare_maria_B51_B57_clean_v1.py').read_text(encoding='utf-8'),{
    'work/Maria_B51_B57_clean_20261109':'work/Maria_B58_B70_clean_20261109',
    'work/story_source_coverage_20261109_SC3_v3':'work/story_source_coverage_20261109_SC3_v5',
    "51<=g['block']<=57":"58<=g['block']<=70",
    'list(range(51,58))':'[58,59,60,61,62,64,65,66,68,70]',
    '==310':'==303',"'records':310":"'records':303",'source_objects=310':'source_objects=303',
    "'complete_exchanges':7":"'complete_exchanges':10",'complete_exchanges=7':'complete_exchanges=10',
    "'B50_separate_registered_integration_in_progress_not_restarted':True":
        "'Maria310_registered_integration_preserved_not_restarted':True",
    'Prepared310 clean-only objects/seven complete exchanges':'Prepared303 clean-only objects/ten complete exchanges',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-disjoint-clean-source-selection303-before-current-English','exec'),globals())
