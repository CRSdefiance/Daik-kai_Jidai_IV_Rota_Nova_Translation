"""Credit363 disjoint clean-source reviews once after registration and own startup."""
import re
from scripts.complete_maria321_registered_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'maria321_B196_B215':'maria363_B216_B252',
    'Maria_SC3_B196_B215':'Maria_SC3_B216_B252',
    'all321_individual_five_gates_pass':'all363_individual_five_gates_pass',
    'scope=dict(source_variants=317,native_body_pages=325,typed_labels=4,observed_source_variants=156,':'scope=dict(source_variants=351,native_body_pages=353,typed_labels=12,observed_source_variants=252,',
    'observed_body_pages=162,observed_page_occurrences=178,offline_only_source_variants=161,':'observed_body_pages=254,observed_page_occurrences=273,offline_only_source_variants=99,',
    'actual_menu_cursor_states=[0,1],observed_menu_instances=3,observed_distinct_menu_objects=2,observed_choice_labels=4,offline_only_captions=0,physical_style_alternatives=21,observed_style_alternatives=2,offline_only_style_alternatives=19':'actual_menu_cursor_states=[0,1,2],observed_menu_instances=9,observed_distinct_menu_objects=5,observed_choice_labels=12,offline_only_captions=0,physical_style_alternatives=85,observed_style_alternatives=10,offline_only_style_alternatives=75',
    "'current_story_gameplay_utterances':156,'current_story_gameplay_pages':162":"'current_story_gameplay_utterances':252,'current_story_gameplay_pages':254",
    'qualified_scoped_names=24,scoped_FE_guard_reserves=0,additional_directly_viewed_page_repairs=1,pages_reclaimed=1,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=19,observed_FE_blank_rows_repaired=0,proposed_revisions=171,justified_retentions=150,observed_current_batch_source_bodies=156,':'qualified_scoped_names=29,scoped_FE_guard_reserves=3,additional_directly_viewed_page_repairs=1,pages_reclaimed=0,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=1,source_bound_layout_changes=15,observed_FE_blank_rows_repaired=1,proposed_revisions=202,justified_retentions=161,observed_current_batch_source_bodies=252,',
    'current_batch_actual_gameplay_observations=156,current_batch_actual_gameplay_pages=162':'current_batch_actual_gameplay_observations=252,current_batch_actual_gameplay_pages=254',
    'Maria B196–B215 contextual letters,training,town quests,source-faithful instructions,wrapping,menus andscoped names integrated once over registered Maria305 B176-B195.':'Maria B216–B252 contextual town andguild quests,forest exchanges,source-faithful riddle instructions,wrapping,menus andscoped names integrated once over registered Maria321 B196-B215.',
    'editorial_review_current.Maria321_B196_B215_completion_v1.pending.json':'editorial_review_current.Maria363_B216_B252_completion_v1.pending.json',
    'Credit321 unique contextual reviews':'Credit363 unique contextual reviews',
    'Credited321 Maria reviews once;171 revisions/150 retentions;original source membership preserved.':'Credited363 Maria reviews once;202 revisions/161 retentions;original source membership preserved.',
})
counts = {'321':'363','171':'202','150':'161','721':'722','56':'57',
    '22386':'22707','22707':'23070','13576':'13778','9131':'9292','22710':'23073'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda m:counts[m[0]],source)

if __name__ == '__main__':
    exec(compile(source,__file__+'::same-once-only-ledger-credit-andexact-earlier-prefix-guards','exec'),globals())
