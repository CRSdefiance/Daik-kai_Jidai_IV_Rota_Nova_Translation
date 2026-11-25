"""Bind explicit EV1 dependencies to complete additional clean exchanges."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B61_B70_context_preparation_v8882')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/inventory_Hodram_B54_B60_context_v8795.py','scripts/inventory_Hodram_B61_B70_context_v8882.py',{
        'Inventory complete clean Hodram B53 andoriginal EV1 context;numeric adjacency proves no chronology.':
            'Inventory clean Hodram B38/B44 explicit EV1 context;numeric adjacency proves no chronology.',
        'work/analysis/Hodram_B54_B60_clean_context_v8795':'work/analysis/Hodram_B61_B70_clean_context_v8882',
        'work/analysis/editorial_handoff_verification_v8790/verified_handoff.json':'work/analysis/editorial_handoff_verification_v8876/verified_handoff.json',
        '==7237':'==7319',
        'all-routes-unified-v8778':'all-routes-unified-v8865',
        '[15,37,65,128,142]':'[38,44]',
        'complete_clean_linked_15_37_65_128_142_context_before_B54_B60_English.json':
            'complete_clean_linked_38_44_context_before_B61_B70_English.json'
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        complete_original_source_inventory_andcoverage_guards_preserved=True,
        dependency_context_not_assumed_attainable_path_ornew_credit=True,full_goal_complete=False))
    print('Prepared clean linked-context inventory; no earlier English exposed.')
