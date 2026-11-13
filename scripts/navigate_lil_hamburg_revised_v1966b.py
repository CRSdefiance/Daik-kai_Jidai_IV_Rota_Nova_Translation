"""Resume the existing cold boot after the first capture wait expired safely."""
from pathlib import Path

SOURCE = Path('scripts/navigate_lil_hamburg_revised_v1966.py')

if __name__ == '__main__':
    predecessor = Path('work/analysis/lil_Hamburg_revised_navigation_v1966')
    assert predecessor.is_dir() and not list(predecessor.iterdir())
    capture = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Hamburg_revised_run_v1965_RESEARCH_ONLY/frame_049440_arm9_ram.bin')
    assert capture.exists() and capture.stat().st_size == 0x400000
    text = SOURCE.read_text(encoding='utf-8')
    assert text.count('lil_Hamburg_revised_navigation_v1966') == 1
    text = text.replace('lil_Hamburg_revised_navigation_v1966','lil_Hamburg_revised_navigation_v1966b')
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
