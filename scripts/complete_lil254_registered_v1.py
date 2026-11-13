"""Credit the 254 Lil reviews once after exact registered integration."""

import re

from scripts.complete_lil278_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'lil278_B299_B311': 'lil254_B312_B319',
    'Lil278_B299_B311': 'Lil254_B312_B319',
    'Lil_SC2_B299_B311': 'Lil_SC2_B312_B319',
    'all278_individual_five_gates_pass': 'all254_individual_five_gates_pass',
    """    assert delta['counts']=={'plan_v1':25,'plan_v2':23} and delta['native_page_count']==280
    assert delta['all_logical_prose_unchanged'] and sha(Path(delta['plan']).read_bytes())==delta['plan_sha256']""":
        """    assert delta['changed_records']==17 and delta['FE_blank_row_repaired']=='DK4_MES_B316_R0205'
    assert [r['id'] for r in delta['changes'] if r['prose_changed']]==['DK4_MES_B319_R0008']
    assert sha(Path('work/Lil254_B312_B319_clean_20261110/plan_v6/automatic_plans.json').read_bytes())==delta['selected_plan_sha256']""",
    'source_variants=272,native_body_pages=280,typed_labels=6,observed_source_variants=52':
        'source_variants=246,native_body_pages=251,typed_labels=8,observed_source_variants=53',
    'observed_body_pages=55,observed_page_occurrences=55,offline_only_source_variants=220':
        'observed_body_pages=58,observed_page_occurrences=58,offline_only_source_variants=193',
    'actual_menu_cursor_states=[0,1],observed_menu_instances=3,observed_distinct_menu_objects=3,observed_choice_labels=6,offline_only_captions=0,physical_style_alternatives=139,observed_style_alternatives=5,offline_only_style_alternatives=134':
        'actual_menu_cursor_states=[0,1,2],observed_menu_instances=3,observed_distinct_menu_objects=3,observed_choice_labels=8,offline_only_captions=0,physical_style_alternatives=158,observed_style_alternatives=4,offline_only_style_alternatives=154',
    "'current_story_gameplay_utterances':52,'current_story_gameplay_pages':55":
        "'current_story_gameplay_utterances':53,'current_story_gameplay_pages':58",
    'scoped_FE_guard_reserves=0,additional_directly_viewed_page_repairs=23':
        'scoped_FE_guard_reserves=1,additional_directly_viewed_page_repairs=11',
    'source_bound_layout_changes=25,observed_FE_blank_rows_repaired=0':
        'source_bound_layout_changes=17,observed_FE_blank_rows_repaired=1',
    'observed_current_batch_source_bodies=52': 'observed_current_batch_source_bodies=53',
    'current_batch_actual_gameplay_observations=52,current_batch_actual_gameplay_pages=55':
        'current_batch_actual_gameplay_observations=53,current_batch_actual_gameplay_pages=58',
    'Lil B299-B311 expedition, spice commission, ferry and temple exchanges, wrapping, glyphs, menus and scoped names integrated once over registered Lil361.':
        'Lil B312-B319 expedition, ruins, divination and trade exchanges integrated once over registered Lil278.',
})
counts = {'278': '254', '170': '151', '108': '103', '729': '730', '64': '65',
          '25105': '25383', '25383': '25637', '15052': '15203', '10331': '10434', '25386': '25640'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(counts) + r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda match: counts[match[0]], source)


if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
