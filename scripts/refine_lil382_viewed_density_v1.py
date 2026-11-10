"""Keep reviewed phrases coherent while restoring fuller native first pages."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/Lil382_residual_A_clean_20261110')


def main():
    before = ROOT/'formatting_v1/viewed_phrase_preferences_v5.json'
    after = ROOT/'formatting_v1/viewed_density_preferences_v6.json'
    assert not after.exists()
    prefs = load(before)
    docpath = ROOT/'formatting_v1/formatting_input.json'
    rows = {r['id']:r for r in load(docpath)['records']}
    baselineview = ROOT/'native_body_v1/direct_visual_review_v1.json'
    phraseview = ROOT/'native_phrase_v1/direct_visual_review_v1.json'
    assert load(baselineview)['body_pages']==386 and load(phraseview)['body_pages']==5
    additions = {
        'DK4_MES_B12_R0006': ([['next','time']], 'Keep next time together in Aziza’s interrupted vow.'),
        'DK4_MES_B12_R0009': ([['next','time']], 'Keep next time together in Angel’s threat answering that vow.'),
        'DK4_MES_B12_R0053': ([['hear',"don't"],["don't",'you']], 'Attach the short question tag to hear instead of leaving it isolated.'),
        'DK4_MES_B12_R0099': ([['gang','up'],['up','on']], 'Keep the gang up on phrase together in Cristina’s condemnation.'),
        'DK4_MES_B12_R0163': ([['two','million']], 'Keep the exact two-million demand together as one readable amount.'),
        'DK4_MES_B13_R0018': ([['next','time']], 'Keep next time together in the separate withdrawal vow.'),
        'DK4_MES_B21_R0036': ([['miss','{macro:fa}']], 'Keep the respectful Miss FA form together without altering the macro or implying a noble title.'),
        'DK4_MES_B236_R0033': ([['gupta','dynasty']], 'Keep the Gupta dynasty reference together in Jam’s reported legend.'),
        'DK4_MES_B236_R0049': ([['jam','jack'],['jack','ludwyan']], 'Keep Jam Jack Ludwyan’s established signature together.'),
        'DK4_MES_B237_R0019': ([['demon-piercing','arrow']], 'Keep the installed Demon-Piercing Arrow title together where the current one-page paragraph permits.'),
        'DK4_MES_B238_R0036': ([['sort','of']], 'Keep sort of together in the port worker’s glove claim.'),
        'DK4_MES_B240_R0033': ([['keep','the'],['the','change']], 'Keep the keep the change punchline together in Gabriel’s fake-payment joke.'),
        'DK4_MES_B240_R0065': ([['get','out'],['out','of'],['of','here']], 'Keep get out of here together in Gabriel’s attempted exit.'),
        'DK4_MES_B240_R0115': ([['came','for']], 'Keep came for together before the barkeep’s short question tag.'),
    }
    for ident,(pairs,reason) in additions.items():
        assert ident not in prefs['records']
        row = rows[ident]
        prefs['records'][ident] = dict(bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']},
            required_pairs=pairs,one_page=True,reason='Direct native-page review: '+reason+' Preserve every word and all physical/native constraints.')
    prefs['records']['DK4_MES_B3_R0033']['required_pairs'].append(['listen','up'])
    prefs['records']['DK4_MES_B3_R0033']['reason'] += ' The fresh page also separates Listen up; keep that phrase intact.'
    for ident,clause in {
        'DK4_MES_B12_R0196':'than an ordinary pirate.',
        'DK4_MES_B17_R0012':'yourself instead of your cargo?',
        'DK4_MES_B235_R0044':'narrowly escaped disaster,',
    }.items():
        assert clause in rows[ident]['english']
        prefs['records'][ident].update(page_clause=clause,
            reason='The directly viewed whole-thought preference makes internal rows on the four-row first page too sparse. Keep more text on page one and the complete closing comparison/escape phrase on page two; preserve all prose and native constraints.')
    prefs.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),
        direct_visual_proofs={str(p):digest(p) for p in [baselineview,phraseview]},
        no_prose_font_viewport_control_or_runtime_change=True,new_credit=0)
    save(after,prefs)
    print('Prepared14 additional phrase preferences,one follow-up andthree density corrections from direct page review.')


if __name__=='__main__':
    main()
