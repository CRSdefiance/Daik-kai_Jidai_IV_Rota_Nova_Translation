"""Reuse the just-verified full audit of the same immutable terminal run."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read


def audit(terminal_frame):
    proof=read('work/analysis/search_reports_actual_v1683/original_revised_failure_forage_and_loss312_verified.json')
    preserved=proof['preservation_audit']
    assert preserved['terminal_frame']==terminal_frame==20792
    assert proof['candidate_sha256']==preserved['candidate_sha256']==sha(Path(proof['candidate']).read_bytes())
    assert preserved['all48_location20_supply10_crew_owned_bytes_and_all_other4MiB_audited']
    assert preserved['all_inputs_snapshots_PNG_hashes_and_unchanged_source_disposable_saves_audited']
    assert sha(Path(preserved['terminal_report']).read_bytes())==preserved['terminal_report_sha256']
    report=read(preserved['terminal_report'])
    assert report['frames']==terminal_frame and report['ROM_sha256']==proof['candidate_sha256']
    assert not report['callback_errors'] and report['cold_boot'] and not report['savestate_loaded']
    return preserved
