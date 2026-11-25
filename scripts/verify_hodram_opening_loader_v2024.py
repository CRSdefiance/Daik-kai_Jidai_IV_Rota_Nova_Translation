"""Original SC1 loads and both parent modes, scoped to the reviewed route."""
from pathlib import Path

SOURCE=Path('scripts/verify_lil_london_loader_v1902.py')

if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    changes={
        'from scripts.prepare_lil_london_research_v1901 import ROM, PARENT':
            'from scripts.research_hodram_opening_v2023 import ROM, PARENT',
        'lil_London_loader_v1902':'hodram_opening_loader_v2024',
        'work/analysis/lil_London_research_v1901/research_image_receipt.json':
            'work/analysis/hodram_opening_relocation_v2023/complete_three_block_typed_relocation_research.json',
        '/data/SC2.DK4':'/data/SC1.DK4',
        'expected == 336':'expected == 325',
        'for route in (2,):':'for route in (1,):',
        'whole_SC2_loads_and_cache_hits':'whole_SC1_loads_and_cache_hits',
        'whole_SC2_and_B26_initial_entry_proof.json':'whole_SC1_and_B42_B44_initial_entry_proof.json',
        'all336_whole_blocks_and672_modes_each_pass':'all325_whole_blocks_and650_modes_each_pass',
        'B26_block_fits_original_0x2400_cache':'B42_B43_B44_fit_original_0x2400_cache',
        'original_EV2_actions_select_by_block_index_without_interior_byte_offset':
            'original_EV1_actions_select_by_block_index_without_interior_byte_offset',
        '336 original loads/cache hits and672 parent entry modes':'325 original loads/cache hits and650 parent entry modes',
        'later London path approval pending.':'Hodram representative revised paths still pending.',
    }
    for old,new in changes.items():
        assert old in text,old
        text=text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
