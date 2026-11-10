"""Reject sparse/longer trials and preserve the preferable original layouts explicitly."""
from copy import deepcopy
from scripts.refine_hodram_B231_B250_visual_v1 import ROOT,PREFERENCES,INITIAL
from scripts.audit_story_glyph_consistency import load,save

OUT=ROOT/'formatting_v1/visual_preferences_v2.json'
RETENTIONS=ROOT/'layout_trial_retentions_v2.json'

def main():
    assert not OUT.exists() and not RETENTIONS.exists()
    prefs=deepcopy(load(PREFERENCES))
    reasons={
        'DK4_MES_B232_R0020':'The complete item-title constraint leaves sparse intermediate rows and detaches shell from its. Original four-row title continuation is preferable.',
        'DK4_MES_B233_R0049':'Original full opening and knew/content-clause continuation read naturally. Trial detaches all from I and makes row two shorter.',
        'DK4_MES_B234_R0035':'Keeping far reaches on one row adds a page. The ordinary adjective/noun continuation is preferable to an avoidable page turn.',
        'DK4_MES_B236_R0030':'The guarded full-width one-page trial necessarily ends a row with the article the. Preserve the passing two-page plan; a complete-sentence page constraint would make the first page sparse. No prose is shortened.',
        'DK4_MES_B239_R0030':'The trial shortens row two and separates begin from its infinitive. Existing explain/it all continuation uses width more naturally.',
        'DK4_MES_B239_R0042':'The find-it constraint adds a row and shortens the opening. Original three-row object continuation is readable.',
        'DK4_MES_B241_R0044':'The give-me constraint adds a row and strands I put them. Original three-row ordinary continuation is preferable.',
        'DK4_MES_B241_R0074':'The trial merely exchanges a well/they continuation for how/well. Retain the established full-width reassurance.',
        'DK4_MES_B243_R0064':'The trial separates are/you and creates a shorter final row. Original considering/it continuation keeps the complete question tag together.',
    }
    for key in reasons: del prefs['records'][key]
    edits={
        'DK4_MES_B238_R0035':dict(page_clause='before the entire convoy was destroyed.'),
        'DK4_MES_B238_R0044':dict(page_clause='escaped the danger.'),
        'DK4_MES_B240_R0018':dict(page_clause='Such a grand name!',required_pairs=[['such','a'],['a','grand'],['grand','name']]),
        'DK4_MES_B240_R0028':dict(required_pairs=[['instead','of']]),
    }
    for key,options in edits.items():
        row=prefs['records'][key]
        prefs['records'][key]={k:row[k] for k in ['reason','bindings']}|options
    save(OUT,prefs)
    original={r['id']:r for r in load(INITIAL)['records']}
    save(RETENTIONS,dict(records=[dict(id=k,reason=v,retained_encoded_hex=original[k]['encoded_hex'],retained_lines=original[k]['lines']) for k,v in reasons.items()],
        all_prose_unchanged=True,first_trial_not_approved=True,new_credit=0))
    print('13 revised scoped trials; nine original layouts retained with reasons.')

if __name__=='__main__':main()
