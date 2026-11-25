"""Preserve the Windows-path selector failure andselect the evidence plan by Path.name."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B227_atomic_tools_v7320c')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('dk4tool/patch/lil_B227_atomic_support_v2.py','dk4tool/patch/lil_B227_atomic_support_v3.py',{'def audit_sealed_scope':'from pathlib import Path\n\ndef audit_sealed_scope',"p.endswith('/run_plan.json')":"Path(p).name=='run_plan.json'"}),derive('dk4tool/patch/lil_B227_editorial_v2.py','dk4tool/patch/lil_B227_editorial_v3.py',{'lil_B227_atomic_support_v2':'lil_B227_atomic_support_v3'}),derive('scripts/validate_lil_B227_atomic_v7321b.py','scripts/validate_lil_B227_atomic_v7321c.py',{'lil_B227_editorial_v2':'lil_B227_editorial_v3','lil_B227_atomic_support_v2':'lil_B227_atomic_support_v3','lil_B227_atomic_v7321b':'lil_B227_atomic_v7321c','lil_B227_atomic_tools_v7320b':'lil_B227_atomic_tools_v7320c','repair_lil_B227_atomic_scope_v7320b.py':'repair_lil_B227_atomic_path_v7320c.py'})]
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_atomic_compiler.json',dict(derivations=rows,original_Windows_separator_StopIteration_before_archive_write_preserved=True,no_semantic_or_native_check_weakened=True))
