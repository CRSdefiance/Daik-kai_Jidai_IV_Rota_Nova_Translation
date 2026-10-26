"""Append the exact sea inspection responses after the entire V1542 stack."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import inspection_status_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/inspection_status_release_v1577')
PROFILE = 'all-routes-unified-v1578'

if __name__ == '__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript = Path('translations/inspection_status_editorial_manuscript_v2.json')
    doc = read(manuscript)
    parent = Path('out/all_routes_combined_v1563_candidate.nds')
    assert sha(parent.read_bytes()) == 'ba126ed72ce7ee1288cc689286cc7c2d98bb2c727f91d5e074568a8953a385a1'
    rom = NdsImage.open(parent)
    c, a, proof = owned.plan(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), doc)
    registry_path, builder = Path('translations/release_stack.json'), Path('scripts/build_integrated_release.py')
    raw, before = registry_path.read_bytes(), builder.read_bytes()
    registry = read(registry_path)
    assert len(registry['accepted_layers']) == 114 and PROFILE not in registry['profiles']
    assert registry['latest_promoted_build']['rom_sha256'] == '96d0eda08db4f6da69a936a44db1f41abcc1cd6ce202370a9edc5517eb5400fd'
    assert b"profile_config.get('inspection_status_editorial')" not in before
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor) == 1
    lo = before.index(b"    sea_responses_editorial = profile_config.get('sea_responses_editorial')")
    hi = before.index(anchor)
    block = before[lo:hi].replace(b'sea_responses_editorial',b'inspection_status_editorial').replace(
        b'SEA_INSPECTION_NATIVE_SELECTION_METADATA',b'INSPECTION_STATUS_NATIVE_METADATA').replace(
        b'SEA_INSPECTION_EXACT_ROLE_TABLE_AND_POSTMACRO_WRAP',b'INSPECTION_STATUS_LITERAL_SYSTEM_MODAL_TEXT')
    after = before[:hi] + block + before[hi:]
    assert after.replace(block, b'', 1) == before
    compile(after, str(builder), 'exec')
    files=set(read('translations/sea_responses_editorial_release_v1.json')['dependencies'])
    files.update([str(manuscript),__file__,'translations/sea_responses_editorial_release_v1.json',
        'dk4tool/patch/inspection_status_editorial.py','translations/inspection_status_editorial_manuscript_v1.json',
        'scripts/author_inspection_status_v1572.py','scripts/author_inspection_status_v1572b.py',
        'scripts/inspection_status_native_plan_v1573.py','scripts/probe_inspection_status_fonts_v1574.py',
        'scripts/verify_inspection_status_copies_v1575.py','scripts/approve_inspection_status_v1576.py',
        'work/analysis/inspection_status_payload_v1573/native_payload_plan.json',doc['source_context'],
        'work/analysis/inspection_status_native_review_v1576/native_approval_receipt.json'])
    for key in ['native_font_proof','native_copy_proof','visual_review']:files.add(doc[key])
    fonts=read(doc['native_font_proof']);files.update(r['preview'] for r in fonts['cases']);files.add(fonts['review_sheet'])
    config = {'format': 'dk4-inspection-status-editorial-v1', 'source_common_sha256': owned.SOURCE_COMMON,
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
    profile = deepcopy(registry['profiles']['all-routes-unified-v1563'])
    profile.update(inspection_status_editorial=owned.CONFIG, status='experimental',
        description='Full V1563 stack plus two faithful source/native-approved inspection status messages306/307.',
        note='Only COMMON4 and original message metadata change.3666 other copies,40 blocks,all native code/selector/gate/fonts/routes/graphics and123040 staged bytes exact.2 complete native/independent glyph planes,12 compiler negatives,7336 copies180 cache pass. Exact patch/startup/both original modal paths pending. V1492 stays promoted.')
    registry['profiles'][PROFILE] = profile
    builder.write_bytes(after)
    save(registry_path, registry)
    restored = deepcopy(read(registry_path))
    restored['profiles'].pop(PROFILE)
    assert restored == read(ROOT / 'registry_before_raw.json')
    save(ROOT / 'registration_provenance.json', {'profile': PROFILE, 'source_profile': 'all-routes-unified-v1563',
        'builder_before_sha256': sha(before), 'builder_after_sha256': sha(after),
        'optional_stage_removal_restores_prior_builder_exact': True, 'registry_before_sha256': sha(raw),
        'registry_after_sha256': sha(registry_path.read_bytes()), 'all_prior_profiles_accepted_layers_batches_and_promotion_preserved': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'build_patch_startup_revised_original_event_and_completion_pending': True,
        'full_goal_complete': False})
    print('Experimental V1563 registered;entire V1542 stack and V1492 promotion preserved. Build/patch/startup/original special-target inspection pending.')
