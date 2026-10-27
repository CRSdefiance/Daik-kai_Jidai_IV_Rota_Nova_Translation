"""Correct a pre-generation replacement key; preserve the failed preparer."""
from scripts.prepare_lil_B156_layout_v3705 import derive

derive('scripts/prepare_lil_B177_registration_v4654.py','scripts/prepare_lil_B177_registration_v4654b.py',{
    '"\'source_A0008_C200384_single_end386_actually_executed\'":"\'source_A0008_C200480_single_end482_actually_executed\'"':
        '"source_A0008_C200384_single_end386_actually_executed":"source_A0008_C200480_single_end482_actually_executed"',
})
print('Corrected keyword replacement key before registration tool generation;no metadata changed.')
