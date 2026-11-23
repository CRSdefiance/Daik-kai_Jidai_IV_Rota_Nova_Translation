"""Reclaim redundant checkpoint files after the published candidate is verified."""

from scripts import cleanup_rafael_east_asia_followup_20261121 as precedent
from scripts import register_rafael_spain_london_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(precedent.source, {
    '"release_stack_with_rafael_east_asia_showdown.json"': '"release_stack_with_rafael_spain_london.json"',
    'live["company_final_hold"]': 'live["reference_final_hold"]',
    '''    for capture in (release.live.REPORT.parent, release.live.REFERENCE_STAGE / "company_replay/capture",
                    release.live.replay.FOCUS_REPORT.parent, release.live.REPLAY_STAGE / "startup/capture",
                    release.live.REFERENCE_STAGE / "startup/capture", release.STARTUP_CAPTURE.parent):''':
        '''    for capture in (release.live.REFERENCE_ROOT / "capture", release.live.replay.REPORT.parent,
                    release.live.REFERENCE_STAGE / "startup/capture", release.STARTUP_CAPTURE.parent):''',
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
