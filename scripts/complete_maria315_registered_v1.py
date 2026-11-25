"""Credit315 disjoint reviews once after all registered release gates pass."""
import re
from scripts.complete_maria349_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'maria349_B275_B285': 'maria315_B286_B302',
    'Maria_SC3_B275_B285': 'Maria_SC3_B286_B302',
    'Maria_B275_B285_clean_20261110': 'Maria_B286_B302_clean_20261110',
    'all349_individual_five_gates_pass': 'all315_individual_five_gates_pass',
    "delta['final_changed_record_count']==10 and delta['pages_reclaimed']==3":
        "delta['final_layout_changes']==7 and delta['pages_reclaimed']==1",
    'scope=dict(source_variants=341,native_body_pages=347,typed_labels=8,observed_source_variants=191,':
        'scope=dict(source_variants=309,native_body_pages=309,typed_labels=6,observed_source_variants=213,',
    'observed_body_pages=193,observed_page_occurrences=193,offline_only_source_variants=150,':
        'observed_body_pages=213,observed_page_occurrences=213,offline_only_source_variants=96,',
    'observed_menu_instances=3,observed_distinct_menu_objects=3,observed_choice_labels=8,offline_only_captions=0,physical_style_alternatives=162,observed_style_alternatives=12,offline_only_style_alternatives=150':
        'observed_menu_instances=3,observed_distinct_menu_objects=3,observed_choice_labels=6,offline_only_captions=0,physical_style_alternatives=113,observed_style_alternatives=17,offline_only_style_alternatives=96',
    "'current_story_gameplay_utterances':191,'current_story_gameplay_pages':193":
        "'current_story_gameplay_utterances':213,'current_story_gameplay_pages':213",
    'qualified_scoped_names=19,scoped_FE_guard_reserves=0,additional_directly_viewed_page_repairs=3,pages_reclaimed=3,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=10,observed_FE_blank_rows_repaired=0,proposed_revisions=184,justified_retentions=165,observed_current_batch_source_bodies=191,':
        'qualified_scoped_names=14,scoped_FE_guard_reserves=0,additional_directly_viewed_page_repairs=6,pages_reclaimed=1,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=7,observed_FE_blank_rows_repaired=0,proposed_revisions=184,justified_retentions=165,observed_current_batch_source_bodies=213,',
    'current_batch_actual_gameplay_observations=191,current_batch_actual_gameplay_pages=193':
        'current_batch_actual_gameplay_observations=213,current_batch_actual_gameplay_pages=213',
    'ledger[BATCH].update(all_five_gates_pending=False,all_fifth_formatting_gates_pending=False,':
        'ledger[BATCH].update(direct_visual_review_pending=False,stored_checks_pending=False,gameplay_pending=False,all_five_gates_pending=False,all_fifth_formatting_gates_pending=False,',
    'Maria B275–B285 contextual smuggler andimpostor exchanges,guardian geography,forest/desert exploration,wrapping,menus andscoped names integrated once over registered Maria359 B253-B274.':
        'Maria B286–B302 contextual incense,armor,fog/cave,ghost ship,guardian,Sextant andmonk/book exchanges,wrapping,glyphs,menus andscoped names integrated once over registered Maria349 B275-B285.',
    'editorial_review_current.Maria349_B275_B285_completion_v1.pending.json':
        'editorial_review_current.Maria315_B286_B302_completion_v1.pending.json',
    'Credit349 unique contextual reviews': 'Credit315 unique contextual reviews',
    'Credited349 Maria reviews once;184 revisions/165 retentions;original source membership preserved.':
        'Credited315 Maria reviews once;162 revisions/153 retentions;original source membership preserved.',
})
counts = {'349': '315', '184': '162', '165': '153', '724': '725', '59': '60',
          '23429': '23778', '23778': '24093', '14181': '14343', '9597': '9750', '23781': '24096'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts, key=len, reverse=True))+r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda m: counts[m[0]], source)
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-once-only-credit-andexact-earlier-ledger-prefix-guards', 'exec'), globals())
