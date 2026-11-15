"""Resolve the directly viewed B98 premature pagination with unchanged full prose."""
from copy import deepcopy
from pathlib import Path
import hashlib
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    prior=ROOT/'continuity_preferences_v1.json';docpath=ROOT/'formatting_FE_v1/physical_manuscript.json'
    prefs=deepcopy(load(prior));doc=load(docpath);out=ROOT/'continuity_preferences_v2.json';assert not out.exists()
    row=next(r for r in doc['records'] if r['id']=='DK4_MES_B98_R0013');assert row['id'] not in prefs['records']
    prefs['records'][row['id']]=dict(one_page=True,
        reason='Directly viewed B98 sheet exposes premature five-row pagination and a short final page. Require a native one-page solution at the same validated width, preserving every word; ordinary complete-word wrapping may split the long tell-you-something phrase.',
        bindings={k:hashlib.sha256(row[k].encode()).hexdigest() for k in ['source_hex','current_hex','english']})
    prefs['evidence'].update({str(p):digest(p) for p in [prior,docpath,ROOT/'native_pages_v1/B98_part1.png',Path(__file__)]})
    save(out,prefs);print('Bound B98 one-page preference to the exact unchanged paragraph and viewed page evidence.')

if __name__=='__main__':main()
