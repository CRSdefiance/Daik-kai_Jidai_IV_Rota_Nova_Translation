"""Record the first56 viewed pages and refine sparse openings and split phrases."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil269_B243_B282_clean_20261110')


def main():
    contact = ROOT / 'visual_blocks_243_250_v1/contact_manifest.json'
    visual = ROOT / 'visual_blocks_243_250_v1/direct_visual_review_v1.json'
    before = ROOT / 'formatting_v2/page_preferences_v5_FE.json'
    output = ROOT / 'formatting_v2/viewed_preferences_v6.json'
    assert not visual.exists() and not output.exists()
    viewed = load(contact)
    assert viewed['records'] == 55 and len(viewed['pages']) == 56 and len(viewed['sheets']) == 4
    assert all(digest(p['source']) == p['source_sha256'] for p in viewed['pages'])
    assert all(digest(s['path']) == s['sha256'] for s in viewed['sheets'])
    findings = {
        'DK4_MES_B243_R0018': 'The short opening A sailor who\'d leaves been on the next row; keep the verb phrase together and use fuller available rows.',
        'DK4_MES_B249_R0005': 'Keep along with together in the complete payment/expenses response.',
        'DK4_MES_B247_R0009': 'Keep called Leveque together in the directions while retaining the complete expedition request on page two.',
    }
    save(visual, dict(contact_manifest=str(contact), contact_manifest_sha256=digest(contact),
        pages=viewed['pages'], sheets=viewed['sheets'], directly_viewed_pages=56,
        every_listed_native_page_directly_viewed=True, complete_glyphs_andconsistent_font_observed=True,
        wrap_findings=findings, old_pages_do_not_approve_new_layouts=True, actual_gameplay=False, new_credit=0))
    prefs = load(before)
    rows = {r['id']: r for r in load(ROOT / 'formatting_v2/formatting_input.json')['records']}
    for ident, pairs in {
        'DK4_MES_B243_R0018': [["who'd", 'been'], ['golden', 'sand']],
        'DK4_MES_B249_R0005': [['along', 'with']],
        'DK4_MES_B247_R0009': [['called', 'leveque']],
    }.items():
        row = rows[ident]
        item = prefs['records'].setdefault(ident, dict(bindings={k: sha(row[k].encode())
            for k in ['source_hex', 'current_hex', 'english']}))
        item.setdefault('required_pairs', []).extend(pairs)
        if ident != 'DK4_MES_B247_R0009':
            item['one_page'] = True
        item['reason'] = 'Direct native-page review: ' + findings[ident] + ' Preserve all prose, full physical width and native constraints.'
    prefs.update(previous_preferences=str(before), previous_preferences_sha256=digest(before),
        direct_visual_receipt=str(visual), direct_visual_receipt_sha256=digest(visual),
        no_prose_font_geometry_or_runtime_changes=True)
    save(output, prefs)
    print('Recorded56 directly viewed pages and three scoped wrap refinements.')


if __name__ == '__main__':
    main()
