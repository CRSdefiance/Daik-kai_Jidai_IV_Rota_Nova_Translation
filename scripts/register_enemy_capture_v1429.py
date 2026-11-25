"""Register the complete V1404 stack plus eight capture reports and exact caller fix."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import enemy_capture_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/enemy_capture_release_v1429')
PROFILE = 'all-routes-unified-v1430'

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript = Path('translations/enemy_capture_editorial_manuscript_v3.json')
    doc = read(manuscript)
    rom = NdsImage.open('out/all_routes_combined_v1404_candidate.nds')
    assert sha(Path('out/all_routes_combined_v1404_candidate.nds').read_bytes())=='68cd0dd412ea00a294775c44069a6d7e1b8a29c65530aeefea371a01226b5a0e'
    c,a,proof = owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    registry_path,builder = Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before = registry_path.read_bytes(),builder.read_bytes()
    registry = read(registry_path)
    assert len(registry['accepted_layers'])==114 and PROFILE not in registry['profiles']
    assert b"profile_config.get('enemy_capture_editorial')" not in before
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor)==1
    lo = before.index(b"    battle_victory_editorial = profile_config.get('battle_victory_editorial')")
    hi = before.index(anchor)
    block = before[lo:hi].replace(b'battle_victory_editorial',b'enemy_capture_editorial').replace(
        b'BATTLE_VICTORY_NATIVE_SELECTION_METADATA',b'ENEMY_CAPTURE_NATIVE_SELECTION_METADATA').replace(
        b'BATTLE_VICTORY_ENTIRE_RUNTIME_UNCHANGED',b'ENEMY_CAPTURE_EXACT_DIRECT_CALLER_NAME_PROTECTION_AND_WRAP')
    after = before[:hi]+block+before[hi:]
    assert after.replace(block,b'',1)==before
    compile(after,str(builder),'exec')
    files = {str(manuscript),'translations/enemy_capture_editorial_manuscript_v1.json',
        'translations/enemy_capture_editorial_manuscript_v2.json','dk4tool/patch/enemy_capture_editorial.py',
        'dk4tool/patch/battle_victory_editorial.py','translations/battle_victory_editorial_release_v1.json',
        'scripts/battle_victory_native_plan_v1396.py','scripts/enemy_capture_native_plan_v1415.py',
        'scripts/enemy_capture_native_plan_v1419.py','scripts/enemy_capture_native_plan_v1423.py',
        'scripts/enemy_capture_runtime_v1417.py','scripts/enemy_capture_runtime_v1417b.py',
        'scripts/ship_sinking_runtime_v1328.py','scripts/battle_aftermath_runtime_v1253.py',
        'scripts/research_enemy_capture_v1413.py','scripts/author_enemy_capture_v1414.py',
        'scripts/refine_enemy_capture_prose_v1422.py','scripts/probe_enemy_capture_fonts_v1420.py',
        'scripts/probe_enemy_capture_fonts_v1424.py','scripts/probe_battle_aftermath_fonts_v1256.py',
        'scripts/verify_enemy_capture_runtime_v1418.py','scripts/verify_enemy_capture_copies_v1425.py',
        'scripts/verify_enemy_capture_escape_v1426.py','scripts/approve_enemy_capture_native_v1427.py',
        'scripts/verify_duel_cache_copies_v1163.py','scripts/verify_battle_aftermath_escape_v1262.py',
        str(Path(__file__)),'work/analysis/enemy_capture_payload_v1423/native_payload_plan.json',doc['source_context'],
        'work/analysis/enemy_capture_runtime_v1418/runtime_plan.json',
        'work/analysis/enemy_capture_runtime_v1418/scope_proof.json',
        'work/analysis/enemy_capture_runtime_v1418/modal_equivalence.json',
        'work/analysis/enemy_capture_runtime_v1418/status_contracts.json'}
    for key in ['native_font_proof','native_copy_proof','escape_regression_proof','native_runtime_proof','visual_review']:
        files.add(doc[key])
    fonts = read(doc['native_font_proof'])
    files.update(r['preview'] for r in fonts['cases'] if r['preview'])
    files.update(r['path'] for r in fonts['sheets_for_visual_review'])
    config = {'format':'dk4-enemy-capture-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,
        'source_arm9_sha256':owned.SOURCE_ARM,'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),
        'directory_sha256':proof['directory_sha256'],'manuscript':str(manuscript),
        'dependencies':{path:sha(Path(path).read_bytes()) for path in sorted(files)}}
    ROOT.mkdir(parents=True)
    save(owned.CONFIG,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2]==(c,a)
    (ROOT/'target_COMMON.bin').write_bytes(c);(ROOT/'target_ARM9.bin').write_bytes(a)
    save(ROOT/'repack_plan.json',proof)
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before
    profile = deepcopy(registry['profiles']['all-routes-unified-v1404'])
    profile.update(enemy_capture_editorial=owned.CONFIG,status='experimental',
        description='Complete V1404 stack plus eight source/native-reviewed enemy ship-capture reports and exact direct-caller name/wrap protection.',
        note='All8 capture paragraphs revised;3660 other messages/copies,all earlier formatter code and staged123040 bytes exact. Existing188-byte selector and172-byte gate add only direct53F40/table02117B00;all529325 gate/ABI,208 native font/name cases,7336 copies180 sequences13 escapes pass. Exact patch,startup and original capture/reward/return still pending;canonical unchanged.')
    registry['profiles'][PROFILE] = profile
    builder.write_bytes(after);save(registry_path,registry)
    restored = deepcopy(read(registry_path));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json')
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1404',
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'optional_stage_removal_restores_prior_builder_exact':True,'registry_before_sha256':sha(raw),
        'registry_after_sha256':sha(registry_path.read_bytes()),'all_prior_profiles_accepted_layers_and_batches_preserved':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'build_patch_startup_replay_and_completion_pending':True,'full_goal_complete':False})
    print('Complete experimental V1430 profile registered;8 capture revisions/exact caller repair. Build/startup/replay pending.',flush=True)
