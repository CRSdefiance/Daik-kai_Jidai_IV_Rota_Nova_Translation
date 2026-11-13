"""Source-lock the existing one-final-commit positive proof for the retrospective stage."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/retrospective_B218_atomic_tools_v7854');assert not root.exists()
    source=Path('scripts/validate_Maria_B36_atomic_v7818b.py').read_text(encoding='utf-8')
    assignment=next(n for n in ast.walk(ast.parse(source)) if isinstance(n,ast.Assign)
        and any(isinstance(t,ast.Name) and t.id=='deps' for t in n.targets))
    deps="""deps={str(p) for p in [DRAFT,APPROVED,SEALED,MAP,SEAL,*map(Path,proofs().values()),
        Path(owned.__file__),Path('dk4tool/patch/retrospective_SC2_reconstruction_v2.py'),
        Path('dk4tool/dialogue/lil_B218_retrospective_profile_v1.py'),
        Path('dk4tool/dialogue/lil_B218_retrospective_layout_v1.py'),
        Path('dk4tool/dialogue/lil_B218_retrospective_plan_v1.py'),
        Path('scripts/retrospective_B218_final_paths_v7853.py'),
        Path('scripts/seal_retrospective_B218_v7853.py'),Path(__file__)]}"""
    result=derive('scripts/validate_Maria_B36_atomic_v7818b.py','scripts/validate_retrospective_B218_atomic_v7854.py',{
        'maria_B36_editorial_v1':'lil_B218_retrospective_v1',
        'scripts.Maria_B36_final_paths_v7816b':'scripts.retrospective_B218_final_paths_v7853',
        'work/analysis/maria_B36_atomic_v7818b':'work/analysis/retrospective_B218_atomic_v7854',
        ast.get_source_segment(source,assignment):deps,
        'dk4-Maria16-B36-editorial-release-v1':'dk4-B218-retrospective-release-v1',
        '/data/SC3.DK4':'/data/SC2.DK4',
        "len(proof['changed_records'])==16":"len(proof['changed_records'])==1 and proof['reviewed_records']==13",
        'positive_records=16':'positive_records=13',
        '16-record atomic positive:one final SC3 commit':'13-record retrospective atomic positive:one changed record/one final SC2 commit',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        complete_original_inverse_whole_ROM_comparison_andone_commit_guards_preserved=True,
        thirteen_reviewed_records_one_changed_record_zero_duplicate_credit=True,full_goal_complete=False))
