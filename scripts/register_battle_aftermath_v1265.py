"""Register the entire V1224 stack plus75 source/native-reviewed paragraphs."""
from copy import deepcopy
from pathlib import Path

from dk4tool.patch import battle_aftermath_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/battle_aftermath_release_v1265')
PROFILE = 'all-routes-unified-v1266'


def main():
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript = Path('translations/battle_aftermath_editorial_manuscript_v3.json')
    doc = read(manuscript)
    rom = NdsImage.open('out/all_routes_combined_v1224_candidate.nds')
    c,a,proof = owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    checkpoint = read('work/analysis/battle_aftermath_checkpoint_v1264/native_checkpoint.json')
    registry_path = Path('translations/release_stack.json')
    registry,raw = read(registry_path),registry_path.read_bytes()
    builder = Path('scripts/build_integrated_release.py')
    before = builder.read_bytes()
    assert PROFILE not in registry['profiles'] and b"profile_config.get('battle_aftermath_editorial')" not in before
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor) == 1
    lo = before.index(b"    duel_special_editorial = profile_config.get('duel_special_editorial')")
    hi = before.index(anchor)
    block = before[lo:hi].replace(b'duel_special_editorial',b'battle_aftermath_editorial').replace(
        b'DUEL_SPECIAL_NATIVE_SELECTION_METADATA',b'BATTLE_AFTERMATH_NATIVE_SELECTION_METADATA').replace(
        b'DUEL_SPECIAL_SOURCE_OWNED_HELPER64_AND_FRONT108',b'BATTLE_AFTERMATH_SELECTOR_SAME_OWNED188_AND172')
    after = before[:hi]+block+before[hi:]
    assert after.replace(block,b'',1) == before
    compile(after,str(builder),'exec')
    files = [str(Path(__file__)),str(manuscript),'dk4tool/patch/battle_aftermath_editorial.py',
        'dk4tool/patch/duel_special_editorial.py','dk4tool/patch/duel_editorial.py',
        'translations/duel_special_editorial_release_v1.json',
        'translations/battle_aftermath_editorial_manuscript_v1.json',
        'translations/battle_aftermath_editorial_manuscript_v2.json']
    # All new producers,including frozen failed predecessors whose successor
    # adapters import their functions,are immutable release dependencies.
    files += [str(p) for p in Path('scripts').glob('*.py') if any(t in p.stem for t in
        ('battle_aftermath','aftermath_contract_codec','aftermath_isa_compiler'))]
    files += [p['path'] for p in checkpoint['proofs'].values()]
    files += [doc[k] for k in ('native_context_proof','complete_source_binding','native_font_proof',
        'native_copy_proof','escape_regression_proof','visual_review')]
    fonts = read(doc['native_font_proof'])
    files += [r['preview'] for r in fonts['cases']]
    files += [r['path'] for r in fonts['review_sheets']]
    config = {'format':'dk4-battle-aftermath-editorial-v1',
        'source_common_sha256':owned.SOURCE_COMMON,'source_arm9_sha256':owned.SOURCE_ARM,
        'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),'directory_sha256':proof['directory_sha256'],
        'manuscript':str(manuscript),
        'native_scope':'work/analysis/battle_aftermath_runtime_v1254c/scope_proof.json',
        'runtime_plan':'work/analysis/battle_aftermath_runtime_v1254c/runtime_plan.json',
        'dependencies':{p:sha(Path(p).read_bytes()) for p in dict.fromkeys(files)}}
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
    profile = deepcopy(registry['profiles']['all-routes-unified-v1224'])
    profile.update(battle_aftermath_editorial=owned.CONFIG,status='experimental',
        description='Complete V1224 stack plus75 source/native-reviewed aftermath,surrender,withdrawal and city-defense paragraphs.',
        note='58 revised17 retained;529273 exact dispatch/ABI;783 original speech/native font cases;7336 copies180 cache sequences13 escape regressions. Existing188-byte metadata and172-byte code allocations only;no staged growth. Startup,exact patch and original gameplay pending;canonical unchanged.')
    registry['profiles'][PROFILE] = profile
    builder.write_bytes(after)
    save(registry_path,registry)
    actual = read(registry_path)
    restored = deepcopy(actual)
    restored['profiles'].pop(PROFILE)
    assert restored == read(ROOT/'registry_before_raw.json')
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1224',
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'optional_stage_removal_restores_prior_builder_exact':True,
        'registry_before_sha256':sha(raw),'registry_after_sha256':sha(registry_path.read_bytes()),
        'all_prior_profiles_accepted_layers_and_batches_preserved':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),
        'build_startup_patch_original_gameplay_and_completion_pending':True,'full_goal_complete':False})
    print('V1266 full experimental profile registered after V1224. Build,patch,startup and original scenes remain pending.',flush=True)


if __name__ == '__main__':
    main()
