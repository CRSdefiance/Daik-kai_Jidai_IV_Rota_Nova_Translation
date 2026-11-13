"""Prepare first English comparison after complete source/name/native review."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B61_B70_current_preparation_v8885')
if __name__=='__main__':
    assert not ROOT.exists()
    changes={
        'First current/effective B31/B53 comparison after clean gloss and full source view.':
            'First current/effective B61-B70 comparison after all224 clean glosses and complete source views.',
        'scripts.Hodram_B31_B53_registered_route_context_v8781':'scripts.Hodram_B54_B60_registered_route_context_v8868',
        'work/analysis/Hodram_B54_B60_current_v8799':'work/analysis/Hodram_B61_B70_current_v8885',
        'work/analysis/Hodram_next_clean_gloss_v8787/82_qualified_clean_glosses_no_unbound_gender_orFA_type.json':
            'work/analysis/Hodram_B61_B70_clean_gloss_v8877/224_complete_clean_first_meanings_all_ten_exchanges_before_current_English.json',
        'work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json':
            'work/analysis/Hodram_B61_B70_source_display_v8881/224_complete_source_dispatches_alignments_pages_andmacro_binding.json',
        'work/analysis/Hodram_B54_B60_source_review_v8798b/source_context_names_display_review_before_current_English.json':
            'work/analysis/Hodram_B61_B70_source_review_v8884/source_context_names_display_review_before_current_English.json',
        'work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json':
            'work/analysis/Hodram_B61_B70_source_controls_v8878/source_controls.json',
        'work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json':
            'work/analysis/Hodram_B61_B70_names_v8879/sixteen_source_identities_current_getters_voices_andplanes.json',
        'work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json':
            'work/analysis/current_V8865_Hodram_native_v8868/current_native_input.json',
        'work/analysis/editorial_handoff_verification_v8790/verified_handoff.json':
            'work/analysis/editorial_handoff_verification_v8876/verified_handoff.json',
        'if __name__==\'__main__\':':
            "BASE_SOURCE=Path('work/analysis/Hodram_next_clean_v8872/complete_clean_SC1_B61_B70_EV1_andcoverage_before_current_English.json')\nif __name__=='__main__':",
        "map(read,[GLOSS,DISPLAY,VIEW,CONTROL,NAMES,INPUT,HANDOFF])":
            "map(read,[GLOSS,DISPLAY,VIEW,CONTROL,NAMES,INPUT,HANDOFF]);base=read(BASE_SOURCE)",
        "verified['completed']==7237":"verified['completed']==7319",
        "view['all82_source_native_pages_and11_sheets_directly_viewed'] and view['existing_B54_B60_English_dialogue_bodies_still_unconsulted']":
            "view['all23_source_sheets224_complete_native_pages_directly_viewed_before_current_English'] and view['current_story_English_dialogue_bodies_still_unconsulted']",
        "view['source_ready_for_current_English_comparison_not_final_localization_orformatting_approval']":
            "view['source_only_no_final_English_localization_formatting_actual_scene_orregistered_release_approval']",
        'all82_clean_utterances_andseven_complete_blocks_read_before_earlier_English':
            'all224_complete_clean_first_meanings_before_current_English',
        'DISPLAY.as_posix()':'str(DISPLAY)',
        'ten_source_selector_voices':'sixteen_source_selector_voices',
        "for source in gloss['groups']:":
            """for original_group,meaning_group in zip(base['groups'],gloss['groups'],strict=True):
        assert original_group['block']==meaning_group['block'] and original_group['clean_block_sha256']==meaning_group['source_block_sha256']
        assert len(original_group['records'])==len(meaning_group['records'])
        for original,meaning in zip(original_group['records'],meaning_group['records'],strict=True):assert all(meaning[k]==v for k,v in original.items())
        source={**original_group,'records':meaning_group['records']}""",
        'if word==0x8000:query_cases.append':'if word in [0x8000,0x8100]:query_cases.append',
        'len(rows)==len(keys)==82 and len(completed)==7237':'len(rows)==len(keys)==224 and len(completed)==7319',
        'len(relative_cases)==24 and len(query_cases)==6':'len(relative_cases)==60 and len(query_cases)==15',
        'all82_source_units_uncredited_in_current_ledger':'all224_source_units_uncredited_in_current_ledger',
        'complete152commands82preambles24relative_targets6queries33nonprose_controls_and7normal_ends_bound':
            'complete392commands224preambles60relative_targets15queries83nonprose_controls_and10normal_ends_bound',
        'source_native_calls_reused_exact_same_own8778_context_not_replayed':'source_native_calls_reused_exact_same_own8865_context_not_replayed',
        '[GLOSS,DISPLAY,VIEW,CONTROL,NAMES,INPUT,HANDOFF,Path(__file__)]':'[GLOSS,BASE_SOURCE,DISPLAY,VIEW,CONTROL,NAMES,INPUT,HANDOFF,Path(__file__)]',
        'First current comparison:82fresh dispatches/120relative cases/6unforcedqueries;152commands fully mapped':
            'First current comparison:224fresh dispatches/300relative cases/15unforcedqueries;392commands fully mapped'
    }
    result=derive('scripts/map_Hodram_B54_B60_current_v8799.py','scripts/map_Hodram_B61_B70_current_v8885.py',changes)
    ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        complete_source_current_commands_preambles_relative_targets_dispatches_actor_voice_catalogue_andcoverage_guards_preserved=True,
        query_scope_includes_original8100_event44_check_not_just8000=True,
        comparison_requires_all224_clean_meanings_and23_native_sheets_first=True,
        current_English_not_exposed_by_preparer=True,new_credit=0,full_goal_complete=False))
    print('Prepared first complete224 current English comparison; no dialogue body exposed yet.')
