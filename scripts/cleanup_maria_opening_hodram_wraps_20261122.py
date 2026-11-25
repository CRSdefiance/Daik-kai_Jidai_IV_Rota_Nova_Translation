"""Clear redundant temporary files once the mixed-route candidate is on Drive."""

from scripts import cleanup_maria_B18_B20_20261122 as previous
from scripts import register_maria_opening_hodram_wraps_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base,stage=release.base,release.writer


def redundant_test_files(candidate_sha,patch_sha):
    return {stage.ROOT/"clean_rebuilt.nds":candidate_sha,stage.ROOT/"translation.xdelta":patch_sha}


source=checked_text(previous.source,{
    '''    earlier = base.load(release.EARLIER)
    first_report = stage.FIRST_ROOT/"focused_gameplay/after/capture_report.json"
    retained[first_report] = earlier["report_sha256"]''':
    '''    hodram = base.load(release.hodram.PROOF)
    retained.update({Path(p):h for p,h in hodram["evidence"].items()})''',
    '''    for shot in [*(row["capture"] for row in live["observations"] + earlier["observations"]),
                 *live["return_frames"].values(),*earlier["return_frames"].values(),
                 *startup["exact_matching_frames"], startup["read_only_snapshot"]]:''':
    '''    for shot in [*(row["capture"] for row in live["observations"]),
                 *live["return_frames"].values(),*(row["observed"] for row in hodram["holds"]),
                 hodram["final_hold"],*startup["exact_matching_frames"],startup["read_only_snapshot"]]:''',
    'release.live.REPORT.parent, first_report.parent, release.STARTUP_CAPTURE.parent':
        'release.live.REPORT.parent, release.hodram.REPORT.parent, release.STARTUP_CAPTURE.parent',
    'release_stack_with_maria_B18_B20.json':'release_stack_with_maria_opening_hodram_wraps.json',
})
scope=previous.scope|globals()
exec(compile(source,__file__+"::verified-mixed-route-cleanup","exec"),scope)

if __name__=="__main__":
    scope["main"]()

