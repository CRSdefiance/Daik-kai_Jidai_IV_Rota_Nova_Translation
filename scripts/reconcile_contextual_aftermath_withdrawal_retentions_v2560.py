"""Eight withdrawal retentions through the frozen registered75-record layer."""
from pathlib import Path
OLD=Path('scripts/reconcile_contextual_aftermath_fled_retentions_v2544.py');source=OLD.read_text()
changes={
 'aftermath_fled':'aftermath_withdrawal','fled-victory-portrait':'withdrawal-portrait',
 "fonts['complete_native_font_cases']==6":"fonts['complete_native_font_cases']==8",
 "fonts['all6_original_role1_pipelines'])==6":"fonts['all8_original_role1_pipelines'])==8",
 "history['only2046_has_individual_historical_activation_other5_use_family_sample']":"history['only2114_has_individual_historical_activation_other7_use_family_sample']",
 "history['no_inputs5773_through10982']":"history['no_inputs_or_fixtures5910_through7310']",
 'original_source_table=0x02117900':'original_source_table=0x02117D00',
 'historical_report_and_sailing_return_transitions':'historical_withdrawal_and_sailing_return_transitions',
 'flight-report/dismissal':'town-withdrawal/dismissal','pre-duel-fixtures-flight-report-and-sailing-return':'prebattle-location-role-fixture-town-withdrawal-and-sailing-return',
}
for a,b in changes.items():
 assert a in source,a
 source=source.replace(a,b)
exec(compile(source,__file__,'exec'),globals())
