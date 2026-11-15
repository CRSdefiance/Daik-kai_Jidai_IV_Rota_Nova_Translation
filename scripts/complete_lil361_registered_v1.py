"""Credit361 disjoint source reviews once after registration and own-candidate checks."""
import re
from scripts.complete_lil269_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'lil269_B243_B282': 'lil361_B283_B298',
    'Lil269_B243_B282_clean_20261110': 'Lil361_B283_B298_clean_20261110',
    'Lil_SC2_B243_B282_contextual_integrated_20261110': 'Lil_SC2_B283_B298_contextual_integrated_20261110',
    'Lil_SC2_B243_B282_clean_20261110': 'Lil_SC2_B283_B298_clean_20261110',
    'all269_individual_five_gates_pass': 'all361_individual_five_gates_pass',
    "delta['final_layout_changes']==16 and delta['pages_reclaimed']==1": "delta['final_layout_changes']==9 and delta['pages_reclaimed']==0",
    'scope=dict(source_variants=262,native_body_pages=264,typed_labels=7,observed_source_variants=139,':
        'scope=dict(source_variants=352,native_body_pages=353,typed_labels=9,observed_source_variants=199,',
    'observed_body_pages=141,observed_page_occurrences=141,offline_only_source_variants=123,':
        'observed_body_pages=200,observed_page_occurrences=242,offline_only_source_variants=153,',
    'actual_menu_cursor_states=[0,1,2],observed_menu_instances=3,observed_distinct_menu_objects=3,observed_choice_labels=7,offline_only_captions=0,physical_style_alternatives=16,observed_style_alternatives=2,offline_only_style_alternatives=14':
        'actual_menu_cursor_states=[0,1,2],observed_menu_instances=4,observed_distinct_menu_objects=4,observed_choice_labels=9,offline_only_captions=0,physical_style_alternatives=177,observed_style_alternatives=24,offline_only_style_alternatives=153',
    "'current_story_gameplay_utterances':139,'current_story_gameplay_pages':141": "'current_story_gameplay_utterances':199,'current_story_gameplay_pages':200",
    'qualified_scoped_names=25,scoped_FE_guard_reserves=2,additional_directly_viewed_page_repairs=10,pages_reclaimed=1,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=16,observed_FE_blank_rows_repaired=1,proposed_revisions=104,justified_retentions=165,observed_current_batch_source_bodies=139,':
        'qualified_scoped_names=15,scoped_FE_guard_reserves=1,additional_directly_viewed_page_repairs=7,pages_reclaimed=0,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=9,observed_FE_blank_rows_repaired=1,proposed_revisions=178,justified_retentions=183,observed_current_batch_source_bodies=199,',
    'current_batch_actual_gameplay_observations=139,current_batch_actual_gameplay_pages=141':
        'current_batch_actual_gameplay_observations=199,current_batch_actual_gameplay_pages=200',
    'Lil B243-B282 town, expedition, figurehead, riddle and wanted-person exchanges, wrapping, glyphs, menus and scoped names integrated once over registered Lil382.':
        'Lil B283-B298 forest, cave, Angkor, fog, cliff and wristband exchanges, wrapping, glyphs, menus and scoped names integrated once over registered Lil269; earlier B294 context preserved without duplicate credit.',
    'editorial_review_current.Lil269_B243_B282_completion_v1.pending.json': 'editorial_review_current.Lil361_B283_B298_completion_v1.pending.json',
    'Credit269 unique contextual reviews': 'Credit361 unique contextual reviews',
    'Credited269 Lil reviews once;104 revisions/165 retentions;original source membership preserved.':
        'Credited361 Lil reviews once;178 revisions/183 retentions;original source membership preserved.',
})
counts = {'269': '361', '104': '178', '165': '183', '727': '728', '62': '63',
    '24475': '24744', '24744': '25105', '14704': '14882', '10040': '10223', '24747': '25108'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(sorted(counts, key=len, reverse=True)) + r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda m: counts[m[0]], source)

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-once-only-credit-unrelated-ledger-andearlier-prefix-guards', 'exec'), globals())
