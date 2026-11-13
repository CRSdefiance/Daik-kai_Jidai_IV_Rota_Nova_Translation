"""Bind every Lil261 editorial decision to stored and representative display proof."""

from scripts.finalize_lil254_research_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "Seal 254 mixed": "Seal 261 mixed",
    "Lil254_B312_B319_clean_20261110": "Lil261_B323_B335_clean_20261110",
    "lil_B312_B319_": "lil_B323_B335_",
    "contextual_review_v2.json": "contextual_review_v1.json",
    "scoped_names_v2.json": "scoped_names_v1.json",
    "formatting_v2/": "formatting_v1/",
    "plan_v6/": "plan_v7/",
    "{'revision':151, 'retention':103}": "{'revision':198, 'retention':63}",
    "== 254": "== 261",
    "== 246": "== 255",
    "len(stored['records']) == 88 and len(stored['style_records']) == 158 and stored['typed_labels_checked'] == 8": "len(stored['records']) == 136 and len(stored['style_records']) == 119 and stored['typed_labels_checked'] == 6",
    "(251, 251, 984)": "(258, 258, 1020)",
    "(41, 210, 330)": "(83, 175, 455)",
    "(158, 216, 27)": "(119, 144, 18)",
    "== 243": "== 162",
    "(25841,1,53,58)": "(26561,1,58,61)",
    "actual['observed_pages_including_repeats'] == 58 and actual['offline_only_source_body_objects'] == 193": "actual['observed_pages_including_repeats'] == 61 and actual['offline_only_source_body_objects'] == 197",
    "actual['repaired_B316_alert_and_B319_company_substitution_observed'] and actual['both_B317_source_selector_00_headers_observed']": "actual['all_thirteen_FE_returns_observed'] and actual['scoped_Guildmaster_and_Charles_headers_observed']",
    "delta['changed_records'] == len(delta['changes']) == 17 and delta['FE_blank_row_repaired'] == 'DK4_MES_B316_R0205'": "delta['changed_records'] == len(delta['changes']) == 30 and delta['no_prose_or_page_count_changed']",
    "delta['selected_plan_sha256']==digest(paths['plan']) and [r['id'] for r in delta['changes'] if r['prose_changed']] == ['DK4_MES_B319_R0008']": "delta['plan_sha256'] == digest(paths['plan'])",
    "all254_": "all261_",
    "all10_": "all9_",
    "len(names['records']) == 10": "len(names['records']) == 9",
    "source246_release_plans": "source255_release_plans",
    "source_editorial_objects=254": "source_editorial_objects=261",
    "source_body_objects=246, physical_native_bodies=246": "source_body_objects=255, physical_native_bodies=255",
    "records=254, revisions=151, retentions=103, complete_exchanges=8": "records=261, revisions=198, retentions=63, complete_exchanges=13",
    "physical_body_candidates=246, native_body_pages=251, typed_labels=8, scoped_names=10, name_strings=13": "physical_body_candidates=255, native_body_pages=258, typed_labels=6, scoped_names=9, name_strings=12",
    "native_body_pages=251, source_editorial_body_objects=246": "native_body_pages=258, source_editorial_body_objects=255",
    "source_styles=158, source_style_objects=27, source_FE_records=7, physical_FE_panels=7": "source_styles=119, source_style_objects=18, source_FE_records=13, physical_FE_panels=13",
    "source_bound_layout_changes=17, scoped_FE_guard_reserves=1": "source_bound_layout_changes=30, scoped_FE_guard_reserves=0",
    "observed_FE_blank_rows_repaired=1": "observed_FE_blank_rows_repaired=0",
    "actual_source_body_objects=53": "actual_source_body_objects=58",
    "actual_body_pages=58": "actual_body_pages=61",
    "actual_pages=58": "actual_pages=61",
    "observed_pages_including_repeats=58": "observed_pages_including_repeats=61",
    "offline_only_source_body_objects=193": "offline_only_source_body_objects=197",
    "actual_caption_strings=8": "actual_caption_strings=6",
    "actual_frames=25841": "actual_frames=26561",
    "Sealed 254 five-gate reviews and 10": "Sealed 261 five-gate reviews and nine",
})


if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
