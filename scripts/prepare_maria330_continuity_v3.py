"""Keep in return intact inside the unchanged B98 one-page paragraph."""
from copy import deepcopy
from pathlib import Path
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    path=ROOT/'continuity_preferences_v2.json';prefs=deepcopy(load(path));out=ROOT/'continuity_preferences_v3.json';assert not out.exists()
    row=prefs['records']['DK4_MES_B98_R0013'];assert row['one_page'] and 'required_pairs' not in row
    row['required_pairs']=[['in','return']]
    row['reason']+=' Keep the idiomatic in return pair together; the failed initial four-row result split it after in.'
    prefs['evidence'].update({str(p):digest(p) for p in [path,ROOT/'plan_continuity_v2/automatic_plans.json',Path(__file__)]})
    save(out,prefs);print('Bound in-return phrase continuity; full B98 paragraph unchanged.')

if __name__=='__main__':main()
