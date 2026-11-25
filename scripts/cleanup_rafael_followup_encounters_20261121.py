"""Remove verified duplicate files after publishing the Rafael encounters."""

from scripts import cleanup_rafael_gerhard_tutorial_20261121 as prior
from scripts import register_rafael_followup_encounters_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(prior.source, {
    '"release_stack_with_rafael_gerhard_tutorial.json"': '"release_stack_with_rafael_followup_encounters.json"',
    'stage.ROOT.with_name("gerhard_staged_v2")': 'stage.ROOT.with_name("staged_v1")',
    "release.live.replay.REPORT.parent": "release.live.REPORT.parent",
})
scope = prior.scope | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
