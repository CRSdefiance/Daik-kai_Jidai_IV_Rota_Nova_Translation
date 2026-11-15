"""Resume the same process after identifying the original Gerhard join panel."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

SOURCE = Path('scripts/navigate_lil_hamburg_original_v1932.py')
INHERITED = Path('work/analysis/lil_Hamburg_arrival_navigation_v1932/original_presentation_observations_LIVE.json')
ROOT = Path('work/analysis/lil_Hamburg_arrival_navigation_v1933')

if __name__ == '__main__':
    inherited = read(INHERITED)
    assert inherited['next_pause_frame']==70890 and len(inherited['rows'])==65
    text = SOURCE.read_text(encoding='utf-8')
    old = '    holds,art,choices = [],[],[]'
    new = """    inherited=read('work/analysis/lil_Hamburg_arrival_navigation_v1932/original_presentation_observations_LIVE.json')
    assert args.frame==inherited['next_pause_frame']==70890 and len(inherited['rows'])==65
    holds,art,choices=inherited['rows'],inherited['art_pauses'],inherited['choices']
    save(root/'inherited65_and_original_join_panel.json',dict(source=str(INHERITED),source_sha256=sha(INHERITED.read_bytes()),
        source_navigator_sha256=sha(SOURCE.read_bytes()),inherited_speech_observations=65,
        original_join_command_offset=3402,original_join_command_hex='00a0ffff10100120',
        actual_Gerhard_full_name_join_panel_viewed=True,same_process_not_restarted=True,no_editorial_credit=True))"""
    assert text.count(old)==1
    text = text.replace(old,new)
    old = "src['first_word'] in (0x4000,0x2000,0x2100)"
    assert text.count(old)==1
    text = text.replace(old,"src['first_word'] in (0x4000,0x2000,0x2100,0xa000)")
    old = """        elif src['first_word']==0x2000:
            assert by_offset[src['instruction_offset']]['whole_command_hex']=='0020'
            art.append(dict(source=src,holds=group,original_art_pause_not_padding_generated_blank=True))"""
    new = """        elif src['first_word'] in (0x2000,0xa000):
            native=by_offset[src['instruction_offset']]['whole_command_hex']
            assert native==('0020' if src['first_word']==0x2000 else '00a0ffff10100120')
            art.append(dict(source=src,holds=group,original_non_speech_command_hex=native,
                original_join_panel=src['first_word']==0xa000,not_padding_generated_blank=True))"""
    assert text.count(old)==1
    text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{**globals(),'__name__':'__main__','__file__':__file__})
