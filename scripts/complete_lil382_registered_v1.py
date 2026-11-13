"""Credit the 382 disjoint Lil reviews once, preserving every earlier ledger prefix."""
import re
from scripts.complete_maria315_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous, {
    'maria315_B286_B302': 'lil382_residual_A',
    'Maria_SC3_B286_B302_contextual_integrated_20261110': 'Lil_SC2_residual_A_382_contextual_integrated_20261110',
    'Maria_SC3_B286_B302_clean_20261110': 'Lil_SC2_residual_A_382_clean_20261110',
    'Maria_B286_B302_clean_20261110': 'Lil382_residual_A_clean_20261110',
    'all315_individual_five_gates_pass': 'all382_individual_five_gates_pass',
    "delta['final_layout_changes']==7 and delta['pages_reclaimed']==1": "delta['final_layout_changes']==30 and delta['pages_reclaimed']==5",
    'scope=dict(source_variants=309,native_body_pages=309,typed_labels=6,observed_source_variants=213,':
        'scope=dict(source_variants=378,native_body_pages=386,typed_labels=4,observed_source_variants=211,',
    'observed_body_pages=213,observed_page_occurrences=213,offline_only_source_variants=96,':
        'observed_body_pages=217,observed_page_occurrences=217,offline_only_source_variants=167,',
    'actual_menu_cursor_states=[0,1],observed_menu_instances=3,observed_distinct_menu_objects=3,observed_choice_labels=6,offline_only_captions=0,physical_style_alternatives=113,observed_style_alternatives=17,offline_only_style_alternatives=96':
        'actual_menu_cursor_states=[0],observed_menu_instances=2,observed_distinct_menu_objects=2,observed_choice_labels=4,offline_only_captions=0,physical_style_alternatives=14,observed_style_alternatives=2,offline_only_style_alternatives=12',
    "'current_story_gameplay_utterances':213,'current_story_gameplay_pages':213": "'current_story_gameplay_utterances':211,'current_story_gameplay_pages':217",
    'qualified_scoped_names=14,scoped_FE_guard_reserves=0,additional_directly_viewed_page_repairs=6,pages_reclaimed=1,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=7,observed_FE_blank_rows_repaired=0,proposed_revisions=162,justified_retentions=153,observed_current_batch_source_bodies=213,':
        'qualified_scoped_names=34,scoped_FE_guard_reserves=0,additional_directly_viewed_page_repairs=16,pages_reclaimed=5,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=30,observed_FE_blank_rows_repaired=0,proposed_revisions=257,justified_retentions=125,observed_current_batch_source_bodies=211,',
    'current_batch_actual_gameplay_observations=213,current_batch_actual_gameplay_pages=213':
        'current_batch_actual_gameplay_observations=211,current_batch_actual_gameplay_pages=217',
    "SC3_sha256=release['target_SC3_sha256']": "SC2_sha256=release['target_SC2_sha256']",
    'Maria B286–B302 contextual incense,armor,fog/cave,ghost ship,guardian,Sextant andmonk/book exchanges,wrapping,glyphs,menus andscoped names integrated once over registered Maria349 B275-B285.':
        'Lil residual A crew, Aziza, cross-story, letters and town/quest exchanges, wrapping, glyphs, menus and scoped names integrated once over registered Maria315; earlier B115 context preserved without duplicate credit.',
    'editorial_review_current.Maria315_B286_B302_completion_v1.pending.json': 'editorial_review_current.Lil382_residual_A_completion_v1.pending.json',
    'Credit315 unique contextual reviews': 'Credit382 unique contextual reviews',
    'Credited315 Maria reviews once;162 revisions/153 retentions;original source membership preserved.':
        'Credited382 Lil reviews once;257 revisions/125 retentions;original source membership preserved.',
})
counts={'315':'382','162':'257','153':'125','725':'726','60':'61',
        '23778':'24093','24093':'24475','14343':'14600','9750':'9875','24096':'24478'}
pattern=re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source=pattern.sub(lambda m:counts[m[0]],source)
if __name__=='__main__':
    exec(compile(source,__file__+'::same-once-only-credit-andunrelated-ledger-prefix-guards','exec'),globals())
