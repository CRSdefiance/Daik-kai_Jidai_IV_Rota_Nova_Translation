"""Credit the 283 disjoint residual SC0 reviews after their registered release."""
import re
from scripts.complete_rafael4903_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'Credit351 unique contextual reviews':'Credit283 unique contextual reviews',
    'work/rafael4903_release_v1':'work/rafael5186_release_v1',
    'rafael_B321_B342_integrated_final_review_v1.json':'rafael_B0_B34_integrated_final_review_v1.json',
    'Rafael_SC0_B321_B342_contextual_integrated_20261106':'Rafael_SC0_B0_B34_contextual_integrated_20261106',
    'Rafael_SC0_B321_B342_clean_20261106':'Rafael_SC0_B0_B34_clean_20261106',
    '==(698,114,33)':'==(700,114,35)',
    "names['both_name_getters_exact_for_actors_35_65_68_70_186_203']":"names['both_name_getters_exact_for_all9_protected_actors']",
    "startup['ARM9_COMMON_HELP_font_equal_registered_runtime_parent'] and release['all_other_files_components_graphics_names_andruntime_exact_to_parent']":
        "startup['COMMON_HELP_font_equal_registered_runtime_parent'] and startup['only_nine_owned_middle_field_bytes_differ_in_ARM9'] and release['all_except_owned_middle_fields_exact_to_parent'] and release['owned_Rafael_residual_middle_fields_verified']",
    'all556_individual_five_gates_pass':'all283_individual_five_gates_pass',
    'scope=dict(source_variants=540,native_body_pages=552,typed_labels=16,observed_source_variants=72,':
        'scope=dict(source_variants=283,native_body_pages=284,typed_labels=0,observed_source_variants=95,',
    "observed_body_pages=76,offline_only_source_variants=468,actual_review=conf['actual'],":
        "observed_body_pages=96,offline_only_source_variants=188,actual_review=conf['actual'],",
    'actual_menu_cursor_states=[0],observed_menu_instances=7,observed_choice_labels=16':
        'actual_menu_cursor_states=[],observed_menu_instances=0,observed_choice_labels=0',
    'Rafael B321–B342 integrated once in Rafael4903.':'Rafael B0–B34 integrated once in Rafael5186.',
    'own startup and six inherited names passed.':'own startup and nine protected original name getters passed.',
    'editorial_review_current.Rafael4903_completion_v1.pending.json':'editorial_review_current.Rafael5186_completion_v1.pending.json',
    'Credited 556 Rafael B321–B342 reviews once.':'Credited 283 Rafael B0–B34 reviews once.',
})
counts={'556':'283','364':'162','192':'121','16192':'16748','16748':'17031',
    '10252':'10414','6496':'6617','16751':'17034'}
source=re.sub(r'(?<![A-Za-z0-9_])(?:556|364|192|16192|16748|10252|6496|16751)(?![0-9])',
    lambda m:counts[m[0]],source)

if __name__=='__main__':exec(compile(source,__file__+'::once-only-registered-completion','exec'),globals())
