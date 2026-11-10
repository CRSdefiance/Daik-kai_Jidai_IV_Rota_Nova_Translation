"""Reject a longer phrasal-verb trial and resolve the three concrete QA findings."""
from copy import deepcopy
from scripts.audit_story_glyph_consistency import load,save
from scripts.refine_hodram_B251_B280_visual_v1 import ROOT,INITIAL,PREFERENCES

OUT=ROOT/'formatting_v1/visual_preferences_v4.json'
RETENTIONS=ROOT/'layout_trial_retentions_v4.json'

def main():
    assert not OUT.exists() and not RETENTIONS.exists()
    p=deepcopy(load(PREFERENCES));key='DK4_MES_B266_R0006';del p['records'][key]
    prior=next(r for r in load(INITIAL)['records'] if r['id']==key)
    save(RETENTIONS,dict(records=[dict(id=key,reason='The take-down constraint adds a row and strands the following subject/contraction. Original two-row ordinary verb/particle continuation uses the width better.',retained_lines=prior['lines'],retained_encoded_hex=prior['encoded_hex'])],new_credit=0))
    p['records']['DK4_MES_B259_R0086']['required_pairs']=[['of','themselves']]
    p['records']['DK4_MES_B271_R0066'].update(one_page=True,required_pairs=[['the','forbidden'],['forbidden','city']])
    p['records']['DK4_MES_B277_R0066']['required_pairs'].append(['an','incredible'])
    p['records']['DK4_MES_B270_R0013']['required_pairs'] += [["you'll",'do'],['do','it'],['it',"won't"],["won't",'you']]
    save(OUT,p);print('15 refined candidates; one worse original trial retained explicitly.')

if __name__=='__main__':main()
