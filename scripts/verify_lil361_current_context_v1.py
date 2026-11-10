"""Verify own-ROM Lil context through unchanged snapshot and original-getter guards."""
from scripts.verify_lil269_current_context_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'Lil269_B243_B282_clean_20261110': 'Lil361_B283_B298_clean_20261110',
    'lil382_residual_A_release_v1': 'lil269_B243_B282_release_v1',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-own-ROM-snapshot-and-original-getter-contract', 'exec'), globals())
