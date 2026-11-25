"""Keep complete life-stake wording in two coherent pages after the one-page trial fails."""
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT
def main():
    original=ROOT/'formatting_v1/preferences_v5_visual_trials.json';out=ROOT/'formatting_v1/preferences_v6_page_retention.json'
    assert not out.exists();pref=load(original);row=pref['records']['DK4_MES_B51_R0082']
    assert row.pop('one_page') and row.pop('ordinary_boundaries')==[['blindly','in']]
    row.update(page_clause='enough to stake his life on it.',reason='The unchanged131-character paragraph has no valid one-page plan under its complete source/QA contract. Retain two pages andkeep the entire life-stake closing phrase together,rather than shortening prose or leaving only his life on it on page2.')
    pref.update(previous_preferences=str(original),previous_preferences_sha256=digest(original),one_page_R82_failure_preserved=True)
    save(out,pref)
if __name__=='__main__':main()
