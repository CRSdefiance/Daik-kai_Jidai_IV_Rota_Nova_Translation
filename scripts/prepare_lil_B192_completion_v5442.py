"""Prepare exact six-target completion with fully reversible earlier history."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B192_completion_tools_v5442')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/complete_lil_B191_v5401.py');text=source.read_text(encoding='utf-8')
    a=text.index("    assert len(transitions['sampled_postscene_whole_RGB_differences_unmasked'])");b=text.index("    assert transitions['whole_RGB_final9001_equal']",a)
    measured="    assert len(transitions['sampled_postscene_whole_RGB_differences_unmasked'])==7 and not transitions['all_sampled_postscene_whole_RGB_equal'] and transitions['nine_timing_seven_original_indicator_and_unequal_PRNG_differences_retained_without_masking_retiming_or_equivalence_claim']\n"
    c=text.index("        inventory['B191_exact_R64_wrap_and_original_no_effect_path']");e=text.index("        for unit in inventory['broader_coverage_units']:",c)
    row=derive(source,'scripts/complete_lil_B192_v5442.py',{
        text[a:b]:measured,text[c:e]:'',
        'B191':'B192','Thirteen':'Eight','thirteen':'eight','completion_v5401':'completion_v5442','verification_v5402':'verification_v5443',
        'manuscript_v5':'manuscript_v4','release_v5397':'release_v5438','startup_v5399':'startup_v5440','registration_v5395':'registration_v5436',
        'actual_v5389/actual_all13_progressive_FE_RNG_effect_or_no_effect_C200_and_single_end':'actual_v5431/actual_all8_progressive_FE_A000_C200_and_single_end',
        'actual_review_v5390/all13_panels_20_fullscreens_no_effect_path':'actual_review_v5432/all8_panels26_fullscreens_linear_return',
        'verification_v5352':'verification_v5402','B192_clean_context_v5405/all8':'B193_clean_context_v5446/all15',
        'Lil-B191-dye-buyout-pitch-repeated-doubt-kinship-free-profit-and-prospective-Calicut13':'Lil-B192-tobacco-question-reversal-hesitation-offer-and-prospective-Istanbul8',
        'editorial_scope_v5401':'editorial_scope_v5442','B191_v5401':'B192_v5442','completion_text_v5401':'completion_text_v5442',
        'all575':'all576','V5346':'V5396',"reg['negative_count']==99":"reg['negative_count']==75",
        "sum(len(r['holds']) for r in actual['actual_panels'])==51":"sum(len(r['holds']) for r in actual['actual_panels'])==31",
        '[5977,5975]':'[4775,4777]','dict(total=12,speech=10,control_or_end=2)':'dict(total=9,speech=7,control_or_end=2)',
        '[759362961,1803218166]':'[790984746,3723009301]','regressions_v5396':'regressions_v5437',"len(manifest['batches'])==575":"len(manifest['batches'])==576",
        'retention_v5400':'retention_v5441',"len(source['records'])==8":"len(source['records'])==15",'[-13:]':'[-8:]',
        "{'revise':5,'retain-wording':8}":"{'revise':5,'retain-wording':3}",'blocks[191]':'blocks[192]','block=191':'block=192','blocks=[191]':'blocks=[192]',
        '6088':'6101','6101':'6109','6104':'6112','3854':'3859','2247':'2250','4203':'4216','4216':'4224','4502':'4510',
        'retained=8':'retained=3','retained_count=8':'retained_count=3','fresh_retentions=8':'fresh_retentions=3','justified_retentions=8':'justified_retentions=3',
        'actual_matching_holds=51':'actual_matching_holds=31','all13':'all8','exactly13':'exactly8','==13':'==8','=13':'=8',
        'event191':'event192','source191':'source192',
        'no_record_specific_ordinary_boundary_exception_required=False,exact_source_prose_R64_after_be_boundary_reviewed=True':'no_record_specific_ordinary_boundary_exception_required=True',
        'editorial_scope_v5351':'editorial_scope_v5401',"inventory.pop('next_Lil_B191_clean_only_v5355')":"inventory.pop('next_Lil_B192_clean_only_v5405')",
        "inventory['next_Lil_B192_clean_only_v5405']":"inventory['next_Lil_B193_clean_only_v5446']",
        'objects=8,uncredited=True,linear11_commands_no_predicates_or_relatives=True':'objects=15,uncredited=True,linear18_commands_no_predicates_or_relatives=True',
        'Lil_B192_clean_only_uncredited_objects=8':'Lil_B193_clean_only_uncredited_objects=15',
        '## V5401:':'## V5442:','cumulative V5396':'cumulative V5437','handoff - V5401':'handoff - V5442',
        'new_clean_only_Lil_B192_uncredited_objects=8':'new_clean_only_Lil_B193_uncredited_objects=15',
        'twelve_timings_four_indicators_unequal_PRNG_and_original_no_effect_path_preserved':'nine_timings_seven_indicators_and_unequal_PRNG_preserved',
        'V5396 integration verified;':'V5437 integration verified;','Eight B192 clean-only glosses pending':'Fifteen B193 clean-only glosses pending',
    })
    old,new=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert old-new==Counter({759362961:1,1803218166:1}) and new-old==Counter({790984746:1,3723009301:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_reversible_completion.json',dict(derivation=row,source_full_nested_history_inverse_preserved=True,
        expected_completed=6109,expected_source_prose=6112,revisions=3859,retentions=2250,SC2=4224,routes=4510,new_keys=8,next_clean_only=15,full_goal_complete=False))
