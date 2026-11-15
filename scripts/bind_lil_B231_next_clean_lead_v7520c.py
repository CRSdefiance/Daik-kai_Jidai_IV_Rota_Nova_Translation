"""Include B233 clean-only name/item evidence before staged completion."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B231_completion_next_tools_v7520c')
PROOF=Path('work/analysis/lil_B233_clean_names_item_v7525/clean_personal_fields_anditem97_before_current_getters.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('work/analysis/lil_B231_completion_v7520').exists();d=read(PROOF)
    assert d['no_predecessor_story_English_exposed'] and d['source_named_item']['record_ID']=='DK4_ITEM_POINTER_097' and d['source_named_item']['Japanese']=='フェイディアスの鑿' and [r['source_selector'] for r in d['source_personal_fields']]==[2,23]
    old="    # Preserve all earlier B225/B226 technical audit leads from the full prior inventory."
    new="    inventory['next_Lil_B233_clean_name_item_lead_v7525']=dict(proof='"+PROOF.as_posix()+"',sha256=sha(Path('"+PROOF.as_posix()+"').read_bytes()),original_personal_fields_anditem97_only_no_current_getter_voice_display_orEnglish_approval=True,new_credit=0)\n"+old
    row=derive('scripts/complete_lil_B231_v7520b.py','scripts/complete_lil_B231_v7520c.py',{old:new,'paths.extend([nextsource,empty])':"paths.extend([nextsource,empty,Path('"+PROOF.as_posix()+"')])"})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_next_clean_lead.json',dict(tool=row,exact_source_only_names_item97_lead_bound=True,no_current_getter_voice_display_orEnglish_approval=True,no_runtime_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
