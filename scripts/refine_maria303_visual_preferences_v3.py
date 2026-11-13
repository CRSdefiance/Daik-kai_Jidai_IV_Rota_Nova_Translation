"""Keep Fernando's short exit imperative intact after direct native review."""
from copy import deepcopy
from pathlib import Path
from hashlib import sha256
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def main():
    old=ROOT/'formatting_v3/preferences_visual_v2.json';target=ROOT/'formatting_v3/preferences_visual_v3.json'
    assert not target.exists();pref=deepcopy(load(old))
    doc=load(ROOT/'formatting_v3/formatting_input_complete_indices_v1.json')
    row=next(r for r in doc['records'] if r['id']=='DK4_MES_B64_R0092')
    pref['records'][row['id']]=dict(one_page=True,
        required_pairs=[["let's",'get'],['get','out'],['out','of'],['of','here']],
        reason='Direct native sheet B64_part2: keep the short exit imperative Let\'s get out of here together rather than leaving out of here on its own row. Preserve the entire paragraph and all controls.',
        bindings={k:sha256(row[k].encode()).hexdigest() for k in ['source_hex','current_hex','english']})
    pref.update(previous_preferences=str(old),previous_preferences_sha256=digest(old),new_credit=0)
    save(target,pref);print('Saved five cumulative direct-visual phrase-continuity trials;prose unchanged.')

if __name__=='__main__':main()
