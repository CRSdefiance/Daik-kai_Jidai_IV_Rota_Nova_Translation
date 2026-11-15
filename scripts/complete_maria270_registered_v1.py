"""Credit the 270 registered subset exactly once while leaving complete B50 uncredited."""
import re
from scripts.complete_maria301_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/maria301_release_v1':'work/maria270_release_v1',
    'maria301_integrated_final_review_v1.json':'maria270_integrated_final_review_v1.json',
    'Maria_SC3_B0_B32_contextual_integrated_20261109':'Maria_SC3_B37_B49_contextual_integrated_20261109',
    'Maria_SC3_B0_B32_clean_20261109':'Maria_SC3_B37_B49_display_20261109',
    'all301_individual_five_gates_pass':'all270_individual_five_gates_pass',
    'observed_menu_instances=1,observed_choice_labels=2':'observed_menu_instances=2,observed_choice_labels=4',
    'typed_labels=2':'typed_labels=4','justified_layout_retentions=2':'justified_layout_retentions=6',
    'Maria B0–B32 contextual dialogue integrated once over the registered cumulative Hodram residual release.':
        'Maria B37–B49 contextual dialogue integrated once over the registered market-corrected cumulative release.',
    'The prior layers and ASCII right-bound correction are preserved.':'The prior layers, market correction and ASCII right-bound correction are preserved.',
    'editorial_review_current.Maria301_completion_v1.pending.json':'editorial_review_current.Maria270_completion_v1.pending.json',
    'Credited301 Maria reviews once.':'Credited270 Maria reviews once;complete B50 remains active anduncredited.',
})
counts={'301':'270','178':'161','123':'109','19161':'19462','19462':'19732','11710':'11871','7752':'7861',
    '19465':'19735','299':'266','303':'272','92':'63','96':'69','207':'203','709':'711','44':'46','36':'28','35':'26'}
pattern=re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source=pattern.sub(lambda m:counts[m[0]],source)
if __name__=='__main__':
    exec(compile(source,__file__+'::same-once-only-credit-prefix-andunrelated-ledger-preservation-contract','exec'),globals())
