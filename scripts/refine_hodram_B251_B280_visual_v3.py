"""Keep two necessary page turns and reject their infeasible one-page trials."""
from copy import deepcopy
from scripts.audit_story_glyph_consistency import load,save
from scripts.refine_hodram_B251_B280_visual_v1 import ROOT,INITIAL
from scripts.refine_hodram_B251_B280_visual_v2 import OUT as PREVIOUS,RETENTIONS as OLD_RETENTIONS

OUT=ROOT/'formatting_v1/visual_preferences_v5.json';RETENTIONS=ROOT/'layout_trial_retentions_v5.json'

def main():
    assert not OUT.exists() and not RETENTIONS.exists()
    p=deepcopy(load(PREVIOUS));kept=deepcopy(load(OLD_RETENTIONS));before={r['id']:r for r in load(INITIAL)['records']}
    reasons={
        'DK4_MES_B259_R0086':'A forced one-page plan ends a row with of; preventing that weak ending makes the guarded one-page layout impossible. Retain the passing full-width two-page paragraph rather than shorten prose or waive QA.',
        'DK4_MES_B277_R0066':'A forced one-page plan ends a row with an; keeping the article with incredible makes the guarded one-page layout impossible. Retain the passing two-page paragraph and its complete hidden-inside phrase without shortening prose.',
    }
    for key,reason in reasons.items():
        del p['records'][key];r=before[key];kept['records'].append(dict(id=key,reason=reason,retained_lines=r['lines'],retained_encoded_hex=r['encoded_hex']))
    p['records']['DK4_MES_B271_R0066']['required_pairs'].append(['to','the'])
    save(OUT,p);save(RETENTIONS,kept);print('13 candidates remain; three original layouts have justified retentions.')

if __name__=='__main__':main()
