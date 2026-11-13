"""Pin the complete verified predecessor and prepare one-commit positive validation."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/prepare_Rafael_B47_production_v8009.py','scripts/pin_Rafael_B48_production_v8062.py',{
        'B47':'B48','V7964':'V8013','Rafael15':'Rafael91',
        'Rafael_B47_production_tools_v8009':'Rafael_B48_production_tools_v8062',
        'Rafael_B47_release_paths_v8006':'Rafael_B48_release_paths_v8060',
        'seal_Rafael_B47_references_v8006':'seal_Rafael_B48_references_v8060',
        '15 speech manifest':'91 speech manifest',
    }))
    print(derive('scripts/validate_Rafael_B47_atomic_positive_v8010.py','scripts/validate_Rafael_B48_atomic_positive_v8063.py',{
        'B47':'B48','R53':'R347','Rafael_B47_atomic_positive_v8010':'Rafael_B48_atomic_positive_v8063',
        'Rafael_B47_release_paths_v8006':'Rafael_B48_release_paths_v8060',
        "len(proof['changed_records'])==15":"len(proof['changed_records'])==91",'positive_records=15':'positive_records=91',
        'all48_commands24_relatives_six_predicates_source00':'all163_commands28_relatives_five_predicates_two_queries_source00_4B71_oneFI_fourFE',
        'four_native_only_speeches':'thirteen_native_only_speeches','15-record atomic':'91-record atomic',
    }))
