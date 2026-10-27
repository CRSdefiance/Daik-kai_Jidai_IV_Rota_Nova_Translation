"""Preserve the first complete-plane mismatch from the new menu consumer."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

OLD=Path('scripts/prove_lil_shrines_choices_v3185b.py')
NEW=Path('scripts/diagnose_lil_three_choice_canvas_v3186b.py')
ROOT=Path('work/analysis/lil_Shrines_Temples_menu_diagnostic_v3186')

if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8').replace('lil_Shrines_Temples_choices_v3185b','lil_Shrines_Temples_choices_v3186b')
    anchor='    cases,pictures = [],[]'
    assert text.count(anchor)==1
    text=text.replace(anchor,"""    original_check='    assert pixels == bytes(expected)'
    diagnostic_check=\"\"\"    if pixels != bytes(expected):
        directory=Path('work/analysis/lil_Shrines_Temples_menu_diagnostic_v3186/mismatch')
        directory.mkdir(parents=True)
        points=[(i%stride,i//stride,v) for i,v in enumerate(pixels) if v]
        expected_points=[(i%stride,i//stride,v) for i,v in enumerate(expected) if v]
        save(directory/'first_complete_plane_mismatch.json',dict(text=text.decode(),style=style,width=width,stride=stride,
            native_nonblank_bounds=[min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points),max(p[1] for p in points)],
            expected_nonblank_bounds=[min(p[0] for p in expected_points),min(p[1] for p in expected_points),max(p[0] for p in expected_points),max(p[1] for p in expected_points)],
            native_points=points,expected_points=expected_points,view_hex=bytes(cpu.mem_read(view,64)).hex(),
            context_hex=bytes(cpu.mem_read(context,64)).hex(),header_hex=raw_header.hex()))
        raise AssertionError('Complete plane diagnostic preserved; no clipping or pixel waiver')
\"\"\"
    assert painter.count(original_check)==1
    painter=painter.replace(original_check,diagnostic_check)
""" + anchor)
    text=text.replace("'LABEL_WIDTH':width,'sha':sha","'LABEL_WIDTH':width,'sha':sha,'Path':Path,'save':save")
    NEW.write_text(text,encoding='utf-8')
    ROOT.mkdir(parents=True)
    save(ROOT/'diagnostic_provenance.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),
        diagnostic=str(NEW),diagnostic_sha256=sha(NEW.read_bytes()),no_pixel_bounds_or_control_waiver=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
