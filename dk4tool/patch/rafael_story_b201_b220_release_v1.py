"""Register the 403 source-bound speech and caption reviews in Rafael B201–B220."""
import inspect
from pathlib import Path

from dk4tool.patch import rafael_story_b141_b160_release_v1 as common
from scripts.source_locked_derivation_v5118 import checked_text


qualification=checked_text(inspect.getsource(common.qualify_evidence),{
    "names['all20_individual_five_gates_pass_for_public_nameplanes'] and len(names['records'])==conf['scoped_name_count']==20":
        "names['all_individual_five_gates_pass_for_public_nameplanes'] and len(names['records'])==conf['scoped_name_count']==41",
    "==conf['native_pages']==558 and visual['all558_body_pages_8_captions_20_public_names_approved']":
        "==conf['native_pages']==383 and visual['all_body_caption_andname_planes_approved']",
    "visual['all193_final_observed_pages_andfour_menus_directly_viewed']":
        "visual['all_actual_pages_and_menus_directly_viewed']",
    "stored['total_relocated_native_relative_cases']==conf['relative_cases']==1190":
        "stored['fresh_relocated_native_relative_cases']==conf['relative_cases']==520",
    "conf['speech_count']==549":"conf['speech_count']==382",
    "conf['FE_count']==6":"conf['FE_count']==34",
    "len(lookup['records'])==549":"len(lookup['records'])==382",
    '(343,2,684)':'(343,40,646)',
    "conf['typed_choice_count']==8 and len(stored['typed_objects'])==len(menu['menus'])==conf['menu_count']==4":
        "conf['typed_choice_count']==21 and len(stored['typed_objects'])==len(menu['menus'])==conf['menu_count']==10",
    "not stored['style_records']":"not stored.get('style_records')",
    "'all four stored choice objects and no personality objects'":"'all ten stored choice objects and no personality objects'",
    """        path=Path(obj['native_proof']);proof=load(path)
        require(sha(path.read_bytes())==obj['native_proof_sha256'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
            and proof['source_index_andcount_preserved'] and len(proof['compiler_negatives_rejected'])==7,'complete caption proof, indices and negatives')
        require((proof['native_provider_alignments'],proof['bridged_modal_returns'],proof['complete_English_caption_style_planes'])==(6,18,8),
            'native menu alignments, styles and returns')""":
        """        path=Path(obj['native_receipt']);proof=load(path)
        require(sha(path.read_bytes())==obj['native_receipt_sha256'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'],
            'exact native caption proof')
        count=len(obj['record_IDs'])
        require((obj['source_word'],count) in ((0x2100,2),(0x2200,3)), 'original choice word and label count')
        require((proof['native_provider_alignments'],proof['bridged_modal_returns'],proof['complete_English_caption_style_planes'])==
            (6,6*(count+1),4*count),'native alignments, styles and bridged returns')
        require(sum(r['version']=='reviewed-English' for r in proof['records'])==2*count,'both reviewed caption styles')
        if count==2:
            require(proof['source_index_andcount_preserved'] and len(proof['compiler_negatives_rejected'])==7,
                'two original menu indices and compiler negatives')
        else:
            original,=proof['menus']
            negatives,=proof['compiler_negatives_rejected']
            require((original['block'],original['source_command_offset'],original['record_IDs'])==
                (209,230,obj['record_IDs']) and original['target_object_hex']==obj['target_object_hex']
                and len(negatives['rejected'])==8,'all three original menu indices and compiler negatives')
        require(obj['target_object_hex']==obj['versions'][-1]['object_hex'],'exact final reviewed object bytes')""",
    "'actual_body_pages','typed_choice_count','offline_speeches'":"'actual_body_pages','actual_choice_labels','offline_speeches'",
    "actual['all_four_menus_default_cursor_andfollowing_fixture_speech_observed']":
        "actual['all_six_menu_instances_default_cursor_and_following_fixture_speech_observed']",
    '})==193':'})==174',
    """    require({(m['block'],m['offset']) for m in actual['menus']}=={(m['block'],m['offset']) for m in stored['typed_objects']},
        'all observed menus bound to final stored commands')""":
        """    stored_menus={(m['block'],m['offset']):m for m in stored['typed_objects']}
    observed_menus={(m['block'],m['source_command_offset']):m for m in actual['menus']}
    require(len(observed_menus)==6 and set(observed_menus)<=set(stored_menus),'six distinct observed final menu occurrences')
    for key,item in observed_menus.items():
        native_item=stored_menus[key]
        require((item['count'],item['word'])==(len(native_item['labels']),native_item['word']) and item['observed_selected_options']==[0],
            'actual default cursor and original menu geometry')
    require(sum(m['count'] for m in observed_menus.values())==13 and actual['offline_only_caption_count']==8,
        'complete caption coverage split')
    require(actual['all_seven_town_forecasts_observed'] and {'DK4_MES_B216_R0074','DK4_MES_B217_R0052','DK4_MES_B218_R0048'}<=observed,
        'distinct forecast, staged layout and pagination observations')""",
})
env={**common.env,'__file__':__file__}
exec(compile(qualification,__file__+'::exact-five-gate-native-qualification', 'exec'),env)
exec(compile(common.source,__file__+'::same-complete-source-bound-transaction', 'exec'),env)
plan_release=env['plan_release']

