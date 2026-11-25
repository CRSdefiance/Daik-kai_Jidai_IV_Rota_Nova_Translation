"""Qualify exact reviewed opening RGB on the planned539 image without preapproving release."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/qualify_rafael_B51_B60_identity_startup.py').read_text(encoding='utf-8'),{
    'Rafael_B51_B60_identity_coldboot_20261104':'Rafael_B61_B80_identity_coldboot_20261104',
    'Shared_tutorial_name_data_release_verified_20261104':'Rafael_B51_B60_release_verified_20261104',
    'Rafael_B51_B60_focused_20261104/composition.json':'Rafael_B61_B80_rebuilt_v12_20261104/reconstruction.json',
    "assert [p for p,v in previous.iter_components() if current.read_file(p)!=v]==['/__arm9__.bin']":
        "assert [p for p,v in previous.iter_components() if current.read_file(p)!=v]==[]",
    '==list(range(51,61))':'==[n for n in range(61,81) if n!=68]',
    "    plan=composition['name_plan'];inverse=bytearray(current.read_file('/__arm9__.bin'))\n    for field in plan['fields']:\n        at,n=field['physical_offset'],field['owned_bytes']\n        assert inverse[at:at+n].hex()==field['new_hex'];inverse[at:at+n]=bytes.fromhex(field['old_hex'])\n    assert bytes(inverse)==previous.read_file('/__arm9__.bin')":
        "    assert current.read_file('/__arm9__.bin')==previous.read_file('/__arm9__.bin')",
    'only_ten_later_scene_blocks_andexclusive_Fernan_field_differ=True':'only_nineteen_reviewed_scene_blocks_differ_all_ARM9_andnames_exact=True',
    'only ten later scenes/Fernan field differ':'only nineteen reviewed scenes differ;all ARM9/name bytes exact',
})
exec(compile(source,__file__+'::same-ten-RGB-pairs-all-code-names-andopening-exact','exec'),globals())
