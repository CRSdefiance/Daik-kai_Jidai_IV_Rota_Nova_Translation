"""Retain complete-word title/region wraps instead of forcing unfit phrase groups."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B37_B50_clean_20261109')

def main():
    old=ROOT/'formatting_v1/preferences_v3_candidates.json';out=ROOT/'formatting_v1/preferences_v4_candidates.json'
    assert not out.exists();doc=deepcopy(load(old))
    for key in ['DK4_MES_B47_R0140','DK4_MES_B50_R0043']:
        doc['records'][key].pop('required_pairs')
    doc['records']['DK4_MES_B47_R0140']['reason']+=' Preserve the valid complete-word Proof/of Conqueror boundary instead of forcing the whole title and losing a page; no term or glyph changes.'
    doc['records']['DK4_MES_B50_R0043']['reason']+=' Trial the unchanged Far/East complete-word boundary within the validated FE guard budget; the extra phrase constraint did not fit.'
    doc.update(previous_preferences=str(old),previous_preferences_sha256=digest(old),two_unfit_phrase_constraints_removed_only=True,new_credit=0)
    save(out,doc)
    print('Savedtwo scoped complete-word wrap trials;no prose, width ornative guard changes.')

if __name__=='__main__':main()
