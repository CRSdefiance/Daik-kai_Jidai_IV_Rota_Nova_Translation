"""Select the actual registered Maria base profile; preserve failed2037."""
from pathlib import Path
SOURCE=Path('scripts/probe_maria_opening_fonts_v2037.py')
if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    assert text.count("get_dialogue_profile('maria-story-live')")==1
    text=text.replace("get_dialogue_profile('maria-story-live')","get_dialogue_profile('maria-story-shared-events-live')")
    text=text.replace("'maria_opening_fonts_v2037'","'maria_opening_fonts_v2037b'")
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
