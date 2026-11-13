"""Register a qualified four-block append after the exact 674-entry canonical prefix."""
from pathlib import Path
from scripts.register_rafael1424_extended_checkpoint_v3 import source as previous, PERCENT_PROOF
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'Rafael1424_registered_extended_resume_v3_20261105':'Rafael1607_registered_extended_resume_v1_20261105',
    'rafael1424_canonical_extension_resume_v3.json':'rafael1607_canonical_extension_resume_v1.json',
    'Rafael557_registered_preparation_v1_20261105':'Rafael_B177_B180_registered_preparation_v1_20261105',
    'Rafael557_release_qualification_v1_20261105':'Rafael_B177_B180_release_qualification_v1_20261105',
    'all-routes-rafael1424-extended-checkpoint-v3-20261105':'all-routes-rafael1607-extended-checkpoint-v1-20261105',
    'rafael557_registered_successor_spec_v1.json':'rafael_B177_B180_registered_successor_spec_v1.json',
    "prepared_registry='work/analysis/Rafael1424_registered_extended_resume_v1_20261105/release_stack_before.json'":
        "prepared_registry=str(root/'release_stack_before.json')",
    'expected_prefix_entries=673':'expected_prefix_entries=674',
    'release_stack.Rafael1424_extended_resume_v3.pending.json':'release_stack.Rafael1607_extended_resume_v1.pending.json',
    'Registered Rafael1424 profile: verified 673-entry prefix plus the 557-record source-bound append':
        'Registered Rafael1607 profile: verified 674-entry prefix plus the 183-record source-bound append',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-v6-chain-next-exact-registered-prefix','exec'),globals())
