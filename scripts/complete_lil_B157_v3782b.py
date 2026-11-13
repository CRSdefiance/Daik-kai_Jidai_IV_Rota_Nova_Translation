"""Preserve the unexecuted draft and correct its receipt-only revision count."""
from pathlib import Path
if __name__=='__main__':
    p=Path('scripts/complete_lil_B157_v3782.py');t=p.read_text(encoding='utf-8');assert t.count('revisions=41,justified_retentions=44')==1;t=t.replace('revisions=41,justified_retentions=44','revisions=31,justified_retentions=44');assert t.count('proofpaths=[')==1;t=t.replace('proofpaths=[','proofpaths=[p,');exec(compile(t,str(p)+'::unexecuted-receipt-count-correction','exec'),dict(__name__='__main__',__file__=__file__,p=p))
