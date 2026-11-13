"""Preserve provisional gloss/scope files and bind the exact approved native name spelling."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    old=Path('work/analysis/lil_B158_clean_context_v3787/all19_complete_B158_exchange_and_fresh_glosses.json');root=Path('work/analysis/lil_B158_clean_context_v3787b');assert not root.exists();d=read(old)
    def names(v):
        if isinstance(v,str):return v.replace('Christina','Cristina')
        if isinstance(v,list):return [names(x) for x in v]
        if isinstance(v,dict):return {k:names(x) for k,x in v.items()}
        return v
    d=names(deepcopy(d));d.update(previous_provisional_glosses=str(old),previous_provisional_glosses_sha256=sha(old.read_bytes()),approved_native_name='Cristina Erneco',correction='The explicit original native getter and registered catalogue use Cristina Erneco. The clean Japanese meaning, full exchange reading and all19 individual glosses are unchanged; use the approved spelling in English notes before older-English comparison.',producer_sha256=sha(Path(__file__).read_bytes()));root.mkdir(parents=True);save(root/old.name,d)
    p=Path('scripts/prepare_lil_B158_scope_v3788.py');t=p.read_text(encoding='utf-8');changes={'lil_B158_source_v3788':'lil_B158_source_v3788b','lil_B158_clean_context_v3787/':'lil_B158_clean_context_v3787b/','Christina':'Cristina'}
    for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
    exec(compile(t,str(p)+'::approved-Cristina-name-successor','exec'),dict(__name__='__main__',__file__=__file__))
