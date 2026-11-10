"""Credit the exact 186 B166–B167 reviews once after own startup and patch verification."""
import re
from scripts.complete_rafael1674_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'Rafael1674_extended_release_verified_v1_20261105':'Rafael1860_extended_release_verified_v1_20261105',
    'rafael_B161_B165_integrated_final_review_v1.json':'rafael_B166_B167_integrated_final_review_v1.json',
    'Rafael_SC0_B161_B165_contextual_integrated_20261105':'Rafael_SC0_B166_B167_contextual_integrated_20261105',
    'Rafael_SC0_B161_B165_research_20261105':'Rafael_SC0_B166_B167_offline_20261105',
    'Rafael1674_extended_release_verify_gc_v1_20261105':'Rafael1860_extended_release_verify_gc_v1_20261105',
    'Rafael1674_extended_startup_gc_v1_20261105':'Rafael1860_extended_startup_gc_v1_20261105',
    'Rafael1674_extended_Fernan_gc_v1_20261105':'Rafael1860_extended_Fernan_gc_v1_20261105',
    '==(684,114,26)':'==(685,114,26)',
    'source_variants=67,native_body_pages=68,typed_labels=0,observed_source_variants=55,':
        'source_variants=186,native_body_pages=187,typed_labels=0,observed_source_variants=101,',
    'observed_body_pages=56,offline_only_source_variants=12':'observed_body_pages=102,offline_only_source_variants=85',
    'editorial_review_current.Rafael1674_completion_v1.pending.json':
        'editorial_review_current.Rafael1860_completion_v1.pending.json',
    "ledger['latest_checkpoint']='Rafael B161–B165 integrated once. All 684 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue the complete clean-first B166 and B167 drafts. Main and full scope preserved.'":
        "ledger['latest_checkpoint']='Rafael B166–B167 integrated once. All 685 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue B168 display and the B169 clean-first drafts. Main and full scope preserved.'",
    'Credited 67 Rafael B161–B165 reviews once. Main preserved and full goal active.':
        'Credited 186 Rafael B166–B167 reviews once. Main preserved and full goal active.',
})
counts={'67':'186','51':'146','16':'40','13452':'13519','13519':'13705','7702':'7848','5817':'5857','13522':'13708'}
source=re.sub(r'(?<![A-Za-z0-9_])(?:67|51|16|13452|13519|7702|5817|13522)(?![0-9])',lambda m:counts[m[0]],source)
source=source.replace('all67_individual_five_gates_pass','all186_individual_five_gates_pass')
if __name__=='__main__':
    exec(compile(source,__file__+'::same-once-only-credit-for-two-complete-blocks','exec'),globals())
