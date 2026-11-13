"""Exact pause inspector for the disclosed Hamburg access run."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

SOURCE = Path('scripts/inspect_lil_speyer_live_v1921.py')

if __name__ == '__main__':
    text = SOURCE.read_text(encoding='utf-8')
    old_run,new_run = 'lil_Speyer_context_run_v1920','lil_Speyer_access_run_v1924'
    assert text.count(old_run) == 2
    text = text.replace(old_run,new_run)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
