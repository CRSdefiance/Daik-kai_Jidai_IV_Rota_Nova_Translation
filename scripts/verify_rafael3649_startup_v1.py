"""Verify the candidate's own Rafael cold boot and all affected name getters."""
import inspect
from pathlib import Path
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.build_registered_rafael3649_v1 import GETTERS, PARENT, QUALIFICATION, STAGED, STARTUP
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prove_lil_B167_names_v4124b import names
from scripts.qualify_rafael_plett_relocation_v1 import CLEAN, plan_surnames
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_registered_rafael_startup_v2 import source as previous


source = checked_text(previous, {
    "    assert release['all_other_files_components_graphics_names_andruntime_exact_to_parent']":
        """    assert release['all_nine_registered_final_stages_preserved'] and release['both_components_whole_parent_inverse_exact']
    assert release['qualification_sha256']==sha(QUALIFICATION.read_bytes())
    qualification=load(QUALIFICATION)
    name_path=Path(qualification['name_proposal'])
    assert sha(name_path.read_bytes())==qualification['name_proposal_sha256']
    proposal=load(name_path)""",
    "    unchanged=['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']":
        """    assert sha(Path(parent['candidate']).read_bytes())==parent['candidate_sha256']
    expected, ownership=plan_surnames(parent_image.read_file('/__arm9__.bin'),proposal,
        NdsImage.open(CLEAN).read_file('/__arm9__.bin'))
    assert image.read_file('/__arm9__.bin')==expected and sha(expected)==release['target_ARM9_sha256']
    assert ownership['all_unowned_bytes_exact'] and ownership['complete_parent_inverse_exact']
    unchanged=['/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']""",
    "    owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]":
        """    pointer_field=ownership['actor65_pointer_field']
    old_slot,old_end=ownership['old_surname_slot']
    jacob=ownership['fixed_jacob_proof']['fields'][0]
    jacob_start=jacob['physical_offset']
    jacob_end=jacob_start+jacob['owned_bytes']+1
    assert raw[pointer_field:pointer_field+4]==arm[pointer_field:pointer_field+4]
    assert raw[old_slot:old_end+8]==arm[old_slot:old_end+8]
    assert raw[jacob_start:jacob_end]==arm[jacob_start:jacob_end]
    owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]""",
    'ARM9_COMMON_HELP_font_equal_registered_runtime_parent=True':
        'COMMON_HELP_font_equal_registered_runtime_parent=True,only_owned_Plett_Jacob_surnames_differ_in_ARM9=True',
})


def verify_getters():
    assert not GETTERS.exists()
    ctx = RegisteredRuntime(STAGED, STARTUP, captain=0)
    expected = {35: 'Fernan Silveira', 65: 'Plett Perrault', 68: 'Jacob Portunto', 186: 'Francisca', 203: 'Sakura'}
    adapter = checked_text(inspect.getsource(names), {'for ident in [2,4,13,23,109]:': 'for ident in ACTORS:'})
    env = {**names.__globals__, 'ACTORS': sorted(expected)}
    exec(compile(adapter, __file__ + '::original-getters-own-registered-target-memory', 'exec'), env)
    result = ctx.execute(env['names'])
    assert len(result['rows']) == 2 * len(expected)
    for actor, text in expected.items():
        rows = [row for row in result['rows'] if row['actor_ID'] == actor]
        assert {row['consumer'] for row in rows} == {'progressive-nameplate', 'full-catalogue'}
        assert all(row['text'] == text and row['text_hex'] == text.encode('ascii').hex() for row in rows)
    assert digest(PARENT) == load(STAGED)['predecessor_release_sha256']
    save(GETTERS, dict(runtime=ctx.receipt(), own_name_consumers=result,
        both_name_getters_exact_for_actors_35_65_68_186_203=True, original_adapter=adapter,
        full_catalogue_UI_unvisited=True, no_historical_RAM_overlay=True, new_credit=0))
    print('Both getters returned all five expected names from Rafael3649’s own startup.')


if __name__ == '__main__':
    if sys.argv[1:] == ['--getters']:
        verify_getters()
    else:
        exec(compile(source, __file__ + '::same-exact-Rafael-startup-with-protected-surnames', 'exec'), globals())
