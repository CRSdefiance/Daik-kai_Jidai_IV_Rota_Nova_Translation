"""Six unique alerts,eight direct voices,and context-only extinguished response."""
from pathlib import Path
OLD=Path('scripts/reconcile_contextual_aftermath_fled_retentions_v2544.py');source=OLD.read_text()
changes={
 'aftermath_fled':'powder_fire',
 "fonts['complete_native_font_cases']==6":"fonts['complete_native_font_cases']==8",
 "fonts['all6_original_role1_pipelines'])==6":"fonts['all8_original_direct_gunner_pipelines'])==8",
 'original-53D44-role1-fled-victory-portrait':'original-53F0C-per-battery-gunner-powder-fire-portrait',
 "history['only2046_has_individual_historical_activation_other5_use_family_sample']":"history['only2053_has_individual_alert_activation_other5_use_family_sample']",
 "history['no_inputs5773_through10982']":"history['original_fire_cleanup_deferred_until_followup_dismissal_in_both_versions']",
 'original_role_selector=1,original_parent=0x02053DB8,original_table_stack_offset=0x27C,original_source_table=0x02117900':'original_entry=0x02053F0C,original_parent=0x02053F40,original_table_stack_offset=0x274,original_source_table=0x02117980,source_speaker_is_original_per_battery_gunner=True',
 'Original53D44 role1 speech;parent02053DB8/table stack+27C':'Original53F0C per-battery gunner direct speech;parent02053F40/table stack+274',
 'powder_fire_role1_35x4':'powder_fire_direct35x4','original role1 portrait-speech fonts':'original direct gunner portrait-speech fonts',
 'historical_report_and_sailing_return_transitions':'historical_fire_followup_cleanup_and_battle_return_transitions',
 'flight-report/dismissal':'fire-alert/extinguished/deferred-cleanup','pre-duel-fixtures-flight-report-and-sailing-return':'prebattle-gunnery-fixture-alert-followup-and-sea-battle-return',
 'retentions-original-role1-228x64-portrait':'retentions-original-direct-228x64-portrait',
}
for a,b in changes.items():
 assert a in source,a
 source=source.replace(a,b)
source=source.replace('changes={\n','changes={\n \'font_previews=count\':\'font_previews=spec["font_previews"]\',\n',1)
exec(compile(source,__file__,'exec'),globals())
