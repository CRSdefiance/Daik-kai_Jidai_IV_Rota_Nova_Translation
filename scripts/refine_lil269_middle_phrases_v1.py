"""Preserve the complete middle-sheet review and keep four displayed phrases intact."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil269_B243_B282_clean_20261110')

if __name__ == '__main__':
    contact = ROOT / 'visual_blocks_251_263_v1/contact_manifest.json'
    visual = ROOT / 'visual_blocks_251_263_v1/direct_visual_review_v1.json'
    before = ROOT / 'formatting_v2/viewed_preferences_v8.json'
    output = ROOT / 'formatting_v2/viewed_preferences_v9.json'
    assert not output.exists() and not visual.exists()
    viewed = load(contact)
    assert viewed['records'] == 106 and len(viewed['pages']) == 106 and len(viewed['sheets']) == 6
    assert all(digest(p['source']) == p['source_sha256'] for p in viewed['pages'])
    assert all(digest(s['path']) == s['sha256'] for s in viewed['sheets'])
    changes = {
        'DK4_MES_B251_R0009': ([['on', 'top'], ['water', 'level']], 'The FE riddle now renders completely; keep on top and water level together within the same unchanged paragraph.'),
        'DK4_MES_B255_R0009': ([['jacks', 'bloom']], 'Keep the bound full name Jacks Bloom together.'),
        'DK4_MES_B257_R0063': ([["you've", 'been']], 'Keep the auxiliary phrase you\'ve been together in the rumor introduction.'),
        'DK4_MES_B262_R0017': ([['up', 'in']], 'Keep up in together in the reported Copenhagen directions.'),
    }
    save(visual, dict(contact_manifest=str(contact), contact_manifest_sha256=digest(contact),
        pages=viewed['pages'], sheets=viewed['sheets'], directly_viewed_pages=106,
        every_listed_native_page_directly_viewed=True, complete_glyphs_andconsistent_font_observed=True,
        FE_riddle_complete_andno_blank_row_observed=True,
        wrap_findings={k: v[1] for k, v in changes.items()},
        old_pages_do_not_approve_new_layouts=True, actual_gameplay=False, new_credit=0))
    prefs = load(before)
    rows = {r['id']: r for r in load(ROOT / 'formatting_v2/formatting_input.json')['records']}
    for ident, (pairs, reason) in changes.items():
        row = rows[ident]
        item = prefs['records'].setdefault(ident, dict(bindings={k: sha(row[k].encode())
            for k in ['source_hex', 'current_hex', 'english']}))
        item.setdefault('required_pairs', []).extend(pairs)
        item['one_page'] = True
        item['reason'] = 'Direct native-page review: ' + reason + ' Preserve all prose, physical geometry and native assertions.'
    prefs.update(previous_preferences=str(before), previous_preferences_sha256=digest(before),
        direct_visual_receipt=str(visual), direct_visual_receipt_sha256=digest(visual), new_credit=0)
    save(output, prefs)
