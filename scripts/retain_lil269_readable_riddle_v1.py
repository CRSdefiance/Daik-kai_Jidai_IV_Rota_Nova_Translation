"""Retain the complete native-proven riddle page after phrase trials add weak endings."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil269_B243_B282_clean_20261110')

if __name__ == '__main__':
    before = ROOT / 'formatting_v2/viewed_preferences_v10.json'
    output = ROOT / 'formatting_v2/viewed_preferences_v11.json'
    assert not output.exists()
    prefs = load(before)
    original = ROOT / 'formatting_v2/page_preferences_v5_FE.json'
    key = 'DK4_MES_B251_R0009'
    proof = ROOT / ('native_body_v2/complete_' + key + '.json')
    assert load(proof)['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
    prefs['records'][key] = load(original)['records'][key]
    prefs['records'][key]['reason'] += ' Retain the directly viewed complete single page: attempted on-top/water-level constraints introduce weak with/the row endings. Preserve the complete readable question and physical FE limits instead of adding a page or shortening prose.'
    prefs.update(previous_preferences=str(before), previous_preferences_sha256=digest(before))
    save(output, prefs)
    save(ROOT / 'riddle_layout_retention_v1.json', dict(id=key,
        native_receipt=str(proof), native_receipt_sha256=digest(proof),
        direct_visual_review=str(ROOT / 'visual_blocks_251_263_v1/direct_visual_review_v1.json'),
        trial_plans=['plan_v9', 'plan_v10'],
        trial_weak_endings_not_waived=True, complete_single_page_native_layout_retained=True,
        reason='The full question is readable and complete across the last two rows. Phrase trials produced weak endings; retain the native-proven page without shortening prose, widening the viewport or adding an unnecessary page.',
        new_credit=0))
