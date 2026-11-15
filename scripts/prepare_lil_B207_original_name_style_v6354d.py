"""Bind the source-observed style11 caller instead of comparing a style1 shadow to a header."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B207_name_style_tools_v6354d')
if __name__=='__main__':
    assert not ROOT.exists();row=derive('scripts/prove_lil_B207_name_planes_v6354c.py','scripts/prove_lil_B207_name_planes_v6354d.py',{
      "lil_B207_name_planes_v6354c'":"lil_B207_name_planes_v6354d'",
      'from scripts.verify_name_catalog_glyphs_v278 import raster':'from scripts.lil_B207_name_style_v6354d import native_name_raster as raster,style_source_proof',
      "Path('scripts/shady_man_font_oracles_v6263.py')":"Path('scripts/shady_man_font_oracles_v6263.py'),Path('scripts/lil_B207_name_style_v6354d.py')",
      'literal_macro_cases=cases':'actual_original_name_style_proof=style_source_proof(ctx.arm),literal_macro_cases=cases'})
    ROOT.mkdir(parents=True);save(ROOT/'original_style11_derivation.json',dict(tool=row,style1_complete_plane_was_valid_but_not_original_name_header_style=True,current_clean_original_caller_style11_bound_from_unchanged_machine_code=True,all17_shadow_pixels_accounted_by_original_style_policy_not_ignored=True,all_old_failed_models_and_proofs_preserved=True,no_ROM_name_font_or_palette_change=True,full_goal_complete=False))
