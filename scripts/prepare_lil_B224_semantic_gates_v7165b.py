"""Preserve the passed initial positive and bind stronger independent semantic gates."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_semantic_tools_v7165b')
if __name__=='__main__':
    assert not ROOT.exists()
    changes={
      'lil_B224_atomic_v7165':'lil_B224_atomic_v7165b',
      "module='dk4tool/patch/lil_B224_editorial_v2.py'":"module='dk4tool/patch/lil_B224_editorial_v3.py'",
      "derive('dk4tool/patch/lil_B224_editorial_v1.py',module,{'all15_objects16_pages_actual_complete':'all15_objects15_pages_actual_complete'})":"derive('dk4tool/patch/lil_B224_editorial_v2.py',module,{'lil_B224_atomic_support_v1':'lil_B224_atomic_support_v2'})",
      'from dk4tool.patch import lil_B224_editorial_v2 as owned':'from dk4tool.patch import lil_B224_editorial_v3 as owned',
      "Path('dk4tool/patch/lil_B224_atomic_support_v1.py'),Path(__file__)":"Path('dk4tool/patch/lil_B224_atomic_support_v1.py'),Path('dk4tool/patch/lil_B224_atomic_support_v2.py'),Path('scripts/prepare_lil_B224_semantic_gates_v7165b.py'),Path(__file__)",
    }
    target='scripts/validate_lil_B224_atomic_v7165b.py';assert not Path(target).exists()
    row=derive('scripts/validate_lil_B224_atomic_v7165.py',target,changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_semantic_positive_successor.json',dict(tool=row,initial_positive_preserved=True,individual_speaker_context_geometry_policy_and_proof_counts_explicit=True,no_new_ROM_or_credit=True))
