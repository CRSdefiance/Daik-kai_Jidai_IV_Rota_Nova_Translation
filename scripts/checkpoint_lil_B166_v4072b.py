"""Preserve the checkpoint draft;use the author's exact zero-credit field spelling."""
from pathlib import Path
if __name__=='__main__':
    draft=Path('scripts/checkpoint_lil_B166_v4072.py');text=draft.read_text(encoding='utf-8');old="author['source_prose_orcompletion_credit_added']";assert text.count(old)==1;text=text.replace(old,"author['source_prose_or_completion_credit_added']");assert text.count('paths=[PRIOR,')==1;text=text.replace('paths=[PRIOR,','paths=[DRAFT,PRIOR,');exec(compile(text,__file__,'exec'),dict(__name__='__main__',__file__=__file__,DRAFT=draft))
