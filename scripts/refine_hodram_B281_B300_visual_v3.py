"""Retain two better layouts and freeze the warning-free visual candidate."""
from copy import deepcopy
from scripts.audit_story_glyph_consistency import load,save
from scripts.refine_hodram_B281_B300_visual_v1 import ROOT,INITIAL

OUT=ROOT/'formatting_v1/visual_preferences_v5.json'
RETENTIONS=ROOT/'layout_trial_retentions_v5.json'

def main():
    assert not OUT.exists() and not RETENTIONS.exists()
    p=deepcopy(load(ROOT/'formatting_v1/visual_preferences_v4.json'))
    before={r['id']:r for r in load(INITIAL)['records']}
    reasons={
        'DK4_MES_B296_R0050':'The current three-row layout already keeps a great deal together, with readable full-width rows and complete gunpowder/rock meaning. The trial produces identical bytes; retain it.',
        'SC1_B290_STYLE_1924_0':'Keeping scare it together first stranded run on a tiny final row; protecting that phrase made the opening only We tried. The original balanced two-row sentence uses the width better. Retain its ordinary scare/it continuation without shortening prose.',
    }
    kept=[]
    for key,reason in reasons.items():
        del p['records'][key]
        kept.append(dict(id=key,reason=reason,retained_lines=before[key]['lines'],retained_encoded_hex=before[key]['encoded_hex']))
    save(OUT,p);save(RETENTIONS,dict(records=kept,new_credit=0))
    print('28 revised layout candidates; two justified layout retentions.')

if __name__=='__main__':main()
