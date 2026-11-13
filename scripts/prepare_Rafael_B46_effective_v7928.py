"""Prepare current captain0 dispatch checks for the complete B46 speech set."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_effective_tools_v7928');assert not root.exists()
    row=derive('scripts/prove_Rafael_B45_effective_v7872.py','scripts/prove_Rafael_B46_effective_v7928.py',{
        'Bind all twelve clean/current speeches through current captain0 dispatch; FE stays separate.':'Bind all24 clean/current B46 speeches through current captain0 dispatch;12 FE panels stay separate.',
        'Rafael_B45_effective_v7872':'Rafael_B46_effective_v7928',
        'Rafael_B45_current_v7871/all12_complete_source_current_refs_before_new_English_manuscript.json':'Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B45_names_v7869/two_static_speakers_four_getters_clean_fields_eight_macro_alignments.json':'Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json',
        'all12_clean_whole_context_glosses_precede_current_English_exposure':'all26_clean_whole_context_glosses_precede_current_English_exposure',
        "count(b'Castor Co.')==1":"count(b'Castor Co.')==0",
        'len(cases)==24 and len(rows)==12':'len(cases)==48 and len(rows)==24',
        "sum(r['source_selector']==254 for r in rows)==1":"sum(r['source_selector']==254 for r in rows)==12",
        'all12_effective_English_templates24_original_dispatches_distinct_FE.json':'all24_effective_English_templates48_original_dispatches12_FE.json',
        'all11_progressive_speakers_andvoices_match':'all12_progressive_speakers_andvoices_match',
        'one_FE_original_null_actor_macro_call_expands_source_FO':'all12_FE_original_null_actor_calls_preserve_zero_macros',
        'FE_actual_panel_percent_bounds_andpagination_pending':'FE_actual_modes_buttons_bounds_andpagination_pending',
        "'24 original dispatches/12 effective templates;catalogue matches'":"'48 original dispatches/24 effective templates;catalogue matches'",
    })
    root.mkdir(parents=True);save(root/'source_locked_derivation.json',row)
