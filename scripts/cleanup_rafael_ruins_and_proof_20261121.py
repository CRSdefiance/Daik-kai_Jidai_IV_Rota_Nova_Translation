"""Clear redundant ruin checkpoint files after the published candidate is read back."""

from scripts import cleanup_rafael_followup_encounters_20261121 as prior
from scripts import register_rafael_ruins_and_proof_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(prior.source, {
    '"release_stack_with_rafael_followup_encounters.json"': '"release_stack_with_rafael_ruins_and_proof.json"',
})
scope = prior.scope | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
