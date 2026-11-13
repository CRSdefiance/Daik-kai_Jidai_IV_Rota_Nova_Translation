"""Add the directly observed short tag-question and farewell-phrase findings."""
from copy import deepcopy
from pathlib import Path
from hashlib import sha256
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def main():
    old=ROOT/'formatting_v3/preferences_visual_v1.json';target=ROOT/'formatting_v3/preferences_visual_v2.json'
    assert not target.exists();pref=deepcopy(load(old))
    doc=load(ROOT/'formatting_v3/formatting_input_complete_indices_v1.json');rows={r['id']:r for r in doc['records']}
    rules={
        'DK4_MES_B62_R0093':dict(required_pairs=[['you','understand'],['understand',"don't"],["don't",'you']],
            reason='Direct native sheet B62_part2: keep You understand, don\'t you as one short question, avoiding a detached don\'t you row while preserving every word.'),
        'DK4_MES_B62_R0099':dict(required_pairs=[['see','you']],
            reason='Direct native sheet B62_part3: keep the short See you farewell together. Natural sentence-boundary wrapping fits the same panel without prose changes.'),
    }
    for ident,rule in rules.items():
        row=rows[ident];assert row['kind']=='progressive';rule['one_page']=True
        rule['bindings']={k:sha256(row[k].encode()).hexdigest() for k in ['source_hex','current_hex','english']}
        pref['records'][ident]=rule
    pref.update(previous_preferences=str(old),previous_preferences_sha256=digest(old),new_credit=0)
    save(target,pref);print('Saved four cumulative visual phrase trials;all prose and native controls unchanged.')

if __name__=='__main__':main()
