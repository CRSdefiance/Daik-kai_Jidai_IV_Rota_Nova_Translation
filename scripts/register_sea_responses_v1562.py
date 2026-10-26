"""Append the exact sea inspection responses after the entire V1542 stack."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import sea_responses_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/sea_responses_release_v1562')
PROFILE = 'all-routes-unified-v1563'

if __name__ == '__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript = Path('translations/sea_responses_editorial_manuscript_v2.json')
    doc = read(manuscript)
    parent = Path('out/all_routes_combined_v1542_candidate.nds')
    assert sha(parent.read_bytes()) == 'b8b256650bb426e99012be06fd060114da0fbf32f763b5c3434204dda8f50437'
    rom = NdsImage.open(parent)
    c, a, proof = owned.plan(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), doc)
    registry_path, builder = Path('translations/release_stack.json'), Path('scripts/build_integrated_release.py')
    raw, before = registry_path.read_bytes(), builder.read_bytes()
    registry = read(registry_path)
    assert len(registry['accepted_layers']) == 114 and PROFILE not in registry['profiles']
    assert registry['latest_promoted_build']['rom_sha256'] == '96d0eda08db4f6da69a936a44db1f41abcc1cd6ce202370a9edc5517eb5400fd'
    assert b"profile_config.get('sea_responses_editorial')" not in before
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor) == 1
    lo = before.index(b"    declaration_responses_editorial = profile_config.get('declaration_responses_editorial')")
    hi = before.index(anchor)
    block = before[lo:hi].replace(b'declaration_responses_editorial', b'sea_responses_editorial').replace(
        b'NPC_DECLARATION_NATIVE_SELECTION_METADATA', b'SEA_INSPECTION_NATIVE_SELECTION_METADATA').replace(
        b'NPC_DECLARATION_EXACT_ACTOR_TABLE_AND_POSTMACRO_WRAP', b'SEA_INSPECTION_EXACT_ROLE_TABLE_AND_POSTMACRO_WRAP')
    after = before[:hi] + block + before[hi:]
    assert after.replace(block, b'', 1) == before
    compile(after, str(builder), 'exec')
    files = set(read('translations/declaration_responses_editorial_release_v1.json')['dependencies'])
    files.update(str(p) for p in [manuscript, Path(__file__), Path('dk4tool/patch/sea_responses_editorial.py'),
        Path('translations/declaration_responses_editorial_release_v1.json'),
        Path('translations/sea_responses_editorial_manuscript_v1.json')])
    files.update(['scripts/inventory_sea_responses_v1551.py', 'scripts/research_sea_context_v1552.py',
        'scripts/author_sea_responses_v1553.py', 'scripts/sea_responses_runtime_v1555.py',
        'scripts/sea_responses_native_plan_v1556.py', 'scripts/verify_sea_runtime_v1557.py',
        'scripts/probe_sea_fonts_v1558.py', 'scripts/verify_sea_copies_v1559.py',
        'scripts/verify_sea_escape_v1560.py', 'scripts/approve_sea_responses_v1561.py',
        'work/analysis/sea_responses_payload_v1556/native_payload_plan.json', doc['source_context'],
        'work/analysis/sea_responses_source_v1551/original_fear_awe_source_packet.json',
        'work/analysis/sea_responses_runtime_v1557/runtime_plan.json', 'work/analysis/sea_responses_runtime_v1557/scope_proof.json',
        'work/analysis/sea_responses_runtime_v1557/modal_equivalence.json', 'work/analysis/sea_responses_runtime_v1557/status_contracts.json'])
    for key in ['native_font_proof', 'native_copy_proof', 'escape_regression_proof', 'native_runtime_proof', 'visual_review']:
        files.add(doc[key])
    fonts = read(doc['native_font_proof'])
    files.update(r['preview'] for r in fonts['cases'])
    files.update(r['path'] for r in fonts['sheets_for_visual_review'])
    config = {'format': 'dk4-sea-inspection-responses-editorial-v1', 'source_common_sha256': owned.SOURCE_COMMON,
        'source_arm9_sha256': owned.SOURCE_ARM, 'target_common_sha256': sha(c), 'target_arm9_sha256': sha(a),
        'directory_sha256': proof['directory_sha256'], 'manuscript': str(manuscript),
        'dependencies': {p: sha(Path(p).read_bytes()) for p in sorted(files)}}
    ROOT.mkdir(parents=True)
    save(owned.CONFIG, config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), owned.CONFIG)[:2] == (c, a)
    (ROOT / 'target_COMMON.bin').write_bytes(c)
    (ROOT / 'target_ARM9.bin').write_bytes(a)
    save(ROOT / 'repack_plan.json', proof)
    (ROOT / 'registry_before_raw.json').write_bytes(raw)
    (ROOT / 'builder_before.py').write_bytes(before)
    (ROOT / 'builder_added_optional_stage.bin').write_bytes(block)
    assert registry_path.read_bytes() == raw and builder.read_bytes() == before
    profile = deepcopy(registry['profiles']['all-routes-unified-v1542'])
    profile.update(sea_responses_editorial=owned.CONFIG, status='experimental',
        description='Full V1542 stack plus eight source/native-approved creature and ghost inspection responses.',
        note='Five revised and three retained paragraphs;186/188 selector,172-byte gate,all prior layers and123040 staged bytes preserved.8 whole fonts/14 compiler negatives/207 actors/7 CPU role fixtures/529455 dispatch cases/7336 copies/180 cache/13 escapes pass. Exact patch,startup,original special-target inspection and completion pending. V1492 stays promoted.')
    registry['profiles'][PROFILE] = profile
    builder.write_bytes(after)
    save(registry_path, registry)
    restored = deepcopy(read(registry_path))
    restored['profiles'].pop(PROFILE)
    assert restored == read(ROOT / 'registry_before_raw.json')
    save(ROOT / 'registration_provenance.json', {'profile': PROFILE, 'source_profile': 'all-routes-unified-v1542',
        'builder_before_sha256': sha(before), 'builder_after_sha256': sha(after),
        'optional_stage_removal_restores_prior_builder_exact': True, 'registry_before_sha256': sha(raw),
        'registry_after_sha256': sha(registry_path.read_bytes()), 'all_prior_profiles_accepted_layers_batches_and_promotion_preserved': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'build_patch_startup_revised_original_event_and_completion_pending': True,
        'full_goal_complete': False})
    print('Experimental V1563 registered;entire V1542 stack and V1492 promotion preserved. Build/patch/startup/original special-target inspection pending.')
