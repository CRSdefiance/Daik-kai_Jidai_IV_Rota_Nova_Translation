"""Qualify the original clean-name fixtures for this sixteen-speaker scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/Hodram_B61_B70_clean_names_preparation_v8880')
if __name__=='__main__':
    assert not ROOT.exists()
    changes={
        'work/analysis/Hodram_B54_B60_clean_names_v8793':'work/analysis/Hodram_B61_B70_clean_names_v8880',
        'work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json':
            'work/analysis/Hodram_B61_B70_names_v8879/sixteen_source_identities_current_getters_voices_andplanes.json',
        'current_B54_B60_English_dialogue_bodies_unconsulted':'current_B61_B70_English_dialogue_bodies_unconsulted',
        'all_twenty_clean_original_consumers_and_owned_or_readonly_memory_paths_exact':
            'all_thirtytwo_clean_original_consumers_and_owned_or_readonly_memory_paths_exact',
        "len(getters['rows'])==20":"len(getters['rows'])==32",
        'fresh_twenty_progressive_andfull_current_getters':'fresh_thirtytwo_progressive_andfull_current_getters',
        "esp=next(r for r in bindings if r['actor_ID']==36 and r['consumer']=='full-catalogue');assert 'デ' in esp['clean_text'] and 'デ' in esp['current_text']":
            """assert len(actors)==16 and set(actors)=={1,2,3,9,10,16,17,18,20,23,24,38,78,105,116,154}
    by_key={(r['actor_ID'],r['consumer']):r for r in bindings}
    assert by_key[154,'progressive-nameplate']['clean_text']=='水夫' and by_key[154,'full-catalogue']['clean_text']=='配下'
    assert by_key[154,'progressive-nameplate']['current_text']=='Sailor' and by_key[154,'full-catalogue']['current_text']=='Retainer'
    assert by_key[3,'full-catalogue']['clean_text']=='マリア・ホアメイ・リー' and by_key[3,'full-catalogue']['current_text']=='Maria Huamei Li'
    assert by_key[9,'full-catalogue']['clean_text']=='カミル・マリヌス・オーフェルアイセル' and by_key[9,'full-catalogue']['current_text']=='Camille Marinus Overijssel'
    for ident,role in [(105,'交易所の親父'),(116,'出港所の兄貴')]:
        assert by_key[ident,'progressive-nameplate']['clean_text']==by_key[ident,'full-catalogue']['clean_text']==role""",
        'twenty_clean_full_andprogressive_compositions_current_binding.json':'thirtytwo_clean_full_andprogressive_compositions_current_binding.json',
        'Geronimo_middle_component_actual_source_fullgetter_contains_de_kana_not_unused=True,':
            'scoped_actor154_progressive_sailor_andfull_retainer_distinction_preserved=True,',
        'Geronimo_untranslated_current_middle_component_requires_ownership_consumer_andeditorial_review=True,':
            'Camille_Marinus_middle_component_is_source_composed_not_automatically_unused_orlegal_name_approval=True,',
        '20clean original name compositions/current binding pass;all constructor/ring writes reversed. Generic regional fields unused inlabels;Geronimo デ iscomposed inactual fullgetter. No gameplay,ROM orcredit.':
            '32clean original name compositions/current binding pass;all constructor/ring writes reversed. Generic regional fields unused inlabels;Maria full name andCamille middle field bound;154 source consumer distinction preserved. No gameplay,ROM orcredit.'
    }
    result=derive('scripts/prove_Hodram_B54_B60_clean_fullnames_v8793.py','scripts/prove_Hodram_B61_B70_clean_fullnames_v8880.py',changes)
    ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        all_source_instruction_constructor_ring_write_ownership_andwhole_memory_inverse_guards_preserved=True,
        changed_scope_identity_assertions_bound_to_complete_clean_andcurrent_getters=True,
        out_of_scope_Geronimo_Alonso_ownership_lead_preserved=True,new_credit=0,full_goal_complete=False))
    print('Prepared 32 clean-source composition cases; not executed yet.')
