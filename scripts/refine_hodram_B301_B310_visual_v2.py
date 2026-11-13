"""Keep necessary page turns at complete sentences instead of shortening prose."""
from copy import deepcopy
from scripts.audit_story_glyph_consistency import load,save
from scripts.refine_hodram_B301_B310_visual_v1 import ROOT,PREFERENCES

OUT=ROOT/'formatting_v1/visual_preferences_v4.json'
def main():
    assert not OUT.exists()
    trial=load(ROOT/'formatting_v1/visual_trial_v3/automatic_plans.json')
    clauses={
        'DK4_MES_B310_R0016':"All right. I'll tell you, but keep it quiet.",
        'SC1_B308_STYLE_8_90':'We were told their village lies far northeast of China.',
        'SC1_B308_STYLE_8_716':'It was... far northeast of China, yes?',
    }
    assert {r['id'] for r in trial['failures']}==clauses.keys()
    p=deepcopy(load(PREFERENCES))
    for key,clause in clauses.items():
        p['records'][key].update(one_page=False,page_clause=clause,
            reason='The full-width one-page trial cannot preserve all words and required phrase boundaries. Keep the necessary page turn, but keep this complete final sentence on one page: '+clause)
    save(OUT,p)
    print('Preserved three necessary page turns; whole final sentences are protected. Prose unchanged.')
if __name__=='__main__':main()
