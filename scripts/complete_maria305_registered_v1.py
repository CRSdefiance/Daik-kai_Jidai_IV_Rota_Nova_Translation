"""Credit305 disjoint original mixed objects once after registration andown startup."""
import re
from scripts.complete_maria390_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'Credit390 unique contextual reviews':'Credit305 unique contextual reviews',
    'work/maria390_B152_B175_release_v1':'work/maria305_B176_B195_release_v1',
    'maria390_B152_B175_integrated_final_review_v1.json':'maria305_B176_B195_integrated_final_review_v1.json',
    'Maria_SC3_B152_B175_contextual_integrated_20261110':'Maria_SC3_B176_B195_contextual_integrated_20261110',
    'Maria_SC3_B152_B175_clean_20261109':'Maria_SC3_B176_B195_clean_20261110',
    'all390_individual_five_gates_pass':'all305_individual_five_gates_pass',
    'scope=dict(source_variants=373,native_body_pages=373,typed_labels=17,observed_source_variants=83,':
        'scope=dict(source_variants=294,native_body_pages=302,typed_labels=11,observed_source_variants=127,',
    'observed_body_pages=83,offline_only_source_variants=290,':
        'observed_body_pages=132,observed_page_occurrences=135,offline_only_source_variants=167,',
    'observed_menu_instances=2,observed_choice_labels=5,offline_only_captions=12':
        'observed_menu_instances=3,observed_choice_labels=7,offline_only_captions=4,physical_style_alternatives=22,observed_style_alternatives=3,offline_only_style_alternatives=19',
    "'current_story_gameplay_utterances':83,'current_story_gameplay_pages':83":
        "'current_story_gameplay_utterances':127,'current_story_gameplay_pages':132",
    'qualified_scoped_names=47,scoped_FE_guard_reserves=8,additional_phrase_wrap_fixes=11,pages_reclaimed=1,owned_FE_padding_bytes_repaired=1,whole_exchange_retentions_reopened=1,proposed_revisions=154,justified_retentions=236,observed_current_batch_source_bodies=83,':
        'qualified_scoped_names=27,scoped_FE_guard_reserves=2,additional_phrase_wrap_fixes=17,pages_reclaimed=0,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=26,observed_FE_blank_rows_repaired=1,proposed_revisions=205,justified_retentions=100,observed_current_batch_source_bodies=127,',
    'current_batch_actual_gameplay_observations=83,current_batch_actual_gameplay_pages=83':
        'current_batch_actual_gameplay_observations=127,current_batch_actual_gameplay_pages=132',
    'Maria B152–B175 contextual town/random dialogue,source-faithful wine reply,wrapping,menus andowned FE padding repair integrated once over registered Maria335 B137-B151.':
        'Maria B176–B195 contextual dialogue,parrot echoes,letter voices andsignatures,wrapping,menus,glyph andFE row repairs integrated once over registered Maria390 B152-B175.',
    'own startup and 12 protected original name getters passed':'own startup and both original getters for12 protected actors passed',
    'editorial_review_current.Maria390_B152_B175_completion_v1.pending.json':'editorial_review_current.Maria305_B176_B195_completion_v1.pending.json',
    'Credited390 Maria reviews once;154 revisions/236 retentions;original source membership preserved.':
        'Credited305 Maria reviews once;205 revisions/100 retentions;original source membership preserved.',
})
counts={'390':'305','154':'205','236':'100','719':'720','54':'55','21691':'22081','22081':'22386',
    '13200':'13405','8881':'8981','22084':'22389'}
pattern=re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source=pattern.sub(lambda m:counts[m[0]],source)
if __name__=='__main__':exec(compile(source,__file__+'::same-once-only-source-credit-andearlier-ledger-prefix-guards','exec'),globals())
