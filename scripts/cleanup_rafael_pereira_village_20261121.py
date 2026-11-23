"""Clear verified duplicate staging metadata and any redundant replay files."""

from inspect import getsource

from scripts import cleanup_rafael_spain_20261121 as prior
from scripts import register_rafael_pereira_village_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(getsource(prior.main), {
    'live["holds"] + live["menus"]': 'live["holds"]',
    '"release_stack_with_rafael_spain.json"': '"release_stack_with_rafael_pereira_village.json"',
    '''    first = stage.ROOT.with_name("staged_v1")
    for capture in (first / "focused_gameplay/capture", first / "startup/capture"):''':
        '''    for capture in (release.live.replay.REPORT.parent, release.STARTUP_CAPTURE.parent):''',
})
scope = vars(prior) | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
