"""Bind every stored body through the original pre-macro lookup and market-data exclusion guards."""
from scripts.check_maria301_stored_catalogue_v1 import source as previous,TEMPLATE
from scripts.check_maria270_stored_v1 import guard_market_independence
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/Maria_B0_B32_clean_20261109/stored_catalogue_all_v1':'work/Maria_B37_B50_clean_20261109/stored270_catalogue_v1',
    'work/Maria_B0_B32_clean_20261109/stored_v1/stored_native_verification.json':'work/Maria_B37_B50_clean_20261109/stored270_v1/stored_native_verification.json',
    'work/Maria_B0_B32_clean_20261109/current_v1/current_effective.json':'work/Maria_B37_B50_clean_20261109/storage270_inputs_v1/packet.json',
    'assert ctx.receipt()==runtime==current[\'runtime\']':
        "assert ctx.receipt()==runtime==current['runtime']\n    rebuilt=load(stored['reconstruction'])\n    qualified_parent=guard_market_independence(ctx,rebuilt)",
    '==299':'==266',
    'all299_stored_effective_body_bindings.json':'all266_stored_effective_body_bindings.json',
    'all299_ordinary_and_style_bodies_checked':'all266_ordinary_and_style_bodies_checked',
    '299 stored ordinary and alternate-voice bodies pass':'266 stored ordinary bodies pass',
    'no_code_font_orROM_changes=True,actual_gameplay=False':
        'no_code_font_orROM_changes=True, exact_registered_market_parent_reuse=qualified_parent, market_pointer_read_andexecution_dependency_guards_pass=True, actual_gameplay=False',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-buffer-native-lookup-explicit266-objects','exec'),globals())
