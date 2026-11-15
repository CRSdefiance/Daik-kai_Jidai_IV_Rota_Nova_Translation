"""Prepare first whole current-English comparison after clean glosses,names andsource controls."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_current_tools_v7871');assert not root.exists()
    result=derive('scripts/map_Maria_confrontation_current_v7789.py','scripts/map_Rafael_B45_current_v7871.py',{
        'First current-English exposure after all67 clean whole-exchange glosses and native names.':
        'First Rafael B45 current-English exposure after twelve clean glosses,names andsource control binding.',
        'work/analysis/maria_confrontation_current_v7789':'work/analysis/Rafael_B45_current_v7871',
        'work/analysis/maria_next_clean_v7786/complete_clean_SC3_B36_EV3_andcoverage_before_current_English.json':
        'work/analysis/Rafael_next_clean_v7864/complete_clean_SC0_B45_EV0_andcoverage_before_current_English.json',
        'work/analysis/maria_confrontation_gloss_v7787/sixteen_clean_whole_exchange_glosses_before_current_English.json':
        'work/analysis/Rafael_B45_clean_gloss_v7864b/twelve_fresh_clean_exchange_glosses_before_current_English.json',
        'work/analysis/maria_confrontation_names_v7788/three_static_speakers_six_getters_clean_fields_source_macros.json':
        'work/analysis/Rafael_B45_names_v7869/two_static_speakers_four_getters_clean_fields_eight_macro_alignments.json',
        "gloss['all16_fresh_source_glosses_written_before_localized_prose'] and names['current_English_dialogue_bodies_still_unread']":
        "gloss['all12_complete_clean_Japanese_speeches_read_before_current_English'] and names['current_English_B45_bodies_still_unread'] and read('work/analysis/Rafael_B45_source_controls_v7870b/source_EV0_five_relative_sites_predicate_resources_structural_andnormal_end.json')['current_B45_English_bodies_still_unread']",
        '/data/EV3.DK4':'/data/EV0.DK4',
        "row.update(kind='progressive',source_kind='progressive',":
        "row.update(kind='system-FE' if src['source_selector']==254 else 'progressive',source_kind='system-FE' if src['source_selector']==254 else 'progressive',",
        'assert len(rows)==16':'assert len(rows)==12',
        'all16_complete_source_current_refs_before_new_English_manuscript':'all12_complete_source_current_refs_before_new_English_manuscript',
        'all16_clean_whole_context_glosses_precede_current_English_exposure':'all12_clean_whole_context_glosses_precede_current_English_exposure',
        'source_dependency_chain=[35,36],source_EV3_file_preserved_not_natural_activation_approval=True':
        'source_explicit_completion_dependencies=[],source_EV0_file_preserved_not_natural_activation_approval=True',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        all_original_native_high_constants_full_preamble_andwhole_command_mapping_guards_preserved=True,
        source_FE_panel_kept_distinct_from_eleven_progressive_speeches=True,
        no_false44_to45_dependency_chain_invented=True,new_credit=0,full_goal_complete=False))
