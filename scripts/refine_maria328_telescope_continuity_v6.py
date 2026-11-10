"""Keep the viewed telescope claim's entire reported closing sentence after A."""
from copy import deepcopy
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    before=ROOT/'formatting_FE_v1/preferences_visual_v5.json'
    target=ROOT/'formatting_FE_v1/preferences_visual_v6.json';assert not target.exists()
    pref=deepcopy(load(before));rule=pref['records']['DK4_MES_B77_R0012']
    rule['page_clause']='They say it could even show the uneven surface of the moon clearly.'
    rule['reason']+=' The viewed first panel ends They say it could even before A. Keep the complete reported final sentence on the second panel; retain its uncertainty and every word.'
    pref.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),new_credit=0)
    save(target,pref)

if __name__=='__main__':main()
