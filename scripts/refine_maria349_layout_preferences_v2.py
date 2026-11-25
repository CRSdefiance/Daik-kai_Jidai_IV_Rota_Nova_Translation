"""Keep fitting one-page candidates, reject impossible constraints and preserve complete phrases."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B275_B285_clean_20261110')

def main():
    before=ROOT/'formatting_v1/page_phrase_preferences_v1.json';after=before.with_name('page_phrase_preferences_v2.json');assert not after.exists()
    prefs=deepcopy(load(before));r=prefs['records']
    failed=load(ROOT/'plan_v2/automatic_plans.json')['failures']
    expected={'DK4_MES_B275_R0128','SC3_B280_STYLE_8_300','SC3_B280_STYLE_8_498'}
    assert {v['id'] for v in failed}==expected
    removed=[]
    for ident in sorted(expected):removed.append(dict(id=ident,preference=r.pop(ident),reason='The unchanged complete paragraph has no guarded four-row solution under this qualified planner. Preserve two pages; do not shorten prose or change width.'))
    for ident,pairs in {
        'DK4_MES_B275_R0151':[['in','command']],
        'SC3_B280_STYLE_8_90':[['as','soon'],['as','possible']],
        'SC3_B280_STYLE_8_614':[['to','the'],['the','proof']],
    }.items():
        assert r[ident]['one_page'];r[ident]['required_pairs']=pairs
        r[ident]['reason']+=' Keep the complete reviewed phrase together so the one-page constraint cannot leave its preposition or article dangling.'
    prefs.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),rejected_one_page_candidates=removed,
        rejected_candidates_keep_full_text_width_andtwo_page_guards=True)
    save(after,prefs);print('Retained three one-page candidates with phrase joins;three genuinely rejected constraints remain two pages.')

if __name__=='__main__':main()
