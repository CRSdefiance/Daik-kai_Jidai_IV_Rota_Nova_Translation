"""Prepare first B47 current exposure only after complete clean glosses,names andbranches."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_current_tools_v7980')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/map_Rafael_B45_current_v7871.py','scripts/map_Rafael_B47_current_v7980.py',{
        'Rafael_B45_current_v7871':'Rafael_B47_current_v7980',
        'Rafael_next_clean_v7864/complete_clean_SC0_B45_EV0_andcoverage_before_current_English.json':
            'Rafael_next_clean_v7971/complete_clean_SC0_B47_EV0_andcoverage_before_current_English.json',
        'Rafael_B45_clean_gloss_v7864b/twelve_fresh_clean_exchange_glosses_before_current_English.json':
            'Rafael_B47_branch_gloss_v7979/15_fresh_glosses_six_source_paths_names_bound_before_current_English.json',
        'Rafael_B45_names_v7869/two_static_speakers_four_getters_clean_fields_eight_macro_alignments.json':
            'Rafael_B47_names_v7976/four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json',
        "names['source_gloss_sha256']==sha(GLOSS.read_bytes())":"names['source_gloss_sha256']==gloss['prior_gloss_sha256']",
        "gloss['all12_complete_clean_Japanese_speeches_read_before_current_English']":
            "gloss['all15_complete_clean_Japanese_speeches_read_before_current_English']",
        'current_English_B45_bodies_still_unread':'current_English_B47_bodies_still_unread',
        'Rafael_B45_source_controls_v7870b/source_EV0_five_relative_sites_predicate_resources_structural_andnormal_end.json':
            'Rafael_B47_source_controls_v7977/source_EV0_24_relative_sites120_cases6_raw_predicates25_seeded_ends.json',
        'current_B45_English_bodies_still_unread':'current_B47_English_bodies_still_unread',
        'assert len(rows)==12':'assert len(rows)==15',
        'all12_complete_source_current_refs_before_new_English_manuscript.json':'all15_complete_source_current_refs_before_new_English_manuscript.json',
        'all12_clean_whole_context_glosses_precede_current_English_exposure':'all15_clean_whole_context_glosses_precede_current_English_exposure',
        'source_explicit_completion_dependencies=[]':'source_explicit_completion_dependencies=[37]',
        'First Rafael B45 current-English exposure after twelve clean glosses,names andsource control binding.':
            'First B47 current-English exposure after15 clean glosses,complete prerequisite,names andnative branch context.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared15-record first-current comparison;prior source-first proof remains immutable.')
