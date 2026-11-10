"""Credit the exact 115 reviews after complete patch and candidate-own startup proof."""
import re

from scripts.complete_rafael1860_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'Rafael1860_extended_release_verified_v1_20261105': 'Rafael1975_extended_release_verified_v1_20261105',
    'rafael_B166_B167_integrated_final_review_v1.json': 'rafael_B168_B169_integrated_final_review_v1.json',
    'Rafael_SC0_B166_B167_contextual_integrated_20261105': 'Rafael_SC0_B168_B169_contextual_integrated_20261105',
    'Rafael_SC0_B166_B167_offline_20261105': 'Rafael_SC0_B168_B169_research_20261105',
    'Rafael1860_extended_release_verify_gc_v1_20261105': 'Rafael1975_extended_release_verify_gc_v1_20261105',
    'Rafael1860_extended_startup_gc_v1_20261105': 'Rafael1975_extended_startup_gc_v1_20261105',
    'Rafael1860_extended_Fernan_gc_v1_20261105': 'Rafael1975_extended_Fernan_gc_v1_20261105',
    '==(685,114,26)': '==(686,114,26)',
    'source_variants=186,native_body_pages=187,typed_labels=0,observed_source_variants=101,':
        'source_variants=115,native_body_pages=117,typed_labels=0,observed_source_variants=58,',
    'observed_body_pages=102,offline_only_source_variants=85': 'observed_body_pages=60,offline_only_source_variants=57',
    'all186_individual_five_gates_pass': 'all115_individual_five_gates_pass',
    'editorial_review_current.Rafael1860_completion_v1.pending.json': 'editorial_review_current.Rafael1975_completion_v1.pending.json',
    'Rafael B166–B167 integrated once. All 685 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue B168 display and the B169 clean-first drafts. Main and full scope preserved.':
        'Rafael B168–B169 integrated once. All 686 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue the 190 sealed B170–B176 drafts. Main and full scope preserved.',
    'Credited 186 Rafael B166–B167 reviews once. Main preserved and full goal active.':
        'Credited 115 Rafael B168–B169 reviews once. Main preserved and full goal active.',
})
counts = {'186':'115','146':'90','40':'25','13519':'13705','13705':'13820','7848':'7938','5857':'5882','13708':'13823'}
source = re.sub(r'(?<![A-Za-z0-9_])(?:186|146|40|13519|13705|7848|5857|13708)(?![0-9])',
                lambda m: counts[m[0]], source)
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-once-only-credit-for-two-complete-blocks', 'exec'), globals())
