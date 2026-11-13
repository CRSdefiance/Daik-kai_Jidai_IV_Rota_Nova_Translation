"""Own cold-boot proof with three exclusive fields and nine protected original getters."""
import inspect
import sys
from pathlib import Path
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from scripts import verify_registered_rafael_startup_v2 as previous
from scripts.audit_story_glyph_consistency import load,save
from scripts.build_registered_rafael5186_v1 import GETTERS,PARENT,STAGED,STARTUP,NAME_CONFIG,CLEAN
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prove_lil_B167_names_v4124b import names
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "    assert release['all_other_files_components_graphics_names_andruntime_exact_to_parent']":
        """    assert release['all_except_owned_middle_fields_exact_to_parent'] and release['both_components_whole_parent_inverse_exact']
    assert sha(NAME_CONFIG.read_bytes())==release['middle_fields_config_sha256']
    name_config=load(NAME_CONFIG)
    proposal=load(name_config['proposal'])""",
    "    unchanged=['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']":
        """    assert sha(Path(parent['candidate']).read_bytes())==parent['candidate_sha256']
    expected,ownership=plan_arm9_name_fields(parent_image.read_file('/__arm9__.bin'),proposal,
        NdsImage.open(CLEAN).read_file('/__arm9__.bin'))
    assert image.read_file('/__arm9__.bin')==expected and sha(expected)==release['target_ARM9_sha256']
    assert ownership['changed_bytes']==9 and ownership['complete_parent_inverse_exact']
    assert ownership['all_unowned_ARM9_bytes_sections_pointer_tables_andallocations_exact']
    unchanged=['/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']""",
    "    owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]":
        """    for field in proposal['fields']:
        start=field['pointer']-BASE
        physical=field['physical_offset']
        size=field['owned_bytes']+1
        assert raw[start:start+size]==arm[physical:physical+size]
        at=field['table_field_offset']
        assert raw[at:at+4]==arm[at:at+4]==field['pointer'].to_bytes(4,'little')
    owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]""",
    'ARM9_COMMON_HELP_font_equal_registered_runtime_parent=True':
        'COMMON_HELP_font_equal_registered_runtime_parent=True,only_nine_owned_middle_field_bytes_differ_in_ARM9=True',
})

def verify_getters():
    assert not GETTERS.exists()
    ctx=RegisteredRuntime(STAGED,STARTUP,captain=0)
    common={35:'Fernan Silveira',65:'Plett Perrault',68:'Jacob Portunto',70:'Zaganos Bey',186:'Francisca',203:'Sakura'}
    expected={actor:{consumer:text for consumer in ('progressive-nameplate','full-catalogue')} for actor,text in common.items()}
    for actor,short,full in [(30,'Dinis Albuquerque','Dinis de Albuquerque'),
            (40,'Antony Kuhn','Antony von Kuhn'),(59,'Garcia Oviedo','Garcia de Oviedo')]:
        expected[actor]={'progressive-nameplate':short,'full-catalogue':full}
    adapter=checked_text(inspect.getsource(names),{'for ident in [2,4,13,23,109]:':'for ident in ACTORS:'})
    env={**names.__globals__,'ACTORS':sorted(expected)}
    exec(compile(adapter,__file__+'::original-getters-own-startup','exec'),env)
    result=ctx.execute(env['names'])
    assert len(result['rows'])==18
    for actor,consumers in expected.items():
        rows=[row for row in result['rows'] if row['actor_ID']==actor]
        assert len(rows)==2 and {r['consumer'] for r in rows}==set(consumers)
        assert all(r['text']==consumers[r['consumer']] and r['text_hex']==r['text'].encode('ascii').hex() for r in rows)
    assert digest(PARENT)==load(STAGED)['predecessor_release_sha256']
    save(GETTERS,dict(runtime=ctx.receipt(),own_name_consumers=result,
        both_name_getters_exact_for_all9_protected_actors=True,expected=expected,original_adapter=adapter,
        full_catalogue_UI_unvisited=True,no_historical_RAM_overlay=True,new_credit=0))
    print('Both original getters returned all nine protected names from Rafael5186 own startup.')

if __name__=='__main__':
    if sys.argv[1:]==['--getters']:verify_getters()
    else:
        env={**vars(previous),**globals()}
        exec(compile(source,__file__+'::own-startup-and-exclusive-fields','exec'),env)
