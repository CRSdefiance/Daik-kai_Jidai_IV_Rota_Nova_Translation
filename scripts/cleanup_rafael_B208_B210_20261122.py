"""Clear verified redundant files after publishing the B208–210 candidate."""

from scripts import cleanup_rafael_B181_B187_20261121 as precedent
from scripts import register_rafael_B208_B210_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(precedent.source, {
    '"release_stack_with_rafael_B181_B187.json"': '"release_stack_with_rafael_B208_B210.json"',
    '''    captures = [release.live.REPORT.parent, release.STARTUP_CAPTURE.parent]
    for version in ("staged_B181_B187",):
        checked = stage.ROOT.with_name(version)
        captures.extend(checked / area / "capture" for area in ("focused_gameplay", "startup"))''':
        '    captures = [release.live.REPORT.parent, release.STARTUP_CAPTURE.parent]',
    'for row in live["holds"]': 'for row in live["holds"] + live["menus"]',
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::verified-checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
