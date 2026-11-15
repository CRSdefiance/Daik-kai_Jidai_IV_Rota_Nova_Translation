"""Keep the displayed subject, short tag, proper names and closing idiom coherent."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil269_B243_B282_clean_20261110')

if __name__ == '__main__':
    before = ROOT / 'formatting_v2/viewed_preferences_v11.json'
    output = ROOT / 'formatting_v2/viewed_preferences_v12.json'
    assert not output.exists()
    contact = ROOT / 'visual_blocks_264_282_v1/contact_manifest.json'
    viewed = load(contact)
    assert viewed['records'] == 100 and len(viewed['pages']) == 101 and len(viewed['sheets']) == 6
    assert all(digest(p['source']) == p['source_sha256'] for p in viewed['pages'])
    assert all(digest(p['path']) == p['sha256'] for p in viewed['sheets'])
    changes = {
        'DK4_MES_B243_R0018': ([['a', 'sailor'], ['sailor', "who'd"]], 'The freshly viewed phrase trial creates an even sparser A sailor opening. Keep its subject and relative-clause verb together, retaining to the New World and golden sand.'),
        'DK4_MES_B270_R0006': ([['heart', "haven't"], ["haven't", 'you']], 'Attach the short haven\'t you question tag to heart.'),
        'DK4_MES_B270_R0013': ([['plett', 'perrault']], 'Keep the approved full name Plett Perrault together.'),
        'DK4_MES_B271_R0019': ([['worth', 'your'], ['your', 'while']], 'Keep worth your while together in the captured-alive reward response.'),
        'DK4_MES_B271_R0067': ([['forbidden', 'city']], 'Keep the source Forbidden City location name together.'),
    }
    save(ROOT / 'visual_blocks_264_282_v1/direct_visual_review_v1.json', dict(
        contact_manifest=str(contact), contact_manifest_sha256=digest(contact),
        pages=viewed['pages'], sheets=viewed['sheets'], directly_viewed_pages=101,
        every_listed_native_page_directly_viewed=True, complete_glyphs_andconsistent_font_observed=True,
        wrap_findings={k: v[1] for k, v in changes.items() if 'B243' not in k},
        old_pages_do_not_approve_new_layouts=True, actual_gameplay=False, new_credit=0))
    prefs = load(before)
    rows = {r['id']: r for r in load(ROOT / 'formatting_v2/formatting_input.json')['records']}
    for ident, (pairs, reason) in changes.items():
        row = rows[ident]
        item = prefs['records'].setdefault(ident, dict(bindings={k: sha(row[k].encode())
            for k in ['source_hex', 'current_hex', 'english']}))
        item.setdefault('required_pairs', []).extend(pairs)
        item['one_page'] = True
        item['reason'] = 'Direct native-page review: ' + reason + ' Preserve every word and native geometry/guards.'
    prefs.update(previous_preferences=str(before), previous_preferences_sha256=digest(before), new_credit=0)
    save(output, prefs)
