"""Prepare first B48 current exposure and182 native source/current speech dispatches."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B48_current_effective_tools_v8028')
if __name__=='__main__':
    assert not ROOT.exists()
    results=[derive('scripts/map_Rafael_B47_current_v7980.py','scripts/map_Rafael_B48_current_v8028.py',{
        'Rafael_B47_current_v7980':'Rafael_B48_current_v8028',
        'Rafael_next_clean_v7971/complete_clean_SC0_B47_EV0_andcoverage_before_current_English.json':
            'Rafael_next_clean_v8020/complete_clean_SC0_B48_EV0_andcoverage_before_current_English.json',
        'Rafael_B47_branch_gloss_v7979/15_fresh_glosses_six_source_paths_names_bound_before_current_English.json':
            'Rafael_B48_branch_gloss_v8027/91_fresh_glosses32_paths_B128_B37_context_before_current_English.json',
        'Rafael_B47_names_v7976/four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json':
            'Rafael_B48_names_v8023/nine_static_speakers18_getters_clean_fields36_synthetic_macro_alignments.json',
        "gloss['source_packet_sha256']==sha(SOURCE.read_bytes())":"read(gloss['source_gloss'])['source_packet_sha256']==sha(SOURCE.read_bytes())",
        "gloss['prior_gloss_sha256']":"gloss['source_gloss_sha256']",
        "gloss['all15_complete_clean_Japanese_speeches_read_before_current_English']":
            "gloss['all91_source_glosses_complete_exchange_nine_identities_and32_paths_bound_before_current_English']",
        'Rafael_B47_source_controls_v7977/source_EV0_24_relative_sites120_cases6_raw_predicates25_seeded_ends.json':
            'Rafael_B48_source_controls_v8024/source_EV0_28_relative_sites140_cases5_raw_predicates2_queries25_seeded_ends.json',
        'current_English_B47_bodies_still_unread':'current_English_B48_bodies_still_unread',
        'current_B47_English_bodies_still_unread':'current_B48_English_bodies_still_unread',
        'assert len(rows)==15':'assert len(rows)==91',
        'all15_complete_source_current_refs_before_new_English_manuscript.json':'all91_complete_source_current_refs_before_new_English_manuscript.json',
        'all15_clean_whole_context_glosses_precede_current_English_exposure':'all91_clean_whole_context_glosses_precede_current_English_exposure',
        'source_explicit_completion_dependencies=[37]':'source_explicit_completion_dependencies=[],source_completion_queries=[128,37]',
        'First B47 current-English exposure after15 clean glosses,complete prerequisite,names andnative branch context.':
            'First B48 current-English exposure after91 clean glosses,B128/B37 callbacks,names and32 native source paths.',
    })]
    results.append(derive('scripts/prove_Rafael_B47_effective_v7981.py','scripts/prove_Rafael_B48_effective_v8029.py',{
        'Rafael_B47_effective_v7981':'Rafael_B48_effective_v8029',
        'Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json':
            'Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B47_names_v7976/four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json':
            'Rafael_B48_names_v8023/nine_static_speakers18_getters_clean_fields36_synthetic_macro_alignments.json',
        'all15_clean_whole_context_glosses_precede_current_English_exposure':'all91_clean_whole_context_glosses_precede_current_English_exposure',
        "names['measured_default_macro_ASCII_lengths']":"names['measured_default_macro_lengths']",
        'len(cases)==30 and len(rows)==15':'len(cases)==182 and len(rows)==91',
        "sum(r['source_selector']==254 for r in rows)==0":"sum(r['source_selector']==254 for r in rows)==4",
        'all15_effective_English_templates30_original_progressive_dispatches.json':'all91_effective_English_templates182_original_dispatches4_FE.json',
        'all15_progressive_speakers_andvoices_match':'all87_progressive_speakers_andvoices_match',
        'no_FE_panels_in_B47_all15_progressive':'four_FE_original_null_actor_calls_preserve_zero_source_FE_macros',
        'all15_actual_body_name_bounds_andpagination_pending':'all91_actual_body_name_bounds_andpagination_pending',
        '30 original dispatches/15 effective templates;catalogue matches':'182 original dispatches/91 effective templates;catalogue matches',
        'Bind all15 clean/current B47 speeches through original progressive dispatch in current captain0.':
            'Bind91 clean/current B48 speeches through original captain0 dispatch;four FE panels remain distinct.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',dict(derivations=results,
        source_first_packets_immutable_no_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
    print('Prepared first current B48 comparison and182 native dispatches after complete clean/context proofs.')
