"""Prepare sixteen-speaker native names review without reading story English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/Hodram_B61_B70_names_preparation_v8879')
if __name__=='__main__':
    assert not ROOT.exists()
    changes={
        'Bind ten source identities and current native names/voices; no scene or full-catalogue claim.':
            'Bind sixteen source identities and current native names/voices; no scene or full-catalogue claim.',
        'scripts.Hodram_B31_B53_registered_route_context_v8781':'scripts.Hodram_B54_B60_registered_route_context_v8868',
        'work/analysis/Hodram_B54_B60_names_v8792':'work/analysis/Hodram_B61_B70_names_v8879',
        'work/analysis/Hodram_next_clean_gloss_v8787/82_qualified_clean_glosses_no_unbound_gender_orFA_type.json':
            'work/analysis/Hodram_B61_B70_clean_gloss_v8877/224_complete_clean_first_meanings_all_ten_exchanges_before_current_English.json',
        'work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json':
            'work/analysis/Hodram_B61_B70_source_controls_v8878/source_controls.json',
        'work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json':
            'work/analysis/current_V8865_Hodram_native_v8868/current_native_input.json',
        'work/analysis/Hodram_B31_B53_registered_startup_view_v8782/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json':
            'work/analysis/Hodram_B54_B60_registered_startup_view_v8869/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json',
        'current_B54_B60_English_dialogue_bodies_still_unconsulted':'current_B61_B70_English_dialogue_bodies_still_unconsulted',
        'all82_clean_utterances_andseven_complete_blocks_read_before_earlier_English':
            'all224_complete_clean_first_meanings_before_current_English',
        'actors==[1,20,23,24,36,84,113,114,119,141]':'actors==[1,2,3,9,10,16,17,18,20,23,24,38,78,105,116,154]',
        "sum(r['source_selector']==254 for g in gloss['groups'] for r in g['records'])==1":
            "sum(r['source_selector']==254 for g in gloss['groups'] for r in g['records'])==0",
        'all_twenty_original_consumers_and_owned_or_readonly_memory_paths_exact':
            'all_thirtytwo_original_consumers_and_owned_or_readonly_memory_paths_exact',
        "len(getters['rows'])==20 and len(voices['rows'])==10":
            "len(getters['rows'])==32 and len(voices['rows'])==16",
        'ten_actor_current_names.png':'sixteen_actor_current_names.png',
        'ten_source_identities_current_getters_voices_andplanes.json':'sixteen_source_identities_current_getters_voices_andplanes.json',
        'ten_clean_ordinary_given_getters':'sixteen_clean_ordinary_given_getters',
        'fresh_twenty_progressive_andfull_current_getters':'fresh_thirtytwo_progressive_andfull_current_getters',
        'ten_source_selector_voices':'sixteen_source_selector_voices',
        'current_B54_B60_English_dialogue_bodies_unconsulted':'current_B61_B70_English_dialogue_bodies_unconsulted',
        'Ten clean given identities /20 current original getters/10voices/':
            'Sixteen clean given identities /32 current original getters/16voices/'
    }
    result=derive('scripts/prove_Hodram_B54_B60_names_v8792.py','scripts/prove_Hodram_B61_B70_names_v8879.py',changes)
    ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        original_name_getter_write_ownership_full_memory_ABI_style11_andpixel_guards_preserved=True,
        full_source_name_composition_editorial_decisions_andactual_headers_pending=True,
        new_credit=0,full_goal_complete=False))
    print('Prepared sixteen-speaker/32-current-getter native review; no names tests executed yet.')
