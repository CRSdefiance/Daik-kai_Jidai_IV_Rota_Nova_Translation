"""Preserve the unexecuted checkpoint draft andcorrect its three prose-only labels."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    p=Path('scripts/checkpoint_lil_B157_v3759.py');t=p.read_text(encoding='utf-8');changes={'5329 fresh rereads:5254 integrated/76pending;source/prose5257':'5329 fresh rereads:5254 integrated/75pending;source/prose5332','## V3759:75 Lil B156 contextual/native reviews':'## V3759:75 Lil B157 contextual/native reviews','5329 reread,5329 integrated,75 pending':'5329 reread,5254 integrated,75 pending'}
    for a,b in changes.items():assert t.count(a)==1,(a,t.count(a));t=t.replace(a,b)
    exec(compile(t,str(p)+'::unexecuted-text-label-correction','exec'),dict(__name__='__main__',__file__=__file__));root=Path('work/analysis/lil_B157_checkpoint_v3759');save(root/'unexecuted_draft_text_label_corrections.json',dict(previous=str(p),previous_sha256=sha(p.read_bytes()),correction='Before any ledger mutation,correct the old prose-only source/prose/pending labels, B157 section label and console integrated count. Core numeric accounting was already correct.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
