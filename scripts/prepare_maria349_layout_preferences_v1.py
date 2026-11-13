"""Bind phrase and page-flow preferences to exact source/current/logical text, without changing prose."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Maria_B275_B285_clean_20261110')

def main():
    p=ROOT/'formatting_v1/formatting_input.json';doc=load(p);byid={r['id']:r for r in doc['records']}
    initial=ROOT/'formatting_v1/initial_preferences.json';out=ROOT/'formatting_v1/page_phrase_preferences_v1.json';assert not out.exists()
    prefs=load(initial)
    def bind(ident,reason,**settings):
        row=byid[ident];prefs['records'][ident]=dict(bindings={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']},reason=reason,**settings)
    for ident in ['DK4_MES_B275_R0128','DK4_MES_B275_R0151','SC3_B280_STYLE_8_90','SC3_B280_STYLE_8_300','SC3_B280_STYLE_8_498','SC3_B280_STYLE_8_614']:
        bind(ident,'Attempt a complete one-page paragraph at the validated width without changing a word. This is a candidate constraint, not approval or a waiver; preserve two pages if no guarded complete-word solution exists.',one_page=True)
    bind('DK4_MES_B278_R0101','Keep taken in as a complete phrasal verb and join the following I at the boundary so the formatter cannot mistake sentence-final in for a dangling preposition.',required_pairs=[['taken','in'],['in','i']])
    bind('DK4_MES_B277_R0109','Keep Xien\'s complete conditional conclusion together on the second page rather than split stand up across a page boundary.',
        page_clause='it might gain the strength to stand up to the great powers.',required_pairs=[['stand','up']])
    bind('SC3_B280_STYLE_8_192','Keep the final complete invitation together; never leave Why at the end of a page.',page_clause="Why don't we go now?",required_pairs=[['why',"don't"]])
    bind('SC3_B280_STYLE_8_716','Keep the recalled far-northeast location and confirming question together rather than strand of China on the next page.',
        page_clause="It was... far northeast of China, wasn't it?",required_pairs=[['far','northeast'],['of','china']])
    prefs.update(manuscript=str(p),manuscript_sha256=digest(p),original_preferences=str(initial),original_preferences_sha256=digest(initial),
        native_guards_width_controls_glyphs_words_andmacro_counts_unchanged=True,new_credit=0)
    save(out,prefs);print('Saved ten exact paragraph preferences;all native/page checks remain required.')

if __name__=='__main__':main()
