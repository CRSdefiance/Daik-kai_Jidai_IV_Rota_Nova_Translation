"""Bind relocated consumers to the strict current runtime; do not force conditions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_relocated_control_tools_v7105')
if __name__=='__main__':
    assert not ROOT.exists()
    source='scripts/prove_lil_B214_relocated_controls_v6721.py'
    target='scripts/prove_lil_B223_relocated_controls_v7105.py'
    changes={
      'B214':'B223','relocated_controls_v6721':'relocated_controls_v7105',
      'Al_Ferid_exact_native_context_v6520':'square_shopkeeper_exact_native_context_v7020',
      'reference_v6718':'reference_v7102','source_v6697':'source_v7078','consumers_v6698':'consumers_v7079',
      'controls_v6708/four_unforced_predicates_ten_structural_cases50_seeded_ends_four_route_models':'controls_v7082/two_unforced_predicate_cases_ten_structural_cases50_seeded_ends_two_route_models',
      'blocks[214]':'blocks[223]','block=214':'block=223','len(block)==1304':'len(block)==1384',
      '{2:3,4:0,23:7,208:4}':'{2:3,13:0,21:1,208:4}',
      '[(882,892,2,0),(1164,1150,0,2)]':'[(1138,1178,2,2)]',
      'block[1298:]==bytes(6)':'block[1380:]==bytes(4)',
      "ctx.arm,block,1298,previous":"ctx.arm,block,1380,previous",
      'seventeen_dispatches207_style_pointers_two_alignment_swaps_five_effects25_ends':'seventeen_dispatches207_style_pointers_one_unforced_predicate_five_effects25_ends',
      'original_static_voices3_0_7_and_D0_fallback4':'original_static_voices3_0_1_and_D0_fallback4',
      'both_opposite_operand_alignment_changes_original_owned_scratch_only_restores4MiB':'one_same_alignment_predicate_original_owned_scratch_only_restores4MiB',
      'both_native_predicates_type2_Boolean0_without_forcing':'one_native_predicate_type2_Boolean0_without_forcing',
      'target_end1298_state0_retains_existing_value_word_and_tail2':'target_end1380_state0_retains_existing_value_word_no_tail',
      'all27_commands_eight_relatives_typed_aliases_two_predicates_staging_A000_and_end':'all22_commands_four_relatives_typed_aliases_one_predicate_staging_A000_and_end',
      'both opposite alignment changes':'one original unforced predicate with unchanged alignment',
      'both changed operand alignments':'the original predicate operand alignment',
    }
    assert not Path(target).exists();checked_text(Path(source).read_text('utf8'),changes)
    row=derive(source,target,changes);ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_tool.json',dict(tool=row,no_native_address_change=True,no_role_state_or_result_forced=True,new_credit=0,full_goal_complete=False))
