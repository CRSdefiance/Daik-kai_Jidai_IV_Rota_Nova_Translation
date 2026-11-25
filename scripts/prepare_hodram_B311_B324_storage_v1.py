"""Bridge the sealed400-record visual proof to the unchanged mixed-object storage schema."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B311_B324_formatting_v1 import ROOT, FORMATTING as DOC
from scripts.review_hodram_B311_B324_contextual_v1 import CURRENT
from scripts.source_locked_derivation_v5118 import checked_text

PLAN = ROOT/'visual_plan_v4/automatic_plans.json'
NATIVE = ROOT/'native_final_v4/compiled_native_pages.json'
STYLES = ROOT/'native_style_delta_v4/compiled_style_objects.json'
VIEW = ROOT/'offline_visual_approval_v4.json'
OUT = ROOT/'storage_inputs_v1'

def main():
    assert not OUT.exists()
    doc, plan, native, styles, view, names = map(load, [DOC, PLAN, NATIVE, STYLES, VIEW,
        ROOT/'name_planes_v1/native_name_planes.json'])
    assert len(doc['records']) == 400 and len(plan['records']) == len(native['records']) == 387
    assert native['pages'] == view['final_native_pages'] == 389
    assert view['final_all389_pages_directly_viewed_or_exact_reused']
    assert view['initial_all389_pages_directly_viewed'] and view['all39_trial_pages_directly_viewed']
    assert view['final_two_new_pages_directly_viewed']
    assert view['eleven_scoped_name_retentions_ten_native_strings_viewed']
    assert view['thirteen_captions_six_native_menus_viewed']
    assert view['layouts_revised'] == 27 and view['layouts_retained'] == 12
    assert view['final_native_sha256'] == digest(NATIVE)
    assert all(view['evidence'][str(p)] == digest(p) for p in [DOC, PLAN, NATIVE, STYLES])
    assert native['manuscript_sha256'] == styles['manuscript_sha256'] == plan['manuscript_sha256'] == digest(DOC)
    assert native['plan_sha256'] == styles['plan_sha256'] == digest(PLAN)
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact'] and not native['actual_gameplay']
    assert native['runtime'] == styles['runtime'] == names['runtime'] == doc['runtime']
    assert all(r['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
               for r in doc['records'])
    assert not plan['failures'] and not any(i['severity'] in ['error','warning']
        for r in plan['records'] for i in r['base_QA']['issues'])
    after = {r['id']: r for r in plan['records']}
    assert len(styles['objects']) == 38 and styles['physical_alternatives'] == 236
    assert styles['native_target_slot_cases'] == 304
    for obj in styles['objects']:
        assert digest(obj['target_path']) == obj['target_sha256']
        for slot in obj['native_slots']:
            assert slot['target_hex'] == bytes.fromhex(after[slot['record_id']]['encoded_hex'])[1:].hex()
            assert slot['complete_original_getter_pointer_body_terminator_stream_owner_andall_unowned4MiB_exact']
    for row in native['records']:
        assert row['compiled_hex'] == after[row['id']]['encoded_hex']
        assert len(row['native_alignment']['cases']) == 4
    # Reuse the original metadata-only bridge and all original menu-provider guards.
    original = Path('scripts/approve_hodram_B281_B300_display_v5.py').read_text(encoding='utf-8')
    suffix = original[original.index('    storage=deepcopy(doc)'):original.index("\nif __name__=='__main__':")]
    source = checked_text('def bridge():\n'+suffix, {
        'all131_style_inputs_match_final_native_plan': 'all236_style_inputs_match_final_native_plan',
        "len(groups)==5 and sum(len(g['record_IDs']) for g in groups)==11":
            "len(groups)==6 and sum(len(g['record_IDs']) for g in groups)==13",
        '374 final native pages approved; 28 wrap revisions, two layout retentions, one FE blank row and five glyph fixes. Storage inputs ready; fifth gates pending.':
            '389 final native pages approved;27 layout revisions,12 retentions andten glyph targets. Storage inputs ready; fifth gates pending.',
    })
    env = {**globals(), **locals()}
    exec(compile(source, __file__+'::original-storage-bridge-and-menu-provider-guards-new-scope', 'exec'), env)
    env['bridge']()

if __name__ == '__main__':
    main()
