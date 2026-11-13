"""Improve four candidate layouts whose first constraints moved the awkward split."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B0_B34_v1 import ROOT

PRIOR=ROOT/'ordinary_visual_preferences_v5.json'
OUT=ROOT/'ordinary_visual_preferences_v6.json'

if __name__=='__main__':
    assert not OUT.exists()
    doc=load(PRIOR)
    doc['records']['DK4_MES_B5_R0056'].update(ordinary_boundaries=[['you','everyone']],
        reason='Keep counting on you complete; permit the normal pause before the appositive everyone so the rally need not grow from two to three rows.')
    doc['records']['DK4_MES_B21_R0005']['line_phrases'].append("isn't entirely undeserved.")
    doc['records']['DK4_MES_B24_R0056']['line_phrases'].append('discipline and thrift')
    doc['records']['DK4_MES_B25_R0048']['line_phrases'].append('old fellow')
    doc['records']['DK4_MES_B26_R0287']['line_phrases'].append('better than')
    save(OUT,{**doc,'previous_preferences':str(PRIOR),'previous_preferences_sha256':digest(PRIOR),
        'trial_refinement_reason':'Reject new sparse rows and newly split phrases in the initial candidate; keep prose exact.'})
