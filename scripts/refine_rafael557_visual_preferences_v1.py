"""Bind observed sparse openings, phrase splits and page tails to exact unchanged prose."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

SOURCE=Path('translations/rafael_B141_B160_visual_preferences_v3.json')
DOC=Path('translations/rafael_B141_B160_formatting_manuscript_v3.json')
OUT=Path('translations/rafael_B141_B160_visual_preferences_v4.json')

if __name__=='__main__':
    assert not OUT.exists();doc,prefs=map(load,[DOC,SOURCE]);prefs=deepcopy(prefs)
    rows={r['id']:r for r in doc['records']}
    def preference(block,index,reason,**values):
        ident=f'DK4_MES_B{block}_R{index:04d}';row=rows[ident]
        prefs['records'][ident]=dict(bindings={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']},reason=reason,**values)
    preference(141,110,'Keep the short rally Let\'s go intact instead of splitting the verb phrase across the two rows.',line_phrases=["Let's go"])
    preference(142,5,'Use two well-filled rows instead of three short ones. The ordinary infinitive break after to preserves the complete continuation; validate native glyphs and bounds.',
        ordinary_boundaries=[['to','deciphering']],QA_line_ending_retention=dict(exact_line='This Red Dye is the key to',
            reason='This ordinary infinitive continuation is clear across two balanced native rows; retaining the narrow to/deciphering boundary avoids an unnecessary third row without shortening prose.'))
    preference(143,5,'Keep the admiral title with the dynamic surname in the guard\'s introduction.',line_phrases=['Admiral {MACRO:FA}'])
    preference(143,63,'Keep Mr. with the dynamic surname in Albuquerque\'s hesitant recognition.',line_phrases=['Mr. {MACRO:FA}'])
    preference(143,137,'Keep the short summon Bring in intact rather than breaking after Bring.',line_phrases=['Bring in'])
    for block,index in [(143,115),(143,129),(143,189),(143,372),(146,15),(150,13),(152,15)]:
        preference(block,index,'The unchanged paragraph should be tested on one complete native page rather than stranding a short fragment or the personal name on a second page. Every ordinary width, phase and QA check still applies.',one_page=True)
    preference(143,123,'Keep the full company-operations/location phrase together on the second page instead of stranding only southeastern Africa.',
        page_clause="in the Espinosa Company's operations in southeastern Africa.")
    preference(143,380,'Start the second page with the complete market-share consequence rather than stranding only its final battle reference.',
        page_clause='Their market share in cities near the battle will fall a little, too.')
    preference(143,403,'Start the second page with the complete build-up advice rather than stranding and for investment.',
        page_clause='Build up enough money for a proper fleet and for investment.')
    preference(152,144,'Keep the complete conditional offer and limit together on page two rather than stranding its final object.',
        page_clause="I can help you defeat him, but I can't support you in anything else.")
    prefs.update(previous_preferences=str(SOURCE),previous_preferences_sha256=sha(SOURCE.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),no_prose_changes_or_authored_breaks=True,
        candidate_preferences_require_fresh_plan_andchanged_native_pages=True)
    save(OUT,prefs);print('Bound17 preferences including the earlier negated question;all wording retained. Newplans/nativepages mustpass.')
