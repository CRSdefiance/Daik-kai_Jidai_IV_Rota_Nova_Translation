"""Credit321 disjoint source reviews once after registration and own startup."""
import re
from scripts.complete_maria305_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'Credit305 unique contextual reviews': 'Credit321 unique contextual reviews',
    'work/maria305_B176_B195_release_v1': 'work/maria321_B196_B215_release_v1',
    'maria305_B176_B195_integrated_final_review_v1.json': 'maria321_B196_B215_integrated_final_review_v1.json',
    'Maria_SC3_B176_B195_contextual_integrated_20261110': 'Maria_SC3_B196_B215_contextual_integrated_20261110',
    'Maria_SC3_B176_B195_clean_20261110': 'Maria_SC3_B196_B215_clean_20261110',
    'all305_individual_five_gates_pass': 'all321_individual_five_gates_pass',
    'scope=dict(source_variants=294,native_body_pages=302,typed_labels=11,observed_source_variants=127,':
        'scope=dict(source_variants=317,native_body_pages=325,typed_labels=4,observed_source_variants=156,',
    'observed_body_pages=132,observed_page_occurrences=135,offline_only_source_variants=167,':
        'observed_body_pages=162,observed_page_occurrences=178,offline_only_source_variants=161,',
    'actual_menu_cursor_states=[0,1,2],observed_menu_instances=3,observed_choice_labels=7,offline_only_captions=4,physical_style_alternatives=22,observed_style_alternatives=3,offline_only_style_alternatives=19':
        'actual_menu_cursor_states=[0,1],observed_menu_instances=3,observed_distinct_menu_objects=2,observed_choice_labels=4,offline_only_captions=0,physical_style_alternatives=21,observed_style_alternatives=2,offline_only_style_alternatives=19',
    "'current_story_gameplay_utterances':127,'current_story_gameplay_pages':132":
        "'current_story_gameplay_utterances':156,'current_story_gameplay_pages':162",
    'qualified_scoped_names=27,scoped_FE_guard_reserves=2,additional_phrase_wrap_fixes=17,pages_reclaimed=0,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=26,observed_FE_blank_rows_repaired=1,proposed_revisions=205,justified_retentions=100,observed_current_batch_source_bodies=127,':
        'qualified_scoped_names=24,scoped_FE_guard_reserves=0,additional_directly_viewed_page_repairs=1,pages_reclaimed=1,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=19,observed_FE_blank_rows_repaired=0,proposed_revisions=171,justified_retentions=150,observed_current_batch_source_bodies=156,',
    'current_batch_actual_gameplay_observations=127,current_batch_actual_gameplay_pages=132':
        'current_batch_actual_gameplay_observations=156,current_batch_actual_gameplay_pages=162',
    'Maria B176–B195 contextual dialogue,parrot echoes,letter voices andsignatures,wrapping,menus,glyph andFE row repairs integrated once over registered Maria390 B152-B175.':
        'Maria B196–B215 contextual letters,training,town quests,source-faithful instructions,wrapping,menus andscoped names integrated once over registered Maria305 B176-B195.',
    'editorial_review_current.Maria305_B176_B195_completion_v1.pending.json':
        'editorial_review_current.Maria321_B196_B215_completion_v1.pending.json',
    'Credited305 Maria reviews once;205 revisions/100 retentions;original source membership preserved.':
        'Credited321 Maria reviews once;171 revisions/150 retentions;original source membership preserved.',
})
counts = {'305':'321','205':'171','100':'150','720':'721','55':'56',
    '22081':'22386','22386':'22707','13405':'13576','8981':'9131','22389':'22710'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda m:counts[m[0]],source)

if __name__ == '__main__':
    exec(compile(source,__file__+'::same-once-only-source-credit-andearlier-ledger-prefix-guards','exec'),globals())
