"""Recheck the final one changed plane andfour compiled alignment cases;reuse332 exact cases."""
from pathlib import Path
if __name__=='__main__':
    draft=Path('scripts/verify_lil_B166_fonts_v4081.py');t=draft.read_text(encoding='utf-8');replacements={
        "OLDPATH=Path('work/analysis/lil_B166_fonts_v4068/current_macro_QA_and_progressive_font_proof.json')":"OLDPATH=Path('work/analysis/lil_B166_fonts_v4081/current_macro_QA_and_progressive_font_proof.json')",
        "doc=read('translations/lil_B166_editorial_manuscript_v3.json')":"doc=read('translations/lil_B166_editorial_manuscript_v4.json')",
        "assert set(CHANGED)=={'DK4_MES_B166_R'+str(i).zfill(4) for i in [27,37,68,112,123,153,157,165,175]}":"assert CHANGED==['DK4_MES_B166_R0175']",
        "('lil_B166_fonts_v4068','lil_B166_fonts_v4081')":"('lil_B166_fonts_v4068','lil_B166_fonts_v4081b')",
        "('lil_B166_editorial_manuscript_v2','lil_B166_editorial_manuscript_v3')":"('lil_B166_editorial_manuscript_v2','lil_B166_editorial_manuscript_v4')",
        "('lil_B166_layout_v1','lil_B166_layout_v3')":"('lil_B166_layout_v1','lil_B166_layout_v4')",
        "Path('work/analysis/lil_B166_fonts_v4081');new=":"Path('work/analysis/lil_B166_fonts_v4081b');new=",
        '9 changed compiled planes/36 alignment calls freshly checked;33 planes/300 cases exact reuse':'1 changed compiled plane/4 alignment calls freshly checked;41 planes/332 cases exact reuse',
        'new_macro_cases=36,exact_reused_macro_cases=300,new_native_planes=9,exact_reused_native_planes=33':'new_macro_cases=4,exact_reused_macro_cases=332,new_native_planes=1,exact_reused_native_planes=41',
        'fresh_macro_cases=36,exact_reused_macro_cases=300':'fresh_macro_cases=4,exact_reused_macro_cases=332'
    }
    for a,b in replacements.items():assert a in t,a;t=t.replace(a,b)
    exec(compile(t,__file__,'exec'),dict(__name__='__main__',__file__=__file__,DRAFT=draft))
