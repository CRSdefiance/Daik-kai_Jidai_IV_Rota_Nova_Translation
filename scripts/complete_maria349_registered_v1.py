"""Credit349 disjoint reviews once after every registered release gate passes."""
import re
from scripts.complete_maria359_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'maria359_B253_B274':'maria349_B275_B285',
    'Maria_SC3_B253_B274':'Maria_SC3_B275_B285',
    'Maria_B253_B274_clean_20261110':'Maria_B275_B285_clean_20261110',
    'all359_individual_five_gates_pass':'all349_individual_five_gates_pass',
    "delta['final_changed_record_count']==34 and delta['pages_reclaimed']==1":"delta['final_changed_record_count']==10 and delta['pages_reclaimed']==3",
    'scope=dict(source_variants=349,native_body_pages=350,typed_labels=10,observed_source_variants=164,':
        'scope=dict(source_variants=341,native_body_pages=347,typed_labels=8,observed_source_variants=191,',
    'observed_body_pages=165,observed_page_occurrences=165,offline_only_source_variants=185,':
        'observed_body_pages=193,observed_page_occurrences=193,offline_only_source_variants=150,',
    'observed_menu_instances=5,observed_distinct_menu_objects=5,observed_choice_labels=10,offline_only_captions=0,physical_style_alternatives=131,observed_style_alternatives=12,offline_only_style_alternatives=119':
        'observed_menu_instances=3,observed_distinct_menu_objects=3,observed_choice_labels=8,offline_only_captions=0,physical_style_alternatives=162,observed_style_alternatives=12,offline_only_style_alternatives=150',
    "'current_story_gameplay_utterances':164,'current_story_gameplay_pages':165":"'current_story_gameplay_utterances':191,'current_story_gameplay_pages':193",
    'qualified_scoped_names=18,scoped_FE_guard_reserves=0,additional_directly_viewed_page_repairs=1,pages_reclaimed=1,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=34,observed_FE_blank_rows_repaired=0,proposed_revisions=219,justified_retentions=140,observed_current_batch_source_bodies=164,':
        'qualified_scoped_names=19,scoped_FE_guard_reserves=0,additional_directly_viewed_page_repairs=3,pages_reclaimed=3,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=10,observed_FE_blank_rows_repaired=0,proposed_revisions=219,justified_retentions=140,observed_current_batch_source_bodies=191,',
    'current_batch_actual_gameplay_observations=164,current_batch_actual_gameplay_pages=165':'current_batch_actual_gameplay_observations=191,current_batch_actual_gameplay_pages=193',
    'Maria B253–B274 contextual town quests,scurvy medicine,jungle andforest exchanges,carronade research,wrapping,menus andscoped names integrated once over registered Maria363 B216-B252.':
        'Maria B275–B285 contextual smuggler andimpostor exchanges,guardian geography,forest/desert exploration,wrapping,menus andscoped names integrated once over registered Maria359 B253-B274.',
    'editorial_review_current.Maria359_B253_B274_completion_v1.pending.json':'editorial_review_current.Maria349_B275_B285_completion_v1.pending.json',
    'Credit359 unique contextual reviews':'Credit349 unique contextual reviews',
    'Credited359 Maria reviews once;219 revisions/140 retentions;original source membership preserved.':'Credited349 Maria reviews once;184 revisions/165 retentions;original source membership preserved.',
})
counts={'359':'349','219':'184','140':'165','723':'724','58':'59',
    '23070':'23429','23429':'23778','13997':'14181','9432':'9597','23432':'23781'}
pattern=re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source=pattern.sub(lambda m:counts[m[0]],source)
if __name__=='__main__':exec(compile(source,__file__+'::same-once-only-credit-andexact-earlier-ledger-prefix-guards','exec'),globals())
