"""Require the exact mapped incidental cursor at the original event-query call."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    old=Path('scripts/prove_lil_B111_B119_relocated_controls_v3243b.py');new=Path('scripts/prove_lil_B111_B119_relocated_controls_v3243d.py');assert not new.exists()
    diagnostic=Path('work/analysis/lil_B111_B119_query_diagnostic_v3243c/current_relocated_query_call_diagnostic.json');d=read(diagnostic)
    a,b=d['cases'];qa,qb=[r['original_event_completion_calls'][0] for r in [a,b]]
    assert qa['args'][:3]==qb['args'][:3] and qa['args'][3]==0x02660000+a['offset'] and qb['args'][3]==0x02660000+b['offset']
    assert d['source_disassembly']['0x23840'][2:4]==['0x2023848 ldr r3, [pc, #0x34]','0x202384c mov r2, r1']
    t=old.read_text(encoding='utf-8')
    anchor="            assert pairs[0]['original_event_completion_calls']==pairs[1]['original_event_completion_calls']"
    assert t.count(anchor)==1
    t=t.replace(anchor,"""            left,right=[p['original_event_completion_calls'] for p in pairs]
            assert len(left)==len(right)
            for a,b in zip(left,right,strict=True):
                assert a['address']==b['address'] and a['args'][:3]==b['args'][:3]
                assert a['args'][3]==0x02660000+command['old_offset']
                assert b['args'][3]==0x02660000+command['new_offset']
""")
    t=t.replace('lil_B111_B119_relocated_controls_v3243b','lil_B111_B119_relocated_controls_v3243d')
    anchor='original_event_queries=queries,canonical_Maria32_copy_not_dispatched_under_Lil_context=True,'
    assert t.count(anchor)==1
    t=t.replace(anchor,anchor+'original_query_r0_r1_r2_and_mapped_incidental_r3_cursor_exact=True,')
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    save(Path('work/analysis/lil_B111_B119_control_tools_v3243/mapped_query_cursor_correction.json'),dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),diagnostic=str(diagnostic),diagnostic_sha256=sha(diagnostic.read_bytes()),finding='The original query receives identical r0/r1/r2, while incidental r3 is the command cursor and correctly moves fromstream+46 tostream+42. The native callee overwrites r3 and r2 before use. Require both raw cursors to equal their mapped command addresses; retain every ABI,operand,result,memory andcanary check.',failed_producer_and_log_preserved=True,no_native_event_or_guard_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
