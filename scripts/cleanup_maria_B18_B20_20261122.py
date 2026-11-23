"""Clear verified scratch files from the registered Maria checkpoint."""

from pathlib import Path

from scripts import cleanup_hodram_B311_B324_20261122 as previous
from scripts import register_maria_B18_B20_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.writer


def redundant_test_files(candidate_sha, patch_sha):
    retained, older = stage.ROOT/"startup/capture", stage.FIRST_ROOT/"startup/capture"
    source = base.load(older/"capture_report.json")
    target = base.load(retained/"capture_report.json")
    assert source["ROM_sha256"] == base.digest(stage.FIRST_ROOT/stage.ROM.name)
    assert target["ROM_sha256"] == candidate_sha
    exact = {s["frame"]:s for s in target["frames_captured"]}
    duplicates = {
        Path(s["path"]):s["PNG_sha256"] for s in source["frames_captured"]
        if s["frame"] in exact and s["PNG_sha256"] == base.digest(exact[s["frame"]]["path"])
        and s["PNG_sha256"] == exact[s["frame"]]["PNG_sha256"]
    }
    return duplicates | {stage.ROOT/"clean_rebuilt.nds":candidate_sha,stage.ROOT/"translation.xdelta":patch_sha}


source = checked_text(previous.source, {
    "release.live.PROOF":"release.live.LIVE",
    '''    retained.update({Path(p): h for p, h in (visual | live["evidence"]).items()})''':
    '''    retained.update({Path(p):h for p,h in visual.items()})
    retained[release.live.REPORT] = live["report_sha256"]
    earlier = base.load(release.EARLIER)
    first_report = stage.FIRST_ROOT/"focused_gameplay/after/capture_report.json"
    retained[first_report] = earlier["report_sha256"]''',
    '''    for shot in [*(row["observed"] for row in live["holds"] + live["menus"]),
                 live["final_hold"], *startup["exact_matching_frames"], startup["read_only_snapshot"]]:''':
    '''    for shot in [*(row["capture"] for row in live["observations"] + earlier["observations"]),
                 *live["return_frames"].values(),*earlier["return_frames"].values(),
                 *startup["exact_matching_frames"], startup["read_only_snapshot"]]:''',
    'release.live.REPORT.parent, release.STARTUP_CAPTURE.parent':
        'release.live.REPORT.parent, first_report.parent, release.STARTUP_CAPTURE.parent',
    'release_stack_with_hodram_B311_B324.json':'release_stack_with_maria_B18_B20.json',
})
scope = previous.scope | globals()
exec(compile(source,__file__+"::verified-Maria-cleanup","exec"),scope)

if __name__=="__main__":
    scope["main"]()

