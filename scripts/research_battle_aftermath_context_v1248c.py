"""Source context with both original roster branches and a declared CPU duty.

The baseline has no type6 crew member,so71968 legitimately emits only the
fallback report. For the full optional exchange,original setters move existing
Charles18 from duty8 to duty15/type6 in a CPU-only copy. No actor identity,
gameplay state,source save,RNG or outcome is changed in an emulator.
"""
import inspect
from pathlib import Path
from scripts import research_battle_aftermath_context_v1248 as previous


if __name__=='__main__':
    source=inspect.getsource(previous.main)
    changes=[
        ('((0x53D44,0x54170),(0x71968,0x71A40)',
         '((0x53D44,0x54160),(0x54164,0x54170),(0x71968,0x71A40)'),
        ('assert arm[lo:hi]==source[lo:hi]',
         "assert arm[lo:hi]==source[lo:hi]\n    assert arm[0x54160:0x54164].hex()=='75a3feeb' and source[0x54160:0x54164].hex()=='ebfdffeb'"),
        ('    town_cases=[]', '''    assert arm[0x82BA8:0x82BD0]==source[0x82BA8:0x82BD0]
    duty=fleet_root+0x2090
    assert get(0x82428,duty,1)==0 and get(0x7B60,1)==6
    assert get(0x82BC4,duty,8)==18 and get(0x82BC4,duty,15)==208
    definitions=get(0x82E04,duty)
    assert get(0x132C0,definitions,15)==6
    get(0x82BA8,duty,8);get(0x82BB8,duty,15,18)
    assert get(0x82428,duty,1)==role_actor
    assigned_raw=bytes(cpu.mem_read(BASE,0x400000))
    changed=[BASE+i for i,(a,b) in enumerate(zip(raw,assigned_raw,strict=True)) if a!=b]
    assert changed==sorted([duty+6+8,duty+6+15])
    role_assignment={'source_snapshot_sha256':sha(raw),'CPU_assigned_snapshot_sha256':sha(assigned_raw),
        'original_clear_setters':[BASE+0x82BA8,BASE+0x82BB8],'moved_existing_actor_ID':18,
        'duty_slots_before_after':[8,15],'target_original_duty_type':6,
        'only_two_original_roster_bytes_changed':changed,
        'actor_objects_IDs_RNG_and_all_other4MiB_bytes_exact':True,
        'CPU_only_no_emulator_fixture_or_actual_town_event':True}
    town_cases=[]'''),
        ('calls,pcpu,pget=source_prefix(arm,raw,0x71968,(0,town),BASE+0x719F8)', '''fallback,_,_=source_prefix(arm,raw,0x71968,(0,town),BASE+0x719F8)
        assert len(fallback)==1 and fallback[0]['entry']==BASE+0x53D44
        assert fallback[0]['arguments'][:3]==[1,0x02117640,name_pointer]
        calls,pcpu,pget=source_prefix(arm,assigned_raw,0x71968,(0,town),BASE+0x719F8)'''),
        ("'original_calls':calls,'entire_original_surrender_exchange_prefix_executes':True,",
         "'original_calls':calls,'original_unassigned_roster_fallback_calls':fallback,'entire_original_surrender_exchange_prefix_executes':True,"),
        ("'source_role1_actor_ID_in_this_snapshot':18,",
         "'source_role1_actor_ID_in_this_snapshot':18,'CPU_original_duty_assignment':role_assignment,'both115_unassigned_fallback_and115_assigned_exchange_prefixes_execute':True,"),
    ]
    for old,new in changes:
        assert source.count(old)==1,old
        source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,
        'ROOT':Path('work/analysis/battle_aftermath_context_v1248c')}
    exec(compile(source,__file__,'exec'),env);env['main']()
