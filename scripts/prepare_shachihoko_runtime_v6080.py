"""Derive a disclosed data-only research cold boot from the registered startup runner."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/run_lil_B203_startup_v6052.py','scripts/run_shachihoko_startup_v6080.py',{
        'lil_B203_runs_v6052':'shachihoko_runs_v6080','lil_B203_v6052':'shachihoko_v6080',
        "version=6050;rom=Path(f'out/all_routes_combined_v{version}_candidate.nds')":"assert case=='newgame';version='6079_RESEARCH_ONLY';receipt=read('work/analysis/shachihoko_item_name_research_v6079/research_image_receipt.json');rom=Path(receipt['research_ROM'])",
        "digest=sha(rom.read_bytes());manifest=read(rom.with_suffix('.manifest.json'));assert manifest['candidate_sha256']==digest":"digest=sha(rom.read_bytes());assert digest==receipt['research_ROM_sha256'];manifest=dict(profile='research-only-unregistered-item116')",
        'not_a_selected_B203_activation':'not_a_selected_B204_activation',
        'no selected B203 activation':'no selected B204 activation',
    }))
