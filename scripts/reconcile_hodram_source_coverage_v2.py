"""Refresh exact clean-source credit bindings after residual integration; no editorial replay."""
from pathlib import Path
from scripts import reconcile_hodram_source_coverage_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/Hodram_source_coverage_20261109_v2')
RELEASE=Path('work/hodram_residual_release_v1/registered_release_verification.json')
ARCHIVE=previous.ARCHIVE
source=checked_text(previous.source,{'== 18767':'== 19161'})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-exact-source-coverage-current-credit-bindings','exec'),env)
if __name__=='__main__':env['main']()
