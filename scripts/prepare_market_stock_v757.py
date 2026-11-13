"""Bind complete source/prose/native evidence to a registered Market candidate."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.market_stock_editorial_v2 import balance_runtime, transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_market_stock_layout_v755 import experimental_arm
from scripts.review_market_stock_v755 import CURRENT
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/market_stock_release_v757')
MANUSCRIPT = Path('translations/market_stock_manuscript_v3.json')
CONFIG = Path('translations/market_stock_editorial_release_v2.json')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not MANUSCRIPT.exists() and not CONFIG.exists()
    matrix_path = Path('work/analysis/market_balanced_v757/native_layout_matrix_RESEARCH.json')
    matrix = read(matrix_path)
    assert matrix['count'] == 31013 and matrix['layout_findings_count'] == 0 and matrix['static_compile_failures'] == []
    previous_matrix = read('work/analysis/market_balanced_v756/attempt2_two_pass/native_layout_matrix_RESEARCH.json')
    assert matrix['all_cases'] == previous_matrix['all_cases']
    assert [r['sha256'] for r in matrix['sampled_complete_font_planes']] == [r['sha256'] for r in previous_matrix['sampled_complete_font_planes']]
    assert matrix['producer_sha256'] == sha(Path('scripts/verify_market_balanced_matrix_v757.py').read_bytes())
    abi_path = Path('work/analysis/market_balanced_v757/ownership_ABI.json')
    abi = read(abi_path)
    assert len(abi['all180_inherited_full_output_controls']) == 180 and len(abi['all12_direct_helper_success_failure_ABI_and_output_controls']) == 12
    assert abi['producer_sha256'] == sha(Path('scripts/verify_market_balanced_owners_v757.py').read_bytes())
    current = NdsImage.open(CURRENT)
    common, arm = current.read_file('/COMMON/MESFILE.DK4'), current.read_file('/__arm9__.bin')
    filtered, _ = experimental_arm(arm)
    runtime, _ = balance_runtime(filtered)
    assert sha(runtime) == abi['research_ARM9_sha256']
    dispatch = read(matrix_path.parent / 'experimental_dispatch.json')
    assert sha(runtime) == dispatch['research_ARM9_sha256']
    doc = deepcopy(read('translations/market_stock_manuscript_v1.json'))
    assert [r['message_id'] for r in doc['records']] == list(range(767, 784))
    for row in doc['records']:
        row['review']['formatting'] = True
        row['status'] = 'source-context-naturalness-native-layout-reviewed-integration-gameplay-pending'
    doc.update({'status': 'native-reviewed-experimental-gameplay-pending',
        'native_formatting_proof': str(matrix_path), 'native_ABI_ownership_proof': str(abi_path),
        'all_preview_sheets_visually_inspected': True})
    common2, arm2, proof = transform(common, arm, doc)
    (ROOT / 'research_COMMON.bin').write_bytes(common2)
    (ROOT / 'research_ARM9.bin').write_bytes(arm2)
    save(ROOT / 'native_integration.json', {'source_ROM': str(CURRENT), 'source_ROM_sha256': sha(CURRENT.read_bytes()),
        'all31013_native_layouts_zero_findings_bound_to_runtime_ARM9': sha(runtime),
        'source_native_context_sha256': sha(Path(doc['context_evidence']).read_bytes()),
        'all_complete_native_preview_planes': matrix['sampled_complete_font_planes'],
        'all_preview_sheets_visually_inspected': True, 'all3651_unselected_texts_preserved': True,
        'repack': proof, 'target_COMMON_sha256': sha(common2), 'target_ARM9_sha256': sha(arm2),
        'full_goal_complete': False})
    save(MANUSCRIPT, doc)
    dependencies = [Path('dk4tool/patch/market_stock_editorial_v2.py'), Path('dk4tool/patch/shop_business_editorial.py'),
        Path('dk4tool/patch/town_stock_rows.py'), Path('scripts/probe_market_stock_layout_v755.py'),
        Path('dk4tool/script/common_message_table.py'), Path('scripts/verify_market_balanced_owners_v757.py'),
        Path('scripts/verify_market_filter_owners_v755.py'),
        Path('work/analysis/market_stock_v755/experimental_filter_ownership.json'),
        Path('work/analysis/market_stock_v755/readonly_source_span_inventory_RESEARCH.json'),
        Path(doc['context_evidence']), matrix_path, matrix_path.parent / 'experimental_dispatch.json',
        abi_path, ROOT / 'native_integration.json']
    save(CONFIG, {'format': 'dk4-market-stock-editorial-v2', 'source_common_sha256': sha(common),
        'source_arm9_sha256': sha(arm), 'target_common_sha256': sha(common2), 'target_arm9_sha256': sha(arm2),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'dependencies': {str(p): sha(p.read_bytes()) for p in dependencies}})
    registry_path = Path('translations/release_stack.json')
    registry = read(registry_path)
    assert 'all-routes-unified-v757' not in registry['profiles']
    save(ROOT / 'release_stack_before_V757.json', registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v754'])
    profile.update({'market_stock_editorial_v2': str(CONFIG), 'status': 'experimental',
        'description': 'Complete V754 plus explicit direct-caller guard and17 Market stock/letter reviews and bounded post-substitution layout retries. Gameplay pending.'})
    registry['profiles']['all-routes-unified-v756'].update({'status': 'revoked', 'description': 'Unpublished V756 superseded by V757: its retry adapter lacked the full original-parent guard and changed non-direct queued outputs with stale767-770 stack IDs. Preserve as research; do not distribute.'})
    registry['profiles']['all-routes-unified-v757'] = profile
    save(registry_path, registry)
    print('Registered experimental V757:17 complete Market entries; native evidence bound; gameplay pending.', flush=True)


if __name__ == '__main__':
    main()
