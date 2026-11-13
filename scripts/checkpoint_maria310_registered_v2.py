"""Preserve the prepared handoff and route new intake/credited metadata through their proper guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/checkpoint_maria310_registered_v1.py').read_text(encoding='utf-8'),{
    'from scripts.save_editorial_progress_checkpoint_v9 import checkpoint':
        'from scripts.save_maria310_registered_checkpoint_v1 import checkpoint',
    "testing=ROOT/'testing_handoff.md';assert not testing.exists()":
        "testing=ROOT/'testing_handoff.md';previous_testing=testing.read_bytes() if testing.exists() else None",
    "    testing.write_text(f'''":"    testing_text=f'''",
    "''',encoding='utf-8',newline='\\n')":
        "'''\n    if previous_testing is not None:assert previous_testing==testing_text.encode('utf-8')\n    else:testing.write_bytes(testing_text.encode('utf-8'))",
    "final_cumulative_integration_complete=True,registered_checkpoint_evidence=evidence),\n            'Maria_SC3_B58_B70_clean_20261109':":
        "final_cumulative_integration_complete=True,registered_checkpoint_evidence=evidence)},\n        new_entries={'Maria_SC3_B58_B70_clean_20261109':",
    "ROOT/'registered_progress_checkpoint_v1'":"ROOT/'registered_progress_checkpoint_v2'",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-verified-release-docs-explicit-new-entry-andcompleted-metadata','exec'),globals())
