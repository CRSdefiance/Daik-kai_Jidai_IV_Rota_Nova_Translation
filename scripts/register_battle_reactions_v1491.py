"""Register a complete V1456 successor with32 source/native-approved reactions."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import battle_reaction_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_reaction_release_v1491')
PROFILE='all-routes-unified-v1492'

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript=Path('translations/battle_reactions_editorial_manuscript_v2.json');doc=read(manuscript)
    parent=Path('out/all_routes_combined_v1456_candidate.nds')
    assert sha(parent.read_bytes())=='2d060af0572c64de56a3749c9feba863afe95edbeed2cb26683d1e9a6ff8ebbe'
    rom=NdsImage.open(parent)
    c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    registry_path,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=registry_path.read_bytes(),builder.read_bytes();registry=read(registry_path)
    assert len(registry['accepted_layers'])==114 and PROFILE not in registry['profiles']
    assert b"profile_config.get('battle_reaction_editorial')" not in before
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1
    lo=before.index(b"    ship_loss_surrender_editorial = profile_config.get('ship_loss_surrender_editorial')")
    hi=before.index(anchor)
    block=before[lo:hi].replace(b'ship_loss_surrender_editorial',b'battle_reaction_editorial').replace(
        b'SHIP_LOSS_SURRENDER_NATIVE_SELECTION_METADATA',b'BATTLE_REACTION_NATIVE_SELECTION_METADATA').replace(
        b'SHIP_LOSS_SURRENDER_THREE_EXACT_ROLE_CALLERS_NAME_PROTECTION_AND_WRAP',b'BATTLE_REACTION_FOUR_EXACT_ACTOR_TABLES_AND_POSTMACRO_WRAP')
    after=before[:hi]+block+before[hi:]
    assert after.replace(block,b'',1)==before;compile(after,str(builder),'exec')
    files=set(read('translations/ship_loss_surrender_editorial_release_v1.json')['dependencies'])
    files.update(str(p) for p in [manuscript,Path(__file__),Path('dk4tool/patch/battle_reaction_editorial.py'),
        Path('translations/ship_loss_surrender_editorial_release_v1.json'),Path('translations/battle_reactions_editorial_manuscript_v1.json')])
    files.update(['scripts/research_battle_reactions_v1478.py','scripts/research_battle_reaction_context_v1479.py',
        'scripts/author_battle_reactions_v1480.py','scripts/author_battle_reactions_v1480b.py',
        'scripts/research_reaction_scope_capacity_v1482.py','scripts/battle_reaction_runtime_v1483.py',
        'scripts/battle_reaction_native_plan_v1484.py','scripts/verify_battle_reaction_runtime_v1485.py',
        'scripts/probe_battle_reaction_fonts_v1486.py','scripts/verify_battle_reaction_copies_v1487.py',
        'scripts/verify_battle_reaction_escape_v1488.py','scripts/approve_battle_reactions_v1489.py',
        'work/analysis/battle_reaction_payload_v1484/native_payload_plan.json',doc['source_context'],
        'work/analysis/battle_reactions_source_v1478/source_inventory.json',
        'work/analysis/battle_reaction_scope_capacity_v1482/scope_capacity.json',
        'work/analysis/battle_reaction_runtime_v1485/runtime_plan.json',
        'work/analysis/battle_reaction_runtime_v1485/scope_proof.json',
        'work/analysis/battle_reaction_runtime_v1485/modal_equivalence.json',
        'work/analysis/battle_reaction_runtime_v1485/status_contracts.json'])
    for key in ['native_font_proof','native_copy_proof','escape_regression_proof','native_runtime_proof','visual_review']:files.add(doc[key])
    fonts=read(doc['native_font_proof']);files.update(r['preview'] for r in fonts['cases'])
    files.update(r['path'] for r in fonts['sheets_for_visual_review'])
    config={'format':'dk4-battle-reaction-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,
        'source_arm9_sha256':owned.SOURCE_ARM,'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),
        'directory_sha256':proof['directory_sha256'],'manuscript':str(manuscript),
        'dependencies':{p:sha(Path(p).read_bytes()) for p in sorted(files)}}
    ROOT.mkdir(parents=True);save(owned.CONFIG,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2]==(c,a)
    (ROOT/'target_COMMON.bin').write_bytes(c);(ROOT/'target_ARM9.bin').write_bytes(a);save(ROOT/'repack_plan.json',proof)
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before
    profile=deepcopy(registry['profiles']['all-routes-unified-v1456'])
    profile.update(battle_reaction_editorial=owned.CONFIG,status='experimental',
        description='Complete V1456 stack plus32 source/native-reviewed battle setup,surprise and wound reactions.',
        note='16 revised16 retained paragraphs;3652 other texts/copies,all prior graphics/fonts/helpers and staged123040 preserved. Four actor scopes fit184/188 bytes;172-byte gate unchanged.529416 native gate/ABI cases,32 full fonts,7336 copies180 cache sequences13 escapes pass. Exact patch,startup and original reaction families remain pending;canonical unchanged.')
    registry['profiles'][PROFILE]=profile;builder.write_bytes(after);save(registry_path,registry)
    restored=deepcopy(read(registry_path));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json')
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1456',
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'optional_stage_removal_restores_prior_builder_exact':True,'registry_before_sha256':sha(raw),
        'registry_after_sha256':sha(registry_path.read_bytes()),'all_prior_profiles_accepted_layers_and_batches_preserved':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'build_patch_startup_original_scenes_and_completion_pending':True,'full_goal_complete':False})
    print('Complete experimental V1492 profile registered;32 source/native-approved reactions. Build/startup/original scenes pending.')
