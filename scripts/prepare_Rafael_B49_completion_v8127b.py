"""Carry fresh B50 clean-only progress into the reversible B49 completion; no B50 credit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from scripts.prepare_Rafael_B49_completion_v8127 import NEXT
ROOT=Path('work/analysis/Rafael_B49_completion_tools_v8127b')
LEAD={
 'source_packet':'work/analysis/Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json',
 'clean_names':'work/analysis/Rafael_B50_clean_names_v8130/three_clean_static_identity_fields_before_current_English.json',
 'first_gloss':'work/analysis/Rafael_B50_clean_gloss_v8131/28_first_clean_glosses_three_source_identities_before_current_English.json',
 'physical_source_objects':28,'source_static_identities':3,'source_macro_counts':dict(FI=1,FA=2,FO=0),
 'event50_category5_action51_no_explicit_prerequisite_exclusion_not_natural_eligibility':True,
 'current_B50_English_body_still_unread':True,'B49_known_approved_names_not_new_B50_current_name_comparison':True,
 'source_gloss_only_no_localized_manuscript':True,'unnamed_celebration_occasion_not_invented':True,
 'native_controls_getters_item_effects_title_context_current_comparison_andrelease_pending':True,
 'completion_credit_added':0,'source_prose_credit_added':0,'full_goal_complete':False,
}
PENDING='Rafael_SC0B50_source_gloss_pending_controls_current_andrelease_v8127'
if __name__=='__main__':
    assert not ROOT.exists()
    for key in ['source_packet','clean_names','first_gloss']:assert Path(LEAD[key]).exists()
    leadnext="B50 source-only progress is already saved:28 complete clean Japanese speeches,three original identities and28first-source glosses. Current B50English bodies remain unread. Event50/category5/action51 has no explicit prerequisite/exclusion list;numeric adjacency toB49 doesnot establish chronology. Lil offers a key to decipher a treasure-location map andlater identifies it as a pigment;Camille says FAisnowtheNorthSealeader. Preparations,newwayoflife,thanks andan unnamed congratulatory gesture leave Rafaelprivatelypuzzled. Preserve that ambiguity;do not invent marriage,romance,pregnancy,retirement orbiography. Verify exactFA2/FI1native getters,source4681/4720/4821 andall controls/item effects/callers/title/context before currentEnglish orprose. Sourcepacket:"+LEAD['source_packet']+';cleanidentities:'+LEAD['clean_names']+';glosses:'+LEAD['first_gloss']+'. These artifacts bind verifiedV8116 whileB49atomic checks ran;cleaninputunchanged. B50hasno completion/source-prosecredit.\n\n'+NEXT
    result=derive('scripts/complete_Rafael_B49_v8127.py','scripts/complete_Rafael_B49_v8127b.py',{
        'NEXT='+repr(NEXT):'NEXT='+repr(leadnext),
        "    prior_scope=old[prior['unfinished_scope']]":"    put(["+repr(PENDING)+'], '+repr(LEAD)+")\n    prior_scope=old[prior['unfinished_scope']]",
        "    inventory[KEY]=dict(final_review=str(FINAL)":"    inventory["+repr(PENDING)+']='+repr(LEAD)+"\n    inventory[KEY]=dict(final_review=str(FINAL)",
        'pending_source_batch=None,next_clean_exchange_not_selected=True':'pending_source_batch='+repr(PENDING)+',next_clean_exchange_not_selected=False',
        "Path(__file__)]}":"*[Path(p) for p in "+repr([LEAD[k] for k in ['source_packet','clean_names','first_gloss']])+"],Path(__file__)]}",
        'source_prose_andcompletion_credit_added_once=True':'source_prose_andcompletion_credit_added_once=True,source_prose_orcompletion_credit_added=True',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared B49 completion successor retaining28 clean-only B50 glosses andall earlier scope;no B50 credit.')
