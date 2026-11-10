"""Preserve complete closing thoughts across the three directly viewed B105 page boundaries."""
from copy import deepcopy
from pathlib import Path
import hashlib
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

CLAUSES={
'DK4_MES_B105_R0101':'I knew very well they feared me far more than my strength warranted.',
'DK4_MES_B105_R0106':'I know very well they fear me far more than my strength warrants.',
'DK4_MES_B105_R0132':"You needn't force yourself when you are with me.",
}

def main():
    path=ROOT/'continuity_preferences_v3.json';docpath=ROOT/'formatting_FE_v1/physical_manuscript.json'
    prefs=deepcopy(load(path));doc=load(docpath);out=ROOT/'continuity_preferences_v4.json';assert not out.exists()
    for ident,clause in CLAUSES.items():
        row=next(r for r in doc['records'] if r['id']==ident);assert row['english'].count(clause)==1 and ident not in prefs['records']
        prefs['records'][ident]=dict(page_clause=clause,
            reason='Directly viewed second page strands a short end of this sentence. Keep the complete closing thought on one page, retaining every word, ordinary wrapping and the validated width; source-specific shorter rows are justified by the coherent page boundary.',
            bindings={k:hashlib.sha256(row[k].encode()).hexdigest() for k in ['source_hex','current_hex','english']})
    prefs['evidence'].update({str(p):digest(p) for p in [path,docpath,ROOT/'native_pages_v1/B105_part3.png',Path(__file__)]})
    save(out,prefs);print('Bound three B105 closing clauses; all prose, controls and widths unchanged.')

if __name__=='__main__':main()
