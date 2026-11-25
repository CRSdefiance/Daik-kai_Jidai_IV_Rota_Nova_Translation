"""Register the full V1266 stack plus six native-reviewed powder-fire alerts."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import powder_fire_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/powder_fire_release_v1315')
PROFILE = 'all-routes-unified-v1316'


def main():
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript = Path('translations/powder_fire_editorial_manuscript_v2.json')
    doc = read(manuscript)
    rom = NdsImage.open('out/all_routes_combined_v1266_candidate.nds')
    c,a,proof = owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    registry_path,builder = Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before = registry_path.read_bytes(),builder.read_bytes()
    registry = read(registry_path)
    assert PROFILE not in registry['profiles'] and b"profile_config.get('powder_fire_editorial')" not in before
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor) == 1
    lo = before.index(b"    battle_aftermath_editorial = profile_config.get('battle_aftermath_editorial')")
    hi = before.index(anchor)
    block = before[lo:hi].replace(b'battle_aftermath_editorial',b'powder_fire_editorial').replace(
        b'BATTLE_AFTERMATH_NATIVE_SELECTION_METADATA',b'POWDER_FIRE_NATIVE_SELECTION_METADATA').replace(
        b'BATTLE_AFTERMATH_SELECTOR_SAME_OWNED188_AND172',b'POWDER_FIRE_TABLE_SAME_OWNED188_GATE_CODE_UNCHANGED')
    after = before[:hi]+block+before[hi:]
    assert after.replace(block,b'',1) == before
    compile(after,str(builder),'exec')
    scope_path = Path('work/analysis/powder_fire_runtime_v1308/scope_proof.json')
    runtime_path = Path('work/analysis/powder_fire_runtime_v1308/runtime_plan.json')
    files = {str(manuscript),'translations/powder_fire_editorial_manuscript_v1.json',
        'dk4tool/patch/powder_fire_editorial.py','dk4tool/patch/battle_aftermath_editorial.py',
        'translations/battle_aftermath_editorial_release_v1.json','scripts/battle_aftermath_runtime_v1253.py',
        'scripts/probe_battle_aftermath_fonts_v1256.py','scripts/verify_duel_cache_copies_v1163.py',
        'scripts/verify_battle_aftermath_escape_v1262.py',str(scope_path),str(runtime_path),
        'work/analysis/powder_fire_runtime_v1308/native_runtime_verification.json',
        'work/analysis/powder_fire_payload_v1309/native_payload_plan.json'}
    files.update(str(path) for path in Path('scripts').glob('*powder_fire*.py'))
    for key in ['source_context','native_font_proof','native_copy_proof','escape_regression_proof','visual_review']:
        files.add(doc[key])
    fonts = read(doc['native_font_proof'])
    files.update(case['preview'] for case in fonts['cases'])
    files.add(fonts['review_sheet'])
    config = {'format':'dk4-powder-fire-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,
        'source_arm9_sha256':owned.SOURCE_ARM,'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),
        'directory_sha256':proof['directory_sha256'],'manuscript':str(manuscript),
        'native_scope':str(scope_path),'runtime_plan':str(runtime_path),
        'dependencies':{path:sha(Path(path).read_bytes()) for path in sorted(files)}}
    ROOT.mkdir(parents=True)
    save(owned.CONFIG,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2] == (c,a)
    (ROOT/'target_COMMON.bin').write_bytes(c)
    (ROOT/'target_ARM9.bin').write_bytes(a)
    save(ROOT/'repack_plan.json',proof)
    (ROOT/'registry_before_raw.json').write_bytes(raw)
    (ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    assert registry_path.read_bytes() == raw and builder.read_bytes() == before
    profile = deepcopy(registry['profiles']['all-routes-unified-v1266'])
    profile.update(powder_fire_editorial=owned.CONFIG,status='experimental',
        description='Complete V1266 stack plus six source/native-reviewed gun-battery powder-fire alerts.',
        note='Six revisions;529286 selector/ABI cases,8 complete voice/font pipelines,206 source selections,7336 copies180 cache sequences13 escape regressions. One table membership only:186 bytes in188 allocation;code and123040 staged bytes unchanged. Exact patch,startup and revised gameplay pending;canonical unchanged.')
    registry['profiles'][PROFILE] = profile
    builder.write_bytes(after)
    save(registry_path,registry)
    restored = deepcopy(read(registry_path))
    restored['profiles'].pop(PROFILE)
    assert restored == read(ROOT/'registry_before_raw.json')
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1266',
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'optional_stage_removal_restores_prior_builder_exact':True,'registry_before_sha256':sha(raw),
        'registry_after_sha256':sha(registry_path.read_bytes()),'all_prior_profiles_accepted_layers_and_batches_preserved':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'build_patch_startup_revised_scene_and_completion_pending':True,'full_goal_complete':False})
    print('V1316 full experimental profile registered after V1266;build and revised gameplay remain pending.',flush=True)


if __name__ == '__main__':
    main()
