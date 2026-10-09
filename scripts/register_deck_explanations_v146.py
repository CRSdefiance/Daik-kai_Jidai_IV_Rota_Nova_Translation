"""Register reviewed Deck explanations after the entire V145 release stack."""

import copy
import json
from pathlib import Path

from dk4tool.patch.deck_explanation_release import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    registry = Path('translations/release_stack.json')
    stack = read(registry)
    if 'all-routes-unified-v146' in stack['profiles']:
        raise ValueError('V146 already registered; inspect current state')
    source = read('work/analysis/deck_explanations_source_proof.json')
    layout = read('work/qa/deck_explanations_native/report.json')
    connected = read('work/analysis/deck_explanations_connected_proof.json')
    pool = read('work/analysis/deck_explanations_pool_proof.json')
    if (len(source['cases']) != 1024 or len(layout['cases']) != 8 or len(connected['cases']) != 8
            or len(connected['native_pointer_consumer_cases']) != 31
            or layout['native_ink_visual_review']['panels_reviewed'] != 4
            or pool['research_arm9_sha256'] != connected['research_arm9_sha256']):
        raise ValueError('Complete reviewed Deck source/ink/connected proof required')
    manuscript = 'translations/deck_explanations_manuscript_v1.json'
    document = read(manuscript)
    for row in document['records']:
        row['review']['formatting'] = True
        row['localization_note'] += ' Complete generated word layout, all four native ink panels, aligned source-owned allocation and connected native caller/bitmap output are reviewed. Physical gameplay remains pending.'
    write(manuscript, document)
    template = 'translations/deck_explanation_pool_v1.json'
    write(template, source['adjacent_complete_owned_pool_lead'])
    evidence = 'translations/deck_explanation_native_review_v1.json'
    write(evidence, {'status': 'reviewed-native-deck-layout-connected-consumers-gameplay-pending',
                     'research_arm9_sha256': connected['research_arm9_sha256'],
                     'pixel_cases': layout['cases'], 'connected_cases': connected['cases'],
                     'native_pointer_consumer_cases': connected['native_pointer_consumer_cases'],
                     'visual_review': layout['native_ink_visual_review'],
                     'native_sheet_sha256': layout['native_sheet_sha256'],
                     'geometry': layout['geometry'], 'source_copy_case_count': len(source['cases']),
                     'consumer_locks': source['consumer_locks'] + layout['consumer_locks'],
                     'canonical_acceptance': False, 'limits': [layout['limits'], connected['limits']]})
    config = 'translations/deck_explanation_release_v1.json'
    write(config, {'format': 'dk4-deck-explanation-release-v1',
                   'target_arm9_sha256': connected['research_arm9_sha256'],
                   'manuscript': manuscript, 'pool': template, 'native_review': evidence,
                   'dependencies': {p: sha(Path(p).read_bytes()) for p in (manuscript, template, evidence)}})
    apply_release(NdsImage.open('out/all_routes_combined_v145_candidate.nds').read_file('/__arm9__.bin'), config)
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v145'])
    profile['deck_explanation_release'] = config
    profile['note'] = 'Complete V145 stack plus four full natural-English Deck explanations and source-owned aligned pool relocation; native connected/layout reviewed, physical gameplay pending.'
    stack['profiles']['all-routes-unified-v146'] = profile
    write(registry, stack)
    print(f'V146 registered with all {len(profile["batches"])} inherited batches.')


if __name__ == '__main__':
    main()
