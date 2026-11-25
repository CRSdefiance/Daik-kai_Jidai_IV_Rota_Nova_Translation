"""Successor: distinguish the closed B74 record from its still-running host."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

SOURCE = Path('scripts/prove_lil_hamburg_controls_v1953.py')

if __name__ == '__main__':
    text = SOURCE.read_text(encoding='utf-8')
    old = "    assert nav['original_process_closed']"
    new = """    terminal_path = Path('work/analysis/lil_Speyer_access_run_v1924/terminal.json')
    assert audit['evidence'][str(terminal_path)] == sha(terminal_path.read_bytes())
    terminal = read(terminal_path)
    assert terminal['frame'] == 93780
    # Navigator1933 ended the B74 record at76170 while the same process
    # continued into Speyer. Its original_process_closed=False is correct.
    assert nav['original_process_closed'] is False
    assert nav['terminal_frame_requested'] == 76170"""
    assert text.count(old) == 1
    text = text.replace(old,new)
    assert text.count('lil_Hamburg_controls_v1953') == 1
    text = text.replace('lil_Hamburg_controls_v1953','lil_Hamburg_controls_v1953b')
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
