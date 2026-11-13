"""Run the same semantic qualification against the corrected lowercase registry binding."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/qualify_rafael_B51_B60_release.py').read_text(encoding='utf-8'),{
    'Rafael_B51_B60_release_qualification_20261104':'Rafael_B51_B60_release_qualification_v2_20261104',
    'work/analysis/Rafael_B51_B60_release_20261104/registered_preparation.json':
        'work/analysis/Rafael_B51_B60_release_registry_v2_20261104/registered_preparation.json',
})
exec(compile(source,__file__+'::same-positive-and-twelve-rejections-corrected-entry-point','exec'),globals())
