"""Eight direct defending-captain challenges;no role1/First Mate attribution."""
from pathlib import Path
OLD=Path('scripts/reconcile_contextual_aftermath_fled_retentions_v2544.py');source=OLD.read_text()
changes={
 'aftermath_fled':'aftermath_city',
 "fonts['complete_native_font_cases']==6":"fonts['complete_native_font_cases']==8",
 "fonts['all6_original_role1_pipelines'])==6":"fonts['all8_original_direct_defender_pipelines'])==8",
 'original-53D44-role1-fled-victory-portrait':'original-53F0C-defending-captain-city-challenge-portrait',
 "history['only2046_has_individual_historical_activation_other5_use_family_sample']":"history['only2043_has_individual_historical_activation_other7_use_family_sample']",
 "history['no_inputs5773_through10982']":"history['original_presence_share_and_unforced_one_in_three_choice_preserved']",
 'original_role_selector=1,original_parent=0x02053DB8,original_table_stack_offset=0x27C,original_source_table=0x02117900':'original_entry=0x02053F0C,original_parent=0x02053F40,original_table_stack_offset=0x274,original_source_table=0x021178C0,source_speaker_is_defending_fleet_captain=True',
 'Original53D44 role1 speech;parent02053DB8/table stack+27C':'Original53F0C defending-captain direct speech;parent02053F40/table stack+274',
 'aftermath_city_role1_35x4':'aftermath_city_direct35x4','original role1 portrait-speech fonts':'original direct defending-captain portrait-speech fonts',
 'historical_report_and_sailing_return_transitions':'historical_challenge_and_defender_battle_entry_transitions',
 'flight-report/dismissal':'city-defender-challenge/battle-entry','pre-duel-fixtures-flight-report-and-sailing-return':'prebattle-location-fixture-city-challenge-and-defender-battle-entry',
 'retentions-original-role1-228x64-portrait':'retentions-original-direct-228x64-portrait',
}
for a,b in changes.items():
 assert a in source,a
 source=source.replace(a,b)
exec(compile(source,__file__,'exec'),globals())
