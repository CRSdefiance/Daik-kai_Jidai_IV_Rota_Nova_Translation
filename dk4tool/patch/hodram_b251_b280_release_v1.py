"""Qualify the complete B251-B280 transaction over the exact registered predecessor."""
from dk4tool.patch import hodram_b231_b250_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

load=previous.load;sha=previous.sha;require=previous.require
evidence_source=checked_text(previous.evidence_source,{
    '(225,115,110)':'(216,129,87)',"conf['scoped_name_count']==19":"conf['scoped_name_count']==21",
    "conf['native_pages']==228":"conf['native_pages']==212", "conf['relative_cases']==170":"conf['relative_cases']==660",
    'all223_ordinary_and_style_bodies_checked':'all209_ordinary_and_style_bodies_checked',
    '(325,36,614)':'(325,60,590)', "(209,14,conf['speech_count'])":"(193,16,conf['speech_count'])",
    'len(planes)==223':'len(planes)==209', "conf['FE_count']==4":"conf['FE_count']==31",
    'all four distinct FE panels':'all 31 FE bodies', "styles['physical_alternatives']==14":"styles['physical_alternatives']==16",
    "len(menu['menus'])==1":"len(menu['menus'])==3", "conf['typed_choice_count']==2":"conf['typed_choice_count']==7",
    "stored['typed_labels_checked']==2 and len(stored['typed_objects'])==1":"stored['typed_labels_checked']==7 and len(stored['typed_objects'])==3",
    '(21521,1,63,68,160)':'(26801,1,86,88,123)',
    'all_four_FE_panels_FI_expansions_two_voice_objects_andrepresentative_pagination_observed':
        'eighteen_of31_FE_panels_FI_FA_two_voice_objects_andboth_selected_two_page_passages_observed',
    "{(243,674,(0,))},'source-bound two-choice menu behavior'":
        "{(251,432,(0,)),(252,270,(0,)),(252,1606,(0,))},'three source-bound two/three-choice menu behaviors'",
    "visual['actual_sheets_directly_viewed']==13":"visual['actual_sheets_directly_viewed']==9",
})
evidence_env={**previous.qualify_evidence.__globals__,**globals(),'__file__':__file__}
exec(compile(evidence_source,__file__+'::same-qualified-native-and-editorial-evidence-new-scope','exec'),evidence_env)
qualify_evidence=evidence_env['qualify_evidence']
source=checked_text(previous.source,{
    "'dk4-reviewed-hodram-b231-b250-release-v1'":"'dk4-reviewed-hodram-b251-b280-release-v1'",
})
env={**previous.env,'qualify_evidence':qualify_evidence,'__file__':__file__}
exec(compile(source,__file__+'::same-SC1-transaction-all-guards-and-inverses','exec'),env)
plan_release=env['plan_release']
