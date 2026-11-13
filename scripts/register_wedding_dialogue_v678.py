"""Register a final canonical-source dialogue stage without altering old batches."""

import copy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.wedding_dialogue_cleanup import transform
from dk4tool.rom.nds import NdsImage
from scripts.prepare_wedding_dialogue_v678 import BATCH, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    registry = Path('translations/release_stack.json')
    stack = read(registry)
    assert stack == pre['source_registry']
    assert sha(registry.read_bytes()) == pre['source_registry_sha256']
    assert sha(BATCH.read_bytes()) == pre['batch_sha256']
    source = NdsImage.open(pre['source_candidate']).read_file('/data/SC2.DK4')
    canonical = NdsImage.open(stack['canonical_baseline']['path']).read_file('/data/SC2.DK4')
    _, proof = transform(source, canonical, read(BATCH))
    path = Path('translations/wedding_dialogue_cleanup_v1.json')
    save(path, {'format': 'dk4-wedding-dialogue-cleanup-v1', 'batch': str(BATCH),
                'batch_sha256': sha(BATCH.read_bytes()), 'proof': proof})
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v666'])
    profile['description'] = 'Experimental full V666 stack plus two source-faithful Lil wedding paragraphs in their existing allocations.'
    profile['wedding_dialogue_cleanup'] = str(path)
    stack['profiles']['all-routes-unified-v678'] = profile
    save(registry, stack)
    save(ROOT / 'registration.json', {'config': str(path), 'config_sha256': sha(path.read_bytes()),
        'batch': str(BATCH), 'batch_sha256': sha(BATCH.read_bytes()),
        'registry_sha256': sha(registry.read_bytes()), 'all470_prior_batches_retained': True,
        'all114_accepted_layers_and_all_prior_profiles_unchanged': True,
        'previous_goal_turn_classification': 'no progress: status answer only; revalidated QA and complete V666 stack before registration',
        'current_goal_turn_classification': 'progress', 'full_goal_complete': False})
    print('Registered V678: complete V666 plus exact two-record final stage.', flush=True)


if __name__ == '__main__':
    main()
