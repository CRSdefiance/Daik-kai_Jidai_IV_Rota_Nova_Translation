"""Prepare reversible six-target completion while retaining the entire old ledger."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B193_completion_tools_v5483')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/complete_lil_B192_v5442c.py');text=source.read_text(encoding='utf-8')
    a=text.index("    assert len(transitions['sampled_postscene_whole_RGB_differences_unmasked'])");b=text.index("    assert transitions['whole_RGB_final9001_equal']",a)
    measured="    assert not transitions['sampled_postscene_whole_RGB_differences_unmasked'] and transitions['all_sampled_postscene_whole_RGB_equal'] and transitions['ten_speech_timing_differences_retained_without_masking_retiming_or_equivalence_claim'] and transitions['three_distinct_original_Lady_portraits_and_four_row_explanation_cooking_offer_and_friendship_observed']\n"
    inventory="""        term=Path(doc['actor_terminology_reconciliation'])
        inventory['legacy_UI_Chili29_older_fidelity_review_open']=dict(path=str(term),sha256=sha(term.read_bytes()),source='トウガラシ',UI='Chili',source_supported_scene_prose='chili peppers',no_UI_rename_or_new_widget_fidelity_credit=True)
"""
    row=derive(source,'scripts/complete_lil_B193_v5483.py',{
        text[a:b]:measured,'B192':'B193','eight':'fifteen','Eight':'Fifteen','completion_v5442':'completion_v5483','verification_v5443':'verification_v5484',
        'release_v5438':'release_v5479','startup_v5440':'startup_v5481','registration_v5436':'registration_v5477',
        'actual_v5431/actual_all8':'actual_v5472/actual_all15','actual_review_v5432/all8_panels26_fullscreens_linear_return':'actual_review_v5473/all15_panels12_fullscreens_three_Ladies_return',
        'verification_v5402':'verification_v5443','B193_clean_context_v5446/all15':'B194_clean_context_v5488/all11',
        'Lil-B192-tobacco-question-reversal-hesitation-offer-and-prospective-Istanbul8':'Lil-B193-three-Ladies-cooking-reported-spice-price-concern-friendship-and-prospective-Seoul15',
        'editorial_scope_v5442':'editorial_scope_v5483','B192_v5442':'B193_v5483','completion_text_v5442':'completion_text_v5483',
        'all576':'all577','V5396':'V5437',"reg['negative_count']==75":"reg['negative_count']==76", "sum(len(r['holds']) for r in actual['actual_panels'])==31":"sum(len(r['holds']) for r in actual['actual_panels'])==59",
        '[4775,4777]':'[6457,6457]','dict(total=9,speech=7,control_or_end=2)':'dict(total=10,speech=10,control_or_end=0)',
        '[790984746,3723009301]':'[463267532,463267532]',"and not transitions['PRNG_equality']":"and transitions['PRNG_equality']",
        'regressions_v5437':'regressions_v5478',"len(manifest['batches'])==576":"len(manifest['batches'])==577",'retention_v5441':'retention_v5482',
        "len(source['records'])==15":"len(source['records'])==11",'[-8:]':'[-15:]',"{'revise':5,'retain-wording':3}":"{'revise':8,'retain-wording':7}",
        'blocks[192]':'blocks[193]','block=192':'block=193','blocks=[192]':'blocks=[193]',
        '6101':'6109','6109':'6124','6112':'6127','3859':'3867','2250':'2257','4216':'4224','4224':'4239','4510':'4525',
        'revised=5':'revised=8','revised_count=5':'revised_count=8','fresh_revisions=5':'fresh_revisions=8','new_revisions=5':'new_revisions=8',
        'retained=3':'retained=7','retained_count=3':'retained_count=7','fresh_retentions=3':'fresh_retentions=7','justified_retentions=3':'justified_retentions=7',
        'actual_matching_holds=31':'actual_matching_holds=59','all8':'all15','exactly8':'exactly15','==8':'==15','=8':'=15',
        'event192':'event193','source192':'source193','editorial_scope_v5401':'editorial_scope_v5442',
        'Lil_B192_completed_v5442':'Lil_B193_completed_v5483','historical_Lil_B192_clean_only_before_v5442':'historical_Lil_B193_clean_only_before_v5483',
        "inventory.pop('next_Lil_B192_clean_only_v5405')":"inventory.pop('next_Lil_B193_clean_only_v5446')",
        "inventory['next_Lil_B193_clean_only_v5446']":"inventory['next_Lil_B194_clean_only_v5488']",
        'objects=15,uncredited=True,linear18_commands_no_predicates_or_relatives=True':'objects=11,uncredited=True,conditional21_commands_one_FI_four_relatives_two_C200_opaque632A=True',
        'Lil_B193_clean_only_uncredited_objects=15':'Lil_B194_clean_only_uncredited_objects=11',
        "        for unit in inventory['broader_coverage_units']:":inventory+"        for unit in inventory['broader_coverage_units']:",
        '## V5442:':'## V5483:','cumulative V5437':'cumulative V5478','handoff - V5442':'handoff - V5483',
        'new_clean_only_Lil_B193_uncredited_objects=15':'new_clean_only_Lil_B194_uncredited_objects=11',
        'nine_timings_seven_indicators_and_unequal_PRNG_preserved':'ten_speech_timings_and_measured_postscene_RGB_PRNG_scope_preserved',
        'V5437 integration verified;':'V5478 integration verified;','Fifteen linear B193 clean-only glosses pending':'Eleven conditional B194 clean-only glosses pending'} )
    old,new=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert old-new==Counter({790984746:1,3723009301:1}) and new-old==Counter({463267532:2})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_reversible_completion.json',dict(derivation=row,full_nested_history_inverse_preserved=True,
        expected_completed=6124,expected_source_prose=6127,revisions=3867,retentions=2257,SC2=4239,routes=4525,new_keys=15,next_clean_only=11,full_goal_complete=False))
