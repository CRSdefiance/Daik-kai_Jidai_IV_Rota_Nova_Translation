"""Register the complete18-entry service layer after all native copy gates."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch import port_services_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.review_port_services_v761 import CURRENT
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/port_services_v762')
MANUSCRIPT = Path('translations/port_services_editorial_manuscript_v2.json')
CONFIG = Path('translations/port_services_editorial_release_v1.json')


def main():
    assert not MANUSCRIPT.exists() and not CONFIG.exists()
    native, repack = [read(ROOT / p) for p in ('owned_native_verification.json', 'common_repack_plan.json')]
    assert native['all40_complete_layout_font_planes_identical_to_reviewed_research'] and not native['writes_into_all_four_immutable_banks']
    assert native['all1124_prior_Yard_outputs_and36680_dispatch_cases_pass']
    copies = [read(ROOT / f'native_copies_block_{k:02d}.json') for k in range(41)]
    assert sum(len(r['cases']) for r in copies) == 7336
    assert all(r['COMMON_sha256'] == repack['target_COMMON_sha256'] and r['ARM9_sha256'] == repack['target_ARM9_sha256'] for r in copies)
    doc = deepcopy(read('translations/port_services_editorial_manuscript_v1.json'))
    for row in doc['records']:
        assert not row['review']['formatting']
        row['review']['formatting'] = True
        row['runtime_argument_contract'] = owned.ARGUMENTS.get(row['message_id'], [])
        row['status'] = 'source-native-reviewed-registered-integration-and-actual-gameplay-pending'
    doc['status'] = 'source-native-owned-storage-copy-reviewed-actual-gameplay-pending'
    doc['prior_manuscript_sha256'] = sha(Path('translations/port_services_editorial_manuscript_v1.json').read_bytes())
    doc['owned_native_evidence'] = str(ROOT / 'owned_native_verification.json')
    rom = NdsImage.open(CURRENT)
    c, a, proof = owned.transform(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), doc)
    assert c == (ROOT / 'research_COMMON.bin').read_bytes() and a == (ROOT / 'research_combined_ARM9.bin').read_bytes()
    save(MANUSCRIPT, doc)
    save(ROOT / 'native_integration.json', {'source_ROM': str(CURRENT), 'source_ROM_sha256': sha(CURRENT.read_bytes()),
        'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a), 'proof': proof,
        'all7336_native_copies_pass': True, 'actual_gameplay_pending': True})
    registry_path = Path('translations/release_stack.json'); registry = read(registry_path)
    assert 'all-routes-unified-v762' not in registry['profiles']
    save(ROOT / 'release_stack_before_v762.json', registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v760'])
    parser = Path('dk4tool/script/common_message_table.py')
    replay = []
    for key, name in (('market_stock_editorial_v2', 'market_stock_replay_for_v762.json'),
                      ('market_contract_editorial', 'market_contract_replay_for_v762.json'),
                      ('shipyard_editorial', 'shipyard_replay_for_v762.json')):
        path = Path(profile[key]); config = read(path)
        keys = [p for p in config['dependencies'] if Path(p).name == parser.name]
        assert len(keys) == 1
        original_sha = sha(path.read_bytes()); config['dependencies'][keys[0]] = sha(parser.read_bytes())
        for p, h in config['dependencies'].items(): assert sha(Path(p).read_bytes()) == h, p
        target = Path('translations') / name; assert not target.exists(); save(target, config)
        profile[key] = str(target)
        replay.append({'frozen_source': str(path), 'source_sha256': original_sha, 'explicit_replay': str(target),
            'only_changed_dependency': keys[0], 'same_target_COMMON_sha256': config['target_common_sha256'],
            'same_target_ARM9_sha256': config['target_arm9_sha256']})
    save(ROOT / 'explicit_parser_replays.json', {'three_frozen_prior_configs_preserved': replay,
        'strict_parser_one_digest_addition': repack['directory_sha256']})
    dependencies = [Path(p) for p in ('dk4tool/patch/port_services_editorial.py', 'dk4tool/patch/shop_business_editorial.py',
        'dk4tool/script/common_message_table.py', 'scripts/verify_port_storage_v762.py', 'scripts/verify_port_owned_native_v762.py',
        'scripts/verify_port_native_copies_v762.py', 'scripts/verify_shipyard_native_copies_v760.py',
        'scripts/review_port_services_v761.py', 'scripts/probe_port_services_v761.py',
        'translations/port_services_editorial_manuscript_v1.json')]
    dependencies += [ROOT / p for p in ('owned_storage.json', 'runtime_plan.json', 'owned_native_verification.json',
        'native_owned/verification.json', 'common_repack_plan.json', 'native_integration.json', 'explicit_parser_replays.json',
        'common_message_table_before_v762.py')]
    dependencies += [ROOT / f'native_copies_block_{k:02d}.json' for k in range(41)]
    save(CONFIG, {'format': 'dk4-port-services-editorial-v1', 'source_common_sha256': sha(rom.read_file('/COMMON/MESFILE.DK4')),
        'source_arm9_sha256': sha(rom.read_file('/__arm9__.bin')), 'target_common_sha256': sha(c), 'target_arm9_sha256': sha(a),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'dependencies': {str(p): sha(p.read_bytes()) for p in dependencies}})
    profile.update({'port_services_editorial': str(CONFIG), 'status': 'experimental',
        'description': 'Full V760 plus18 reviewed Port/companion/Tavern/shared price replies and exact808/1245/1246 literal balancing. Owned storage/full native copies/fonts pass; actual cold-boot gameplay pending.'})
    registry['profiles']['all-routes-unified-v762'] = profile; save(registry_path, registry)
    print('Complete18-entry V762 profile registered;three frozen earlier stages have explicit identical-output parser replays.', flush=True)


if __name__ == '__main__': main()
