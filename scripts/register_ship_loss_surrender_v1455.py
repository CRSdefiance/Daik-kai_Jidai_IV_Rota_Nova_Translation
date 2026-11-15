"""Register the full V1430 stack plus the24 reviewed loss/surrender reports."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import ship_loss_surrender_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_loss_surrender_release_v1455')
PROFILE = 'all-routes-unified-v1456'

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript = Path('translations/ship_loss_surrender_editorial_manuscript_v3.json');doc = read(manuscript)
    parent = Path('out/all_routes_combined_v1430_candidate.nds')
    assert sha(parent.read_bytes())=='db464eea08a5cdf5a0b840aa39f9a29fed0e13a52aa47f606e9060d71e590a76'
    rom = NdsImage.open(parent)
    c,a,proof = owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    registry_path,builder = Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before = registry_path.read_bytes(),builder.read_bytes();registry = read(registry_path)
    assert len(registry['accepted_layers'])==114 and PROFILE not in registry['profiles']
    assert b"profile_config.get('ship_loss_surrender_editorial')" not in before
    anchor = b'    # Lexically valid "% o"';assert before.count(anchor)==1
    lo = before.index(b"    enemy_capture_editorial = profile_config.get('enemy_capture_editorial')")
    hi = before.index(anchor)
    block = before[lo:hi].replace(b'enemy_capture_editorial',b'ship_loss_surrender_editorial').replace(
        b'ENEMY_CAPTURE_NATIVE_SELECTION_METADATA',b'SHIP_LOSS_SURRENDER_NATIVE_SELECTION_METADATA').replace(
        b'ENEMY_CAPTURE_EXACT_DIRECT_CALLER_NAME_PROTECTION_AND_WRAP',b'SHIP_LOSS_SURRENDER_THREE_EXACT_ROLE_CALLERS_NAME_PROTECTION_AND_WRAP')
    after = before[:hi]+block+before[hi:]
    assert after.replace(block,b'',1)==before;compile(after,str(builder),'exec')
    files = {str(manuscript),'translations/ship_loss_surrender_editorial_manuscript_v1.json',
        'translations/ship_loss_surrender_editorial_manuscript_v2.json','dk4tool/patch/ship_loss_surrender_editorial.py',
        'dk4tool/patch/enemy_capture_editorial.py','translations/enemy_capture_editorial_release_v1.json',
        'scripts/ship_loss_surrender_native_plan_v1444.py','scripts/ship_loss_surrender_native_plan_v1444b.py',
        'scripts/ship_loss_surrender_native_plan_v1447.py','scripts/ship_loss_surrender_runtime_v1442.py',
        'scripts/ship_loss_surrender_runtime_v1442b.py','scripts/enemy_capture_runtime_v1417.py',
        'scripts/enemy_capture_runtime_v1417b.py','scripts/ship_sinking_runtime_v1328.py',
        'scripts/battle_aftermath_runtime_v1253.py','scripts/research_ship_loss_surrender_v1439.py',
        'scripts/author_ship_loss_surrender_v1440.py','scripts/refine_ship_loss_surrender_v1446.py',
        'scripts/probe_ship_loss_surrender_fonts_v1445.py','scripts/probe_ship_loss_surrender_fonts_v1448.py',
        'scripts/probe_battle_aftermath_fonts_v1256.py','scripts/verify_ship_loss_surrender_runtime_v1443.py',
        'scripts/verify_ship_loss_surrender_runtime_v1443b.py','scripts/verify_ship_loss_surrender_copies_v1451.py',
        'scripts/verify_ship_loss_surrender_escape_v1452.py','scripts/approve_ship_loss_surrender_v1453.py',
        'scripts/verify_duel_cache_copies_v1163.py','scripts/verify_battle_aftermath_escape_v1262.py',
        str(Path(__file__)),'work/analysis/ship_loss_surrender_payload_v1447/native_payload_plan.json',doc['source_context'],
        'work/analysis/ship_loss_surrender_runtime_v1443b/runtime_plan.json',
        'work/analysis/ship_loss_surrender_runtime_v1443b/scope_proof.json',
        'work/analysis/ship_loss_surrender_runtime_v1443b/modal_equivalence.json',
        'work/analysis/ship_loss_surrender_runtime_v1443b/status_contracts.json'}
    for key in ['native_font_proof','native_copy_proof','escape_regression_proof','native_runtime_proof','visual_review']:
        files.add(doc[key])
    fonts = read(doc['native_font_proof']);files.update(r['preview'] for r in fonts['cases'] if r['preview'])
    files.update(r['path'] for r in fonts['sheets_for_visual_review'])
    config = {'format':'dk4-ship-loss-surrender-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,
        'source_arm9_sha256':owned.SOURCE_ARM,'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),
        'directory_sha256':proof['directory_sha256'],'manuscript':str(manuscript),
        'dependencies':{p:sha(Path(p).read_bytes()) for p in sorted(files)}}
    ROOT.mkdir(parents=True);save(owned.CONFIG,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2]==(c,a)
    (ROOT/'target_COMMON.bin').write_bytes(c);(ROOT/'target_ARM9.bin').write_bytes(a);save(ROOT/'repack_plan.json',proof)
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before
    profile = deepcopy(registry['profiles']['all-routes-unified-v1430'])
    profile.update(ship_loss_surrender_editorial=owned.CONFIG,status='experimental',
        description='Complete V1430 stack plus24 source/native-reviewed loss/surrender reports and three exact role1 caller name/wrap protections.',
        note='24 revised paragraphs;3644 other messages/copies,all earlier formatter/status/graphics/font code and staged123040 exact. Existing188/172 owned banks preserve all prior scopes plus role53DB8/tables02117AC0,02117B80,02117C60.529364 gate/ABI,624 font/name,7336 copies180 cache sequences13 escape checks pass. Exact patch,startup and three original event families remain pending;canonical unchanged.')
    registry['profiles'][PROFILE] = profile;builder.write_bytes(after);save(registry_path,registry)
    restored = deepcopy(read(registry_path));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json')
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1430',
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'optional_stage_removal_restores_prior_builder_exact':True,'registry_before_sha256':sha(raw),
        'registry_after_sha256':sha(registry_path.read_bytes()),'all_prior_profiles_accepted_layers_and_batches_preserved':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'build_patch_startup_original_events_and_completion_pending':True,'full_goal_complete':False})
    print('Complete experimental V1456 profile registered;24 revised reports/three exact role caller repairs. Build/startup/events pending.',flush=True)
