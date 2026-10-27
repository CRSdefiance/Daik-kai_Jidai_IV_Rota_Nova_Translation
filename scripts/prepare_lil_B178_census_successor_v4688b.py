"""Correct the remaining inherited thirteen-command guard;preserve the failed census."""
from scripts.prepare_lil_B156_layout_v3705 import derive

derive('scripts/verify_lil_B178_references_v4688.py','scripts/verify_lil_B178_references_v4688b.py',{
    'lil_B178_reference_census_v4688':'lil_B178_reference_census_v4688b',
    "sum(len(r['mapped_commands'])for r in result)==13":"sum(len(r['mapped_commands'])for r in result)==16",
    'native_commands_each=13':'native_commands_each=16',
})
print('Prepared sixteen-command census successor;no ROM or metadata changed.')
