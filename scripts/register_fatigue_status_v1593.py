"""Append the exact sea inspection responses after the entire V1542 stack."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import fatigue_status_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/fatigue_status_release_v1593')
PROFILE = 'all-routes-unified-v1594'

if __name__ == '__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript = Path('translations/fatigue_status_editorial_manuscript_v2.json')
    doc = read(manuscript)
    parent = Path('out/all_routes_combined_v1578_candidate.nds')
    assert sha(parent.read_bytes()) == 'd29f08026385628b47fcc0aa996402501975f986dbe2426ba348be723b37e79b'
    rom = NdsImage.open(parent)
    c, a, proof = owned.plan(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), doc)
    registry_path, builder = Path('translations/release_stack.json'), Path('scripts/build_integrated_release.py')
    raw, before = registry_path.read_bytes(), builder.read_bytes()
    registry = read(registry_path)
    assert len(registry['accepted_layers']) == 114 and PROFILE not in registry['profiles']
    assert registry['latest_promoted_build']['rom_sha256'] == '96d0eda08db4f6da69a936a44db1f41abcc1cd6ce202370a9edc5517eb5400fd'
    assert b"profile_config.get('fatigue_status_editorial')" not in before
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor) == 1
    lo = before.index(b"    inspection_status_editorial = profile_config.get('inspection_status_editorial')")
    hi = before.index(anchor)
    block=before[lo:hi].replace(b'inspection_status_editorial',b'fatigue_status_editorial').replace(
        b'INSPECTION_STATUS_NATIVE_METADATA',b'FATIGUE_STATUS_NATIVE_METADATA').replace(
        b'INSPECTION_STATUS_LITERAL_SYSTEM_MODAL_TEXT',b'FATIGUE_STATUS_SOURCE_NUMERIC_SYSTEM_MODAL_TEXT')
    after = before[:hi] + block + before[hi:]
    assert after.replace(block, b'', 1) == before
    compile(after, str(builder), 'exec')
    files=set(read('translations/inspection_status_editorial_release_v1.json')['dependencies'])
    files.update([str(manuscript),__file__,'translations/inspection_status_editorial_release_v1.json',
        'dk4tool/patch/fatigue_status_editorial.py','translations/fatigue_status_editorial_manuscript_v1.json',
        'scripts/inventory_fatigue_status_v1587.py','scripts/author_fatigue_status_v1588.py',
        'scripts/fatigue_status_native_plan_v1589.py','scripts/probe_fatigue_status_fonts_v1590.py',
        'scripts/verify_fatigue_status_copies_v1591.py','scripts/approve_fatigue_status_v1592.py',
        'work/analysis/fatigue_status_payload_v1589/native_payload_plan.json',doc['source_context'],
        'work/analysis/fatigue_status_native_review_v1592/native_approval_receipt.json'])
    for key in ['native_font_proof','native_copy_proof','visual_review']:files.add(doc[key])
    fonts=read(doc['native_font_proof']);files.update(r['preview'] for r in fonts['cases'] if 'preview' in r);files.add(fonts['review_sheet'])
    config = {'format': 'dk4-fatigue-status-editorial-v1', 'source_common_sha256': owned.SOURCE_COMMON,
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
    profile = deepcopy(registry['profiles']['all-routes-unified-v1578'])
    profile.update(fatigue_status_editorial=owned.CONFIG, status='experimental',
        description='Full V1578 stack plus two source/native-approved fatigue change statuses308/309.',
        note='Only COMMON4 and original message metadata change.3666 other copies,40 blocks,all native code/selector/gate/fonts/routes/graphics and123040 staged bytes exact.202 complete original numeric/native-independent glyph planes,15 compiler negatives,7336 copies180 cache and13 viewed panels pass. Exact patch/startup/original increase-recovery events pending. V1492 stays promoted.')
    registry['profiles'][PROFILE] = profile
    builder.write_bytes(after)
    save(registry_path, registry)
    restored = deepcopy(read(registry_path))
    restored['profiles'].pop(PROFILE)
    assert restored == read(ROOT / 'registry_before_raw.json')
    save(ROOT / 'registration_provenance.json', {'profile': PROFILE, 'source_profile': 'all-routes-unified-v1578',
        'builder_before_sha256': sha(before), 'builder_after_sha256': sha(after),
        'optional_stage_removal_restores_prior_builder_exact': True, 'registry_before_sha256': sha(raw),
        'registry_after_sha256': sha(registry_path.read_bytes()), 'all_prior_profiles_accepted_layers_batches_and_promotion_preserved': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'build_patch_startup_revised_original_event_and_completion_pending': True,
        'full_goal_complete': False})
    print('Experimental V1594 registered after full V1578;V1492 promotion preserved.Build/patch/startup/original fatigue events pending.')
