"""Derive whole SC2 native load/cache and two-mode handoff checks without altering native guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_loader_tools_v8222')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/verify_Rafael_B50_loaders_v8152.py','scripts/verify_Gerhard_loaders_v8222.py',{
        'scripts.create_Rafael_B50_reference_v8151 import ROM,PARENT':'scripts.create_Gerhard_reference_v8215 import ROM',
        'Rafael_B50_loaders_v8152':'Gerhard_loaders_v8222',
        'Rafael_B50_reference_v8151':'Gerhard_reference_v8215',
        "RECEIPT=Path('work/analysis/Rafael_B50_reference_v8151/research_image_receipt.json')":
        "RECEIPT=Path('work/analysis/Gerhard_reference_v8215/research_image_receipt.json')\nPARENT=Path(read(RECEIPT)['parent'])",
        'for r in [0]':'for r in [2]','counts=={0:343}':'counts=={2:336}','for route in [0]:':'for route in [2]:',
        "'for route in (0,):'":"'for route in (2,):'",
        'loaded == 343':'loaded == 336','len(cases) == 686':'len(cases) == 672',
        'whole_SC0_native':'whole_SC2_native','343_whole_native_loads_cache_hits686_initial_parent_modes':'336_whole_native_loads_cache_hits672_initial_parent_modes',
        'fresh_native_whole_loads_andcache_hits=343,fresh_initial_parent_modes=686':'fresh_native_whole_loads_andcache_hits=336,fresh_initial_parent_modes=672',
        'exact_B50_header_andall_mapped_targets_fit_original_0x2400_cache':'exact_B27_B74_headers_andall_mapped_targets_fit_original_0x2400_cache',
        'all_original_EV0_actions_select_block_indices_not_interior_offsets':'all_original_EV2_actions_select_block_indices_not_interior_offsets',
        'Run every native load/cache path andboth parent modes in the resized Rafael SC0 archive.':'Run every native SC2 load/cache path andboth parent modes in the five-surname research image.',
        'Resized SC0:343 complete native loads/cache hits and686 original initial parent modes pass.':'Resized SC2:336 complete native loads/cache hits and672 original initial parent modes pass.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared exact native SC2 loader/cache/parent probes;only route/count/artifact bindings change.')
