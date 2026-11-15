"""Distinguish selected native alignments from the extra rejected layout’s executed cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/approve_maria270_offline_v1.py').read_text(encoding='utf-8'),{
    "offline270_display_approval_v1.json":"offline270_display_approval_v2.json",
    "final270_native_v1":"final270_native_v2",
    "final270_plan_v1":"final270_plan_v2",
    "fresh_compiled_alignments=108,reused_compiled_alignments=960":
        "fresh_compiled_alignments=104,reused_compiled_alignments=960,total_fresh_alignment_cases_executed=108,rejected_layout_alignment_cases=4",
})
exec(compile(source,__file__+'::same-selected-pixels-proof-reuse-selected-versus-rejected-case-accounting','exec'),globals())
