"""Bind Xien0A as an exact native speech selector,not a text line break."""
from pathlib import Path
SOURCE=Path('scripts/probe_maria_opening_fonts_v2037.py')
if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    changes={"get_dialogue_profile('maria-story-live')":"get_dialogue_profile('maria-story-shared-events-live')",
        'frozenset({21,74})':'frozenset({10,21,74})',"'maria_opening_fonts_v2037'":"'maria_opening_fonts_v2037c'"}
    for old,new in changes.items():
        assert text.count(old)==1,old
        text=text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
