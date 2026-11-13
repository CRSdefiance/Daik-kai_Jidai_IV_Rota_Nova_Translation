"""Successor compares original arrival context instead of assuming Port type7."""
from pathlib import Path

SOURCE = Path('scripts/audit_lil_hamburg_revised_v1967.py')

if __name__ == '__main__':
    assert not Path('work/analysis/lil_Hamburg_revised_audit_v1967').exists()
    text = SOURCE.read_text(encoding='utf-8')
    assert text.count('lil_Hamburg_revised_audit_v1967') == 2
    text = text.replace('lil_Hamburg_revised_audit_v1967','lil_Hamburg_revised_audit_v1967b')
    old = '        assert context[:2] == [7,5]'
    new = """        old_capture = (old_context['old_text_observations'][0]['holds'][0]['capture']
            if at == 49440 else old_context['terminal_capture'])
        old_raw = Path(old_capture.replace('_navigation.png','_arm9_ram.bin')).read_bytes()
        old_index = old_raw.find(ev[:96])
        assert old_index >= 0
        old_cpu, old_get = get_machine(arm,old_raw)
        old_owner = BASE+old_index-0x34
        original_context = list(struct.unpack('<3I',old_cpu.mem_read(old_owner+0x2454,12)))
        assert context == original_context
        assert bytes(old_cpu.mem_read(BASE,0x400000)) == old_raw"""
    assert text.count(old) == 1
    text = text.replace(old,new)
    old = 'current_original_event_context=context,all4MiB_unchanged_by_queries=True'
    new = 'current_original_event_context=context,original_observed_event_context=original_context,all4MiB_unchanged_by_queries=True'
    assert text.count(old) == 1
    text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
