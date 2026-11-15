"""Credit the final 261 native Lil reviews once after exact integration."""

import re

from scripts.complete_lil254_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "lil254_B312_B319": "lil261_B323_B335",
    "Lil254_B312_B319": "Lil261_B323_B335",
    "Lil_SC2_B312_B319": "Lil_SC2_B323_B335",
    "all254_individual": "all261_individual",
    "    assert delta['changed_records']==17 and delta['FE_blank_row_repaired']=='DK4_MES_B316_R0205'\n    assert [r['id'] for r in delta['changes'] if r['prose_changed']]==['DK4_MES_B319_R0008']": "    assert delta['changed_records'] == 30 and delta['no_prose_or_page_count_changed']",
    "plan_v6/automatic_plans.json": "plan_v7/automatic_plans.json",
    "delta['selected_plan_sha256']": "delta['plan_sha256']",
    "'registered_release_andcompletion_credit_pending','native_style_dispatch": "'registered_release_and_completion_credit_pending','registered_release_andcompletion_credit_pending','native_style_dispatch",
    "source_variants=246,native_body_pages=251,typed_labels=8,observed_source_variants=53": "source_variants=255,native_body_pages=258,typed_labels=6,observed_source_variants=58",
    "observed_body_pages=58,observed_page_occurrences=58,offline_only_source_variants=193": "observed_body_pages=61,observed_page_occurrences=61,offline_only_source_variants=197",
    "actual_menu_cursor_states=[0,1,2]": "actual_menu_cursor_states=[0,1]",
    "observed_choice_labels=8": "observed_choice_labels=6",
    "physical_style_alternatives=158": "physical_style_alternatives=119",
    "offline_only_style_alternatives=154": "offline_only_style_alternatives=115",
    "'current_story_gameplay_utterances':53,'current_story_gameplay_pages':58": "'current_story_gameplay_utterances':58,'current_story_gameplay_pages':61",
    "qualified_scoped_names=10,scoped_FE_guard_reserves=1,additional_directly_viewed_page_repairs=11": "qualified_scoped_names=9,scoped_FE_guard_reserves=0,additional_directly_viewed_page_repairs=30",
    "source_bound_layout_changes=17,observed_FE_blank_rows_repaired=1": "source_bound_layout_changes=30,observed_FE_blank_rows_repaired=0",
    "observed_current_batch_source_bodies=53": "observed_current_batch_source_bodies=58",
    "current_batch_actual_gameplay_observations=53,current_batch_actual_gameplay_pages=58": "current_batch_actual_gameplay_observations=58,current_batch_actual_gameplay_pages=61",
    "Lil B312-B319 expedition, ruins, divination and trade exchanges integrated once over registered Lil278.": "Lil B323-B335 fog, cave, trade commissions, survey and alchemy exchanges integrated once over registered Lil254.",
})

counts = {"65":"66","103":"63","151":"198","254":"261","730":"731","10434":"10497","15203":"15401","25383":"25637","25637":"25898","25640":"25901"}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(counts) + r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda match: counts[match[0]], source)

if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
