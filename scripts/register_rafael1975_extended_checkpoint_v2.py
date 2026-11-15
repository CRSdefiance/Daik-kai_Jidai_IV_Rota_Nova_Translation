"""Use the qualified FU-capable preparation after the preserved schema failure."""
from scripts.register_rafael1975_extended_checkpoint_v1 import source as previous, PERCENT_PROOF
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'Rafael_B168_B169_registered_preparation_v1_20261105': 'Rafael_B168_B169_registered_preparation_v2_20261105',
    'rafael_B168_B169_registered_successor_spec_v1.json': 'rafael_B168_B169_registered_successor_spec_v2.json',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-v6-chain-qualified-preparation-v2', 'exec'), globals())
