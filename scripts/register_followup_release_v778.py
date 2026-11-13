"""Register the exact25-entry follow-up layer and preserve all prior outputs."""

import importlib
from copy import deepcopy
from pathlib import Path

from dk4tool.patch import scheme_followup_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.prepare_followup_common_v778 import ROOT, MANUSCRIPT
from scripts.review_scheme_followup_v777 import CURRENT, ROOT as SOURCE
from scripts.verify_village_wrap_v608 import read, save

CONFIG = Path('translations/scheme_followup_editorial_release_v1.json')


def main():
    assert not CONFIG.exists()
    plan = read(ROOT/'prospective_common_repack.json')
    layout = read(ROOT/'scoped_layout_verification.json')
    assert layout['count'] == 13699 and layout['manuscript_sha256'] == sha(MANUSCRIPT.read_bytes())
    copies = [read(ROOT/f'native_copies/native_copies_block_{n:02d}.json') for n in range(41)]
    assert {(r['message_id'], r['cold_cache']) for p in copies for r in p['cases']} == {(n, c) for n in range(3668) for c in (False, True)}
    assert all(p['COMMON_sha256'] == plan['target_COMMON_sha256'] and p['ARM9_sha256'] == plan['target_ARM9_sha256'] for p in copies)
    assert all(r['complete_native_copy']['entire_native_span_including_post_NUL_payload_exact'] for p in copies for r in p['cases'])
    assert not read(ROOT/'current_storage_references.json')['unexpected']
    parser_path = Path(parser.__file__)
    text = parser_path.read_text(encoding='utf-8')
    digest = plan['directory_sha256']
    assert digest not in text
    (ROOT/'common_message_table_before_v778.py').write_text(text, encoding='utf-8')
    marker = 'RELOCATED_DIRECTORY_HASHES = frozenset({\n'
    assert text.count(marker) == 1
    parser_path.write_text(text.replace(marker, marker+f'    # V778: exact2697 selections164-2860;25 follow-up paragraphs.\n    "{digest}",\n', 1), encoding='utf-8')
    importlib.reload(parser)
    rom = NdsImage.open(CURRENT)
    c, a, proof = owned.transform(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), read(MANUSCRIPT))
    assert c == (ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes() and a == (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    save(ROOT/'native_integration.json', {'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a), 'proof': proof, 'actual_gameplay_pending': True})
    registry_path = Path('translations/release_stack.json')
    registry = read(registry_path)
    assert len(registry['accepted_layers']) == 114 and 'all-routes-unified-v778' not in registry['profiles']
    save(ROOT/'release_stack_before_v778.json', registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v776'])
    replays = []
    for key in ('market_stock_editorial_v2', 'market_contract_editorial', 'shipyard_editorial', 'port_services_editorial',
                'tavern_conversations_editorial', 'tavern_continuation_editorial', 'recruitment_editorial', 'tavern_schemes_editorial'):
        original = Path(profile[key])
        cfg = read(original)
        matches = [p for p in cfg['dependencies'] if Path(p).name == parser_path.name]
        assert len(matches) == 1
        cfg['dependencies'][matches[0]] = sha(parser_path.read_bytes())
        for p, h in cfg['dependencies'].items():
            assert sha(Path(p).read_bytes()) == h, p
        target = Path('translations')/f'{key}_replay_for_v778.json'
        assert not target.exists()
        save(target, cfg)
        profile[key] = str(target)
        replays.append({'original': str(original), 'original_sha256': sha(original.read_bytes()),
                        'explicit_replay': str(target), 'only_updated_dependency': matches[0],
                        'same_output_COMMON_sha256': cfg['target_common_sha256'], 'same_output_ARM9_sha256': cfg['target_arm9_sha256']})
    save(ROOT/'explicit_parser_replays.json', replays)
    paths = [Path(p) for p in ('dk4tool/patch/scheme_followup_editorial.py', 'dk4tool/patch/scheme_followup_runtime.py',
                               'dk4tool/patch/tavern_schemes_editorial.py', 'dk4tool/patch/tavern_schemes_runtime.py',
                               'dk4tool/patch/recruitment_editorial_runtime.py', 'dk4tool/script/common_message_table.py',
                               'scripts/verify_followup_inputs_v777.py', 'scripts/prepare_followup_runtime_v778.py',
                               'scripts/prepare_followup_common_v778.py', 'scripts/verify_followup_copies_v778.py',
                               'scripts/verify_followup_scoped_layout_v778.py')]
    paths += [SOURCE/p for p in ('input_contract.json', 'native_context.json', 'layouts_v1/verification.json')]
    paths += [ROOT/p for p in ('current_storage_references.json', 'runtime_plan.json', 'scope_proof.json',
                               'effective_storage_proof.py', 'effective_selector_proof.py', 'prospective_common_repack.json',
                               'scoped_layout_verification.json', 'scoped_format_case.py', 'native_integration.json', 'explicit_parser_replays.json')]
    paths += [ROOT/f'native_copies/native_copies_block_{n:02d}.json' for n in range(41)]
    save(CONFIG, {'format': 'dk4-scheme-followup-editorial-v1',
                  'source_common_sha256': sha(rom.read_file('/COMMON/MESFILE.DK4')), 'source_arm9_sha256': sha(rom.read_file('/__arm9__.bin')),
                  'target_common_sha256': sha(c), 'target_arm9_sha256': sha(a),
                  'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
                  'dependencies': {str(p): sha(p.read_bytes()) for p in paths}})
    profile.update({'scheme_followup_editorial': str(CONFIG), 'status': 'experimental',
                    'description': 'V776 full stack plus25 source-reviewed followup/bribe/crowded/condition replies;110-byte exact routing table,unchanged code and memory geometry. Actual scenes pending.'})
    registry['profiles']['all-routes-unified-v778'] = profile
    save(registry_path, registry)
    print('V778 registered with eight frozen-output parser replays;actual gameplay remains pending.', flush=True)


if __name__ == '__main__':
    main()
