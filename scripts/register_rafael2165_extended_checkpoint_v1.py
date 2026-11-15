"""Register the exact 678-entry prefix and next seven-block append."""
from scripts.register_rafael1975_extended_checkpoint_v1 import source as previous, PERCENT_PROOF
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'Rafael1975_registered_extended_resume_v1_20261105': 'Rafael2165_registered_extended_resume_v1_20261105',
    'rafael1975_canonical_extension_resume_v1.json': 'rafael2165_canonical_extension_resume_v1.json',
    'Rafael_B168_B169_registered_preparation_v1_20261105': 'Rafael_B170_B176_registered_preparation_v1_20261105',
    'Rafael_B168_B169_release_qualification_v1_20261105': 'Rafael_B170_B176_release_qualification_v1_20261105',
    'all-routes-rafael1975-extended-checkpoint-v1-20261105': 'all-routes-rafael2165-extended-checkpoint-v1-20261105',
    'rafael_B168_B169_registered_successor_spec_v1.json': 'rafael_B170_B176_registered_successor_spec_v1.json',
    'expected_prefix_entries=677': 'expected_prefix_entries=678',
    'release_stack.Rafael1975_extended_resume_v1.pending.json': 'release_stack.Rafael2165_extended_resume_v1.pending.json',
    'Registered Rafael1975 profile: verified 677-entry prefix plus the 115-record source-bound append':
        'Registered Rafael2165 profile: verified 678-entry prefix plus the 190-record source-bound append',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::qualified-v6-registration-seven-blocks', 'exec'), globals())
