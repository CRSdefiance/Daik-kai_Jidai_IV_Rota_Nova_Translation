"""Preserve2637 legacy-parser refusal;bind the registered current parser."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/verify_sighting_fonts_v2637.py').read_text();source=source.replace('from dk4tool.patch.grand_race_menu_release import sha','from dk4tool.patch.grand_race_menu_release import sha\nfrom dk4tool.patch.refit_contextual_spritsail_v1 import current_entries');source=source.replace("'ROM':ctx.rompath,'DOC':DOC}","'ROM':ctx.rompath,'DOC':DOC,'current_entries':current_entries}").replace('sighting_fonts_v2637','sighting_fonts_v2637b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
