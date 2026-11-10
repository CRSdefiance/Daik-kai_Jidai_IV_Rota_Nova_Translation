"""Bind the reconstruction to the exact clean Lil header; preserve the rejected Maria assumption."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/retrospective_B218_relocation_repair_v7839b');assert not root.exists()
    src=Path('scripts/relocate_retrospective_B218_v7839.py').read_text(encoding='utf-8')
    assignment=next(n for n in ast.walk(ast.parse(src)) if isinstance(n,ast.Assign)
        and any(isinstance(t,ast.Name) and t.id=='provenance' for t in n.targets))
    changes={
        'work/analysis/retrospective_B218_relocation_v7839':'work/analysis/retrospective_B218_relocation_v7839b',
        ast.get_source_segment(src,assignment):"provenance=read('work/analysis/retrospective_B218_relocation_repair_v7839b/provenance.json')['helper_derivation']",
        'from dk4tool.patch.retrospective_SC2_reconstruction_v1 import reconstruct':'from dk4tool.patch.retrospective_SC2_reconstruction_v2 import reconstruct',
    }
    checked_text(src,changes)
    correction={"b'CS\\1\\1'":"b'CS\\0\\1'"}
    checked_text(Path('dk4tool/patch/retrospective_SC2_reconstruction_v1.py').read_text(encoding='utf-8'),correction)
    helper=derive('dk4tool/patch/retrospective_SC2_reconstruction_v1.py','dk4tool/patch/retrospective_SC2_reconstruction_v2.py',correction)
    producer=derive('scripts/relocate_retrospective_B218_v7839.py','scripts/relocate_retrospective_B218_v7839b.py',changes)
    root.mkdir(parents=True);save(root/'provenance.json',dict(helper_derivation=helper,producer_derivation=producer,
        exact_clean_B218_header_prefix='43530001',rejected_unrelated_Maria_prefix='43530101',
        both_clean_andcurrent_Lil_headers_require_same_exact_prefix=True,
        all_other_source_numeric_layout_control_andinverse_guards_unchanged=True,
        failed_original_helper_producer_andempty_root_preserved=True,no_ROM_orledger_change=True,full_goal_complete=False))
