"""Compare the hide call's carried source cursor through the exact relocation map."""
from pathlib import Path
def picture_calls_preserved(a,b,c):
    if c['word']!=0x4700:return a==b
    assert len(a)==len(b)==1 and a[0]['address']==b[0]['address']==0x02028A8C
    assert a[0]['args'][3]==0x02660000+c['old_offset'] and b[0]['args'][3]==0x02660000+c['new_offset']
    aa={**a[0],'args':a[0]['args'][:3]+[0x02660000]};bb={**b[0],'args':b[0]['args'][:3]+[0x02660000]};assert aa==bb
    return True
if __name__=='__main__':
    a=Path('scripts/prove_lil_B142_B145_relocated_controls_v3600.py');t=a.read_text(encoding='utf-8');changes=[('lil_B142_B145_relocated_controls_v3600','lil_B142_B145_relocated_controls_v3600b'),("assert result['original_picture_boundary_calls']==previous_case['original_picture_boundary_calls'] and result['native_result']==previous_case['native_result']","assert picture_calls_preserved(previous_case['original_picture_boundary_calls'],result['original_picture_boundary_calls'],c) and result['native_result']==previous_case['native_result']"),('all_original_picture_descriptors_layouts_and_hide_boundary_preserved=True','all_original_picture_descriptors_layouts_and_hide_boundary_preserved=True,hide_boundary_carried_R3_source_cursor_maps_exactly_from482_to534=True,hide_boundary_R0_owner_R1_word_R2_length_pointer_and_all_other_fields_exact=True,initial_harness_diagnostic="work/analysis/lil_B142_B145_relocated_controls_diagnostic_v3600/source_and_target_picture_boundary_differences.json"')]
    for x,y in changes:assert x in t,x;t=t.replace(x,y)
    exec(compile(t,str(Path(__file__))+'::mapped_hide_source_cursor','exec'),dict(__name__='__main__',__file__=__file__,picture_calls_preserved=picture_calls_preserved))
