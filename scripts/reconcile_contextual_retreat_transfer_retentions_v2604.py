"""Seven records,eight voices and208 complete one-name role1 displays."""
from pathlib import Path
outer=Path('scripts/reconcile_contextual_enemy_capture_retentions_v2598.py').read_text();needle="exec(compile(source,__file__,'exec'),globals())";assert outer.count(needle)==1;env={};exec(compile(outer.replace(needle,'captured=source'),__file__,'exec'),env);source=env['captured']
changes={
 'enemy_capture':'retreat_transfer',
 'all208_original_direct_named_capture_pipelines':'all208_original_role1_named_retreat_pipelines',
 'original-53F0C-attacker-selector8-named-enemy-ship-capture-portrait':'original-53D44-logical-role1-replacement-ship-retreat-portrait',
 "history['only2082_has_individual_historical_activation_other7_use_family_sample']":"history['only2684_has_individual_historical_activation_other6_and_voice3_fallback_use_family_sample']",
 'original_entry=0x02053F0C,original_parent=0x02053F40,original_table_stack_offset=0x274,original_source_table=0x02117B00,original_attacker_selector=0x02055DC4,original_attacker_selector_argument=8,native_ship_name_arguments=1':'original_entry=0x02053D44,original_parent=0x02053DB8,original_table_stack_offset=0x27C,original_source_table=0x02117080,original_role_selector=1,native_ship_name_arguments=1',
 'Original53F0C attacker-selector8 named-ship speech;parent02053F40/table stack+274':'Original53D44 logical-role1 replacement-ship speech;parent02053DB8/table stack+27C',
 'historical_named_capture_flagship_victory_rewards_cargo_and_sailing_transitions':'historical_defeat_retreat_transfer_and_sailing_transitions',
 'named-ship-capture/flagship/victory/rewards/cargo/sailing':'defeat/evacuation/replacement-ship-transfer/sailing',
 'sole-own-ship-position-fixture-named-capture-and-original-return':'sole-own-ship-position-fixture-defeat-transfer-and-original-return',
 "fonts[\"no_actor_or_roster_fixture\"]":"len(fonts[\"CPU_only_role_counterfactuals_entire4MiB_audited\"])==7 and fonts[\"actual_voice1_logical16_physical0_unchanged\"]",
}
for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
exec(compile(source,__file__,'exec'),globals())
