"""Keep a short question and idiom together after direct native-page review."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def main():
    old=ROOT/'formatting_v3/preferences_page_continuity_v2.json'
    target=ROOT/'formatting_v3/preferences_visual_v1.json';assert not target.exists()
    docpath=ROOT/'formatting_v3/formatting_input_complete_indices_v1.json'
    doc=load(docpath);rows={r['id']:r for r in doc['records']};pref=deepcopy(load(old))
    rules={
        'DK4_MES_B58_R0178':dict(required_pairs=[['where','are'],['are','they']],
            reason='Direct native sheet B58_part4: keep the short Where are they question together. Preserve every word and ordinary automatic wrapping.'),
        'DK4_MES_B61_R0050':dict(required_pairs=[['worth','your'],['your','while']],
            reason='Direct native sheet B61_part2: keep the short worth your while idiom together instead of leaving your while on a separate row. Prose remains verbatim.'),
    }
    for ident,rule in rules.items():
        row=rows[ident];assert row['kind']=='progressive';rule['one_page']=True
        from hashlib import sha256
        rule['bindings']={k:sha256(row[k].encode()).hexdigest() for k in ['source_hex','current_hex','english']}
        pref['records'][ident]=rule
    pref.update(previous_preferences=str(old),previous_preferences_sha256=digest(old),
        direct_native_visual_findings_only=True,no_prose_shortening_no_metrics_control_orQA_waiver=True,new_credit=0)
    save(target,pref)
    print('Saved two phrase-continuity trials from directly viewed native pages;prose unchanged.')

if __name__=='__main__':main()
