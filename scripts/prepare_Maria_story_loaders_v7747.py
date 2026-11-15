"""Freeze unchanged complete native loaders against the exact three-block reference."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_story_loader_tools_v7747');assert not root.exists()
    result=derive('scripts/verify_Maria_B207_loaders_v7699.py','scripts/verify_Maria_story_loaders_v7747.py',{
        'from scripts.create_Maria_B207_reference_v7698 import ROM,PARENT':'from scripts.create_Maria_story_reference_v7746 import ROM,PARENT',
        'maria_B207_loaders_v7699':'maria_story_loaders_v7747',
        'maria_B207_reference_v7698/research_image_receipt':'maria_story_reference_v7746/research_image_receipt',
        'two-resized-original-loaders':'three-resized-original-loaders',
        'Maria1472_byte_target_preserves_CS0101_andfits_original_0x2400_cache':
        'three_exact_source_headers_andmapped_targets_fit_original_0x2400_cache',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,no_native_high_constants_orABI_guards_changed=True,new_credit=0,full_goal_complete=False))
    print('Frozen original SC3 complete303load/cache and606parent-mode proof against three-block reference.')
