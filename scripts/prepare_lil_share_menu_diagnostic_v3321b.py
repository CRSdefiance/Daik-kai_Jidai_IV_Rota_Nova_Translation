"""Preserve3321; save exact native/independent-plane differences before failure."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/prove_lil_B131_B133_choices_v3321.py');new=Path('scripts/diagnose_lil_B131_B133_choices_v3321b.py');assert not new.exists();t=old.read_text(encoding='utf-8').replace('lil_B131_B133_choices_v3321','lil_B131_B133_choices_diagnostic_v3321b')
    anchor='    cases,pictures = [],[]';assert t.count(anchor)==1
    injected='''    needle='    assert pixels == bytes(expected)'
    diagnostic="""    if pixels!=bytes(expected):
        diagnostic_root.mkdir(parents=True,exist_ok=True)
        differences=[dict(x=i%stride,y=i//stride,native=a,expected=b) for i,(a,b) in enumerate(zip(pixels,expected)) if a!=b]
        save(diagnostic_root/'native_complete_plane_difference.json',dict(label=text.decode('ascii'),logical_width=width,storage_stride=stride,expected_origin=[x,y],native_plane_sha256=sha(pixels),independent_plane_sha256=sha(bytes(expected)),differences=differences,native_view_words=list(struct.unpack('<20I',bytes(cpu.mem_read(view,80)))),native_context_words=list(struct.unpack('<12I',bytes(cpu.mem_read(context,48)))),input_and_header_and_canaries_preserved=bytes(cpu.mem_read(string-16,96))==original and bytes(cpu.mem_read(header,20))==raw_header))
        print(dict(label=text.decode('ascii'),logical_width=width,storage_stride=stride,differing_pixels=len(differences),difference_x_bounds=[min(d['x'] for d in differences),max(d['x'] for d in differences)]),flush=True)
    assert pixels == bytes(expected)"""
    assert painter.count(needle)==1
    painter=painter.replace(needle,diagnostic)
'''
    t=t.replace(anchor,injected+anchor);a="env = {**prior.__dict__,'LABEL_WIDTH':width,'sha':sha}";assert a in t;t=t.replace(a,"env = {**prior.__dict__,'LABEL_WIDTH':width,'sha':sha,'save':save,'diagnostic_root':MAINROOT}")
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_share_menu_diagnostic_tools_v3321b');root.mkdir(parents=True);save(root/'successor_provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),all_native_pixel_ABI_source_and_bounds_assertions_retained=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
