"""Qualify the reviewed B281-B300 append over the complete registered predecessor."""
from dk4tool.patch import hodram_b251_b280_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

load=previous.load;sha=previous.sha;require=previous.require
evidence_source=checked_text(previous.evidence_source,{
    '(216,129,87)':'(384,181,203)',"conf['scoped_name_count']==21":"conf['scoped_name_count']==18",
    "conf['native_pages']==212":"conf['native_pages']==374","conf['relative_cases']==660":"conf['relative_cases']==1415",
    'all209_ordinary_and_style_bodies_checked':'all373_ordinary_and_style_bodies_checked',
    '(325,60,590)':'(325,40,610)',"(193,16,conf['speech_count'])":"(242,131,conf['speech_count'])",
    'len(planes)==209':'len(planes)==373',"conf['FE_count']==31":"conf['FE_count']==16",
    'all 31 FE bodies':'all 16 FE bodies',
    "len(styles['objects'])==2 and styles['native_target_slot_cases']==16 and styles['physical_alternatives']==16":
        "len(styles['objects'])==18 and styles['native_target_slot_cases']==144 and styles['physical_alternatives']==131",
    "for r in styles['compiler_negatives'])==18":"for r in styles['compiler_negatives'])==162",
    "len(menu['menus'])==3":"len(menu['menus'])==5","conf['typed_choice_count']==7":"conf['typed_choice_count']==11",
    "stored['typed_labels_checked']==7 and len(stored['typed_objects'])==3":"stored['typed_labels_checked']==11 and len(stored['typed_objects'])==5",
    '(26801,1,86,88,123)':'(38561,1,134,135,239)',
    'eighteen_of31_FE_panels_FI_FA_two_voice_objects_andboth_selected_two_page_passages_observed':
        'twelve_of16_FE_panels_FI_FA_seven_voice_objects_royal_pagination_andcorrected_injury_rows_observed',
    "{(251,432,(0,)),(252,270,(0,)),(252,1606,(0,))},'three source-bound two/three-choice menu behaviors'":
        "{(290,876,(0,)),(290,1876,(0,)),(291,1114,(0,)),(294,820,(0,)),(300,560,(0,))},'five source-bound two/three-choice menu behaviors'",
    "visual['actual_sheets_directly_viewed']==9":"visual['actual_sheets_directly_viewed']==13",
})
evidence_env={**previous.qualify_evidence.__globals__,**globals(),'__file__':__file__}
exec(compile(evidence_source,__file__+'::same-complete-qualified-evidence-exact-new-scope','exec'),evidence_env)
qualify_evidence=evidence_env['qualify_evidence']
source=checked_text(previous.source,{
    "'dk4-reviewed-hodram-b251-b280-release-v1'":"'dk4-reviewed-hodram-b281-b300-release-v1'",
    "len(styles['objects']) == 2":"len(styles['objects']) == 18",
})
env={**previous.env,'qualify_evidence':qualify_evidence,'__file__':__file__}
exec(compile(source,__file__+'::same-SC1-transaction-all-source-and-inverse-guards','exec'),env)
plan_release=env['plan_release']
