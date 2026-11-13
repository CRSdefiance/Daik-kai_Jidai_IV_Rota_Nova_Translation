"""Prefer the fuller item opening and keep the riddle's short question complete."""
from copy import deepcopy
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    before=ROOT/'formatting_FE_v1/preferences_visual_v3.json'
    out=ROOT/'formatting_FE_v1/preferences_visual_v4.json'
    assert not out.exists()
    pref=deepcopy(load(before))
    removed=pref['records'].pop('DK4_MES_B76_R0012')
    pref['item_wrap_retention']=dict(id='DK4_MES_B76_R0012',trial=removed,
        reason="The intact item-name trial leaves only Let's look on the opening row. Retain the fuller original row ending Jaguar and its ordinary word boundary before God's Vest; no clipped glyph, split word or ambiguity. Avoid a premature opening break merely to keep an entire compound title on one row.")
    rule=pref['records']['DK4_MES_B87_R0139_FE_PAGE_2']
    rule['required_pairs']=[['how','many'],['many','adults'],['adults','are'],['are','there']]
    rule['reason']+=' Keep the complete short how many adults are there? question together rather than isolating are there? on its final row.'
    pref.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),new_credit=0)
    save(out,pref)
    print('Kept the fuller item opening; the riddle question receives one source-bound phrase preference.')

if __name__=='__main__':main()
