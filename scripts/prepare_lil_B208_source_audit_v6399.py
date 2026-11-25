"""Prepare the observed B208 path audit without asserting a particular later-screen outcome."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B208_source_audit_tools_v6399')
if __name__=='__main__':
    assert not ROOT.exists();r=derive('scripts/audit_lil_B207_source_v6347.py','scripts/audit_lil_B208_source_v6399.py',{
        'B207':'B208','source_actual_v6347':'source_actual_v6399','source_fixture_v6345':'source_fixture_v6397','source_run_v6346':'source_run_v6398','source_event207':'source_event208','event207':'event208',
        '11001':'16001','all15_source_commands_retained':'all29_source_commands_retained',
        'len(observations)==13':'len(observations)==24','[5,8,12,15,19,23,26,30,33,37,41,45,48]':'[5,9,13,17,21,25,28,32,36,40,44,48,51,55,59,62,66,70,73,76,79,82,86,90]',
        'len(pairs)==24':'len(pairs)==38','all24_stored_fixture_commands':'all38_stored_fixture_commands',"pairs[-1]['source_offset']==650":"pairs[-1]['source_offset']==1182",'==[642]':'==[1166,1174]',
        'range(0,13,6)':'range(0,24,6)','all13_complete_Japanese_source_sheet':'all24_complete_Japanese_source_sheet',
        'all13_source_speeches_all24_commands_and_complete_return.json':'all24_source_panels_all38_commands_and_observed_return.json',
        'source_distinct_speech_observations=13,total_speech_observations=13':'source_distinct_speech_observations=24,total_speech_observations=24',
        'all15_source_commands_and9_original_initializers_observed':'all29_source_commands_and9_original_initializers_observed','source_effect_offsets_executed=[642]':'source_effect_offsets_executed=[1166,1174]',
        'current_Emilio_fullwidth_F_storage_is_a_display_review_lead_not_yet_an_approved_name_change':'Cristina_Erneco_Mysterious_Old_Man_names_and_private_thought_named_FE_notice_localization_pending',
        'source_speeches=13':'source_speeches=24','complete13-speech source run to all24':'complete24-panel source run to all38'})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tool.json',r);print('B20824-panel/38-command source audit prepared;later outcome remains observed,not assumed.')
