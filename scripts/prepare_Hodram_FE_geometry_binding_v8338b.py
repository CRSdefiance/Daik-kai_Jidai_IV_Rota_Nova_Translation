"""Preserve8338 failed synthetic-offset assumption; read original live VRAM with source-bound mapping."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_FE_geometry_binding_tools_v8338b');assert not root.exists()
    result=derive('scripts/bind_Hodram_outcome_FE_geometry_v8338.py','scripts/bind_Hodram_outcome_FE_geometry_v8338b.py',{
        'Hodram_outcome_FE_geometry_v8338':'Hodram_outcome_FE_geometry_v8338b',
        'from scripts.trace_file_ids_v683 import mapped_read':'from scripts.trace_file_ids_v683 import mapped_read\nfrom scripts.actual_Hodram_FE_VRAM_v8338b import read_bitmap',
        'assert header[:3]==[4,72,48] and header[4]==20':'assert header[:3]==[4,72,48]',
        'stored=readram(view[4]+20,288*48//2);pixels=':'stored,vram_binding=read_bitmap(fullreport,frame,header,view[4]);pixels=',
        'persistent_view_bitmap_header_andpalette_exact=True':'persistent_view_bitmap_header_andpalette_exact=True,actual_bitmap_VRAM_binding=vram_binding',
    })
    root.mkdir(parents=True);save(root/'live_original_VRAM_not_synthetic_painter_allocation_successor.json',dict(derivation=result,
        reason='Original live header4 is a relative pixel pointer into CPU VRAM,not the20-byte synthetic-painter allocation offset. Pinned DeSmuME MMU.cpp/MMU.h plus captured VRAM controls map the bitmap through bankD ABG to LCDM. The original paint context is temporary stack storage;the view/header/palette persist during holds.',
        failed_binder_andall_completed_runs_preserved=True,no_new_capture_orROM_orcontroller_orpalette_change=True,all_prior_native_high_constants_andmultiplicity_preserved=True,new_credit=0,full_goal_complete=False))
