"""Bind two distinct wrap decisions to the exact selected paragraphs."""
from copy import deepcopy
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from pathlib import Path
import hashlib

def main():
    path=ROOT/'formatting_FE_v1/physical_manuscript.json';doc=load(path)
    prior_path=ROOT/'formatting_FE_v1/preferences.json';prefs=deepcopy(load(prior_path));out=ROOT/'continuity_preferences_v1.json'
    assert not out.exists()
    def preference(ident,**fields):
        row=next(r for r in doc['records'] if r['id']==ident)
        assert ident not in prefs['records']
        prefs['records'][ident]=dict(fields,bindings={k:hashlib.sha256(row[k].encode()).hexdigest() for k in ['source_hex','current_hex','english']})
    preference('SC3_B99_STYLE_446_366',required_pairs=[['as','a'],['a','figurehead'],['figurehead','see']],
        reason='Keep the child\'s as-a-figurehead phrase and short See reaction together, avoiding an orphaned final prompt without changing a word.')
    preference('DK4_MES_B115_R0035',QA_line_ending_retention=dict(line_index=0,exact_line="So that's what this platter is for?",
        reason='This is a complete idiomatic question ending in for, not a phrase interrupted after a preposition. Retain its natural full-width opening row; all glyph, word, bounds and pagination guards still apply.'))
    prefs['evidence']={str(p):digest(p) for p in [path,prior_path,Path(__file__)]};save(out,prefs)
    print('Prepared exact phrase continuity and one complete-question row retention; no prose or width change.')

if __name__=='__main__':main()
