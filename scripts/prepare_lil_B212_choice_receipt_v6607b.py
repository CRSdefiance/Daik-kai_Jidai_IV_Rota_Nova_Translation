"""Preserve the renderer's own style field when recording its plane proof."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B212_choice_tools_v6607b')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/prove_lil_B212_choice_planes_v6607.py','scripts/prove_lil_B212_choice_planes_v6607b.py',{'lil_B212_choice_planes_v6607':'lil_B212_choice_planes_v6607b','planes.append(dict(index=index,style=style,native_plane':'assert proof[\'style\']==style;planes.append(dict(index=index,native_plane'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_style_metadata_correction.json',dict(proof=proof,failed_runner_preserved='scripts/prove_lil_B212_choice_planes_v6607.py',reason='Native proof already supplies style. Assert equality and keep that single source value rather than passing it twice to dict(). No renderer or expected pixel change.',new_credit=0,full_goal_complete=False))
