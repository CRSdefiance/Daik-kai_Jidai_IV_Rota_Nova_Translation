"""Register the31-entry source-locked layer and frozen-output parser replays."""

import importlib
from copy import deepcopy
from pathlib import Path

from dk4tool.patch import barmaid_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.prepare_barmaid_common_v780 import ROOT, MANUSCRIPT
from scripts.context_barmaid_dialogue_v779 import CURRENT, ROOT as SOURCE
from scripts.verify_village_wrap_v608 import read, save

CONFIG = Path('translations/barmaid_editorial_release_v1.json')


def main():
    assert not CONFIG.exists()
    plan = read(ROOT/'prospective_common_repack.json')
    layout = read(ROOT/'scoped_layout_verification.json')
    assert layout['count'] == 273 and not layout['unresolved_layout_findings']
    assert layout['manuscript_sha256'] == sha(MANUSCRIPT.read_bytes())
    copies = [read(ROOT/f'native_copies/native_copies_block_{n:02d}.json') for n in range(41)]
    assert {(r['message_id'], r['cold_cache']) for p in copies for r in p['cases']} == {(n, c) for n in range(3668) for c in (False, True)}
    assert all(p['COMMON_sha256'] == plan['target_COMMON_sha256'] and p['ARM9_sha256'] == plan['target_ARM9_sha256'] for p in copies)
    assert all(r['complete_native_copy']['entire_native_span_including_post_NUL_payload_exact'] for p in copies for r in p['cases'])
    assert not read(ROOT/'current_storage_references.json')['unexpected']
    parser_path = Path(parser.__file__)
    text = parser_path.read_text(encoding='utf-8')
    digest = plan['directory_sha256']
    assert digest not in text
    (ROOT/'common_message_table_before_v780.py').write_text(text, encoding='utf-8')
    marker = 'RELOCATED_DIRECTORY_HASHES = frozenset({\n'
    assert text.count(marker) == 1
    parser_path.write_text(text.replace(marker, marker+f'    # V780: exact2336 selections933-3268;31 complete barmaid paragraphs.\n    "{digest}",\n', 1), encoding='utf-8')
    importlib.reload(parser)
    rom = NdsImage.open(CURRENT)
    c, a, proof = owned.transform(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), read(MANUSCRIPT))
    assert c == (ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes() and a == (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    save(ROOT/'native_integration.json', {'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a), 'proof': proof, 'actual_gameplay_pending': True})
    registry_path = Path('translations/release_stack.json')
    registry = read(registry_path)
    assert len(registry['accepted_layers']) == 114 and 'all-routes-unified-v780' not in registry['profiles']
    save(ROOT/'release_stack_before_v780.json', registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v778'])
    replays = []
    for key in ('market_stock_editorial_v2', 'market_contract_editorial', 'shipyard_editorial', 'port_services_editorial',
                'tavern_conversations_editorial', 'tavern_continuation_editorial', 'recruitment_editorial',
                'tavern_schemes_editorial', 'scheme_followup_editorial'):
        original = Path(profile[key])
        cfg = read(original)
        matches = [p for p in cfg['dependencies'] if Path(p).name == parser_path.name]
        assert len(matches) == 1
        cfg['dependencies'][matches[0]] = sha(parser_path.read_bytes())
        for p, h in cfg['dependencies'].items():
            assert sha(Path(p).read_bytes()) == h, p
        target = Path('translations')/f'{key}_replay_for_v780.json'
        assert not target.exists()
        save(target, cfg)
        profile[key] = str(target)
        replays.append({'original': str(original), 'original_sha256': sha(original.read_bytes()),
                        'explicit_replay': str(target), 'only_updated_dependency': matches[0],
                        'same_output_COMMON_sha256': cfg['target_common_sha256'], 'same_output_ARM9_sha256': cfg['target_arm9_sha256']})
    save(ROOT/'explicit_parser_replays.json', replays)
    paths = [Path(p) for p in ('dk4tool/patch/barmaid_editorial.py', 'dk4tool/patch/barmaid_editorial_runtime.py',
                               'dk4tool/patch/scheme_followup_editorial.py', 'dk4tool/patch/scheme_followup_runtime.py',
                               'dk4tool/patch/tavern_schemes_editorial.py', 'dk4tool/script/common_message_table.py',
                               'scripts/classify_barmaid_windows_v780.py', 'scripts/close_barmaid_context_v780.py',
                               'scripts/prepare_barmaid_runtime_v780.py', 'scripts/prepare_barmaid_common_v780.py',
                               'scripts/verify_barmaid_copies_v780.py', 'scripts/verify_barmaid_scoped_layout_v780.py')]
    paths += [SOURCE/p for p in ('native_context.json', 'captain_first_name_bound.json', 'layouts_v1/verification.json', 'layouts_v1/name_token_findings.json')]
    paths += [ROOT/p for p in ('classified_source_windows.json', 'latent996_caller_closure.json', 'effective_caller_closure.py',
                               'current_storage_references.json', 'runtime_plan.json', 'scope_proof.json',
                               'effective_storage_proof.py', 'effective_selector_proof.py', 'prospective_common_repack.json',
                               'minimum_repack_range.json', 'scoped_layout_verification.json', 'scoped_format_case.py',
                               'native_integration.json', 'explicit_parser_replays.json')]
    paths += [ROOT/f'native_copies/native_copies_block_{n:02d}.json' for n in range(41)]
    save(CONFIG, {'format': 'dk4-barmaid-editorial-v1',
                  'source_common_sha256': sha(rom.read_file('/COMMON/MESFILE.DK4')), 'source_arm9_sha256': sha(rom.read_file('/__arm9__.bin')),
                  'target_common_sha256': sha(c), 'target_arm9_sha256': sha(a),
                  'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
                  'dependencies': {str(p): sha(p.read_bytes()) for p in paths}})
    profile.update({'barmaid_editorial': str(CONFIG), 'status': 'experimental',
                    'description': 'V778 full stack plus31 source-reviewed barmaid paragraphs;114-byte exact routing table and complete2336-message existing-block repack. Actual scenes pending.'})
    registry['profiles']['all-routes-unified-v780'] = profile
    save(registry_path, registry)
    print('V780 registered with nine frozen-output parser replays;actual scenes remain pending.', flush=True)


if __name__ == '__main__':
    main()
