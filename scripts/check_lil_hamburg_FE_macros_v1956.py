"""Hamburg FE24 exact null-actor native macro and alignment cases."""
from pathlib import Path

SOURCE = Path('scripts/check_lil_london_FE_macros_v1897.py')

if __name__ == '__main__':
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        "ROOT=Path('work/analysis/lil_London_FE_macros_v1897')":"ROOT=Path('work/analysis/lil_Hamburg_FE_macros_v1956')",
        "DOC=Path('translations/lil_london_editorial_manuscript_v3.json')":"DOC=Path('translations/lil_hamburg_recruitment_editorial_manuscript_v2.json')",
        'work/analysis/lil_London_FE_v1896/all3_FE_native_planes_and_actual_mode_reconciliation.json':
            'work/analysis/lil_Hamburg_FE_v1955/all3_FE_native_planes_and_actual_mode_reconciliation.json',
        'lil_London_context_run_v1884_RESEARCH_ONLY/frame_052110_arm9_ram.bin':
            'lil_Speyer_revised_run_v1938_RESEARCH_ONLY/frame_093780_arm9_ram.bin',
    }
    for old,new in changes.items():
        assert text.count(old) == 1,old
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
