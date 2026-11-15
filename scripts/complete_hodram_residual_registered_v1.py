"""Credit394 unique residual reviews once after mixed registration,clean patch andown startup."""
import re
from scripts.complete_hodram_B251_B280_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/hodram_B251_B280_release_v1':'work/hodram_residual_release_v1',
    'hodram_B251_B280_integrated_final_review_v1.json':'hodram_residual_integrated_final_review_v1.json',
    'Hodram_SC1_B251_B280_contextual_integrated_20261107':'Hodram_SC1_residual_contextual_integrated_20261109',
    'Hodram_B251_B280_clean_next_20261107':'Hodram_SC1_B0_B41_clean_next_20261107',
    '==(703,114,38)':'==(708,114,43)',
    'both_name_getters_exact_for_all9_protected_actors':'both_name_getters_exact_for_all12_protected_actors',
    "assert startup['ARM9_COMMON_HELP_font_equal_registered_runtime_parent'] and release['all_other_files_components_graphics_names_andruntime_exact_to_parent'] and release['owned_Rafael_residual_middle_fields_verified'] and startup['frames']==4001":
        "assert startup['COMMON_HELP_font_equal_registered_runtime_parent'] and startup['only28_owned_surname_bytes_differ_in_ARM9'] and release['all_except_SC1_andthree_owned_surnames_exact_to_parent'] and release['both_components_whole_parent_inverse_exact'] and release['owned_Rafael_residual_middle_fields_verified'] and release['owned_Hodram_residual_surnames_verified'] and startup['frames']==4001",
    "'all_five_review_gates_pending')":"'all_five_review_gates_pending','fresh_native_visual_stored_gameplay_andregistered_integration_pending')",
    'all216_individual_five_gates_pass':'all394_individual_five_gates_pass',
    'observed_menu_instances=3,observed_choice_labels=7':'observed_menu_instances=3,observed_choice_labels=6',
    'Hodram B251–B280 integrated once over registered B231–B250.':'All residual Hodram SC1 dialogue andthree owned surnames integrated once over registered B311–B324.',
    'nine protected original name getters passed.':'12 protected original name getters passed. Full editorial scope remains active.',
    'editorial_review_current.Hodram_B251_B280_completion_v1.pending.json':'editorial_review_current.Hodram_residual_completion_v1.pending.json',
    'Credited 216 Hodram B251–B280 reviews once.':'Credited 394 residual Hodram reviews once.',
})
counts={'216':'394','129':'221','87':'173','17533':'18767','17749':'19161','10828':'11532','6921':'7629','17752':'19164',
    '209':'388','212':'389','7':'6','86':'169','88':'170','123':'219'}
pattern=re.compile(r'(?<![A-Za-z0-9_])(?:'+ '|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source=pattern.sub(lambda m:counts[m[0]],source)
needle="    ledger[FAMILY]=dict("
source=checked_text(source,{needle:
    """    ledger[BATCH].update(all_fifth_gates_pending=False,all_five_gates_research_pass=True,
        name_actual_headers_andregistered_layer_pending=False,name_actual_headers_pending=False,
        qualified_owned_name_field_fixes=3,qualified_owned_name_field_bytes=28,
        registered_name_fields_verified=True,final_cumulative_integration_complete=True)
"""+needle})
compile(source,__file__+'::once-only-credit-all-unrelated-ledger-keys-andprefixes-preserved','exec')
if __name__=='__main__':exec(compile(source,__file__+'::registered-mixed-residual-once-only-credit','exec'),globals())
