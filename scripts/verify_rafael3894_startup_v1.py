"""Verify the candidate's own Rafael startup and the affected original name getters."""
import inspect
import sys

from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from scripts.audit_story_glyph_consistency import load, save
from scripts.build_registered_rafael3894_v1 import GETTERS, PARENT, QUALIFICATION, STAGED, STARTUP
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prove_lil_B167_names_v4124b import names
from scripts.qualify_rafael_zaganos_name_v1 import CLEAN
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_rafael3649_startup_v1 import source as previous
from scripts.verify_rafael3649_startup_v1 import verify_getters as previous_getters


source = checked_text(previous, {
    "release['all_nine_registered_final_stages_preserved']": "release['all_predecessor_stage_dependencies_preserved']",
    'expected, ownership=plan_surnames(': 'expected, ownership=plan_arm9_name_fields(',
    "ownership['all_unowned_bytes_exact']": "ownership['changed_bytes']==1",
    """    pointer_field=ownership['actor65_pointer_field']
    old_slot,old_end=ownership['old_surname_slot']
    jacob=ownership['fixed_jacob_proof']['fields'][0]
    jacob_start=jacob['physical_offset']
    jacob_end=jacob_start+jacob['owned_bytes']+1
    assert raw[pointer_field:pointer_field+4]==arm[pointer_field:pointer_field+4]
    assert raw[old_slot:old_end+8]==arm[old_slot:old_end+8]
    assert raw[jacob_start:jacob_end]==arm[jacob_start:jacob_end]""":
        """    field,=proposal['fields']
    start=field['physical_offset']
    pointer_field=field['table_field_offset']
    assert raw[start:start+4]==arm[start:start+4]==b'Bey\\0'
    assert raw[pointer_field:pointer_field+4]==arm[pointer_field:pointer_field+4]==field['pointer'].to_bytes(4,'little')""",
    'only_owned_Plett_Jacob_surnames_differ_in_ARM9=True': 'only_owned_Zaganos_surname_differs_in_ARM9=True',
})

getters_source = checked_text(inspect.getsource(previous_getters), {
    "68: 'Jacob Portunto', 186:": "68: 'Jacob Portunto', 70: 'Zaganos Bey', 186:",
    'both_name_getters_exact_for_actors_35_65_68_186_203':
        'both_name_getters_exact_for_actors_35_65_68_70_186_203',
    'all five expected names from Rafael3649': 'all six expected names from Rafael3894',
})


if __name__ == '__main__':
    if sys.argv[1:] == ['--getters']:
        exec(compile(getters_source, __file__ + '::own-original-name-getters', 'exec'), globals())
        verify_getters()
    else:
        exec(compile(source, __file__ + '::own-exact-Rafael-startup-and-Zaganos-field', 'exec'), globals())
