"""Package cumulative V5531 with exact clean-input patch and all broader scope intact."""
from scripts.source_locked_derivation_v5118 import derive

if __name__=='__main__':
    print(derive('scripts/package_lil_B193_v5485.py','scripts/package_lil_B194_v5538.py',{
        'B193':'B194','all_routes_unified_v5478':'all_routes_unified_v5531','V5478':'V5531','V5437':'V5478',
        'completion_text_v5483':'completion_text_v5536','verification_v5484':'verification_v5537','release_v5479':'release_v5532',
        "len(manifest['batches'])==577":"len(manifest['batches'])==578",'len(final[\'records\'])==15':"len(final['records'])==11",
        "{'revise':8,'retain-wording':7}":"{'revise':4,'retain-wording':7}",
        '==6124':'==6135','editorial_scope_v5483':'editorial_scope_v5536',
        'next_Lil_B194_clean_only_v5488':'next_Lil_B195_clean_only_v5540',
        "nextscene['objects']==11":"nextscene['objects']==20",
        "nextscene['conditional21_commands_one_FI_four_relatives_two_C200_opaque632A']":"nextscene['linear23_commands_no_macros_predicates_or_relatives']",
        'combined_v5437':'combined_v5478','All577':'All578',
        '6,124':'6,135','3,867':'3,871','2,257':'2,264','6,127':'6,138','4,525':'4,536',
        "B194's11 clean-only glosses":"B195's20 clean-only glosses",
        'Observe the three-Lady cooking scene if naturally encountered. The two B22 content tests provide focused scene/display evidence;they do not prove natural event193 eligibility,a full route or hardware behavior.':
        'Observe the sake exchange if naturally encountered. Four disclosed B22 content tests cover both unforced availability paths,including the original recruitment setup used to show Julio. They do not prove earned recruitment,natural event194 eligibility,a full route or hardware behavior.',
        "changed_blocks={'/data/SC2.DK4':[193]}":"changed_blocks={'/data/SC2.DK4':[194]}",
        'all577_manifest':'all578_manifest','completed=6124':'completed=6135','source_prose=6127':'source_prose=6138','revised=3867':'revised=3871','retained=2257':'retained=2264','unique_completed_historical_keys=6124':'unique_completed_historical_keys=6135',
        'next11_B194_clean_only_objects_uncredited':'next20_B195_clean_only_objects_uncredited',
        '6124 unique completions;8 revisions/7 retentions':'6135 unique completions;4 revisions/7 retentions',
        'Next11 clean-only objects':'Next20 clean-only objects',
    }))
