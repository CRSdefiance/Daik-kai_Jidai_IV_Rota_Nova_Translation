"""Register the v6 chain over the exact verified 677-entry prefix."""
from scripts.register_rafael1860_extended_checkpoint_v1 import source as previous, PERCENT_PROOF
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'Rafael1860_registered_extended_resume_v1_20261105': 'Rafael1975_registered_extended_resume_v1_20261105',
    'rafael1860_canonical_extension_resume_v1.json': 'rafael1975_canonical_extension_resume_v1.json',
    'Rafael_B166_B167_registered_preparation_v1_20261105': 'Rafael_B168_B169_registered_preparation_v1_20261105',
    'Rafael_B166_B167_release_qualification_v1_20261105': 'Rafael_B168_B169_release_qualification_v1_20261105',
    'all-routes-rafael1860-extended-checkpoint-v1-20261105': 'all-routes-rafael1975-extended-checkpoint-v1-20261105',
    'rafael_B166_B167_registered_successor_spec_v1.json': 'rafael_B168_B169_registered_successor_spec_v1.json',
    'expected_prefix_entries=676': 'expected_prefix_entries=677',
    'release_stack.Rafael1860_extended_resume_v1.pending.json': 'release_stack.Rafael1975_extended_resume_v1.pending.json',
    'Registered Rafael1860 profile: verified 676-entry prefix plus the 186-record source-bound append':
        'Registered Rafael1975 profile: verified 677-entry prefix plus the 115-record source-bound append',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-qualified-v6-registration', 'exec'), globals())
