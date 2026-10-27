"""Re-execute303 source/current cache loads and606 original parent modes per image."""
from pathlib import Path
SOURCE=Path('scripts/verify_lil_london_loader_v1902.py')
if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    changes=[
        ('from scripts.prepare_lil_london_research_v1901 import ROM, PARENT',"from scripts.approve_maria_B109_native_v3520 import ROM\nPARENT=Path('out/all_routes_combined_v3487_candidate.nds')"),
        ('lil_London_loader_v1902','maria_B109_loader_v3521'),
        ('work/analysis/lil_London_research_v1901/research_image_receipt.json','work/analysis/maria_B109_native_approval_v3520/approval_and_production_scope_research_receipt.json'),
        ('/data/SC2.DK4','/data/SC3.DK4'),('expected == 336','expected == 303'),('for route in (2,):','for route in (3,):'),
        ('whole_SC2_loads_and_cache_hits','whole_SC3_loads_and_cache_hits'),
        ('whole_SC2_and_B26_initial_entry_proof.json','whole_SC3_and_B109_initial_entry_proof.json'),
        ('all336_whole_blocks_and672_modes_each_pass','all303_whole_blocks_and606_modes_each_pass'),
        ('B26_block_fits_original_0x2400_cache','B109_CS0101_fits_original_0x2400_cache'),
        ('original_EV2_actions_select_by_block_index_without_interior_byte_offset','original_EV3_actions_select_by_block_index_without_interior_byte_offset'),
        ('336 original loads/cache hits and672 parent entry modes','303 original loads/cache hits and606 parent entry modes'),
        ('later London path approval pending.','B109 content display is separately covered by the explicit B33 entry fixture.')]
    for a,b in changes:assert a in text,a;text=text.replace(a,b)
    exec(compile(text,str(SOURCE)+'::Maria-B109','exec'),{'__name__':'__main__','__file__':__file__})
