"""Register the full reviewed name migration after current native verification."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_reviewed_name_release_v299 import CONFIG, ROOT, read


def main():
    proof, native, dependencies = [read(ROOT / p) for p in
                                   ('transform_proof.json', 'full_native_proof.json', 'dependency_native_proof.json')]
    digest = proof['target_file_sha256']['/__arm9__.bin']
    assert native['ARM9_sha256'] == dependencies['target_ARM9_sha256'] == digest
    assert native['all444_complete_body_glyphs_pass'] and not native['failures']
    assert len(dependencies['native_getter_cases']) == 621 and len(dependencies['COMMON_full_native_glyph_cases']) == 24
    config = read(CONFIG)
    for name in ('native_lookup_proof.json', 'full_native_proof.json', 'dependency_native_proof.json'):
        path = str(ROOT / name)
        config['verification_evidence_sha256'] = {**config.get('verification_evidence_sha256', {}),
                                                 path: sha(Path(path).read_bytes())}
    config['status'] = 'experimental-full-reviewed-migration-native-verified-cold-boot-pending'
    CONFIG.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    path = Path('translations/release_stack.json')
    stack = read(path)
    parent = stack['profiles']['all-routes-unified-v298']
    profile = copy.deepcopy(parent)
    profile['reviewed_name_integration_release'] = str(CONFIG)
    profile['note'] = ('Complete V298 captions and inherited layers plus all444 reviewed route paragraphs, '
                       'five shared names, sixCOMMON messages and eight source-faithful HELP pages. '
                       'Complete native tests pass; current actual gameplay and all18 plaque audits remain open. '
                       'Low-resolution Online images exempt.')
    profile['status'] = 'experimental'
    old = stack['profiles'].get('all-routes-unified-v299')
    assert old is None or old == profile
    stack['profiles']['all-routes-unified-v299'] = profile
    assert profile['batches'] == parent['batches']
    path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('V299 registered with all467 inherited batches and complete name/text/art dependencies.')


if __name__ == '__main__':
    main()
