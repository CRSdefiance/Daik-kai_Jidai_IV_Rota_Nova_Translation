"""Apply exact phrase and page preferences to three reported wrapping findings."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B201_B220_v1 import FORMATTING, PREFERENCES, ROOT, digest
from dk4tool.patch.grand_race_menu_release import sha


OUT = ROOT/'ordinary_visual_preferences_v2.json'
PREFS = {
    'DK4_MES_B205_R0025': dict(one_page=True,
        reason='Keep the short explanation of the peppers and local ingredients on one page.'),
    'DK4_MES_B208_R0229': dict(line_phrases=['the time to buy'],
        reason='Keep the purchase thought together and remove the orphaned final fragment.'),
    'DK4_MES_B218_R0048': dict(page_clause="You'll be on good terms just like that.",
        reason='Turn the page between complete sentences so the seller’s final assurance starts intact.'),
}


def main():
    assert not OUT.exists()
    prefs = load(PREFERENCES)
    rows = {r['id']:r for r in load(FORMATTING)['records']}
    prefs['records'] = {ident:{**spec,'bindings':{key:sha(rows[ident][key].encode('utf-8'))
        for key in ('source_hex','current_hex','english')}} for ident,spec in PREFS.items()}
    prefs['prior_plan_diagnostics_sha256'] = digest(ROOT/'ordinary_plans_v1/diagnostics.json')
    save(OUT,prefs)


if __name__ == '__main__':
    main()

