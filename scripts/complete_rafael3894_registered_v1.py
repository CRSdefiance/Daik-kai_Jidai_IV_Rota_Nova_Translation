"""Credit the 245 reviewed records once after registered patch and startup verification."""
import re

from scripts.complete_rafael3649_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'work/rafael3649_release_v1': 'work/rafael3894_release_v1',
    'rafael_B261_B280_integrated_final_review_v1.json': 'rafael_B281_B300_integrated_final_review_v1.json',
    'Rafael_SC0_B261_B280_contextual_integrated_20261106': 'Rafael_SC0_B281_B300_contextual_integrated_20261106',
    'Rafael_SC0_B261_B280_clean_20261106': 'Rafael_SC0_B281_B300_clean_20261106',
    '==(694,114,29)': '==(696,114,31)',
    "and release['all_nine_registered_final_stages_preserved']":
        "and release['all_nine_registered_final_stages_preserved'] and release['owned_Zaganos_surname_verified']",
    "names['both_name_getters_exact_for_actors_35_65_68_186_203']":
        "names['both_name_getters_exact_for_actors_35_65_68_70_186_203']",
    "startup['only_owned_Plett_Jacob_surnames_differ_in_ARM9']":
        "startup['only_owned_Zaganos_surname_differs_in_ARM9']",
    'all135_individual_five_gates_pass': 'all245_individual_five_gates_pass',
    'scope=dict(source_variants=130,native_body_pages=131,typed_labels=5,observed_source_variants=42,':
        'scope=dict(source_variants=240,native_body_pages=248,typed_labels=5,observed_source_variants=27,',
    "observed_body_pages=43,offline_only_source_variants=88,actual_review=conf['actual'],":
        "observed_body_pages=31,offline_only_source_variants=213,actual_review=conf['actual'],",
    'Rafael B261–B280 integrated once. Rafael3649 preserves the nine prior stages and adds both verified surnames. Exact patch and own startup pass. Continue with the next complete clean Japanese exchanges.':
        'Rafael B281–B300 integrated once in Rafael3894. The prior stages and ASCII right-bound correction are preserved. The exact clean-input patch, own startup and Zaganos name getters passed.',
    'editorial_review_current.Rafael3649_completion_v1.pending.json':
        'editorial_review_current.Rafael3894_completion_v1.pending.json',
    'Credited 135 Rafael B261–B280 reviews once.': 'Credited 245 Rafael B281–B300 reviews once.',
})
counts = {'135': '245', '118': '202', '17': '43', '15359': '15494', '15494': '15739',
          '9289': '9491', '6205': '6248', '15497': '15742'}
source = re.sub(r'(?<![A-Za-z0-9_])(?:135|118|17|15359|15494|9289|6205|15497)(?![0-9])',
                lambda match: counts[match[0]], source)

if __name__ == '__main__':
    exec(compile(source, __file__ + '::verified-once-only-credit', 'exec'), globals())
