"""Register reviewed complete damaged-save prose after the full V144 stack."""

import copy
import json
from pathlib import Path

from dk4tool.patch.damaged_save_release import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    registry = Path('translations/release_stack.json')
    stack = json.loads(registry.read_text(encoding='utf-8'))
    if 'all-routes-unified-v145' in stack['profiles']:
        raise ValueError('V145 already registered; inspect existing state')
    proof_path = Path('work/analysis/damaged_save_message_proof.json')
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    pixel_path = Path('work/qa/damaged_save_native/report.json')
    pixels = json.loads(pixel_path.read_text(encoding='utf-8'))
    if (len(proof['cases']) != 256 or len(pixels['cases']) != 12
            or pixels['prepared_proof_sha256'] != sha(proof_path.read_bytes())
            or any(c['split_words'] for c in pixels['cases'])
            or not pixels.get('native_ink_visual_review', {}).get('formatting_approved')):
        raise ValueError('Complete native preparation and reviewed word layout required')
    manuscript = 'translations/damaged_save_message_manuscript_v1.json'
    document = json.loads(Path(manuscript).read_text(encoding='utf-8'))
    document['records'][0]['review']['formatting'] = True
    document['records'][0]['localization_note'] += ' Generated guarded word-boundary layout preserves the complete paragraph; all six final native panels are visually reviewed. Physical gameplay remains pending.'
    write(manuscript, document)
    evidence = 'translations/damaged_save_native_review_v1.json'
    write(evidence, {'status': 'reviewed-native-damaged-save-layout-gameplay-pending',
                     'source_sha256': proof['source_sha256'], 'research_sha256': proof['research_sha256'],
                     'consumer_locks': proof['consumer_locks'], 'preparation_cases': proof['cases'],
                     'pixel_cases': pixels['cases'], 'native_sheet_sha256': pixels['native_sheet_sha256'],
                     'visual_review_complete': True, 'canonical_acceptance': False,
                     'limits': proof['limits'] + [pixels['limits']]})
    config = 'translations/damaged_save_release_v1.json'
    write(config, {'format': 'dk4-damaged-save-release-v1',
                   'target_arm9_sha256': proof['research_sha256'], 'manuscript': manuscript,
                   'native_review': evidence,
                   'dependencies': {p: sha(Path(p).read_bytes()) for p in (manuscript, evidence)}})
    source = NdsImage.open('out/all_routes_combined_v144_candidate.nds').read_file('/__arm9__.bin')
    apply_release(source, config)
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v144'])
    profile['damaged_save_release'] = config
    profile['note'] = 'Complete V144 stack plus complete natural damaged-save message with reviewed native numeric/copy/formatter/word layout; physical gameplay pending.'
    stack['profiles']['all-routes-unified-v145'] = profile
    write(registry, stack)
    print(f'V145 registered with {len(profile["batches"])} inherited batches.')


if __name__ == '__main__':
    main()
