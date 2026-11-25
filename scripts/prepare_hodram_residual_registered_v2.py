"""Recover the exact review projection and freeze all observed run plans before qualification."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/prepare_hodram_residual_registered_v1.py').read_text(encoding='utf-8'),{
    'from dk4tool.patch.hodram_residual_release_v1 import plan_release':'from dk4tool.patch.hodram_residual_release_v2 import plan_release',
    "OUT=ROOT/'registered_preparation_v1'":"OUT=ROOT/'registered_preparation_v2'",
    'assert not OUT.exists() and not CONFIG.exists() and not FINAL.exists()':'assert not OUT.exists() and not CONFIG.exists() and FINAL.exists()',
    '    OUT.mkdir();save(FINAL,doc)':'    OUT.mkdir();assert load(FINAL)==doc',
    "Path('dk4tool/patch/hodram_residual_release_v1.py')]}":
        "Path('dk4tool/patch/hodram_residual_release_v1.py'),Path('dk4tool/patch/hodram_residual_release_v2.py'),*[Path(r['terminal']).parent/'run_plan.json' for r in load(evidence['actual'])['runs']]]}",
})
exec(compile(source,__file__+'::same-source-qualification-readback-andfrozen-run-plan-dependencies','exec'),globals())
