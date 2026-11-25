"""Reject the orphaned cabin trial while preserving the other three layout candidates."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B0_B34_v1 import ROOT


PRIOR=ROOT/'ordinary_visual_preferences_v2.json'
OUT=ROOT/'ordinary_visual_preferences_v3.json'


def main():
    assert not OUT.exists()
    prefs=load(PRIOR)
    prefs['records']['DK4_MES_B1_R0058'].update(line_phrases=['Then shall we put it',"Clau's cabin"],
        reason='The first trial stranded cabin alone. Keep the opening verb-object phrase and the cabin reference intact, requiring fresh plan and native review.')
    save(OUT,{**prefs,'previous_preferences':str(PRIOR),'previous_preferences_sha256':digest(PRIOR),
        'rejected_trial':'refined_plan_v1: the cabin line created an orphaned last word; no approval was granted.'})


if __name__=='__main__':main()
