"""Preserve the unexecuted audit draft; correct selected-block literals and make newline filtering explicit."""
from pathlib import Path
import re
if __name__=='__main__':
    p=Path('scripts/verify_editorial_handoff_v3867.py');t=p.read_text(encoding='utf-8');assert '[158]' in t and "row['block']==158" in t;t=t.replace('[158]','[159]').replace("row['block']==158","row['block']==159");t,count=re.subn(r"if c not in '[^']+'","if c not in (' ',chr(10))",t);assert count==1;exec(compile(t,str(p)+'::unexecuted-B159-block-and-newline-filter-correction','exec'),dict(__name__='__main__',__file__=__file__))
