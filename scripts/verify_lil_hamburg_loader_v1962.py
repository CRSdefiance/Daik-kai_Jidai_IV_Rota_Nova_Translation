"""All336 native loads/cache hits and672 parent modes per Hamburg test ROM."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

SOURCE = Path('scripts/verify_lil_london_loader_v1902.py')
SOURCE_SHA = '8e9dcc4cb6e2fe88032eab25edebb0c2edd18d5eabe72925098fe4b8c1fe6fe8'

if __name__ == '__main__':
    assert sha(SOURCE.read_bytes()) == SOURCE_SHA
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'scripts.prepare_lil_london_research_v1901':'scripts.prepare_lil_hamburg_research_v1961',
        'lil_London_loader_v1902':'lil_Hamburg_loader_v1962',
        'work/analysis/lil_London_research_v1901/research_image_receipt.json':'work/analysis/lil_Hamburg_research_v1961/research_image_receipt.json',
        'whole_SC2_and_B26_initial_entry_proof.json':'whole_SC2_and_B74_initial_entry_proof.json',
        'B26_block_fits_original_0x2400_cache':'B74_block_fits_original_0x2400_cache',
        'later London path approval pending.':'later Hamburg path approval pending.',
    }
    for old,new in changes.items():
        assert text.count(old) == 1,old
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
