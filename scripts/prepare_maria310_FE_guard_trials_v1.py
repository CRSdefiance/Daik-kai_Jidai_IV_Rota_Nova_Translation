"""Trial the existing scoped FE guard reserve after the concrete epilogue row failure."""
from copy import deepcopy
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

def main():
    out=ROOT/'formatting_v1/preferences_v2_FE36_trials.json';assert not out.exists()
    original=ROOT/'formatting_v1/initial_preferences.json';pref=deepcopy(load(original))
    doc_path=ROOT/'formatting_v1/formatting_input.json';doc=load(doc_path)
    wanted={'DK4_MES_B54_R0499','DK4_MES_B54_R0507'}
    for row in doc['records']:
        if row['id'] not in wanted:continue
        assert row['kind']=='system-FE' and row['source_selector']==254
        pref['records'][row['id']]=dict(FE_planning_cells=36,
            reason='Trial the already qualified source-scoped FE36 guard reserve after the unchanged native row-membership check fails at B54R499. R507 has the same long guarded-row risk. Physical228px geometry,font,prose andengine remain unchanged;fresh native proof is required.',
            bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
    assert set(pref['records'])==wanted
    pref.update(previous_preferences=str(original),previous_preferences_sha256=digest(original),
        original_failed_native_output=str(ROOT/'initial_native_v1'),
        exact_failing_record='DK4_MES_B54_R0499',native_guard_not_waived=True,new_credit=0)
    save(out,pref);print('Saved two source-bound FE36 guard trials; no prose,physical geometry orengine change.')
if __name__=='__main__':main()
