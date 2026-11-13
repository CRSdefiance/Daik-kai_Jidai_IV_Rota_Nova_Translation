"""Prepare all source/current progressive dispatch checks before B47 editorial decisions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_effective_tools_v7981')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/prove_Rafael_B46_effective_v7928.py','scripts/prove_Rafael_B47_effective_v7981.py',{
        'Rafael_B46_effective_v7928':'Rafael_B47_effective_v7981',
        'Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json':
            'Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json':
            'Rafael_B47_names_v7976/four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json',
        'all26_clean_whole_context_glosses_precede_current_English_exposure':'all15_clean_whole_context_glosses_precede_current_English_exposure',
        'len(cases)==48 and len(rows)==24':'len(cases)==30 and len(rows)==15',
        "sum(r['source_selector']==254 for r in rows)==12":"sum(r['source_selector']==254 for r in rows)==0",
        'all24_effective_English_templates48_original_dispatches12_FE.json':'all15_effective_English_templates30_original_progressive_dispatches.json',
        'all12_progressive_speakers_andvoices_match':'all15_progressive_speakers_andvoices_match',
        'all12_FE_original_null_actor_calls_preserve_zero_macros':'no_FE_panels_in_B47_all15_progressive',
        'FE_actual_modes_buttons_bounds_andpagination_pending':'all15_actual_body_name_bounds_andpagination_pending',
        "'48 original dispatches/24 effective templates;catalogue matches'":"'30 original dispatches/15 effective templates;catalogue matches'",
        'Bind all24 clean/current B46 speeches through current captain0 dispatch;12 FE panels stay separate.':
            'Bind all15 clean/current B47 speeches through original progressive dispatch in current captain0.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared30 source/current progressive dispatch checks forB47.')
