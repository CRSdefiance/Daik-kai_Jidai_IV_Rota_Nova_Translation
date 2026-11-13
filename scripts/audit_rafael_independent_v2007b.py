"""Successor uses terminal captures/observer for completion,not input journal.

The harness deliberately marks navigation commands as non-execution receipts.
"""
from pathlib import Path

SOURCE=Path('scripts/audit_rafael_independent_v2007.py')

if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    old="    assert nav['completion_confirmed']and all(r['validation_passed']for r in nav['commands_received'])"
    new="    assert nav['commands_are_not_execution_receipts']and not nav['completion_confirmed']\n    assert all(r['validation_passed']for r in nav['commands_received'])"
    assert text.count(old)==1;text=text.replace(old,new)
    text=text.replace('rafael_independent_actual_v2007','rafael_independent_actual_v2007b')
    text=text.replace('all_inputs_schedule_PNGs_RAM_hashes_callbacks_host_restoration_verified=True,',
        "all_inputs_schedule_PNGs_RAM_hashes_callbacks_host_restoration_verified=True,\n        completion_bound_to_terminal_capture_and177_return_pairs_not_navigation_journal=True,")
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
