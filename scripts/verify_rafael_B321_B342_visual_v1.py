"""Combine exact native models after accepting or retaining each reviewed layout."""
from pathlib import Path
import inspect
from types import FunctionType

from scripts import verify_rafael_B281_B300_visual_delta_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B321_B342_v1 import ROOT
from scripts.source_locked_derivation_v5118 import checked_text


FORMATTING = ROOT / 'ordinary_formatting_manuscript_v2.json'
ORIGINAL = ROOT / 'refined_plan_v2/automatic_plans.json'
PLAN = ROOT / 'visual_plan_v3/automatic_plans.json'
FIRST_NATIVE = ROOT / 'native_pages_v1/compiled_native_pages.json'
DELTA_MANUSCRIPT = ROOT / 'visual_delta_inputs_v1/manuscript.json'
DELTA_PLAN = ROOT / 'visual_delta_inputs_v1/plan.json'
FRESH = ROOT / 'visual_delta_native_v1/compiled_native_pages.json'
FINAL = ROOT / 'final_native_pages_v1.json'
SHEETS = ROOT / 'accepted_delta_sheets_v1'
EXCLUDED = {
    'DK4_MES_B331_R0010', 'SC0_B333_STYLE_1784_168',
    'DK4_MES_B341_R0006', 'DK4_MES_B341_R0013', 'DK4_MES_B342_R0104',
}
APPROVAL = ROOT / 'complete_visual_review_v1.json'


source = checked_text(inspect.getsource(previous.combine), {
    "    new = {row['id']: row for row in fresh['records']}":
        """    all_fresh = {row['id']: row for row in fresh['records']}
    new = {ident: row for ident, row in all_fresh.items() if ident in delta}
    assert set(all_fresh) - set(new) == EXCLUDED
    assert len(all_fresh) == 57 and len(new) == 52""",
    "fresh['fresh_compiled_alignments'] == 4 * len(new)":
        "fresh['fresh_compiled_alignments'] == 4 * len(all_fresh)",
    "'review_sheets': [],":
        "'review_sheets': [], 'rejected_layout_candidates': sorted(EXCLUDED),",
})
env = {**vars(previous), **globals()}
env['inputs'] = FunctionType(previous.inputs.__code__, env)
exec(compile(source, __file__ + '::exact-model-selection-and-complete-native-provenance', 'exec'), env)


def approve():
    assert not APPROVAL.exists()
    native, baseline, fresh = map(load, (FINAL, FIRST_NATIVE, FRESH))
    first = load(ROOT / 'complete_baseline_visual_review_v1.json')
    assert first['native_sha256'] == digest(FIRST_NATIVE)
    viewed = load(ROOT / 'reviewed_refresh_sheets_v1.json')
    assert {(row['path'], row['sha256']) for row in viewed['sheets']} == {
        (row['path'], row['sha256']) for row in fresh['review_sheets']}
    names = load(ROOT / 'retained_name_planes_v1/native_name_planes.json')
    assert names['scoped_actors'] == 16 and names['distinct_strings'] == 15
    assert names['all_scoped_progressive_names_ASCII_complete_andfit_native216px']
    assert {(row['path'], row['sha256']) for row in viewed['name_sheets']} == {
        (row['path'], row['sha256']) for row in names['review_sheets']}
    menus = load(ROOT / 'second_visual_review_v1.json')['all_menu_sheets_directly_viewed']
    all_sheets = first['sheets'] + viewed['sheets'] + viewed['name_sheets'] + menus
    assert all(digest(row['path']) == row['sha256'] for row in all_sheets)
    assert native['runtime'] == baseline['runtime'] == fresh['runtime'] == names['runtime']
    assert (len(native['records']), native['pages']) == (540, 552)
    assert (native['fresh_visual_delta_records'], native['reused_unchanged_visual_records']) == (52, 488)
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact'] and not native['actual_gameplay']
    save(APPROVAL, dict(
        native=str(FINAL), native_sha256=digest(FINAL), plan=str(PLAN), plan_sha256=digest(PLAN),
        all_final_body_caption_and_name_sheets_directly_viewed=True, sheets=all_sheets,
        baseline_body_sheets=58, refreshed_sheets=len(viewed['sheets']), scoped_actors=16,
        five_proposed_layouts_rejected_and_original_reviewed_bytes_retained=sorted(EXCLUDED),
        fresh_accepted_layouts=52, exact_original_layouts_reused=488,
        all_final_speech_pages=552, logical_prose_unchanged=True, actual_gameplay=False, new_credit=0,
        stored_script_andactual_headers_transitions_andregistered_release_pending=True,
        evidence={str(path): digest(path) for path in (
            FINAL, FIRST_NATIVE, FRESH, PLAN, FORMATTING,
            ROOT/'complete_baseline_visual_review_v1.json',
            ROOT/'ordinary_visual_preferences_v8.json', Path(__file__),
        )},
    ))
    print('All 552 final pages, menu captions and scoped names are visually reviewed. Stored checks and gameplay remain.')


if __name__ == '__main__':
    env['combine']()
    approve()
