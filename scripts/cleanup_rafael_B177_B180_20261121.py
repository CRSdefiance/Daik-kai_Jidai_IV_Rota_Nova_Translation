"""Apply the established hash-checked cleanup to the registered tutorial batch."""

from scripts import cleanup_rafael_B161_B169_20261121 as precedent
from scripts import register_rafael_B177_B180_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(precedent.source, {
    '"release_stack_with_rafael_B161_B169.json"': '"release_stack_with_rafael_B177_B180.json"',
    'row["observed"] for row in live["holds"]': 'row["observed"] for row in live["holds"] + live["menus"]',
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::registered-checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
