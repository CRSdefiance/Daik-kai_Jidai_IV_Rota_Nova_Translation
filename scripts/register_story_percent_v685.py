"""Register the full V678 stack plus four source-bound percentage repairs."""

import copy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.story_literal_percent import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.format_safety import reject_story_percent_commands
from scripts.prepare_story_percent_v685 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    registry = Path('translations/release_stack.json')
    stack = read(registry)
    assert stack == pre['source_registry'] and sha(registry.read_bytes()) == pre['source_registry_sha256']
    current, canonical, clean = [NdsImage.open(p) for p in (
        pre['source_candidate'], stack['canonical_baseline']['path'], 'work/clean.nds')]
    after, proof = {}, {}
    for path, spec in pre['files'].items():
        after[path], proof[path] = transform(current.read_file(path), canonical.read_file(path), spec)
    paths = [f'/data/SC{i}.DK4' for i in range(4)]
    gate = reject_story_percent_commands({p: clean.read_file(p) for p in paths},
                                        {p: after.get(p, current.read_file(p)) for p in paths})
    config = Path('translations/story_literal_percent_v1.json')
    save(config, {'format': 'dk4-story-literal-percent-v1', 'files': pre['files'], 'proof': proof})
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v678'])
    profile['description'] = 'Experimental complete V678 stack plus four natural literal-percent records and source-bound final story format-contract enforcement.'
    profile['story_literal_percent_safety'] = str(config)
    stack['profiles'][pre['profile']] = profile
    save(registry, stack)
    save(ROOT / 'registration.json', {'config': str(config), 'config_sha256': sha(config.read_bytes()),
        'registry_sha256': sha(registry.read_bytes()), 'four_record_proof': proof, 'final_source_contract_gate': gate,
        'all470_existing_batches114_accepted_layers_and_prior_profiles_retained': True,
        'canonical_promoted': False, 'full_goal_complete': False})
    print('V685 full V678 plus four percent repairs registered; final story contract census clear.', flush=True)


if __name__ == '__main__':
    main()
