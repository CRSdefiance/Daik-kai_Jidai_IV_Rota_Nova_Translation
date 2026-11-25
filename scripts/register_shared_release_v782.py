"""Register the reviewed50-entry layer and ten explicit frozen-output replays."""

import importlib
from copy import deepcopy
from pathlib import Path

from dk4tool.patch import shared_dialogue_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.context_shared_dialogue_v781 import CURRENT, ROOT as SOURCE
from scripts.review_shared_dialogue_v781 import MANUSCRIPT as DRAFT
from scripts.verify_village_wrap_v608 import read, save

ROOT = owned.ROOT
MANUSCRIPT = Path('translations/shared_dialogue_editorial_manuscript_v2.json')
CONFIG = Path('translations/shared_dialogue_editorial_release_v1.json')


def main():
    assert not CONFIG.exists()
    plan, layout = read(ROOT/'prospective_common_repack.json'), read(ROOT/'production_layout/verification.json')
    assert layout['native_layouts'] == 857 and not layout['findings']
    assert layout['manuscript_sha256'] == sha(Path(DRAFT).read_bytes())
    copies = [read(ROOT/f'native_copies/native_copies_block_{n:02d}.json') for n in range(41)]
    assert {(r['message_id'], r['cold_cache']) for p in copies for r in p['cases']} == {(n, c) for n in range(3668) for c in (False, True)}
    assert all(p['COMMON_sha256'] == plan['target_COMMON_sha256'] and p['ARM9_sha256'] == plan['target_ARM9_sha256'] for p in copies)
    assert all(r['complete_native_copy']['entire_native_span_including_post_NUL_payload_exact'] for p in copies for r in p['cases'])
    assert not read(ROOT/'current_storage_references.json')['unexpected']
    manuscript = deepcopy(read(DRAFT))
    for row in manuscript['records']:
        assert not row['review']['formatting']
        row['review']['formatting'] = True
        row['status'] = 'native-reviewed-production-integration-and-gameplay-pending'
    manuscript.update({'caller_filter_proof': str(ROOT/'caller_filters.json'),
                       'consumer_routing_proof': str(ROOT/'consumer_routing.json'),
                       'production_layout_proof': str(ROOT/'production_layout/verification.json'),
                       'reviewed_research_manuscript': str(DRAFT), 'reviewed_research_manuscript_sha256': sha(Path(DRAFT).read_bytes()),
                       'status': 'native-reviewed-production-integration-and-gameplay-pending'})
    save(MANUSCRIPT, manuscript)
    parser_path = Path(parser.__file__)
    text = parser_path.read_text(encoding='utf-8')
    digest = plan['directory_sha256']
    assert digest not in text
    (ROOT/'common_message_table_before_v782.py').write_text(text, encoding='utf-8')
    marker = 'RELOCATED_DIRECTORY_HASHES = frozenset({\n'
    assert text.count(marker) == 1
    parser_path.write_text(text.replace(marker, marker+f'    # V782: exact2661 selections1007-3667;50 complete shared paragraphs.\n    "{digest}",\n', 1), encoding='utf-8')
    importlib.reload(parser)
    rom = NdsImage.open(CURRENT)
    c, a, proof = owned.transform(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), manuscript)
    assert c == (ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes() and a == (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    save(ROOT/'native_integration.json', {'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a), 'proof': proof, 'actual_gameplay_pending': True})
    registry_path = Path('translations/release_stack.json')
    registry = read(registry_path)
    assert len(registry['accepted_layers']) == 114 and 'all-routes-unified-v782' not in registry['profiles']
    save(ROOT/'release_stack_before_v782.json', registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v780'])
    replays = []
    for key in ('market_stock_editorial_v2', 'market_contract_editorial', 'shipyard_editorial', 'port_services_editorial',
                'tavern_conversations_editorial', 'tavern_continuation_editorial', 'recruitment_editorial',
                'tavern_schemes_editorial', 'scheme_followup_editorial', 'barmaid_editorial'):
        original = Path(profile[key])
        cfg = read(original)
        matches = [p for p in cfg['dependencies'] if Path(p).name == parser_path.name]
        assert len(matches) == 1
        cfg['dependencies'][matches[0]] = sha(parser_path.read_bytes())
        for p, h in cfg['dependencies'].items():
            assert sha(Path(p).read_bytes()) == h, p
        target = Path('translations')/f'{key}_replay_for_v782.json'
        assert not target.exists()
        save(target, cfg)
        profile[key] = str(target)
        replays.append({'original': str(original), 'original_sha256': sha(original.read_bytes()),
                        'explicit_replay': str(target), 'only_updated_dependency': matches[0],
                        'same_output_COMMON_sha256': cfg['target_common_sha256'], 'same_output_ARM9_sha256': cfg['target_arm9_sha256']})
    save(ROOT/'explicit_parser_replays.json', replays)
    paths = [Path(p) for p in ('dk4tool/patch/shared_dialogue_editorial.py', 'dk4tool/patch/shared_dialogue_runtime.py',
                               'dk4tool/patch/barmaid_editorial_runtime.py', 'dk4tool/patch/tavern_schemes_runtime.py',
                               'dk4tool/patch/scheme_followup_editorial.py', 'dk4tool/script/common_message_table.py',
                               'scripts/prepare_shared_runtime_v782.py', 'scripts/verify_shared_consumers_v782.py',
                               'scripts/verify_shared_filters_v782.py', 'scripts/prepare_shared_common_v782.py',
                               'scripts/probe_shared_production_v782.py', 'scripts/verify_shared_copies_v782.py', str(DRAFT))]
    paths += [SOURCE/p for p in ('native_context.json', 'layouts_v2/verification.json', 'layouts_v2/visual_review.json')]
    paths += [ROOT/p for p in ('current_storage_references.json', 'runtime_plan.json', 'scope_proof.json',
                               'effective_storage_proof.py', 'effective_selector_proof.py', 'consumer_routing.json', 'caller_filters.json',
                               'prospective_common_repack.json', 'production_layout/verification.json', 'production_layout/effective_format_case.py',
                               'native_integration.json', 'explicit_parser_replays.json')]
    paths += [ROOT/f'native_copies/native_copies_block_{n:02d}.json' for n in range(41)]
    save(CONFIG, {'format': 'dk4-shared-dialogue-editorial-v1',
                  'source_common_sha256': sha(rom.read_file('/COMMON/MESFILE.DK4')), 'source_arm9_sha256': sha(rom.read_file('/__arm9__.bin')),
                  'target_common_sha256': sha(c), 'target_arm9_sha256': sha(a),
                  'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
                  'dependencies': {str(p): sha(p.read_bytes()) for p in paths}})
    profile.update({'shared_dialogue_editorial': str(CONFIG), 'status': 'experimental',
                    'description': 'V780 full stack plus50 source-reviewed shared paragraphs;exact no-growth routing,28 existing COMMON blocks. Actual scenes pending.'})
    registry['profiles']['all-routes-unified-v782'] = profile
    save(registry_path, registry)
    print('V782 registered with ten frozen-output parser replays;actual scenes remain pending.', flush=True)


if __name__ == '__main__':
    main()
