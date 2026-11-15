"""Register reviewed native Options prompts after the complete V143 stack."""

import copy
import json
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.options_narrow_release import SLOTS, SOURCE, apply_release
from dk4tool.rom.nds import NdsImage


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    parent = NdsImage.open('out/all_routes_combined_v143_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    proof_path = Path('work/analysis/options_narrow_prompts_proof.json')
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    if (sha(parent) != SOURCE or proof['source_sha256'] != SOURCE
            or len(proof['cases']) != 10 or len(proof['native_pixels']) != 8
            or len(proof['native_responses']) != 20 or not proof.get('native_ink_visual_review')):
        raise ValueError('Complete Options native/visual review required')
    rows = []
    for at, (capacity, literal, english) in SLOTS.items():
        rows.append({'id': f'OPTIONS_NARROW_{at:06X}', 'offset': at, 'capacity': capacity,
                     'source_hex': clean[at:at + capacity].hex().upper(),
                     'canonical_source_hex': canonical[at:at + capacity].hex().upper(),
                     'parent_hex': parent[at:at + capacity].hex().upper(),
                     'japanese': clean[at:at + capacity].split(b'\0', 1)[0].decode('cp932'),
                     'english': english + '{PAD}', 'speaker': 'Options confirmation dialog',
                     'context': f'Exact prompt literal at {0x02000000 + literal:08X}; native Options state selector passes current state then proposed state to 546F8. Existing Reports/Sailing Help menu labels retained.',
                     'source_meaning': 'States the current setting and asks whether to change to the second supplied setting.',
                     'localization_note': 'Full natural American English uses the established menu label and current tense; both substitutions retain their source order. One paragraph without authored wrapping. Actual native preparation, response behavior and every ink panel reviewed; physical gameplay remains pending.',
                     'review': {gate: True for gate in ('source', 'context', 'localization', 'naturalness', 'formatting')}})
    document = {'format': 'dk4-arm9-prompt-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
                'target_locale': 'en-US', 'encoder': 'dialogue-fixed-v1',
                'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'], 'records': rows}
    validate_natural_dialogue_batch(document)
    manuscript = 'translations/options_narrow_manuscript_v1.json'
    evidence = 'translations/options_narrow_native_review_v1.json'
    config_path = 'translations/options_narrow_release_v1.json'
    write(manuscript, document)
    write(evidence, {**proof, 'status': 'reviewed-native-options-layout-gameplay-pending',
                     'proof_sha256': sha(proof_path.read_bytes()), 'canonical_acceptance': False})
    write(config_path, {'format': 'dk4-options-narrow-release-v1', 'source_arm9_sha256': SOURCE,
                       'target_arm9_sha256': proof['research_sha256'], 'manuscript': manuscript,
                       'native_review': evidence,
                       'dependencies': {p: sha(Path(p).read_bytes()) for p in (manuscript, evidence)}})
    apply_release(parent, config_path)
    registry = Path('translations/release_stack.json')
    stack = json.loads(registry.read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v143'])
    profile['options_narrow_release'] = config_path
    profile['note'] = 'Complete V143 stack plus source-faithful narrow Reports/Sailing Help confirmations. Native prose/layout/response reviewed; experimental widget/input and cold-boot gameplay pending.'
    if 'all-routes-unified-v144' in stack['profiles']:
        raise ValueError('V144 already registered; inspect existing state before changing it')
    stack['profiles']['all-routes-unified-v144'] = profile
    write(registry, stack)
    print(f'V144 registered with all {len(profile["batches"])} inherited batches and strict narrow Options stage.')


if __name__ == '__main__':
    main()
