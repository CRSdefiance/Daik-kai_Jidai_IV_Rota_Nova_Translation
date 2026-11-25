"""Preserve cumulative,reconstruction and all five B194 research ROMs."""
from scripts.source_locked_derivation_v5118 import derive

if __name__=='__main__':
    print(derive('scripts/pin_lil_B193_v5482.py','scripts/pin_lil_B194_v5535.py',{
        'B193':'B194','retention_v5482':'retention_v5535','release_v5479':'release_v5532',
        'reference_v5464':'reference_v5509','display_v5469':'display_v5514','V5478':'V5531',
        "Path(release['exact_patch_reconstruction'])":"Path('out/lil_B194_available_v5519_clean_Japanese_RESEARCH_ONLY.nds'),Path('out/lil_B194_available_v5519_reviewed_English_RESEARCH_ONLY.nds'),Path(release['exact_patch_reconstruction'])",
        'all5_B193_ROM_paths':'all7_B194_ROM_paths','all three previous':'all five previous',
    }))
