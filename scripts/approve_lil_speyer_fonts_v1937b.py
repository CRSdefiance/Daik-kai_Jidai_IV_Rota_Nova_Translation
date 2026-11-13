"""Successor adds completed formatting to batch-level gate declarations as well."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

SOURCE = Path('scripts/approve_lil_speyer_fonts_v1937.py')
SOURCE_SHA = '3abec4851dac995ffb8021d9cdf4a2c78ca56b4d6ca26b32f82680bc79b66013'

if __name__ == '__main__':
    assert sha(SOURCE.read_bytes())==SOURCE_SHA
    text = SOURCE.read_text(encoding='utf-8')
    assert text.count('lil_Speyer_font_approval_v1937')==1
    text = text.replace('lil_Speyer_font_approval_v1937','lil_Speyer_font_approval_v1937b')
    old = '    validate_natural_dialogue_batch(revised)'
    new = """    revised['review_gates']=['source','context','localization','naturalness','formatting']
    revised_menu['review_gates']=['source','context','localization','naturalness','formatting']
    revised['frozen1937_rejected_missing_batch_formatting_gate_before_outputs']=True
    validate_natural_dialogue_batch(revised)"""
    assert text.count(old)==1
    text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
