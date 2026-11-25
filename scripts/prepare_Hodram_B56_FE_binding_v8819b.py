"""Preserve stopped four-hold assumption;bind the three actual complete FE holds."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B56_FE_tools_v8819b');assert not root.exists()
    actual=Path('work/analysis/Hodram_B56_actual_v8818/B56/paired_actual_dialogue_headers_flow_returns.json');packet=read(actual)
    held=[{h['frame'] for s in g['speeches'] if s['source_selector']==254 for h in s['complete_holds']} for g in packet['groups']]
    assert held==[{4090,4150,4210},{4090,4150,4210}]
    result=derive('scripts/bind_Hodram_B56_FE_v8819.py','scripts/bind_Hodram_B56_FE_v8819b.py',{
        'Hodram_B56_FE_binding_v8819':'Hodram_B56_FE_binding_v8819b',
        'held=={4030,4090,4150,4210}':'held=={4090,4150,4210}',
        'assert len(holds)==4':'assert len(holds)==3',
        'two_original_FE_paint_snapshots_eight_exact_bitmap_palette_RGB_holds.json':'two_original_FE_paint_snapshots_six_exact_bitmap_palette_RGB_holds.json',
        'snapshots/eight same-run':'snapshots/six same-run',
    })
    root.mkdir(parents=True);save(root/'qualified_actual_FE_hold_membership.json',dict(derivation=result,
        actual_audit=str(actual),actual_audit_sha256=__import__('hashlib').sha256(actual.read_bytes()).hexdigest(),
        actual_three_complete_holds_perlanguage=sorted(held[0]),earlier4030_sample_not_counted_as_complete=True,
        original_failed_producer_preserved_no_scene_orcallback_replay=True,
        all_native_geometry_palette_bitmap_VRAM_RGB_andreadonly_guards_unchanged=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
