"""Register the exact 679-entry prefix and twenty-block append."""
from scripts.register_rafael2165_extended_checkpoint_v1 import source as earlier, PERCENT_PROOF
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(earlier, {
    'Rafael2165_registered_extended_resume_v1_20261105': 'Rafael2549_registered_extended_resume_v1_20261106',
    'rafael2165_canonical_extension_resume_v1.json': 'rafael2549_canonical_extension_resume_v1.json',
    'Rafael_B170_B176_registered_preparation_v1_20261105': 'Rafael_B181_B200_registered_preparation_v1_20261106',
    'Rafael_B170_B176_release_qualification_v1_20261105': 'Rafael_B181_B200_release_qualification_v1_20261106',
    'all-routes-rafael2165-extended-checkpoint-v1-20261105': 'all-routes-rafael2549-extended-checkpoint-v1-20261106',
    'rafael_B170_B176_registered_successor_spec_v1.json': 'rafael_B181_B200_registered_successor_spec_v1.json',
    'expected_prefix_entries=678': 'expected_prefix_entries=679',
    'release_stack.Rafael2165_extended_resume_v1.pending.json': 'release_stack.Rafael2549_extended_resume_v1.pending.json',
    'Registered Rafael2165 profile: verified 678-entry prefix plus the 190-record source-bound append':
        'Registered Rafael2549 profile: verified 679-entry prefix plus the 384-record source-bound append',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::qualified-v6-registration-twenty-blocks', 'exec'), globals())
