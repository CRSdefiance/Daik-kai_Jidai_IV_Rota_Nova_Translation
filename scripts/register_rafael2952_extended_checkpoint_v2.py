"""Bind the successful versioned preparation and successor spec."""
from scripts.register_rafael2952_extended_checkpoint_v1 import source as previous, PERCENT_PROOF
from scripts.source_locked_derivation_v5118 import checked_text


source=checked_text(previous,{
    'Rafael_B201_B220_registered_preparation_v1_20261106':'Rafael_B201_B220_registered_preparation_v2_20261106',
    'rafael_B201_B220_registered_successor_spec_v1.json':'rafael_B201_B220_registered_successor_spec_v2.json',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-qualified-v6-registration-with-exact-corrected-preparation','exec'),globals())

