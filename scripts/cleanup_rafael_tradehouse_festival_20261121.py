"""Reclaim redundant festival checkpoint files after publishing the candidate."""

from scripts import cleanup_rafael_pereira_village_20261121 as prior
from scripts import register_rafael_tradehouse_festival_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(prior.source, {
    '"release_stack_with_rafael_pereira_village.json"': '"release_stack_with_rafael_tradehouse_festival.json"',
    '    for capture in (release.live.replay.REPORT.parent, release.STARTUP_CAPTURE.parent):':
        '''    for capture in (release.live.REFERENCE_GAMEPLAY / "capture", release.live.REPORT.parent,
                    release.live.REFERENCE_ROOT / "startup/capture", release.STARTUP_CAPTURE.parent):''',
})
scope = prior.scope | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
