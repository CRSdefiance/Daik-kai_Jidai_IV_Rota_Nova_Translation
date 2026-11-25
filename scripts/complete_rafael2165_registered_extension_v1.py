"""Credit the 190 B170–B176 reviews after the verified clean patch and own startup."""
import re

from scripts.complete_rafael1975_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'Rafael1975_extended_release_verified_v1_20261105': 'Rafael2165_extended_release_verified_v1_20261105',
    'rafael_B168_B169_integrated_final_review_v1.json': 'rafael_B170_B176_integrated_final_review_v1.json',
    'Rafael_SC0_B168_B169_contextual_integrated_20261105': 'Rafael_SC0_B170_B176_contextual_integrated_20261105',
    'Rafael_SC0_B168_B169_research_20261105': 'Rafael_SC0_B170_B176_research_20261105',
    'Rafael1975_extended_release_verify_gc_v1_20261105': 'Rafael2165_extended_release_verify_gc_v1_20261105',
    'Rafael1975_extended_startup_gc_v1_20261105': 'Rafael2165_extended_startup_gc_v1_20261105',
    'Rafael1975_extended_Fernan_gc_v1_20261105': 'Rafael2165_extended_Fernan_gc_v1_20261105',
    '==(686,114,26)': '==(687,114,26)',
    'source_variants=115,native_body_pages=117,typed_labels=0,observed_source_variants=58,':
        'source_variants=190,native_body_pages=190,typed_labels=0,observed_source_variants=72,',
    'observed_body_pages=60,offline_only_source_variants=57': 'observed_body_pages=72,offline_only_source_variants=118',
    'all115_individual_five_gates_pass': 'all190_individual_five_gates_pass',
    'editorial_review_current.Rafael1975_completion_v1.pending.json': 'editorial_review_current.Rafael2165_completion_v1.pending.json',
    'Rafael B168–B169 integrated once. All 686 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue the 190 sealed B170–B176 drafts. Main and full scope preserved.':
        'Rafael B170–B176 integrated once. All 687 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue the B181–B200 clean intake. Main and full scope preserved.',
    'Credited 115 Rafael B168–B169 reviews once. Main preserved and full goal active.':
        'Credited 190 Rafael B170–B176 reviews once. Main preserved and full goal active.',
})
counts = {'115':'190','90':'152','25':'38','13705':'13820','13820':'14010','7938':'8090','5882':'5920','13823':'14013'}
source = re.sub(r'(?<![A-Za-z0-9_])(?:115|90|25|13705|13820|7938|5882|13823)(?![0-9])',
                lambda m: counts[m[0]], source)
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-once-only-credit-seven-complete-blocks', 'exec'), globals())
