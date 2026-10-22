"""Successor bounds the world sweep to114 real CTown objects.

The next embedded world member is CAdman,not a town. V1248c's RTTI guard
correctly stopped that overrun before saving any context approval.
"""
from pathlib import Path


if __name__=='__main__':
    path=Path('scripts/research_battle_aftermath_context_v1248c.py')
    script=path.read_text(encoding='utf-8')
    old="exec(compile(source,__file__,'exec'),env);env['main']()"
    assert script.count(old)==1
    new="""source=source.replace('range(115)','range(114)').replace('115_original_town','114_original_town').replace('both115_unassigned_fallback_and115_assigned','both114_unassigned_fallback_and114_assigned').replace('115 town exchanges','114 town exchanges')
    source=source.replace('    branch_cases=[]',\"    assert rtti(raw,struct.unpack('<I',cpu.mem_read(town_root+4+114*108,4))[0])=='6CAdman'\\n    branch_cases=[]\")
    source=source.replace(\"'CPU_original_duty_assignment':role_assignment\",\"'CPU_original_duty_assignment':role_assignment,'native_world_real_Town_slots':114,'next_world_member_RTTI':'6CAdman'\")
    env['ROOT']=Path('work/analysis/battle_aftermath_context_v1248d')
    exec(compile(source,__file__,'exec'),env);env['main']()"""
    script=script.replace(old,new)
    exec(compile(script,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
