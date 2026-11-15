"""Document one ordinary complete-word soft wrap that avoids an unnecessary second page."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B275_B285_clean_20261110')

def main():
    before=ROOT/'formatting_v1/page_phrase_preferences_v2.json';after=before.with_name('page_phrase_preferences_v3.json');assert not after.exists()
    prefs=deepcopy(load(before));item=prefs['records']['SC3_B280_STYLE_8_90'];assert item['one_page']
    assert item.pop('required_pairs')==[['as','soon'],['as','possible']]
    item['reason']='Retain a complete-word ordinary soft wrap inside as soon as possible. This preserves the complete source paragraph on one page instead of stranding I was told on a separate page. No viewport, glyph, control, native phase or bounds rule changes.'
    item['QA_line_ending_retention']=dict(line_index=1,exact_line='guarding the map to the Proof as',
        reason='This exact ordinary word boundary keeps all words and facts on one readable page. The source/current/English hashes bind it; the original stylistic warning is retained. Fresh native complete-character, bounds, consumption andpagination checks remain required.')
    prefs.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),one_scoped_ordinary_soft_boundary_not_a_native_guard_waiver=True)
    save(after,prefs);print('Bound one exact complete-word soft-wrap retention;no prose or native guard changes.')

if __name__=='__main__':main()
