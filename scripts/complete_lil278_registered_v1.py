"""Credit the Lil B299–B311 contextual reviews after exact cumulative registration."""

import re

from scripts.complete_lil361_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'lil361_B283_B298': 'lil278_B299_B311',
    'Lil361_B283_B298': 'Lil278_B299_B311',
    'Lil_SC2_B283_B298': 'Lil_SC2_B299_B311',
    'all361_individual_five_gates_pass': 'all278_individual_five_gates_pass',
    'final_layout_delta_v2.json': 'final_layout_delta_v1.json',
    """    assert delta['final_layout_changes']==9 and delta['pages_reclaimed']==0
    for p,h in delta['evidence'].items():assert sha(Path(p).read_bytes())==h""":
        """    assert delta['counts']=={'plan_v1':25,'plan_v2':23} and delta['native_page_count']==280
    assert delta['all_logical_prose_unchanged'] and sha(Path(delta['plan']).read_bytes())==delta['plan_sha256']""",
    'source_variants=352,native_body_pages=353,typed_labels=9,observed_source_variants=199':
        'source_variants=272,native_body_pages=280,typed_labels=6,observed_source_variants=52',
    'observed_body_pages=200,observed_page_occurrences=242,offline_only_source_variants=153':
        'observed_body_pages=55,observed_page_occurrences=55,offline_only_source_variants=220',
    'actual_menu_cursor_states=[0,1,2],observed_menu_instances=4,observed_distinct_menu_objects=4,observed_choice_labels=9,offline_only_captions=0,physical_style_alternatives=177,observed_style_alternatives=24,offline_only_style_alternatives=153':
        'actual_menu_cursor_states=[0,1],observed_menu_instances=3,observed_distinct_menu_objects=3,observed_choice_labels=6,offline_only_captions=0,physical_style_alternatives=139,observed_style_alternatives=5,offline_only_style_alternatives=134',
    "'current_story_gameplay_utterances':199,'current_story_gameplay_pages':200":
        "'current_story_gameplay_utterances':52,'current_story_gameplay_pages':55",
    'qualified_scoped_names=15,scoped_FE_guard_reserves=1,additional_directly_viewed_page_repairs=7,pages_reclaimed=0,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=9,observed_FE_blank_rows_repaired=1':
        'qualified_scoped_names=10,scoped_FE_guard_reserves=0,additional_directly_viewed_page_repairs=23,pages_reclaimed=0,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=25,observed_FE_blank_rows_repaired=0',
    'observed_current_batch_source_bodies=199': 'observed_current_batch_source_bodies=52',
    'current_batch_actual_gameplay_observations=199,current_batch_actual_gameplay_pages=200':
        'current_batch_actual_gameplay_observations=52,current_batch_actual_gameplay_pages=55',
    'Lil B283-B298 forest, cave, Angkor, fog, cliff and wristband exchanges, wrapping, glyphs, menus and scoped names integrated once over registered Lil269; earlier B294 context preserved without duplicate credit.':
        'Lil B299-B311 expedition, spice commission, ferry and temple exchanges, wrapping, glyphs, menus and scoped names integrated once over registered Lil361.',
    'Credit361 unique contextual reviews': 'Credit 278 unique contextual reviews',
    'Credited361 Lil reviews once;178 revisions/183 retentions;original source membership preserved.':
        'Credited 278 Lil reviews once. Original source membership is preserved.',
})
counts = {'361': '278', '178': '170', '183': '108', '728': '729', '63': '64', '24744': '25105',
          '25105': '25383', '14882': '15052', '10223': '10331', '25108': '25386'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(counts) + r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda match: counts[match[0]], source)

if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
