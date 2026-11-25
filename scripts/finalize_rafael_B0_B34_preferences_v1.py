"""Retain the better Valdes layout and finish the Gerhard opening phrase."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B0_B34_v1 import ROOT

PRIOR=ROOT/'ordinary_visual_preferences_v6.json'
OUT=ROOT/'ordinary_visual_preferences_v7.json'

if __name__=='__main__':
    assert not OUT.exists()
    doc=load(PRIOR)
    rejected=doc['records'].pop('DK4_MES_B21_R0005')
    doc['records']['DK4_MES_B24_R0056']['line_phrases'].append("That's why I taught you")
    save(OUT,{**doc,'previous_preferences':str(PRIOR),'previous_preferences_sha256':digest(PRIOR),
        'rejected_layout_candidates':{'DK4_MES_B21_R0005':dict(candidate=rejected,
            reason='The new constraints created a sparse It seems we will opening and split the modal predicate. Retain the original four filled rows, including the complete reputation clause; its ordinary verb/object continuation is clearer overall.')},
        'additional_visual_findings_resolved_as_candidates':dict(changed=15,retained=1)})
