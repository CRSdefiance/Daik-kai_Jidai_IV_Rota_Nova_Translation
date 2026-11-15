"""Try the complete conqueror-warning paragraph on one native page without changing prose."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Maria_B286_B302_clean_20261110')
def main():
    manuscript=ROOT/'formatting_v1/formatting_input.json';initial=ROOT/'formatting_v1/initial_preferences.json'
    out=ROOT/'formatting_v1/question_page_preference_v1.json';assert not out.exists()
    doc=load(manuscript);row=next(r for r in doc['records'] if r['id']=='DK4_MES_B298_R0049')
    prefs=load(initial);assert row['id'] not in prefs['records']
    prefs['records'][row['id']]=dict(bindings={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']},
        reason='Initial native plans leave into their hands on a second page. Try the unchanged complete paragraph on one page at the validated width;reject rather than shorten prose orwaive native guards if it cannot fit.',
        one_page=True,required_pairs=[['by','force'],['into','their'],['their','hands']])
    prefs.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),original_preferences=str(initial),original_preferences_sha256=digest(initial),
        full_prose_font_width_controls_andruntime_unchanged=True,new_credit=0)
    save(out,prefs)
if __name__=='__main__':main()
