"""336 loads/cache hits and672 parent modes per ROM for Speyer resizing."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

SOURCE = Path('scripts/verify_lil_london_loader_v1902.py')
SOURCE_SHA = '8e9dcc4cb6e2fe88032eab25edebb0c2edd18d5eabe72925098fe4b8c1fe6fe8'

if __name__ == '__main__':
    assert sha(SOURCE.read_bytes()) == SOURCE_SHA
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'scripts.prepare_lil_london_research_v1901':'scripts.prepare_lil_speyer_research_v1929',
        'lil_London_loader_v1902':'lil_Speyer_loader_v1930',
        'work/analysis/lil_London_research_v1901/research_image_receipt.json':
            'work/analysis/lil_Speyer_research_v1929/research_image_receipt.json',
        'whole_SC2_and_B26_initial_entry_proof.json':'whole_SC2_and_B25_B128_initial_entry_proof.json',
        'B26_block_fits_original_0x2400_cache':'B25_B128_blocks_fit_original_0x2400_cache',
        'later London path approval pending.':'later Speyer path approval pending.',
    }
    for old,new in changes.items():
        assert text.count(old) == 1,old
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
