"""Register the complete V1316 stack plus sixteen reviewed sinking reports."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import ship_sinking_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_sinking_release_v1343')
PROFILE = 'all-routes-unified-v1344'


def main():
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript = Path('translations/ship_sinking_editorial_manuscript_v4.json')
    doc = read(manuscript)
    rom = NdsImage.open('out/all_routes_combined_v1316_candidate.nds')
    c,a,proof = owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    registry_path,builder = Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before = registry_path.read_bytes(),builder.read_bytes()
    registry = read(registry_path)
    assert len(registry['accepted_layers'])==114 and PROFILE not in registry['profiles']
    assert b"profile_config.get('ship_sinking_editorial')" not in before
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor)==1
    lo = before.index(b"    powder_fire_editorial = profile_config.get('powder_fire_editorial')")
    hi = before.index(anchor)
    block = before[lo:hi].replace(b'powder_fire_editorial',b'ship_sinking_editorial').replace(
        b'POWDER_FIRE_NATIVE_SELECTION_METADATA',b'SHIP_SINKING_NATIVE_SELECTION_METADATA').replace(
        b'POWDER_FIRE_TABLE_SAME_OWNED188_GATE_CODE_UNCHANGED',b'SHIP_SINKING_TABLE_SAME_OWNED188_GATE_CODE_UNCHANGED')
    after = before[:hi]+block+before[hi:]
    assert after.replace(block,b'',1)==before
    compile(after,str(builder),'exec')
    scope = Path('work/analysis/ship_sinking_runtime_v1329/scope_proof.json')
    runtime = Path('work/analysis/ship_sinking_runtime_v1329/runtime_plan.json')
    files = {str(manuscript),'dk4tool/patch/ship_sinking_editorial.py','dk4tool/patch/powder_fire_editorial.py',
        'translations/powder_fire_editorial_release_v1.json','scripts/battle_aftermath_runtime_v1253.py',
        'scripts/powder_fire_runtime_v1307.py','scripts/probe_battle_aftermath_fonts_v1256.py',
        'scripts/verify_duel_cache_copies_v1163.py','scripts/verify_battle_aftermath_escape_v1262.py',
        'scripts/verify_ship_name_bound_v1335.py','scripts/verify_ship_name_bound_v1335b.py',
        'dk4tool/patch/name_editor_atomic_append.py',str(scope),str(runtime),
        'work/analysis/ship_sinking_runtime_v1329/native_runtime_verification.json',
        'work/analysis/ship_sinking_payload_v1337/native_payload_plan.json',
        'work/analysis/ship_name_bound_v1335b/original_ship_rename_capacity.json'}
    files.update(str(p) for p in Path('scripts').glob('*ship_sinking*.py'))
    files.update(str(p) for p in Path('translations').glob('ship_sinking_editorial_manuscript_v*.json'))
    for key in ['source_context','native_font_proof','native_copy_proof','escape_regression_proof','visual_review']:
        files.add(doc[key])
    fonts = read(doc['native_font_proof'])
    files.update(case['preview'] for case in fonts['cases'] if case['preview'])
    files.update(sheet['path'] for sheet in fonts['sheets_for_required_visual_review'])
    config = {'format':'dk4-ship-sinking-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,
        'source_arm9_sha256':owned.SOURCE_ARM,'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),
        'directory_sha256':proof['directory_sha256'],'manuscript':str(manuscript),
        'native_scope':str(scope),'runtime_plan':str(runtime),
        'dependencies':{path:sha(Path(path).read_bytes()) for path in sorted(files)}}
    ROOT.mkdir(parents=True)
    save(owned.CONFIG,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2]==(c,a)
    (ROOT/'target_COMMON.bin').write_bytes(c)
    (ROOT/'target_ARM9.bin').write_bytes(a)
    save(ROOT/'repack_plan.json',proof)
    (ROOT/'registry_before_raw.json').write_bytes(raw)
    (ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before
    profile = deepcopy(registry['profiles']['all-routes-unified-v1316'])
    profile.update(ship_sinking_editorial=owned.CONFIG,status='experimental',
        description='Complete V1316 stack plus sixteen source/native-reviewed ship-sinking reports.',
        note='Eight revisions,eight retained wordings;529312 selector/ABI cases,416 full native fonts,412 source voice selections,7336 copies180 cache sequences13 escape regressions. Two exact memberships fill188-byte table;code/sections/cache/123040 staged bytes unchanged. Exact patch,startup and original sinking scenes pending;canonical unchanged.')
    registry['profiles'][PROFILE] = profile
    builder.write_bytes(after)
    save(registry_path,registry)
    restored = deepcopy(read(registry_path))
    restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json')
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1316',
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'optional_stage_removal_restores_prior_builder_exact':True,'registry_before_sha256':sha(raw),
        'registry_after_sha256':sha(registry_path.read_bytes()),'all_prior_profiles_accepted_layers_and_batches_preserved':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'build_patch_startup_original_scene_and_completion_pending':True,'full_goal_complete':False})
    print('V1344 full experimental profile registered after V1316;build and original sinking gameplay remain pending.',flush=True)


if __name__=='__main__':
    main()
