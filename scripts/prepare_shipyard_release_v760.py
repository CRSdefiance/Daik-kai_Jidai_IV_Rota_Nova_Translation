"""Bind all source/native gates to the complete registered Yard release layer."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial_release import transform
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shipyard_storage_v760')
MANUSCRIPT = Path('translations/shipyard_editorial_manuscript_v3.json')
CONFIG = Path('translations/shipyard_editorial_release_v1.json')


def main():
    assert not MANUSCRIPT.exists() and not CONFIG.exists()
    native = read(ROOT / 'native_owned/verification.json')
    assert len(native['all1124_complete_native_layouts_equal_verified_prototype']) == 1124
    assert len(native['all68_complete_font_planes_equal_independent_rasters_and_prior_reviewed_previews']) == 68
    assert not native['constant_bank_writes']
    assert len(native['all77_complete_RAM_buffer_comparisons']) == 77
    assert len(native['all24_original_numeric_call_and_copy_fragments']) == 24
    assert len(native['all180_complete_inherited_outputs']) == 180
    assert native['producer_sha256'] == sha(Path('scripts/verify_shipyard_owned_runtime_v760.py').read_bytes())
    repack = read(ROOT / 'common_repack_plan.json')
    copies = [read(ROOT / f'native_copies_block_{k:02d}.json') for k in range(41)]
    assert sum(len(r['cases']) for r in copies) == 7336
    assert all(r['COMMON_sha256'] == repack['target_COMMON_sha256'] and r['ARM9_sha256'] == repack['target_combined_ARM9_sha256'] for r in copies)
    old = NdsImage.open('out/all_routes_combined_v758_candidate.nds')
    doc = deepcopy(read('translations/shipyard_editorial_manuscript_v2.json'))
    doc['status'] = 'source-native-owned-storage-copy-reviewed-actual-gameplay-pending'
    doc['all6_native_prototype_preview_sheets_visually_inspected_and_owned_planes_identical'] = True
    for row in doc['records']:
        assert all(row['review'][gate] for gate in ('source', 'context', 'localization', 'naturalness'))
        assert not row['review']['formatting']
        row['review']['formatting'] = True
        row['status'] = 'native-reviewed-registered-integration-and-gameplay-pending'
        row['formatting_release_evidence'] = {'owned_native_execution': str(ROOT / 'native_owned/verification.json'),
            'owned_native_execution_sha256': sha((ROOT / 'native_owned/verification.json').read_bytes()),
            'all41_warm_cold_native_copies': str(ROOT), 'actual_gameplay_pending': True}
    c, a, proof = transform(old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin'), doc)
    assert c == (ROOT / 'research_COMMON.bin').read_bytes() and a == (ROOT / 'research_combined_ARM9.bin').read_bytes()
    save(MANUSCRIPT, doc)
    save(ROOT / 'native_integration.json', {'source_ROM': str(old.source), 'source_ROM_sha256': sha(old.source.read_bytes()),
        'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a), 'proof': proof,
        'all7336_warm_cold_copies_and68_complete_font_planes_pass': True,
        'registered_integration_and_actual_gameplay_pending': True})
    parser = Path('dk4tool/script/common_message_table.py')
    old_parser = (ROOT / 'common_message_table_before_v760.py').read_text(encoding='utf-8')
    addition = ('    # V760: exact1549 complete selections164-1712 in existing blocks2-18.\n'
                '    # Every unselected text byte and packed payload block remains preserved.\n'
                '    "7e2fc3325ac41442354ecb8547c6cf85a74bd14d05bd19ff39ec93d18c78cfd5",\n')
    assert parser.read_text(encoding='utf-8').replace(addition, '', 1) == old_parser
    registry_path = Path('translations/release_stack.json')
    registry = read(registry_path)
    assert 'all-routes-unified-v760' not in registry['profiles']
    save(ROOT / 'release_stack_before_V760.json', registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v758'])
    replay_rows = []
    for key, name in (('market_stock_editorial_v2', 'market_stock_replay_for_v760.json'),
                      ('market_contract_editorial', 'market_contract_replay_for_v760.json')):
        source_path = Path(profile[key])
        config = read(source_path)
        keys = [k for k in config['dependencies'] if Path(k).name == parser.name]
        assert len(keys) == 1
        config['dependencies'][keys[0]] = sha(parser.read_bytes())
        for path, digest in config['dependencies'].items():
            assert sha(Path(path).read_bytes()) == digest, path
        dest = Path('translations') / name
        assert not dest.exists()
        save(dest, config)
        profile[key] = str(dest)
        replay_rows.append({'source': str(source_path), 'source_sha256': sha(source_path.read_bytes()), 'explicit_replay': str(dest),
                            'only_changed_dependency': keys[0], 'unchanged_stage_target_COMMON': config['target_common_sha256'],
                            'unchanged_stage_target_ARM9': config['target_arm9_sha256']})
    save(ROOT / 'explicit_parser_replay.json', {'monotonic_exact_digest_only': True, 'original_frozen_configs_unchanged': replay_rows,
                                              'before_parser_snapshot': str(ROOT / 'common_message_table_before_v760.py')})
    dependencies = [Path(p) for p in ('dk4tool/patch/shipyard_editorial.py', 'dk4tool/patch/shipyard_common.py',
        'dk4tool/patch/shipyard_editorial_release.py', 'dk4tool/script/common_message_table.py',
        'scripts/verify_shipyard_storage_v760.py', 'scripts/verify_shipyard_owned_runtime_v760.py',
        'scripts/verify_shipyard_native_copies_v760.py', 'translations/village_promised_words_manuscript_v1.json',
        'translations/shipyard_editorial_manuscript_v2.json')]
    dependencies += [ROOT / p for p in ('owned_source_storage.json', 'runtime_plan.json', 'common_repack_plan.json',
        'common_preservation.json', 'native_owned/verification.json', 'native_integration.json',
        'explicit_parser_replay.json', 'common_message_table_before_v760.py')]
    dependencies += [ROOT / f'native_copies_block_{k:02d}.json' for k in range(41)]
    save(CONFIG, {'format': 'dk4-shipyard-editorial-v1', 'source_common_sha256': sha(old.read_file('/COMMON/MESFILE.DK4')),
        'source_arm9_sha256': sha(old.read_file('/__arm9__.bin')), 'target_common_sha256': sha(c), 'target_arm9_sha256': sha(a),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'dependencies': {str(p): sha(p.read_bytes()) for p in dependencies}})
    profile.update({'shipyard_editorial': str(CONFIG), 'status': 'experimental',
        'description': 'Full V758 plus21 faithful Shipyard paragraphs, scoped typed currency/days and literal ship names. Owned const storage, complete native copies/layout/font and source-preservation gates pass; actual cold-boot Yard gameplay pending.'})
    registry['profiles']['all-routes-unified-v760'] = profile
    save(registry_path, registry)
    print('V760 registered: all21 Shipyard entries and owned runtime; explicit byte-identical prior-stage replay; actual gameplay pending.', flush=True)


if __name__ == '__main__':
    main()
