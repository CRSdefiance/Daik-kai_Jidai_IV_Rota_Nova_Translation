"""Reclaim the obsolete copies after the registered and published builds agree."""

from scripts import cleanup_rafael_tradehouse_festival_20261121 as prior
from scripts import register_rafael_east_asia_followup_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(prior.source, {
    '"release_stack_with_rafael_tradehouse_festival.json"': '"release_stack_with_rafael_east_asia_showdown.json"',
    '    for shot in [*(row["observed"] for row in live["holds"]),':
        '''    reference = base.load(release.live.REFERENCE_GAMEPLAY)
    for shot in [*(row["observed"] for row in reference["holds"] + live["holds"]),''',
    'live["final_hold"], *startup["exact_matching_frames"]':
        'live["final_hold"], live["company_final_hold"], *startup["exact_matching_frames"]',
    '''    for capture in (release.live.REFERENCE_GAMEPLAY / "capture", release.live.REPORT.parent,
                    release.live.REFERENCE_ROOT / "startup/capture", release.STARTUP_CAPTURE.parent):''':
        '''    for capture in (release.live.REPORT.parent, release.live.REFERENCE_STAGE / "company_replay/capture",
                    release.live.replay.FOCUS_REPORT.parent, release.live.REPLAY_STAGE / "startup/capture",
                    release.live.REFERENCE_STAGE / "startup/capture", release.STARTUP_CAPTURE.parent):''',
})
scope = prior.scope | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
