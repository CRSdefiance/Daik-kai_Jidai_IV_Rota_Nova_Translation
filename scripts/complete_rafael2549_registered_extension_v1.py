"""Credit the exact 384 records once after clean patch and own startup checks."""
import re
from scripts.complete_rafael2165_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'Rafael2165_extended_release_verified_v1_20261105': 'Rafael2549_extended_release_verified_v1_20261106',
    'rafael_B170_B176_integrated_final_review_v1.json': 'rafael_B181_B200_integrated_final_review_v1.json',
    'Rafael_SC0_B170_B176_contextual_integrated_20261105': 'Rafael_SC0_B181_B200_contextual_integrated_20261106',
    'Rafael_SC0_B170_B176_research_20261105': 'Rafael_SC0_B181_B200_research_20261106',
    'Rafael2165_extended_release_verify_gc_v1_20261105': 'Rafael2549_extended_release_verify_gc_v1_20261106',
    'Rafael2165_extended_startup_gc_v1_20261105': 'Rafael2549_extended_startup_gc_v1_20261106',
    'Rafael2165_extended_Fernan_gc_v1_20261105': 'Rafael2549_extended_Fernan_gc_v1_20261106',
    '==(687,114,26)': '==(688,114,26)',
    'all190_individual_five_gates_pass': 'all384_individual_five_gates_pass',
    'editorial_review_current.Rafael2165_completion_v1.pending.json': 'editorial_review_current.Rafael2549_completion_v1.pending.json',
    'Rafael B170–B176 integrated once. All 687 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue the B181–B200 clean intake. Main and full scope preserved.':
        'Rafael B181–B200 integrated once. All 688 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue the B201–B220 clean intake. Main and full scope preserved.',
    'Credited 190 Rafael B170–B176 reviews once. Main preserved and full goal active.':
        'Credited 384 Rafael B181–B200 reviews once. Main preserved and full goal active.',
})
counts = {'190':'384','152':'317','38':'67','13820':'14010','14010':'14394',
    '8090':'8407','5920':'5987','14013':'14397','72':'148','118':'236'}
source = re.sub(r'(?<![A-Za-z0-9_])(?:190|152|38|13820|14010|8090|5920|14013|72|118)(?![0-9])',
    lambda match: counts[match[0]], source)
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-once-only-credit-twenty-complete-blocks', 'exec'), globals())
