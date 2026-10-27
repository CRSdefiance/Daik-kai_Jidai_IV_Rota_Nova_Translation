"""Successor records the observed Lisbon pair11,0 rather than assuming town0.

Preserve failed2007/b/c producers; the error was in audit expectations,not gameplay.
"""
from pathlib import Path

SOURCE=Path('scripts/audit_rafael_independent_v2007.py')

if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    changes={
        "    assert nav['completion_confirmed']and all(r['validation_passed']for r in nav['commands_received'])":
            "    assert nav['commands_are_not_execution_receipts']and not nav['completion_confirmed']\n    assert all(r['validation_passed']for r in nav['commands_received'])",
        'rafael_independent_actual_v2007':'rafael_independent_actual_v2007d',
        'assert town==[0,0]':'assert town==[11,0]',
        'normal_Lisbon_town_ID=0':'normal_Lisbon_town_ID=11',
        'assert get(0x7F244)==get(0x2E58C)==0 and get(0x34674,get(0xCB1A8)+4)==0':
            "assert get(0x7F244)==get(0x2E58C)==0\n    native_fleet_field=get(0x34674,get(0xCB1A8)+4);assert native_fleet_field==11\n    assert bytes(cpu.mem_read(0x02000000,0x400000))==final",
        'normal_docked_fleet_state=0,':'original_native_fleet_field_uninterpreted=11,not_claimed_a_dock_or_sailing_flag=True,',
        'all_inputs_schedule_PNGs_RAM_hashes_callbacks_host_restoration_verified=True,':
            'all_inputs_schedule_PNGs_RAM_hashes_callbacks_host_restoration_verified=True,\n        completion_bound_to_terminal_capture_and177_return_pairs_not_navigation_journal=True,',
    }
    for old,new in changes.items():
        assert old in text,old
        text=text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
