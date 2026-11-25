"""Remove superseded capture and release scratch after the Drive readback."""

from scripts import cleanup_rafael_B161_B169_20261121 as precedent
from scripts import register_rafael_B170_B176_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(precedent.source, {
    '"release_stack_with_rafael_B161_B169.json"': '"release_stack_with_rafael_B170_B176.json"',
    '    for capture in (release.live.REPORT.parent, release.STARTUP_CAPTURE.parent):':
        '''    captures = [release.live.REPORT.parent, release.STARTUP_CAPTURE.parent]
    for version in ("staged_B170_B176", "staged_B170_B176_v2"):
        checked = stage.ROOT.with_name(version)
        captures.extend(checked / area / "capture" for area in ("focused_gameplay", "startup"))
    for capture in captures:''',
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::verified-checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
