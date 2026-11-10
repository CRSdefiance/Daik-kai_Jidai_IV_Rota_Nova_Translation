"""Run all own-startup/state/protected-getter checks on the market-fixed Maria270 candidate."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/verify_maria301_startup_v1.py').read_text(encoding='utf-8'),{
    'scripts.build_registered_maria301_v1':'scripts.build_registered_maria270_v1',
    "OUT/'own_startup_capture_v2/capture_report.json'":"OUT/'own_startup_run_v1/capture/capture_report.json'",
    'all12 protected names from the Maria301 cumulative candidate own startup':
        'all12 protected names from the Maria270 cumulative candidate own startup',
})
exec(compile(source,__file__+'::same-own-candidate-state-complete-RAM-andboth-original-getter-contracts','exec'),globals())
