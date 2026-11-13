"""All343 original SC0 loads/cache hits and686 parent modes per ROM."""
from pathlib import Path

SOURCE=Path('scripts/verify_lil_london_loader_v1902.py')

if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    changes={
        'from scripts.prepare_lil_london_research_v1901 import ROM, PARENT':
            "from scripts.research_rafael_opening_v2001 import PARENT\nROM=Path('work/analysis/rafael_opening_relocation_v2001b/rafael_opening_V1986_derived_RESEARCH_ONLY.nds')",
        'lil_London_loader_v1902':'rafael_opening_loader_v2002',
        'work/analysis/lil_London_research_v1901/research_image_receipt.json':'work/analysis/rafael_opening_relocation_v2001b/current_B44_typed_relocation_research.json',
        '/data/SC2.DK4':'/data/SC0.DK4',
        'expected == 336':'expected == 343',
        'for route in (2,):':'for route in (0,):',
        'whole_SC2_loads_and_cache_hits':'whole_SC0_loads_and_cache_hits',
        'whole_SC2_and_B26_initial_entry_proof.json':'whole_SC0_and_B44_initial_entry_proof.json',
        'all336_whole_blocks_and672_modes_each_pass':'all343_whole_blocks_and686_modes_each_pass',
        'B26_block_fits_original_0x2400_cache':'B44_block_fits_original_0x2400_cache',
        'original_EV2_actions_select_by_block_index_without_interior_byte_offset':'original_EV0_actions_select_by_block_index_without_interior_byte_offset',
        '336 original loads/cache hits and672 parent entry modes':'343 original loads/cache hits and686 parent entry modes',
        'later London path approval pending.':'Rafael original/revised choice paths still pending.',
    }
    for old,new in changes.items():
        assert old in text,old
        text=text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
