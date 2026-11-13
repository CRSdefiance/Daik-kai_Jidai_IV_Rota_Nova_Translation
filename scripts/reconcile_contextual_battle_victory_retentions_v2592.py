"""Reconcile eight reports under their original legacy portrait consumer."""
from pathlib import Path
outer=Path('scripts/reconcile_contextual_aftermath_fled_retentions_v2544.py').read_text();needle="exec(compile(source,__file__,'exec'),globals())";assert outer.count(needle)==1
env={};exec(compile(outer.replace(needle,'captured=source'),__file__,'exec'),env);source=env['captured']
changes={
 'aftermath_fled':'battle_victory',
 "fonts['complete_native_font_cases']==6 and len(fonts['all6_original_role1_pipelines'])==6":"fonts['complete_native_font_cases']==8 and len(fonts['all8_original_role1_pipelines'])==8",
 'original-53D44-role1-fled-victory-portrait':'original-53D44-logical-role1-legacy-battle-victory-portrait',
 "history['only2046_has_individual_historical_activation_other5_use_family_sample']":"history['only2131_has_individual_historical_activation_other7_use_family_sample']",
 "history['no_inputs5773_through10982']":"history['no_fixtures_after4800']",'0x02117900':'0x02117EE0',
 '35 cells x4 rows,16px row stride,uniform native x6 at screen16,296;compiler-owned presentation guard and generated pair-safe post-macro wrapping':'one short native row within35 cells,16px row stride,uniform native x6 at screen16,296;compiler emits no guard,the original legacy nonmember formatter adds one leading cell and the native ASCII painter emits the exact optional trailing blank',
 'historical_report_and_sailing_return_transitions':'historical_capture_victory_rewards_cargo_and_sailing_transitions',
 'flight-report/dismissal':'victory-report/rewards/cargo/sailing','pre-duel-fixtures-flight-report-and-sailing-return':'sole-own-ship-position-fixture-victory-rewards-cargo-and-sailing',
}
for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
source=source.replace(' notes.update(original_role_selector=1,',' assert fonts["all8_original_legacy_leading_cells_ordered_glyphs_odd_pair_blanks_and_unchanged_actor_models_verified"] and len(fonts["invalid_compiler_inputs_rejected"])==14\n notes.update(legacy_formatter_supplies_leading_cell=True,compiler_emits_no_authored_guard=True,source2132_collective_IC_plural_binding_preserved=True,original_role_selector=1,')
exec(compile(source,__file__,'exec'),globals())
