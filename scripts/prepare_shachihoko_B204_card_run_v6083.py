"""Source-lock the same ordinary input run to the disclosed item-name fixture."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/run_lil_B204_source_fixture_v6071.py','scripts/run_shachihoko_B204_card_v6083.py',{
        'work/analysis/lil_B204_source_fixture_v6070/complete_B204_source_B22_fixture.json':'work/analysis/shachihoko_B204_card_fixture_v6082/complete_B204_source_B22_fixture_with_provisional_item_name.json',
        'lil_B204_source_run_v6071_clean_Japanese':'shachihoko_B204_card_run_v6083_clean_Japanese',
        'lil_B204_source_v6071_clean_Japanese':'shachihoko_B204_card_v6083_clean_Japanese',
    }))
