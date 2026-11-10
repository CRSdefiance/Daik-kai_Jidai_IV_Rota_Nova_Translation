"""Use FE36 for the observed row failure and trial FE37 for the full135-character clause."""
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT
def main():
    original=ROOT/'formatting_v1/preferences_v2_FE36_trials.json';out=ROOT/'formatting_v1/preferences_v3_FE37_trial.json'
    assert not out.exists();pref=load(original);row=pref['records']['DK4_MES_B54_R0507']
    assert row['FE_planning_cells']==36
    row.update(FE_planning_cells=37,reason='The full135-character epilogue clause cannot be planned in guarded FE36. Trial the existing FE37 budget with complete native pixels/consumption/rows/bounds required;preserve every word and the physical228px viewport.')
    pref.update(previous_preferences=str(original),previous_preferences_sha256=digest(original),only_R507_guard_trial_changed=True)
    save(out,pref)
if __name__=='__main__':main()
