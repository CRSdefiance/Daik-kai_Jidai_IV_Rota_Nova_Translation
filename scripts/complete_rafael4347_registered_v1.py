"""Credit Rafael B301–B320 once after release registration."""
import re

from scripts.complete_rafael3894_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'work/rafael3894_release_v1': 'work/rafael4347_release_v1',
    'rafael_B281_B300_integrated_final_review_v1.json': 'rafael_B301_B320_integrated_final_review_v1.json',
    'Rafael_SC0_B281_B300_contextual_integrated_20261106': 'Rafael_SC0_B301_B320_contextual_integrated_20261106',
    'Rafael_SC0_B281_B300_clean_20261106': 'Rafael_SC0_B301_B320_clean_20261106',
    '==(696,114,31)': '==(697,114,32)',
    "startup['only_owned_Zaganos_surname_differs_in_ARM9']":
        "startup['ARM9_COMMON_HELP_font_equal_registered_runtime_parent'] and release['all_other_files_components_graphics_names_andruntime_exact_to_parent']",
    'all245_individual_five_gates_pass': 'all453_individual_five_gates_pass',
    'scope=dict(source_variants=240,native_body_pages=248,typed_labels=5,observed_source_variants=27,':
        'scope=dict(source_variants=442,native_body_pages=444,typed_labels=11,observed_source_variants=45,',
    "observed_body_pages=31,offline_only_source_variants=213,actual_review=conf['actual'],":
        "observed_body_pages=47,offline_only_source_variants=397,actual_review=conf['actual'],",
    'observed_menu_instances=2,observed_choice_labels=5':
        'observed_menu_instances=5,observed_choice_labels=11',
    'Rafael B281–B300 integrated once in Rafael3894. The prior stages and ASCII right-bound correction are preserved. The exact clean-input patch, own startup and Zaganos name getters passed.':
        'Rafael B301–B320 integrated once in Rafael4347. The prior layers and ASCII right-bound correction are preserved. The exact clean-input patch, own startup and six inherited names passed.',
    'editorial_review_current.Rafael3894_completion_v1.pending.json':
        'editorial_review_current.Rafael4347_completion_v1.pending.json',
    'Credited 245 Rafael B281–B300 reviews once.': 'Credited 453 Rafael B301–B320 reviews once.',
})
counts = {'245': '453', '202': '397', '43': '56', '15494': '15739', '15739': '16192',
          '9491': '9888', '6248': '6304', '15742': '16195'}
source = re.sub(r'(?<![A-Za-z0-9_])(?:245|202|43|15494|15739|9491|6248|15742)(?![0-9])',
                lambda match: counts[match[0]], source)


if __name__ == '__main__':
    exec(compile(source, __file__ + '::verified-once-only-credit', 'exec'), globals())
