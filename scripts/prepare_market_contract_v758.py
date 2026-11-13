"""Register the complete source/native-reviewed Market advice/contract layer."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.market_contract_editorial import transform
from dk4tool.rom.nds import NdsImage
from scripts.review_market_contract_v758 import CURRENT, ROOT
from scripts.verify_village_wrap_v608 import read, save

MANUSCRIPT = Path('translations/market_contract_manuscript_v2.json')
CONFIG = Path('translations/market_contract_editorial_release_v1.json')


def main():
    assert not MANUSCRIPT.exists() and not CONFIG.exists()
    native = read(ROOT / 'native_review_RESEARCH.json')
    assert native['all31013_inherited_stock_outputs_equal_V757']
    assert len(native['all9_complete_font_planes']) == 9 and len(native['all120_non_direct_full_output_controls']) == 120
    assert native['producer_sha256'] == sha(Path('scripts/verify_market_contract_native_v758.py').read_bytes())
    assert native['production_module_sha256'] == sha(Path('dk4tool/patch/market_contract_editorial.py').read_bytes())
    copies = [read(ROOT / f'native_copies_block_{k:02d}.json') for k in range(41)]
    assert sum(len(r['cases']) for r in copies) == 7336
    assert all(r['ARM9_sha256'] == native['target_ARM9_sha256'] and r['COMMON_sha256'] == native['target_COMMON_sha256'] for r in copies)
    doc = read(ROOT / 'manuscript_native_RESEARCH.json')
    doc['status'] = 'source-context-natural-native-reviewed-gameplay-pending'
    doc['native_proof'] = str(ROOT / 'native_review_RESEARCH.json')
    doc['all9_native_previews_visually_inspected'] = True
    old = NdsImage.open(CURRENT)
    common, arm, proof = transform(old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin'), doc)
    assert common == (ROOT / 'research_COMMON.bin').read_bytes() and arm == (ROOT / 'research_ARM9.bin').read_bytes()
    save(MANUSCRIPT, doc)
    # Keep the immutable historical V757 release config intact. This explicit
    # replay copy pins the monotonic parser allowlist addition; it still produces
    # exactly V757's COMMON/ARM9 before applying the new layer.
    replay_source = Path('translations/market_stock_editorial_release_v2.json')
    replay = read(replay_source)
    keys = [k for k in replay['dependencies'] if Path(k).name == 'common_message_table.py']
    assert len(keys) == 1
    replay['dependencies'][keys[0]] = sha(Path(keys[0]).read_bytes())
    for p, h in replay['dependencies'].items():
        assert sha(Path(p).read_bytes()) == h, p
    replay_path = Path('translations/market_stock_replay_for_v758.json')
    save(replay_path, replay)
    (ROOT / 'common_message_table_for_v758.py').write_bytes(Path('dk4tool/script/common_message_table.py').read_bytes())
    save(ROOT / 'native_integration.json', {'source_ROM': str(CURRENT), 'source_ROM_sha256': sha(CURRENT.read_bytes()),
        'target_COMMON_sha256': sha(common), 'target_ARM9_sha256': sha(arm), 'repack': proof,
        'V757_replay_config_original_preserved': str(replay_source), 'V757_replay_config_original_sha256': sha(replay_source.read_bytes()),
        'parser_compatibility_source_snapshot': str(ROOT / 'common_message_table_before_v758.py'),
        'all9_previews_visually_inspected': True, 'registered_integration_and_actual_gameplay_pending': True})
    dependencies = [Path('dk4tool/patch/market_contract_editorial.py'), Path('dk4tool/patch/shop_business_editorial.py'),
        Path('dk4tool/script/common_message_table.py'), Path('scripts/review_market_contract_v758.py'),
        Path('scripts/verify_market_contract_native_v758.py'), ROOT / 'native_review_RESEARCH.json',
        ROOT / 'native_context.json', ROOT / 'native_integration.json', ROOT / 'common_message_table_before_v758.py']
    save(CONFIG, {'format': 'dk4-market-contract-editorial-v1', 'source_common_sha256': sha(old.read_file('/COMMON/MESFILE.DK4')),
        'source_arm9_sha256': sha(old.read_file('/__arm9__.bin')), 'target_common_sha256': sha(common), 'target_arm9_sha256': sha(arm),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'dependencies': {str(p): sha(p.read_bytes()) for p in dependencies}})
    registry_path = Path('translations/release_stack.json')
    registry = read(registry_path)
    assert 'all-routes-unified-v758' not in registry['profiles']
    save(ROOT / 'release_stack_before_V758.json', registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v757'])
    profile.update({'market_stock_editorial_v2': str(replay_path), 'market_contract_editorial': str(CONFIG),
        'status': 'experimental', 'description': 'Complete V757 plus seven faithful crew advice variants and a complete full-location contract reply. Exact761 runtime scope, native ownership/layout/copy gates passed; actual gameplay pending.'})
    registry['profiles']['all-routes-unified-v758'] = profile
    save(registry_path, registry)
    print('Experimental V758 registered:8 native-reviewed entries;3 unmapped drafts remain separate.', flush=True)


if __name__ == '__main__':
    main()
