"""Remove the redundant release scratch files after exact Drive readback."""

from scripts import cleanup_rafael_homeland_and_maps_20261121 as precedent
from scripts import register_rafael_B161_B169_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(precedent.source, {
    '"release_stack_with_rafael_homeland_and_maps.json"': '"release_stack_with_rafael_B161_B169.json"',
    '''    previous_play = base.load(live["earlier_gameplay_proof"])
    for shot in [*(row["observed"] for row in previous_play["holds"] + live["holds"] + live["menus"]),
                 previous_play["final_hold"], live["final_hold"], *startup["exact_matching_frames"], startup["read_only_snapshot"]]:''':
        '''    for shot in [*(row["observed"] for row in live["holds"]),
                 live["final_hold"], *startup["exact_matching_frames"], startup["read_only_snapshot"]]:''',
    '''    for capture in (Path(live["earlier_gameplay_proof"]).parent / "capture",
                    release.live.REPORT.parent, release.STARTUP_CAPTURE.parent):''':
        '''    with open_gzip(release.PACKAGE / "build_release_stack.json.gz", "rb") as archived:
        assert file_digest(archived, "sha256").hexdigest() == transaction["registry_after"]
    for capture in (release.live.REPORT.parent, release.STARTUP_CAPTURE.parent):''',
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::verified-checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
