"""Resolve fallback, direct-caller and touchscreen-dismissal research assumptions."""
import inspect
from pathlib import Path
from scripts import research_powder_fire_context_v1303 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    changes = [
        ('values == [2052,2053,2054,2054,2054,2055,2056,2057]',
         'values == [2052,2053,0xFFFFFFFF,0xFFFFFFFF,2054,2055,2056,2057]'),
        ('number == values[voice]','number == (values[0] if values[voice] == 0xFFFFFFFF else values[voice])'),
        ("'all8_voice_selections':values", "'raw8_voice_table':values,'all8_effective_voice_selections':[values[0] if n == 0xFFFFFFFF else n for n in values]"),
        ('for frame in [7210,7310]:','for frame in [7210]:'),
        ("'native_Gunnery_role':9", "'current_Gunnery_role':9,'original_direct_parent':0x02053F40,'original_direct_call':0x02075610"),
    ]
    for old,new in changes:
        assert source.count(old) == 1,old
        source = source.replace(old,new)
    old = "        assert template == entries[number].text"
    addition = """        assert template == entries[number].text
        mobile = get(0x36C70,fleets+4+132+12)
        native_gunners = [get(0x55DC4,mobile,i) for i in range(4)]
        assert actor in native_gunners
"""
    assert source.count(old) == 1
    source = source.replace(old,addition)
    source = source.replace("'new_translation_or_formatting_or_family_completion_not_claimed':True,",
        "'new_translation_or_formatting_or_family_completion_not_claimed':True,'predecessor_fallback_and_role_assumptions_corrected':True,'touch_at7310_dismisses_notice_not_a_second_hold':True,")
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/powder_fire_context_v1303c')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
