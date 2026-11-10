"""Credit303 disjoint source objects exactly once after registered release andown startup."""
import re
from scripts.complete_maria301_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'work/maria301_release_v1': 'work/maria303_release_v1',
    'maria301_integrated_final_review_v1.json': 'maria303_integrated_final_review_v1.json',
    'Maria_SC3_B0_B32_contextual_integrated_20261109': 'Maria_SC3_B58_B70_contextual_integrated_20261109',
    'Maria_SC3_B0_B32_clean_20261109': 'Maria_SC3_B58_B70_clean_20261109',
    'all301_individual_five_gates_pass': 'all303_individual_five_gates_pass',
    'observed_menu_instances=1,observed_choice_labels=2': 'observed_menu_instances=2,observed_choice_labels=4',
    'typed_labels=2': 'typed_labels=4',
    'justified_layout_retentions=2,': 'justified_layout_retentions=4,',
    'final_cumulative_integration_complete=True)':
        'final_cumulative_integration_complete=True,stored_andrepresentative_checks_pending=False,all_individual_fifth_gates_still_pending=False,current_batch_actual_gameplay_observations=116,current_batch_actual_gameplay_pages=116)',
    'Maria B0–B32 contextual dialogue integrated once over the registered cumulative Hodram residual release.':
        'Maria B58–B70 contextual dialogue andmenus integrated once over the registered cumulative Maria310 release.',
    'The prior layers and ASCII right-bound correction are preserved.':
        'All prior layers, the market fix, six-section ARM9 and ASCII right-bound correction are preserved.',
    'editorial_review_current.Maria301_completion_v1.pending.json': 'editorial_review_current.Maria303_completion_v1.pending.json',
    'Credited301 Maria reviews once.': 'Credited303 Maria reviews once;181 revisions/122 retentions.',
})
counts = {'301':'303', '178':'181', '123':'122', '19161':'20058', '19462':'20361',
    '11710':'12245', '7752':'8116', '19465':'20364', '303':'299', '92':'116', '96':'116',
    '207':'183', '709':'714', '44':'49', '36':'20', '35':'7'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda m: counts[m[0]], source)
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-once-only-credit-andexact-unrelated-ledger-prefixes303', 'exec'), globals())
