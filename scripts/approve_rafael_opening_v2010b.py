"""Syntax-only successor; preserve V2010's unexecuted malformed update call."""
from pathlib import Path

SOURCE=Path('scripts/approve_rafael_opening_v2010.py')

if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    old='no_new_gameplay_display_or_editorial_completion_credit=False,editorial_completion_not_granted_until_registered_integration=True))'
    new='no_new_gameplay_display_or_editorial_completion_credit=False,editorial_completion_not_granted_until_registered_integration=True)'
    assert text.count(old)==1;text=text.replace(old,new)
    text=text.replace('rafael_opening_approval_v2010','rafael_opening_approval_v2010b')
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
