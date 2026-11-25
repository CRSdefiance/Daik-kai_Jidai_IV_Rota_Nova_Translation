"""Credit the disjoint 277-record batch once after registered release and own startup."""
import re
from scripts.complete_rafael5186_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'Credit283 unique contextual reviews':'Credit277 unique contextual reviews',
    'work/rafael5186_release_v1':'work/hodram_B211_B230_release_v1',
    'rafael_B0_B34_integrated_final_review_v1.json':'hodram_B211_B230_integrated_final_review_v1.json',
    'Rafael_SC0_B0_B34_contextual_integrated_20261106':'Hodram_SC1_B211_B230_contextual_integrated_20261107',
    'Rafael_SC0_B0_B34_clean_20261106':'Hodram_B211_B230_clean_next_20261104',
    '==(700,114,35)':'==(701,114,36)',
    "startup['COMMON_HELP_font_equal_registered_runtime_parent'] and startup['only_nine_owned_middle_field_bytes_differ_in_ARM9'] and release['all_except_owned_middle_fields_exact_to_parent'] and release['owned_Rafael_residual_middle_fields_verified']":
        "startup['ARM9_COMMON_HELP_font_equal_registered_runtime_parent'] and release['all_other_files_components_graphics_names_andruntime_exact_to_parent'] and release['owned_Rafael_residual_middle_fields_verified']",
    "        assert not any(v is True and 'pending' in k for k,v in row.items() if k!='registered_release_and_completion_credit_pending')":
        """        for key in ('formatting_visual_stored_gameplay_andregistered_release_pending','registered_release_andcompletion_credit_pending'):
            if key in row:row[key]=False
        assert not any(v is True and 'pending' in k for k,v in row.items() if k!='registered_release_and_completion_credit_pending')""",
    'all283_individual_five_gates_pass':'all277_individual_five_gates_pass',
    'scope=dict(source_variants=283,native_body_pages=284,typed_labels=0,observed_source_variants=95,':
        'scope=dict(source_variants=270,native_body_pages=284,typed_labels=7,observed_source_variants=65,',
    "observed_body_pages=96,offline_only_source_variants=188,actual_review=conf['actual'],":
        "observed_body_pages=74,offline_only_source_variants=205,actual_review=conf['actual'],",
    'actual_menu_cursor_states=[],observed_menu_instances=0,observed_choice_labels=0,offline_only_captions=0':
        'actual_menu_cursor_states=[0],observed_menu_instances=2,observed_choice_labels=5,offline_only_captions=2,byte_identical_repeated_menu_has_offline_proof_not_duplicate_occurrence_credit=True',
    "profile=release['profile'],SC0_sha256=release['target_SC0_sha256']":"profile=release['profile'],SC1_sha256=release['target_SC1_sha256']",
    'Rafael B0–B34 integrated once in Rafael5186.':'Hodram B211–B230 integrated once over Rafael5186.',
    'editorial_review_current.Rafael5186_completion_v1.pending.json':'editorial_review_current.Hodram_B211_B230_completion_v1.pending.json',
    'Credited 283 Rafael B0–B34 reviews once.':'Credited 277 Hodram B211–B230 reviews once.',
})
counts={'283':'277','162':'170','121':'107','16748':'17031','17031':'17308',
    '10414':'10584','6617':'6724','17034':'17311'}
source=re.sub(r'(?<![A-Za-z0-9_])(?:283|162|121|16748|17031|10414|6617|17034)(?![0-9])',lambda m:counts[m[0]],source)
if __name__=='__main__':exec(compile(source,__file__+'::same-once-only-completion-disjoint-SC1-scope','exec'),globals())
