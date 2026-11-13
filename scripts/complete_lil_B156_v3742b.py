"""Preserve the unexecuted completion draft andbind its prose/actual-name companions."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    p=Path('scripts/complete_lil_B156_v3742.py');t=p.read_text(encoding='utf-8');changes={'source/prose5181':'source/prose5257','28revisions/22retentions;5178reread/integrated,5181source-prose':'41revisions/35retentions;5254reread/integrated,5257source-prose',"proofpaths=[DOC,":"proofpaths=[Path('scripts/lil_B156_completion_text_v3742.py'),Path(doc['actual_nameplate_reconciliation']),Path(doc['actual_transition_review']),DOC,"}
    for a,b in changes.items():assert t.count(a)==1,(a,t.count(a));t=t.replace(a,b)
    exec(compile(t,str(p)+'::unexecuted-note-and-companion-binding-correction','exec'),dict(__name__='__main__',__file__=__file__));root=Path('work/analysis/lil_B156_completion_v3742');save(root/'unexecuted_completion_draft_note_and_evidence_correction.json',dict(previous=str(p),previous_sha256=sha(p.read_bytes()),correction='Correct two leftover digits-adjacent prose summaries to5257 source/prose,5254 completed,41 revised/35 retained;bind the immutable completion-text module,source-owned Sailor UI alias andviewed actual transition proofs. The draft wasnot executed before correction. Core accounting/prose/ROM bytes unchanged.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
