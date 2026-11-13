"""Credit269 disjoint reviews once only after registration and own-candidate checks."""
import re
from scripts.complete_lil382_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'lil382_residual_A': 'lil269_B243_B282',
    'Lil_SC2_residual_A_382_contextual_integrated_20261110': 'Lil_SC2_B243_B282_contextual_integrated_20261110',
    'Lil_SC2_residual_A_382_clean_20261110': 'Lil_SC2_B243_B282_clean_20261110',
    'Lil382_residual_A_clean_20261110': 'Lil269_B243_B282_clean_20261110',
    'all382_individual_five_gates_pass': 'all269_individual_five_gates_pass',
    'final_layout_delta_v1.json': 'final_layout_delta_v2.json',
    "delta['final_layout_changes']==30 and delta['pages_reclaimed']==5": "delta['final_layout_changes']==16 and delta['pages_reclaimed']==1",
    'scope=dict(source_variants=378,native_body_pages=386,typed_labels=4,observed_source_variants=211,':
        'scope=dict(source_variants=262,native_body_pages=264,typed_labels=7,observed_source_variants=139,',
    'observed_body_pages=217,observed_page_occurrences=217,offline_only_source_variants=167,':
        'observed_body_pages=141,observed_page_occurrences=141,offline_only_source_variants=123,',
    'actual_menu_cursor_states=[0],observed_menu_instances=2,observed_distinct_menu_objects=2,observed_choice_labels=4,offline_only_captions=0,physical_style_alternatives=14,observed_style_alternatives=2,offline_only_style_alternatives=12':
        'actual_menu_cursor_states=[0,1,2],observed_menu_instances=3,observed_distinct_menu_objects=3,observed_choice_labels=7,offline_only_captions=0,physical_style_alternatives=16,observed_style_alternatives=2,offline_only_style_alternatives=14',
    "'current_story_gameplay_utterances':211,'current_story_gameplay_pages':217": "'current_story_gameplay_utterances':139,'current_story_gameplay_pages':141",
    'qualified_scoped_names=34,scoped_FE_guard_reserves=0,additional_directly_viewed_page_repairs=16,pages_reclaimed=5,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=30,observed_FE_blank_rows_repaired=0,proposed_revisions=257,justified_retentions=125,observed_current_batch_source_bodies=211,':
        'qualified_scoped_names=25,scoped_FE_guard_reserves=2,additional_directly_viewed_page_repairs=10,pages_reclaimed=1,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=16,observed_FE_blank_rows_repaired=1,proposed_revisions=257,justified_retentions=125,observed_current_batch_source_bodies=139,',
    'current_batch_actual_gameplay_observations=211,current_batch_actual_gameplay_pages=217':
        'current_batch_actual_gameplay_observations=139,current_batch_actual_gameplay_pages=141',
    'Lil residual A crew, Aziza, cross-story, letters and town/quest exchanges, wrapping, glyphs, menus and scoped names integrated once over registered Maria315; earlier B115 context preserved without duplicate credit.':
        'Lil B243-B282 town, expedition, figurehead, riddle and wanted-person exchanges, wrapping, glyphs, menus and scoped names integrated once over registered Lil382.',
    'editorial_review_current.Lil382_residual_A_completion_v1.pending.json': 'editorial_review_current.Lil269_B243_B282_completion_v1.pending.json',
    'Credit382 unique contextual reviews': 'Credit269 unique contextual reviews',
    'Credited382 Lil reviews once;257 revisions/125 retentions;original source membership preserved.':
        'Credited269 Lil reviews once;104 revisions/165 retentions;original source membership preserved.',
})
counts = {'382': '269', '257': '104', '125': '165', '726': '727', '61': '62',
    '24093': '24475', '24475': '24744', '14600': '14704', '9875': '10040', '24478': '24747'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(sorted(counts, key=len, reverse=True)) + r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda m: counts[m[0]], source)
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-once-only-credit-andunrelated-ledger-prefix-guards', 'exec'), globals())
