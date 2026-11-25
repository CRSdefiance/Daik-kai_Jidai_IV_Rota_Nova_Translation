"""Clear verified redundant files after publishing the B221–240 candidate."""

from scripts import cleanup_rafael_B211_B220_20261122 as precedent
from scripts import register_rafael_B221_B240_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(precedent.source, {
    '"release_stack_with_rafael_B211_B220.json"': '"release_stack_with_rafael_B221_B240.json"',
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::verified-checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
