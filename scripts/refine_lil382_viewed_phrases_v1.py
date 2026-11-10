"""Record the first63 directly viewed pages and keep five split phrases together."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/Lil382_residual_A_clean_20261110')


def main():
    manifestpath = ROOT/'body_visual_B0_B11_v1/contact_manifest.json'
    receipt = ROOT/'body_visual_B0_B11_v1/direct_visual_review_v1.json'
    before = ROOT/'formatting_v1/page_coherence_preferences_v4.json'
    after = ROOT/'formatting_v1/viewed_phrase_preferences_v5.json'
    assert not receipt.exists() and not after.exists()
    manifest = load(manifestpath)
    assert manifest['records']==63 and len(manifest['pages'])==63 and len(manifest['sheets'])==4
    assert all(digest(s['path'])==s['sha256'] for s in manifest['sheets'])
    assert all(digest(p['source'])==p['source_sha256'] for p in manifest['pages'])
    findings = {
        'DK4_MES_B3_R0033': ([['blood','pumping']], 'Keep blood pumping together in Aziza’s excited battle speech.'),
        'DK4_MES_B8_R0009': ([['mouth','of'],['of','yours']], 'Keep mouth of yours together instead of the isolated final of yours row.'),
        'DK4_MES_B10_R0009': ([['out','of']], 'Keep out of together in Hayreddin’s southern-Mediterranean warning.'),
        'DK4_MES_B11_R0054': ([['all','of'],['of','a'],['a','sudden']], 'Keep all of a sudden together in Lil’s baffled poetry question.'),
        'DK4_MES_B11_R0066': ([['romantic','bone']], 'Keep romantic bone together in Camille’s affectionate teasing.'),
    }
    save(receipt,dict(contact_manifest=str(manifestpath),contact_manifest_sha256=digest(manifestpath),
        pages=manifest['pages'],sheets=manifest['sheets'],directly_viewed_pages=63,
        every_listed_native_page_directly_viewed=True,complete_glyphs_andconsistent_font_observed=True,
        wrap_findings={k:v[1] for k,v in findings.items()},
        old_pages_do_not_approve_new_layouts=True,actual_gameplay=False,new_credit=0))
    docpath = ROOT/'formatting_v1/formatting_input.json'
    rows = {r['id']:r for r in load(docpath)['records']}
    prefs = load(before)
    for ident,(pairs,reason) in findings.items():
        assert ident not in prefs['records']
        row = rows[ident]
        prefs['records'][ident] = dict(bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']},
            required_pairs=pairs,one_page=True,
            reason='Direct native-page review: '+reason+' Preserve all words and the full native width.')
    prefs.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),
        direct_visual_receipt=str(receipt),direct_visual_receipt_sha256=digest(receipt),
        no_prose_font_width_control_or_runtime_change=True,new_credit=0)
    save(after,prefs)
    print('Saved direct63-page review andfive phrase preferences;fresh changed pages still require native review.')


if __name__=='__main__':
    main()
