"""Remove verified duplicate files after publishing the Yifa and Aziza candidate."""

from scripts import cleanup_rafael_B170_B176_20261121 as precedent
from scripts import register_rafael_B181_B187_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(precedent.source, {
    '("release_stack_with_rafael_B170_B176.json", "registry_after")':
        '("release_stack_with_rafael_B181_B187.json", "registry_after")',
    '    for version in ("staged_B170_B176", "staged_B170_B176_v2"):':
        '    for version in ("staged_B181_B187",):',
    '    for capture in captures:\n        report = base.load(capture / "capture_report.json")':
        '    for capture in captures:\n        report_path = capture / "capture_report.json"\n'
        '        if not report_path.is_file():\n'
        '            continue\n'
        '        report = base.load(report_path)',
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::verified-checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
