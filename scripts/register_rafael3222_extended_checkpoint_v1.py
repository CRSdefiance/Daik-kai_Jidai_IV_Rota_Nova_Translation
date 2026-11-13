"""Register the exact Rafael2952 canonical prefix and verified 270-record append."""
from scripts.register_rafael2952_extended_checkpoint_v2 import source as previous, PERCENT_PROOF
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'Rafael2952_registered_extended_resume_v1_20261106': 'Rafael3222_registered_extended_resume_v1_20261106',
    'rafael2952_canonical_extension_resume_v1.json': 'rafael3222_canonical_extension_resume_v1.json',
    'Rafael_B201_B220_registered_preparation_v2_20261106': 'Rafael_B221_B240_registered_preparation_v1_20261106',
    'Rafael_B201_B220_release_qualification_v1_20261106': 'Rafael_B221_B240_release_qualification_v1_20261106',
    'all-routes-rafael2952-extended-checkpoint-v1-20261106': 'all-routes-rafael3222-extended-checkpoint-v1-20261106',
    'rafael_B201_B220_registered_successor_spec_v2.json': 'rafael_B221_B240_registered_successor_spec_v1.json',
    'expected_prefix_entries=680': 'expected_prefix_entries=681',
    'release_stack.Rafael2952_extended_resume_v1.pending.json': 'release_stack.Rafael3222_extended_resume_v1.pending.json',
    'Registered Rafael2952 profile: verified 680-entry prefix plus the 403-record source-bound append':
        'Registered Rafael3222 profile: verified 681-entry prefix plus the 270-record source-bound append',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-v6-registration-for-the-mixed-270-record-append', 'exec'), globals())

