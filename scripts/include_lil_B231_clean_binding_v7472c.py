"""Include new clean-only source evidence before executing the completion producer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B230_next_binding_tools_v7472c')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('work/analysis/lil_B230_completion_v7472').exists();lead='work/analysis/lil_B231_clean_names_item_v7476/clean_personal_fields_anditem99_before_current_getters.json'
    anchor='    # Preserve all earlier B225/B226 technical audit leads from the full prior inventory.'
    extra="    inventory['next_Lil_B231_clean_name_item_lead_v7476']=dict(proof='"+lead+"',sha256=sha(Path('"+lead+"').read_bytes()),original_personal_fields_anditem99_only_no_current_getter_voice_display_orEnglish_approval=True,new_credit=0)\n"
    row=derive('scripts/complete_lil_B230_v7472b.py','scripts/complete_lil_B230_v7472c.py',{'paths.append(nextsource)':"paths.extend([nextsource,Path('"+lead+"')])",anchor:extra+anchor});ROOT.mkdir(parents=True);save(ROOT/'source_locked_next_clean_binding.json',dict(tool=row,unexecuted_completion_producers_preserved=True,next_source_binding_no_duplicate_credit_orcurrent_English_approval=True,no_ROM_runtime_counter_orledger_change_from_preparation=True,new_credit=0,full_goal_complete=False))
