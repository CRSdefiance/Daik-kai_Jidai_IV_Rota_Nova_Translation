"""Clear verified redundant files after publishing the B261–280 candidate."""

from scripts import cleanup_rafael_B221_B240_20261122 as precedent
from scripts import register_rafael_B261_B280_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(precedent.source, {
    '"release_stack_with_rafael_B221_B240.json"': '"release_stack_with_rafael_B261_B280.json"',
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::verified-checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
