"""Shared reconciliation with explicit per-consumer geometry and native contracts."""
from pathlib import Path
outer=Path('scripts/reconcile_contextual_aftermath_fled_retentions_v2544.py').read_text();needle="\nexec(compile(source,__file__,'exec'),globals())";assert outer.count(needle)==1;env={'__file__':__file__};exec(compile(outer.replace(needle,'\ncaptured=source'),__file__,'exec'),env);source=env['captured']
changes={
 "fonts['current_portrait_consumer_no_Deck_or_duel_projection_claim']":"fonts[spec['consumer_pass_key']]",
 "fonts['complete_native_font_cases']==6 and len(fonts['all6_original_role1_pipelines'])==6":"fonts['complete_native_font_cases']==spec['font_executions']and fonts[spec['pipeline_count_key']]==spec['font_executions']",
 "r['consumer']=='original-53D44-role1-fled-victory-portrait'":"r['consumer']==spec['consumer']",
 "history['only2046_has_individual_historical_activation_other5_use_family_sample']":"(history['only2209_individually_activated_other7_use_family_sample']if spec['kind']=='sea'else history['both306_307_individually_activated'])",
 "history['no_inputs5773_through10982']":"history['no_fixtures_after4800']",
 "notes.update(original_role_selector=1,original_parent=0x02053DB8,original_table_stack_offset=0x27C,original_source_table=0x02117900,source_voice_alternatives_not_sequential_conversation=True)":"notes.update(**spec['native_contract'],separate_inspection_consumers_and_context_only_credit=True)",
 "display_contract='Original53D44 role1 speech;parent02053DB8/table stack+27C;228x64 portrait body,35 cells x4 rows,16px row stride,uniform native x6 at screen16,296;compiler-owned presentation guard and generated pair-safe post-macro wrapping'":"display_contract=spec['display_contract']",
 'historical_aftermath_fled_current_binding':'historical_inspection_current_binding',
 'scoped_historical_cancellation_and_battle_transitions_freshly_rechecked':'scoped_historical_inspection_and_return_transitions_freshly_rechecked',
 'no_new_current_battle_emulator_runs_or_family_visits':'no_new_current_emulator_runs_or_visits',
 'new_current_aftermath_fled_ID_visits':'new_current_inspection_ID_visits',
 'current_native_aftermath_fled_font':'current_native_inspection_consumer_font',
 'aftermath_fled_role1_35x4':'inspection_registered_consumer',
 'historical_report_and_sailing_return_transitions':'historical_inspection_and_Inspect_return_transitions',
 'flight-report/dismissal':'original-inspection/dismissal',
 'pre-duel-fixtures-flight-report-and-sailing-return':'existing-monster-registration-lookout-fixture-and-Inspect-return',
 'original role1 portrait-speech fonts':'original mapped inspection-consumer native fonts',
 'retentions-original-role1-228x64-portrait':'retentions-original-inspection-consumer',
}
for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
source=source.replace(' validate_natural_dialogue_batch(notes);',' assert fonts["blank_space_font_freshly_verified_zero_ink"]and history["both_original_Inspect_returns_not_Sea_View"]and history["completed_48_and46_owned_byte_whole4MiB_registration_fixture_audits_hash_bound"]\n validate_natural_dialogue_batch(notes);')
exec(compile(source,__file__,'exec'),globals())
