"""Fourteen paired-report retentions using the frozen75-record release layer."""
from pathlib import Path
OLD=Path('scripts/reconcile_contextual_aftermath_fled_retentions_v2544.py');source=OLD.read_text()
changes={
 'aftermath_fled':'aftermath_defeat','fled-victory-portrait':'paired-defeat-portrait',
 "fonts['complete_native_font_cases']==6":"fonts['complete_native_font_cases']==14",
 "fonts['all6_original_role1_pipelines'])==6":"fonts['all14_original_role1_pipelines'])==14",
 "history['only2046_has_individual_historical_activation_other5_use_family_sample']":"history['only2016_and2138_have_individual_historical_activation_other12_use_family_sample']",
 "history['no_inputs5773_through10982']":"history['no_inputs5773_through6922']",
 'original_source_table=0x02117900':'original_source_tables=[0x02117760,0x02117F00]',
 'historical_report_and_sailing_return_transitions':'historical_paired_defeat_GameOver_title_transitions',
 'flight-report/dismissal':'paired-defeat/GameOver/title',
 'flight-report-and-sailing-return':'paired-defeat-and-title',
}
for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
exec(compile(source,__file__,'exec'),globals())
