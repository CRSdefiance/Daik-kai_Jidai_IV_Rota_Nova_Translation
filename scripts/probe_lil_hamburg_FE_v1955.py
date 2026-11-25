"""Hamburg FE mode1 planes reconciled to all six existing original holds."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

SOURCE = Path('scripts/probe_lil_london_FE_v1896.py')

if __name__ == '__main__':
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'from dk4tool.dialogue.lil_london_profile import profile_for':'from dk4tool.dialogue.lil_hamburg_profile import profile_for',
        "ROOT=Path('work/analysis/lil_London_FE_v1896')":"ROOT=Path('work/analysis/lil_Hamburg_FE_v1955')",
        "DOC=Path('translations/lil_london_editorial_manuscript_v3.json')":"DOC=Path('translations/lil_hamburg_recruitment_editorial_manuscript_v2.json')",
        "NAV=Path('work/analysis/lil_London_context_navigation_v1891/closed_original_B26_context.json')":"NAV=Path('work/analysis/lil_Hamburg_arrival_navigation_v1933/closed_original_scene_context.json')",
        ".blocks[26],'FE-paper'": ".blocks[74],'FE-paper'",
        'all6_original_London_FE_holds_match_complete_native_mode1_ink':'all6_original_Hamburg_FE_holds_match_complete_native_mode1_ink',
    }
    for old, new in changes.items():
        assert text.count(old) == 1, old
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
