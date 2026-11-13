"""Rebind the old probe to actual current loader metadata and both source ITCM sections."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    src=Path('scripts/prove_shachihoko_detail_fonts_v6101.py').read_text('utf-8');start=src.index('    adapted=checked_text(');end=src.index('    for version,path,directory',start);block=src[start:end]
    print(derive('scripts/prove_shachihoko_detail_fonts_v6101.py','scripts/prove_shachihoko_detail_fonts_v6101b.py',{
        block:"    from scripts.current_item_detail_machine_v6102 import SOURCE as adapted,make_execute\n",
        "env={**old_execute.__globals__,'CURRENT_DIRECTORY_SHA256':directory};exec(compile(adapted,__file__+'::exact-current-COMMON-directory','exec'),env);execute=env['execute']":"execute=make_execute(directory,arm)",
        "Path('scripts/probe_map_tooltip_cp932_pixels.py')":"Path('scripts/probe_map_tooltip_cp932_pixels.py'),Path('scripts/current_item_detail_machine_v6102.py')",
    }))
