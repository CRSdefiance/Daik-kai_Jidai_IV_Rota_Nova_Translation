"""Register the exact Rafael3222 prefix and the verified 292-record SC0 append."""
from scripts.register_rafael3222_extended_checkpoint_v1 import PERCENT_PROOF, source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'work/analysis/Rafael3222_registered_extended_resume_v1_20261106': 'work/Rafael3514_dialogue_registered_resume_v1_20261106',
    'rafael3222_canonical_extension_resume_v1.json': 'rafael3514_dialogue_canonical_extension_resume_v1.json',
    'work/analysis/Rafael_B221_B240_registered_preparation_v1_20261106': 'work/Rafael_B241_B260_registered_preparation_v1_20261106',
    'work/analysis/Rafael_B221_B240_release_qualification_v1_20261106': 'work/Rafael_B241_B260_release_qualification_v1_20261106',
    'all-routes-rafael3222-extended-checkpoint-v1-20261106': 'all-routes-rafael3514-dialogue-extended-v1-20261106',
    'rafael_B221_B240_registered_successor_spec_v1.json': 'rafael_B241_B260_registered_successor_spec_v1.json',
    'expected_prefix_entries=681': 'expected_prefix_entries=682',
    'release_stack.Rafael3222_extended_resume_v1.pending.json': 'release_stack.Rafael3514_dialogue_resume_v1.pending.json',
    'Registered Rafael3222 profile: verified 681-entry prefix plus the 270-record source-bound append':
        'Registered Rafael3514 dialogue stage: verified 682-entry prefix plus the 292-record source-bound append',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::qualified-v6-dialogue-only-checkpoint', 'exec'), globals())
