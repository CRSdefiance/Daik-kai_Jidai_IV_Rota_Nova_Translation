"""Bind complete13-plane native tests to exact B207 actors/prose/current context."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B207_font_tools_v6361')
if __name__=='__main__':
    assert not ROOT.exists();row=derive('scripts/verify_lil_B206_fonts_v6295.py','scripts/verify_lil_B207_fonts_v6361.py',{
      'B206':'B207','fonts_v6295':'fonts_v6361','editorial_manuscript_v4.json':'editorial_manuscript_v4.json',
      'len(cases)==24 and calls==192':'len(cases)==13 and calls==104',"sum(bool(r['reviewed_ordinary_boundaries']) for r in cases)==2":"sum(bool(r['reviewed_ordinary_boundaries']) for r in cases)==1",
      '.blocks[206]':'.blocks[207]','blocks[206]':'blocks[207]','for selector in [2,7,173]':'for selector in [2,14]',"format(7 if selector==2 else 2,'02X')":"format(14 if selector==2 else 2,'02X')",
      'all24_progressive_complete_native_planes192_alignment_cases':'all13_progressive_complete_native_planes104_alignment_cases',
      'current_original_macro_alignment_calls=192':'current_original_macro_alignment_calls=104','complete_progressive_planes=24':'complete_progressive_planes=13','original_alignment_calls=192':'original_alignment_calls=104',
      'source_three_static_actors_zero_macros_and_separate_four_approved_menu_labels':'source_two_static_actors_zero_macros_no_FE_menus_or_branches',
      '24 complete current-native progressive planes and192 original alignment calls;four menus separate.':'13 complete current-native progressive planes and104 original alignment calls;no FE,menus or branches.'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_complete_native_font_tools.json',dict(tool=row,source_speeches=13,current_native_alignment_cases=104,source_static_actors=[2,14],one_exact_source_ordinary_it_if_boundary=True,no_inherited_B206_actor_menu_FE_macro_or_boundary_case=True,original_font_216x64_sixpx_four_rows_guards_pair_phase_and_native_addresses_preserved=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('B20713 complete native-plane/104 alignment-case verifier prepared with current strict input and original glyph/address guards.')
