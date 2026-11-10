"""Prepare the complete B211 source-scene observation audit without inventing later outcomes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_source_audit_tools_v6561')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/audit_lil_B210_source_v6510.py','scripts/audit_lil_B211_source_v6561.py',{
        'B210':'B211','source_actual_v6510':'source_actual_v6561','source_fixture_v6503':'source_fixture_v6555','source_run_v6504':'source_run_v6556','source_event210':'source_event211','event210':'event211','all12_source_commands_retained':'all14_source_commands_retained',
        'len(observations)==10':'len(observations)==12','[5,8,11,15,19,23,26,29,33,36]':'[5,9,13,17,21,24,28,32,36,39,42,45]','len(pairs)==21':'len(pairs)==23','all21_stored_fixture_commands':'all23_stored_fixture_commands',"pairs[-1]['source_offset']==682":"pairs[-1]['source_offset']==636",'==[674]':'==[628]','range(0,10,6)':'range(0,12,6)','all10_complete_Japanese_source_sheet':'all12_complete_Japanese_source_sheet','all10_source_panels_all21_commands':'all12_source_panels_all23_commands','source_distinct_speech_observations=10,total_speech_observations=10':'source_distinct_speech_observations=12,total_speech_observations=12','all12_source_commands_and9':'all14_source_commands_and9','source_effect_offsets_executed=[674]':'source_effect_offsets_executed=[628]','Lil_Al_progressive_names_and_full_additional_name_field_typography_review_separate':'Lil_Cristina_names_three_FE_animal_panels_one_FI_and_unknown_object_identity_review_separate','source_speeches=10':'source_speeches=12','complete10-panel source run to all21':'complete12-panel source run to all23'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_audit.json',dict(proof=proof,all_source_native_constants_and_actual_scope_preserved=True,full_goal_complete=False))
