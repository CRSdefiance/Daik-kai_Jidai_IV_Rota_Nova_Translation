"""Test the separately validated FE37 budget for the unchanged long counterfactual."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B37_B50_clean_20261109')

def main():
    old=ROOT/'formatting_v1/preferences_v4_candidates.json';out=ROOT/'formatting_v1/preferences_v5_FE37_trial.json'
    assert not out.exists();doc=deepcopy(load(old));row=doc['records']['DK4_MES_B50_R0043']
    assert row['FE_planning_cells']==36
    row.update(FE_planning_cells=37,reason='Test the existing validated scoped FE37 plan budget after FE36 could not retain the whole139-character counterfactual. Native full-row membership, complete glyphs andbounds must pass before acceptance; no prose, physical viewport orfont changes.')
    doc.update(previous_preferences=str(old),previous_preferences_sha256=digest(old),only_B50_R43_budget_changed=True,new_credit=0)
    save(out,doc)

if __name__=='__main__':main()
