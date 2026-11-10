"""Use the documented harness START option; preserve the pre-frame argument rejection."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/run_market_goods_info_fix_checks_v1.py').read_text(encoding='utf-8'),{
    "mode+'_run_v1'":"mode+'_run_v2'",
    "'--start-frame'":"'--press-start'",
})
exec(compile(source,__file__+'::same-isolated-coldboot-inputs-correct-documented-START-option','exec'),globals())
