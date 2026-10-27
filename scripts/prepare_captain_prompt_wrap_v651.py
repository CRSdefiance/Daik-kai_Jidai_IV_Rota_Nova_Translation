"""Register the bounded modal formatter after every inherited V640 layer."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/captain_prompt_wrap_v651')


def main():
    path = Path('translations/release_stack.json')
    stack = read(path)
    previous = deepcopy(stack)
    before = sha(path.read_bytes())
    name = 'all-routes-unified-v651'
    assert name not in stack['profiles']
    profile = deepcopy(stack['profiles']['all-routes-unified-v640'])
    profile['description'] = 'Experimental full V640 stack plus complete captain-instruction modal word wrapping; no prose or graphics changes.'
    profile['captain_prompt_wrap'] = 'translations/captain_prompt_wrap_v1.json'
    stack['profiles'][name] = profile
    save(path, stack)
    saved = read(path)
    restored = deepcopy(saved)
    del restored['profiles'][name]
    assert restored == previous
    save(ROOT / 'preflight.json', {'source_candidate': 'out/all_routes_combined_v640_candidate.nds',
        'source_candidate_sha256': sha(Path('out/all_routes_combined_v640_candidate.nds').read_bytes()),
        'source_registry_sha256': before, 'registered_registry_sha256': sha(path.read_bytes()),
        'canonical_baseline': previous['canonical_baseline'],
        'accepted_layers': previous['accepted_layers'], 'inherited_profile': previous['profiles']['all-routes-unified-v640'],
        'only_one_new_profile_added': True, 'profile': name,
        'all_original_audits_before': {n: read(Path('translations') / n) for n in
            ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json', 'graphics_completion_requirements_v313.json')},
        'previous_goal_turn_classification': 'progress: V650 terminal five-ship test archived and two actual wrapping defects identified'})
    print('V651 registered;every prior profile and accepted layer preserved.')


if __name__ == '__main__':
    main()
