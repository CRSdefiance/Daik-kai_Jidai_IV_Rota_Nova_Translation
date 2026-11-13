"""Register the complete V1364 profile plus eight reviewed victory alternatives."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import battle_victory_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/battle_victory_release_v1403')
PROFILE = 'all-routes-unified-v1404'


if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript = Path('translations/battle_victory_editorial_manuscript_v2.json')
    doc = read(manuscript)
    rom = NdsImage.open('out/all_routes_combined_v1364_candidate.nds')
    c,a,proof = owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    registry_path,builder = Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before = registry_path.read_bytes(),builder.read_bytes()
    registry = read(registry_path)
    assert len(registry['accepted_layers'])==114 and PROFILE not in registry['profiles']
    assert b"profile_config.get('battle_victory_editorial')" not in before
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor)==1
    lo = before.index(b"    flagship_capture_precision = profile_config.get('flagship_capture_precision')")
    hi = before.index(anchor)
    block = before[lo:hi].replace(b'flagship_capture_precision',b'battle_victory_editorial').replace(
        b'FLAGSHIP_CAPTURE_PRECISION_NATIVE_SELECTION_METADATA',b'BATTLE_VICTORY_NATIVE_SELECTION_METADATA').replace(
        b'FLAGSHIP_CAPTURE_PRECISION_ENTIRE_RUNTIME_UNCHANGED',b'BATTLE_VICTORY_ENTIRE_RUNTIME_UNCHANGED')
    after = before[:hi]+block+before[hi:]
    assert after.replace(block,b'',1)==before
    compile(after,str(builder),'exec')
    files = {str(manuscript),'translations/battle_victory_editorial_manuscript_v1.json',
        'dk4tool/patch/battle_victory_editorial.py','dk4tool/patch/flagship_capture_precision.py',
        'translations/flagship_capture_precision_release_v1.json','scripts/battle_victory_native_plan_v1396.py',
        'scripts/probe_battle_aftermath_fonts_v1256.py','scripts/verify_duel_cache_copies_v1163.py',
        'scripts/verify_battle_aftermath_escape_v1262.py','scripts/ship_sinking_runtime_v1328.py',
        'scripts/research_battle_victory_v1392.py','scripts/research_battle_victory_v1392b.py',
        'scripts/author_battle_victory_v1393.py','scripts/probe_battle_victory_fonts_v1397.py',
        'scripts/probe_battle_victory_fonts_v1397b.py','scripts/verify_battle_victory_copies_v1399.py',
        'scripts/verify_battle_victory_escape_v1400.py','scripts/approve_battle_victory_v1401.py',str(Path(__file__)),
        'work/analysis/battle_victory_payload_v1396/native_payload_plan.json',doc['source_context']}
    for key in ['native_font_proof','native_copy_proof','escape_regression_proof','visual_review']:
        files.add(doc[key])
    fonts = read(doc['native_font_proof'])
    files.update(r['preview'] for r in fonts['cases'])
    files.add(fonts['review_sheet'])
    config = {'format':'dk4-battle-victory-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,
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
    profile = deepcopy(registry['profiles']['all-routes-unified-v1364'])
    profile.update(battle_victory_editorial=owned.CONFIG,status='experimental',
        description='Complete V1364 stack plus eight source/native-reviewed victory alternatives,two prose revisions.',
        note='Only2136/2137 prose changes;all3666 other texts/copies and every runtime/selector/code byte remain exact. Eight original native voice/font pipelines,206 selections,7336 copies180 sequences13 escape regressions pass. Memory/staged123040 unchanged. Exact patch,startup and original victory/reward replay pending;canonical unchanged.')
    registry['profiles'][PROFILE] = profile
    builder.write_bytes(after)
    save(registry_path,registry)
    restored = deepcopy(read(registry_path))
    restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json')
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1364',
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'optional_stage_removal_restores_prior_builder_exact':True,'registry_before_sha256':sha(raw),
        'registry_after_sha256':sha(registry_path.read_bytes()),'all_prior_profiles_accepted_layers_and_batches_preserved':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'build_patch_startup_replay_and_completion_pending':True,
        'full_goal_complete':False})
    print('V1404 complete experimental profile registered;only2136/2137 prose revisions. Build/startup/replay pending.',flush=True)
