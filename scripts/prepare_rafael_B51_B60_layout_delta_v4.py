"""Refresh only the two final boundary refinements from the exact combined v3 proof."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/prepare_rafael_B51_B60_layout_delta.py').read_text(encoding='utf-8'),{
    "output=ROOT/'layout_delta_v3'":"output=ROOT/'layout_delta_v4'",
    "old_path=ROOT/'automatic_v1/automatic_plans.json';new_path=ROOT/'automatic_v3/automatic_plans.json'":
        "old_path=ROOT/'automatic_v3/automatic_plans.json';new_path=ROOT/'automatic_v4/automatic_plans.json'",
    "native_path=ROOT/'speech_native_v1/compiled_native_pages.json'":"native_path=ROOT/'combined_native_v3.json'",
})
exec(compile(source,__file__+'::same-exact-native-byte-reuse-only-two-final-boundaries','exec'),globals())
