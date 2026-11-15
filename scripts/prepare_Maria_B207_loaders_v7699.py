"""Source-lock the full303-block target SC3 native load andparent checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_loader_tools_v7699')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/verify_papal_trade_loaders_v7643.py','scripts/verify_Maria_B207_loaders_v7699.py',{
        'Run original native loaders/cache paths and both initial parent modes for both archives.':'Run every native load/cache path andboth parent modes in the resized Maria SC3 archive.',
        'from scripts.create_papal_trade_reference_v7642 import ROM,PARENT':'from scripts.create_Maria_B207_reference_v7698 import ROM,PARENT',
        'papal_trade_loaders_v7643':'maria_B207_loaders_v7699','papal_trade_reference_v7642':'maria_B207_reference_v7698',
        'for r in [0,1]':'for r in [3]','counts=={0:343,1:325}':'counts=={3:303}','for route in [0,1]':'for route in [3]',
        'for route in (0,1):':'for route in (3,):',
        'loaded == 668':'loaded == 303','len(cases) == 1336':'len(cases) == 606',
        'two_archives_native_loads':'whole_SC3_native_loads','two_archives_native_parent_modes':'whole_SC3_native_parent_modes',
        '668_whole_native_loads_cache_hits1336_initial_parent_modes':'303_whole_native_loads_cache_hits606_initial_parent_modes',
        'fresh_native_whole_loads_andcache_hits=668':'fresh_native_whole_loads_andcache_hits=303',
        'fresh_initial_parent_modes=1336':'fresh_initial_parent_modes=606',
        'both1508_byte_targets_fit_original_0x2400_cache=True':'Maria1472_byte_target_preserves_CS0101_andfits_original_0x2400_cache=True',
        'all_original_EV0_EV1_actions_select_block_indices_not_interior_offsets':'all_original_EV3_actions_select_block_indices_not_interior_offsets',
        'Both resized archives:668 complete native loads/cache hits and1336 original initial parent modes pass.':'Resized SC3:303 complete native loads/cache hits and606 original initial parent modes pass.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_whole_SC3_loader_andparent.json',dict(derivation=result,no_native_high_constants_changed=True,new_credit=0,full_goal_complete=False))
