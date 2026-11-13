"""Register the qualified five-block append over the exact verified 675-entry prefix."""
from pathlib import Path

from scripts.register_rafael1607_extended_checkpoint_v1 import source as previous, PERCENT_PROOF
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'Rafael1607_registered_extended_resume_v1_20261105': 'Rafael1674_registered_extended_resume_v1_20261105',
    'rafael1607_canonical_extension_resume_v1.json': 'rafael1674_canonical_extension_resume_v1.json',
    'Rafael_B177_B180_registered_preparation_v1_20261105': 'Rafael_B161_B165_registered_preparation_v2_20261105',
    'Rafael_B177_B180_release_qualification_v1_20261105': 'Rafael_B161_B165_release_qualification_v1_20261105',
    'all-routes-rafael1607-extended-checkpoint-v1-20261105': 'all-routes-rafael1674-extended-checkpoint-v1-20261105',
    'rafael_B177_B180_registered_successor_spec_v1.json': 'rafael_B161_B165_registered_successor_spec_v2.json',
    'expected_prefix_entries=674': 'expected_prefix_entries=675',
    'release_stack.Rafael1607_extended_resume_v1.pending.json': 'release_stack.Rafael1674_extended_resume_v1.pending.json',
    'Registered Rafael1607 profile: verified 674-entry prefix plus the 183-record source-bound append':
        'Registered Rafael1674 profile: verified 675-entry prefix plus the 67-record source-bound append',
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-v6-chain-next-exact-registered-prefix', 'exec'), globals())
