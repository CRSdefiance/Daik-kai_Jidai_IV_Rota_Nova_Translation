"""Own coldboot with every runtime byte unchanged and a fresh final read-only snapshot."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/verify_registered_startup.py').read_text(encoding='utf-8'), {
    "    snapshot=next(p for p in capture['read_only_capture_RAM_snapshots'] if p['frame']==4000)":
        "    assert capture['read_only_RAM_snapshot']['read_only_export']\n    snapshot={**capture['read_only_RAM_snapshot'],'frame':capture['frames'],'source_report_key':'read_only_RAM_snapshot','recorded_after_final_frame_no_historical_overlay':True}",
})
exec(compile(source, __file__ + '::unchanged-complete-runtime-own-final-4001-snapshot', 'exec'), globals())
