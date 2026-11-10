"""Source-lock the single-block native reference andshipped-caller census."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_reference_tools_v7700')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/verify_papal_trade_references_v7644.py','scripts/verify_Maria_B207_references_v7700.py',{
        'Bind the shipped caller census and all40 clean/current/relocated command boundaries.':'Bind the shipped caller census andall20 Maria clean/current/relocated command boundaries.',
        'from scripts.create_papal_trade_reference_v7642 import ROM,PARENT,PLAN':'from scripts.create_Maria_B207_reference_v7698 import ROM,PARENT,PLAN',
        'from scripts.draft_papal_trade_prose_v7631 import CURRENT':'from scripts.draft_Maria_B207_prose_v7687 import CURRENT',
        'papal_trade_reference_census_v7644':'maria_B207_reference_census_v7700',
        'papal_trade_loaders_v7643/668_whole_native_loads_cache_hits1336_initial_parent_modes':'maria_B207_loaders_v7699/303_whole_native_loads_cache_hits606_initial_parent_modes',
        "loader['fresh_native_whole_loads_andcache_hits']==668 and loader['fresh_initial_parent_modes']==1336":"loader['fresh_native_whole_loads_andcache_hits']==303 and loader['fresh_initial_parent_modes']==606",
        "zip(mapping['groups'],current['groups'],strict=True)":"zip(mapping['groups'],[current],strict=True)",
        'all40_commands_two_block_entries_one_fresh_shipped_caller_census':'Maria_all20_commands_one_entry_one_fresh_shipped_caller_census',
        'fresh_target_walks=2':'fresh_target_walks=1',
        'original_EV0_EV1_block_index_loader_andtwo_parent_modes_verified':'original_EV3_block_index_loader_andtwo_parent_modes_verified',
        'all40_commands_complete_preambles_opaque_operands_andnormal_ends_preserved':'all20_commands_complete_preambles_opaque_operands_andnormal_end_preserved',
        'All40 clean/current/relocated commands andboth original block entries pass;one fresh shipped caller census matches exact native units.':'All20 Maria clean/current/relocated commands andoriginal block entry pass;one fresh shipped caller census matches exact native units.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_Maria_reference_census.json',dict(derivation=result,no_native_high_constant_changes=True,new_credit=0,full_goal_complete=False))
