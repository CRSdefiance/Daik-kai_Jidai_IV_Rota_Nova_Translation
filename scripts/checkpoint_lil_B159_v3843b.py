"""Preserve the unexecuted draft; correct its approval-gate label before any ledger mutation."""
from pathlib import Path
if __name__=='__main__':
    draft=Path('scripts/checkpoint_lil_B159_v3843.py');t=draft.read_text(encoding='utf-8');assert t.count('all19_five_review_gates_true')==1;t=t.replace('all19_five_review_gates_true','all41_five_review_gates_true');assert t.count('Record19 contextual/native reviews')==1;t=t.replace('Record19 contextual/native reviews','Record41 contextual/native reviews');assert t.count('paths=[')==1;t=t.replace('paths=[','paths=[DRAFT,');exec(compile(t,str(draft)+'::unexecuted-source41-approval-label-correction','exec'),dict(__name__='__main__',__file__=__file__,DRAFT=draft))
