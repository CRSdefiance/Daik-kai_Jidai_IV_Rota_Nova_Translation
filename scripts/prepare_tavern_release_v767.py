"""Register all31 reviewed Tavern paragraphs after complete native copy gates."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch import tavern_conversations_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_tavern_common_v767 import CURRENT, RESEARCH, ROOT
from scripts.verify_village_wrap_v608 import read, save

MANUSCRIPT = Path('translations/tavern_conversations_editorial_manuscript_v4.json')
CONFIG = Path('translations/tavern_conversations_editorial_release_v1.json')


def main():
    assert not MANUSCRIPT.exists() and not CONFIG.exists()
    copies = [read(ROOT / f'native_copies_block_{k:02d}.json') for k in range(41)]
    repack = read(ROOT / 'common_repack_plan.json')
    assert sum(len(r['cases']) for r in copies) == 7336
    assert {(r['message_id'], r['cold_cache']) for report in copies for r in report['cases']} == {(n, cold) for n in range(3668) for cold in (False, True)}
    assert all(r['COMMON_sha256'] == repack['target_COMMON_sha256'] and r['ARM9_sha256'] == repack['target_ARM9_sha256'] for r in copies)
    assert all(case['complete_native_copy']['entire_native_span_including_post_NUL_payload_exact'] for report in copies for case in report['cases'])
    source = Path('translations/tavern_conversations_editorial_manuscript_v3.json')
    native = read(RESEARCH / 'verification.json'); assert native['manuscript_sha256'] == sha(source.read_bytes())
    doc = deepcopy(read(source))
    for row in doc['records']:
        assert not row['review']['formatting']
        row['review']['formatting'] = True
        row['status'] = 'source-native-copies-reviewed-registered-build-and-actual-scenes-pending'
    doc['status'] = 'source-native-owned-storage-copy-reviewed-actual-gameplay-pending'
    doc['prior_manuscript_sha256'] = sha(source.read_bytes())
    doc['native_layout_evidence'] = str(RESEARCH / 'verification.json')
    doc['native_copy_evidence'] = str(ROOT)
    rom = NdsImage.open(CURRENT)
    c, a, proof = owned.transform(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), doc)
    assert c == (ROOT / 'research_COMMON.bin').read_bytes() and a == (ROOT / 'research_combined_ARM9.bin').read_bytes()
    save(MANUSCRIPT, doc)
    save(ROOT / 'native_integration.json', {'source_ROM': str(CURRENT), 'source_ROM_sha256': sha(CURRENT.read_bytes()),
        'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a), 'proof': proof,
        'all7336_whole_native_copy_spans_pass': True, 'actual_gameplay_pending': True})
    registry_path = Path('translations/release_stack.json'); registry = read(registry_path)
    assert 'all-routes-unified-v767' not in registry['profiles']
    save(ROOT / 'release_stack_before_v767.json', registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v762']); parser = Path('dk4tool/script/common_message_table.py')
    replays = []
    for key in ('market_stock_editorial_v2', 'market_contract_editorial', 'shipyard_editorial', 'port_services_editorial'):
        previous = Path(profile[key]); config = read(previous)
        matches = [p for p in config['dependencies'] if Path(p).name == parser.name]; assert len(matches) == 1
        previous_sha = sha(previous.read_bytes()); config['dependencies'][matches[0]] = sha(parser.read_bytes())
        for p, h in config['dependencies'].items(): assert sha(Path(p).read_bytes()) == h, p
        target = Path('translations') / f'{key}_replay_for_v767.json'
        assert not target.exists(); save(target, config); profile[key] = str(target)
        replays.append({'original': str(previous), 'sha256': previous_sha, 'explicit_replay': str(target),
            'only_dependency_changed': matches[0], 'target_common_sha256': config['target_common_sha256'], 'target_arm9_sha256': config['target_arm9_sha256']})
    save(ROOT / 'explicit_parser_replays.json', {'four_original_configs_preserved': replays, 'one_exact_new_directory_hash': repack['directory_sha256']})
    dependencies = [Path(p) for p in ('dk4tool/patch/tavern_conversations_editorial.py',
        'dk4tool/patch/tavern_coordinate_runtime.py', 'dk4tool/patch/tavern_editorial_runtime.py',
        'dk4tool/script/common_message_table.py', 'scripts/prepare_tavern_common_v767.py',
        'scripts/verify_tavern_copies_v767.py', 'scripts/verify_shipyard_native_copies_v760.py',
        'scripts/verify_tavern_coordinates_v766.py', 'scripts/verify_coordinate_buffers_v766.py',
        'scripts/verify_tavern_prior_v766.py', 'scripts/verify_tavern_providers_v766.py',
        'scripts/native_machine_scoped_v764.py', 'scripts/native_call_abi_v764.py')]
    dependencies += [RESEARCH / name for name in ('owned_runtime_plan.json', 'verification.json', 'visual_review.json',
        'coordinate_buffer_contracts.json', 'inherited_outputs.json', 'actual_leader_layout_matrix.json', 'owned_provider_fragments.json')]
    dependencies += [ROOT / name for name in ('common_repack_plan.json', 'native_integration.json',
        'explicit_parser_replays.json', 'common_message_table_before_v767.py')]
    dependencies += [ROOT / f'native_copies_block_{k:02d}.json' for k in range(41)]
    save(CONFIG, {'format': 'dk4-tavern-conversations-editorial-v1',
        'source_common_sha256': sha(rom.read_file('/COMMON/MESFILE.DK4')), 'source_arm9_sha256': sha(rom.read_file('/__arm9__.bin')),
        'target_common_sha256': sha(c), 'target_arm9_sha256': sha(a),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'dependencies': {str(p): sha(p.read_bytes()) for p in dependencies}})
    profile.update({'tavern_conversations_editorial': str(CONFIG), 'status': 'experimental',
        'description': 'Complete V762 plus31 reviewed Tavern paragraphs,private English location/profession providers,literal names and842-only typed coordinate pairs. Full native/copy gates pass;actual cold-boot scene verification pending.'})
    registry['profiles']['all-routes-unified-v767'] = profile; save(registry_path, registry)
    print('Complete31-entry V767 profile registered;four prior configurations preserved through explicit identical-output parser replays.', flush=True)


if __name__ == '__main__': main()
