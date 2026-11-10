"""Retain a better two-row layout and protect complete page-boundary sentences."""
from copy import deepcopy
from scripts.audit_story_glyph_consistency import load,save
from scripts.refine_hodram_B301_B310_visual_v1 import ROOT,INITIAL

OUT=ROOT/'formatting_v1/visual_preferences_v5.json'
def main():
    assert not OUT.exists()
    p=deepcopy(load(ROOT/'formatting_v1/visual_preferences_v4.json'))
    key='SC1_B309_STYLE_1590_0'
    del p['records'][key]
    before=next(r for r in load(INITIAL)['records'] if r['id']==key)
    save(ROOT/'layout_trial_retention_v5.json',dict(records=[dict(id=key,
        reason='Protecting prompt-treatment creates three rows and a new wolf/has-fled split. The original balanced two-row reassurance reads better; retain its ordinary prompt/treatment continuation and full prospective meaning.',
        retained_lines=before['lines'],retained_encoded_hex=before['encoded_hex'])],new_credit=0))
    p['records']['DK4_MES_B310_R0016']['required_pairs'] += [['name','now'],['now','anyway']]
    p['records']['SC1_B308_STYLE_8_716']['required_pairs'] += [['where','its'],['its','guardian'],['guardian','clan'],['clan','lives']]
    p['records']['SC1_B309_STYLE_1590_394']['required_pairs'] += [['off','too']]
    save(OUT,p)
    print('Retained one better two-row layout; tightened three sentence/phrase boundaries.')
if __name__=='__main__':main()
