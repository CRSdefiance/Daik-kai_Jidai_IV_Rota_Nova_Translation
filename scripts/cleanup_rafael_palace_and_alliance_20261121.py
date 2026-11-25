"""Clear verified duplicate artifacts after publishing the palace candidate."""

from scripts import cleanup_rafael_ruins_and_proof_20261121 as precedent
from scripts import register_rafael_palace_and_alliance_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(precedent.source, {
    '"release_stack_with_rafael_ruins_and_proof.json"': '"release_stack_with_rafael_palace_and_alliance.json"',
    '''    earlier = stage.ROOT.with_name("staged_v1")
    reference = base.load(earlier / "focused_gameplay/verified_gameplay.json")
    earlier_sheets = base.load(earlier / "native_display/native_display.json")["sheets"] + reference["sheets"]
    retained.update({Path(sheet["path"]): sheet["sha256"] for sheet in earlier_sheets})
    retained.update({Path(p): h for p, h in reference["evidence"].items()})
    for shot in [*(row["observed"] for row in reference["holds"] + reference["menus"] + live["holds"] + live["menus"]),
                 live["final_hold"], reference["final_hold"], *startup["exact_matching_frames"], startup["read_only_snapshot"]]:''':
        '''    guard = release.guard_spec()
    retained[Path(guard["path"])] = guard["sha256"]
    guard_receipt = base.load(stage.GUARD)
    retained[stage.GUARD_SC0] = guard_receipt["prior_receipt"]["sha256"]
    previous_play = base.load(live["earlier_gameplay_proof"])
    for shot in [*(row["observed"] for row in previous_play["holds"] + live["holds"] + live["menus"]),
                 previous_play["final_hold"], live["final_hold"], *startup["exact_matching_frames"], startup["read_only_snapshot"]]:''',
    '''    for capture in (earlier / "focused_gameplay/capture", release.live.REPORT.parent,
                    release.STARTUP_CAPTURE.parent):''':
        '''    for capture in (Path(live["earlier_gameplay_proof"]).parent / "capture",
                    release.live.REPORT.parent, release.STARTUP_CAPTURE.parent):''',
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
