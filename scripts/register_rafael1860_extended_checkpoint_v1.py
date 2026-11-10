"""Register the v6 chain over the verified 676-entry prefix."""
from scripts.register_rafael1674_extended_checkpoint_v1 import source as previous,PERCENT_PROOF
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'Rafael1674_registered_extended_resume_v1_20261105':'Rafael1860_registered_extended_resume_v1_20261105',
    'rafael1674_canonical_extension_resume_v1.json':'rafael1860_canonical_extension_resume_v1.json',
    'Rafael_B161_B165_registered_preparation_v2_20261105':'Rafael_B166_B167_registered_preparation_v1_20261105',
    'Rafael_B161_B165_release_qualification_v1_20261105':'Rafael_B166_B167_release_qualification_v1_20261105',
    'all-routes-rafael1674-extended-checkpoint-v1-20261105':'all-routes-rafael1860-extended-checkpoint-v1-20261105',
    'rafael_B161_B165_registered_successor_spec_v2.json':'rafael_B166_B167_registered_successor_spec_v1.json',
    'expected_prefix_entries=675':'expected_prefix_entries=676',
    'release_stack.Rafael1674_extended_resume_v1.pending.json':'release_stack.Rafael1860_extended_resume_v1.pending.json',
    'Registered Rafael1674 profile: verified 675-entry prefix plus the 67-record source-bound append':
        'Registered Rafael1860 profile: verified 676-entry prefix plus the 186-record source-bound append',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-qualified-v6-registration','exec'),globals())
