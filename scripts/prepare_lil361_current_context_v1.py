"""Prepare the exact registered Lil269 ROM's ordinary-input captain2 context."""
from scripts.prepare_lil269_current_context_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'Lil269_B243_B282_clean_20261110': 'Lil361_B283_B298_clean_20261110',
    'lil382_residual_A_release_v1': 'lil269_B243_B282_release_v1',
    'sealed_269_clean_drafts': 'sealed_361_clean_drafts',
    'opening_not_new_269_optional_event_activation': 'opening_not_new_361_optional_event_activation',
    'onregistered Lil382': 'onregistered Lil269',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-own-ROM-ordinary-input-captain2-contract', 'exec'), globals())
