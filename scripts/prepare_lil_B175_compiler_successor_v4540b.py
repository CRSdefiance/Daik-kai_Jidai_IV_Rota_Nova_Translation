"""Close the proven relocated-reference metadata gap and preserve the failed producer."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B175_compiler_successor_v4540b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('translations/lil_B175_editorial_release_v1.json').exists()
    stable=read('work/analysis/lil_B175_reference_checkpoint_v4537/checkpoint_receipt.json')['preserved_release_files']
    for p in ['translations/release_stack.json','scripts/build_integrated_release.py','translations/promoted_build.json']:
        assert sha(Path(p).read_bytes())==stable[p]
    compiler=derive('dk4tool/patch/lil_B175_editorial_v1.py','dk4tool/patch/lil_B175_editorial_v2.py',{
        "    commands=spec['mapped_native_commands'];":
        """    for change in changes:
        ref=refs[change['id']];at=mapped(change['old_offset'])
        require(at==change['new_offset']==ref['new_offset'] and target[:at].count(b'\\0')==ref['new_record_index'],
            'relocated record offset/index differs:'+change['id'])
    commands=spec['mapped_native_commands'];""",
    })
    registration=derive('scripts/register_lil_B175_v4540.py','scripts/register_lil_B175_v4540b.py',{
        'lil_B175_editorial_v1':'lil_B175_editorial_v2',
        'lil_B175_registration_v4540':'lil_B175_registration_v4540b',
        'build_integrated_release_v4540.tmp':'build_integrated_release_v4540b.tmp',
        "        ('wrong-parity','reference_map'":
            "        ('wrong-stored-index','reference_map',lambda v:v['blocks'][0]['text_records'][0].update(new_record_index=1)),\n        ('wrong-parity','reference_map'",
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'failed_atomic_reference_guard_and_successor.json',dict(
        failed_producer='scripts/register_lil_B175_v4540.py',failed_case='wrong-stored-offset',
        failure='Original compiler accepted a changed reported new_offset although final ROM bytes remained the approved bytes. Exact ledger/runtime reference provenance requires rejection.',
        no_release_config_registry_builder_or_main_ROM_mutation=True,original_compiler_and_failed_producer_preserved=True,
        compiler_successor=compiler,registration_successor=registration,added_runtime_derived_offset_and_NUL_record_index_guards=True,
        new_gameplay_runs=0,full_goal_complete=False))
    print('Prepared B175 compiler v2 with reconstructed offset/index validation and both metadata negatives;earlier failure preserved.')
