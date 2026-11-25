"""Qualify the same cold boot using its explicitly recorded final frame4001 snapshot."""
from dk4tool.patch.owned_name_fields_v3 import plan_arm9_name_fields
from scripts import verify_registered_startup_v5 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    "    snapshot=next(p for p in capture['read_only_capture_RAM_snapshots'] if p['frame']==4000)":
    """    assert capture['frames']==4001 and capture['read_only_RAM_snapshot']['read_only_export']
    snapshot={**capture['read_only_RAM_snapshot'],'frame':capture['frames'],'source_report_key':'read_only_RAM_snapshot','recorded_after_final_frame_no_historical_overlay':True}""",
})
exec(compile(source, __file__ + '::same-owned-coldboot-checks-explicit-final-snapshot', 'exec'), globals())
