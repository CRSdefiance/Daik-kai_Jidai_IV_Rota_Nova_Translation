"""Credit Rafael B221–B240 once after the complete registered release and startup checks."""
import re

from scripts.complete_rafael2952_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'work/analysis/Rafael2952_extended_release_verified_v1_20261106': 'work/Rafael3222_extended_release_verified_v1_20261106',
    'rafael_B201_B220_integrated_final_review_v1.json': 'rafael_B221_B240_integrated_final_review_v1.json',
    'Rafael_SC0_B201_B220_contextual_integrated_20261106': 'Rafael_SC0_B221_B240_contextual_integrated_20261106',
    'Rafael_SC0_B201_B220_clean_20261106': 'Rafael_SC0_B221_B240_clean_20261106',
    'work/analysis/Rafael2952_extended_release_verify_gc_v1_20261106': 'work/Rafael3222_extended_release_verify_gc_v1_20261106',
    'work/analysis/Rafael2952_extended_startup_gc_v1_20261106': 'work/Rafael3222_extended_startup_gc_v1_20261106',
    'work/analysis/Rafael2952_extended_Fernan_gc_v1_20261106': 'work/Rafael3222_extended_Fernan_gc_v1_20261106',
    '==(689,114,26)': '==(690,114,26)',
    'all403_individual_five_gates_pass': 'all270_individual_five_gates_pass',
    'scope=dict(source_variants=382,native_body_pages=383,typed_labels=21,observed_source_variants=173,\n        observed_body_pages=174,offline_only_source_variants=209,actual_review=conf[\'actual\'],':
        "scope=dict(source_variants=263,native_body_pages=279,typed_labels=7,observed_source_variants=86,\n"
        "        observed_body_pages=94,offline_only_source_variants=177,actual_review=conf['actual'],",
    'observed_menu_instances=6,observed_choice_labels=13,offline_only_captions=8':
        'observed_menu_instances=3,observed_choice_labels=7,offline_only_captions=0',
    "        assert not any(v is True and 'pending' in k for k,v in row.items() if k!='registered_release_and_completion_credit_pending')":
        """        if row.get('source_context_localization_formatting_gates_pending'):
            assert all(row['review'].values()) and not row['fresh_formatting_binding_pending']
            row['source_context_localization_formatting_gates_pending']=False
        assert not any(v is True and 'pending' in k for k,v in row.items() if k!='registered_release_and_completion_credit_pending')""",
    'editorial_review_current.Rafael2952_completion_v1.pending.json': 'editorial_review_current.Rafael3222_completion_v1.pending.json',
    'Rafael B201–B220 integrated once. All 689 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue with the next complete Rafael exchanges.':
        'Rafael B221–B240 integrated once. All 690 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue with the next complete Rafael exchanges.',
    'Credited 403 Rafael B201–B220 reviews once.': 'Credited 270 Rafael B221–B240 reviews once.',
})
counts = {'403':'270', '299':'221', '104':'49', '14394':'14797', '14797':'15067',
          '8706':'8927', '6091':'6140', '14800':'15070'}
source = re.sub(r'(?<![A-Za-z0-9_])(?:403|299|104|14394|14797|8706|6091|14800)(?![0-9])',
                lambda match: counts[match[0]], source)
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-registered-only-coverage-credit', 'exec'), globals())

