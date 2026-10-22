"""Preserve the complete V651 stack and register the shared queued formatter."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/queued_portrait_wrap_v653')


def main():
    path = Path('translations/release_stack.json')
    stack = read(path)
    previous = deepcopy(stack)
    before = sha(path.read_bytes())
    native = read(ROOT / 'native_dispatch_proof.json')
    assert len(native['all19_voice_entries114_native_layouts']) == 114
    name = 'all-routes-unified-v653'
    assert name not in stack['profiles']
    profile = deepcopy(stack['profiles']['all-routes-unified-v651'])
    profile['description'] = 'Experimental complete V651 plus shared wrapping for both original queued role/portrait parents; prose and graphics unchanged.'
    profile['queued_portrait_wrap'] = 'translations/queued_portrait_wrap_v1.json'
    stack['profiles'][name] = profile
    save(path, stack)
    restored = read(path)
    del restored['profiles'][name]
    assert restored == previous
    source = Path('out/all_routes_combined_v651_candidate.nds')
    save(ROOT / 'preflight.json', {
        'source_candidate': str(source), 'source_candidate_sha256': sha(source.read_bytes()),
        'source_registry_sha256': before, 'registered_registry_sha256': sha(path.read_bytes()),
        'canonical_baseline': previous['canonical_baseline'],
        'accepted_layers': previous['accepted_layers'],
        'inherited_profile': previous['profiles']['all-routes-unified-v651'],
        'only_one_new_profile_added': True, 'profile': name,
        'previous_goal_turn_classification': 'no progress: status-only response; V652 live records revalidated before this repair',
        'all_original_audits_before': {n: read(Path('translations') / n) for n in
            ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json', 'graphics_completion_requirements_v313.json')}})
    print('V653 registered; all preceding profiles, layers and audit scope preserved.')


if __name__ == '__main__':
    main()
