"""Stop ordinary source inputs after the whole letter,then inspect menus through appended controls."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/run_shachihoko_B204_card_v6083.py','scripts/run_shachihoko_item_menu_v6104.py',{
        'work/analysis/shachihoko_B204_card_fixture_v6082/complete_B204_source_B22_fixture_with_provisional_item_name.json':'work/analysis/shachihoko_item_menu_fixture_v6103/complete_B204_source_B22_fixture_with_coordinated_item_data.json',
        'shachihoko_B204_card_run_v6083_clean_Japanese':'shachihoko_item_menu_run_v6104',
        'shachihoko_B204_card_v6083_clean_Japanese':'shachihoko_item_menu_v6104',
        'range(2600,12501,240)':'range(2600,7881,240)',
        '"\'--frames\',\'13001\'"':'"\'--frames\',\'30001\'"',
        '"\'--capture-at\',*map(str,range(2350,13001,60))"':'"\'--capture-at\',\'4510\',\'4750\',\'5530\',\'7870\',\'--pause-at\',\'8000\'"',
        '"\'--dump-ram\'"':'"\'--dump-pause-ram\',\'--dump-ram\'"',
    }))
