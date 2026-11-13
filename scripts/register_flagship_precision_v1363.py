"""Register the complete V1344 stack plus the source-reviewed2015 correction."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import flagship_capture_precision as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/flagship_precision_release_v1363')
PROFILE = 'all-routes-unified-v1364'


def main():
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript = Path('translations/flagship_capture_precision_manuscript_v2.json')
    doc = read(manuscript)
    rom = NdsImage.open('out/all_routes_combined_v1344_candidate.nds')
    c,a,proof = owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    registry_path,builder = Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before = registry_path.read_bytes(),builder.read_bytes()
    registry = read(registry_path)
    assert len(registry['accepted_layers'])==114 and PROFILE not in registry['profiles']
    assert b"profile_config.get('flagship_capture_precision')" not in before
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor)==1
    lo = before.index(b"    ship_sinking_editorial = profile_config.get('ship_sinking_editorial')")
    hi = before.index(anchor)
    block = before[lo:hi].replace(b'ship_sinking_editorial',b'flagship_capture_precision').replace(
        b'SHIP_SINKING_NATIVE_SELECTION_METADATA',b'FLAGSHIP_CAPTURE_PRECISION_NATIVE_SELECTION_METADATA').replace(
        b'SHIP_SINKING_TABLE_SAME_OWNED188_GATE_CODE_UNCHANGED',b'FLAGSHIP_CAPTURE_PRECISION_ENTIRE_RUNTIME_UNCHANGED')
    after = before[:hi]+block+before[hi:]
    assert after.replace(block,b'',1)==before
    compile(after,str(builder),'exec')
    files = {str(manuscript),'translations/flagship_capture_precision_manuscript_v1.json',
        'translations/battle_aftermath_editorial_manuscript_v3.json',
        'dk4tool/patch/flagship_capture_precision.py','dk4tool/patch/ship_sinking_editorial.py',
        'translations/ship_sinking_editorial_release_v1.json','scripts/ship_sinking_native_plan_v1330.py',
        'scripts/ship_sinking_runtime_v1328.py','scripts/battle_aftermath_layout_v1250.py',
        'scripts/probe_battle_aftermath_fonts_v1256.py','scripts/verify_duel_cache_copies_v1163.py',
        'scripts/verify_battle_aftermath_escape_v1262.py',
        'work/analysis/flagship_capture_verified_v1354b/actual_flagship_capture_verification.json',
        'work/analysis/flagship_precision_payload_v1356/native_payload_plan.json'}
    files.update(str(p) for p in Path('scripts').glob('*flagship_precision*.py'))
    for key in ['native_font_proof','native_copy_proof','escape_regression_proof','visual_review']:
        files.add(doc[key])
    fonts = read(doc['native_font_proof'])
    files.update(case['preview'] for case in fonts['cases'])
    files.add(fonts['review_sheet'])
    config = {'format':'dk4-flagship-capture-precision-v1','source_common_sha256':owned.SOURCE_COMMON,
        'source_arm9_sha256':owned.SOURCE_ARM,'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),
        'directory_sha256':proof['directory_sha256'],'manuscript':str(manuscript),
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
    profile = deepcopy(registry['profiles']['all-routes-unified-v1344'])
    profile.update(flagship_capture_precision=owned.CONFIG,status='experimental',
        description='Complete V1344 stack plus one source/native-reviewed flagship-crew precision correction.',
        note='Only2015 prose changes;all other3667 messages and every runtime/selector/code byte preserved.8 voice/five-text native font pipelines,206 existing voice choices,7336 copies180 sequences13 escape regressions pass. Sections/cache/123040 staged bytes unchanged. Exact patch/startup and new-ROM original capture replay pending;canonical unchanged.')
    registry['profiles'][PROFILE] = profile
    builder.write_bytes(after)
    save(registry_path,registry)
    restored = deepcopy(read(registry_path))
    restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json')
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1344',
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'optional_stage_removal_restores_prior_builder_exact':True,'registry_before_sha256':sha(raw),
        'registry_after_sha256':sha(registry_path.read_bytes()),'all_prior_profiles_accepted_layers_and_batches_preserved':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'build_patch_startup_replay_and_completion_pending':True,'full_goal_complete':False})
    print('V1364 full experimental profile registered;only2015 prose changes. Build/replay pending.',flush=True)


if __name__=='__main__':
    main()
