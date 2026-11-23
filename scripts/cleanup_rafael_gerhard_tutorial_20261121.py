"""Clear redundant Gerhard tutorial files after the Drive build is read back."""

from pathlib import Path

from scripts import cleanup_rafael_spain_london_20261121 as prior
from scripts import register_rafael_gerhard_tutorial_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(prior.source, {
    '"release_stack_with_rafael_spain_london.json"': '"release_stack_with_rafael_gerhard_tutorial.json"',
    '''    reference = base.load(release.live.REFERENCE_GAMEPLAY)
    for shot in [*(row["observed"] for row in reference["holds"] + live["holds"]),
                 live["final_hold"], live["reference_final_hold"], *startup["exact_matching_frames"], startup["read_only_snapshot"]]:''':
        '''    earlier = stage.ROOT.with_name("gerhard_staged_v2")
    reference = base.load(earlier / "focused_gameplay/verified_gameplay.json")
    earlier_sheets = base.load(earlier / "native_display/native_display.json")["sheets"] + reference["sheets"]
    retained.update({Path(sheet["path"]): sheet["sha256"] for sheet in earlier_sheets})
    retained.update({Path(p): h for p, h in reference["evidence"].items()})
    for shot in [*(row["observed"] for row in reference["holds"] + reference["menus"] + live["holds"] + live["menus"]),
                 live["final_hold"], reference["final_hold"], *startup["exact_matching_frames"], startup["read_only_snapshot"]]:''',
    '''    for capture in (release.live.REFERENCE_ROOT / "capture", release.live.replay.REPORT.parent,
                    release.live.REFERENCE_STAGE / "startup/capture", release.STARTUP_CAPTURE.parent):''':
        '''    for capture in (earlier / "focused_gameplay/capture", release.live.replay.REPORT.parent,
                    release.STARTUP_CAPTURE.parent):''',
})
scope = prior.scope | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
