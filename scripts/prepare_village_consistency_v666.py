"""Register the seven scoped village repairs while retaining the entire V653 stack."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_port_consistency import transform
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/village_consistency_v666')
AUDITS = ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json',
          'graphics_completion_requirements_v313.json')


def main():
    path = Path('translations/release_stack.json')
    stack = read(path)
    previous = deepcopy(stack)
    name = 'all-routes-unified-v666'
    assert name not in stack['profiles'] and not (ROOT / 'preflight.json').exists()
    source = Path('out/all_routes_combined_v653_candidate.nds')
    assert sha(source.read_bytes()) == 'c4e9c4faf18c212e5b6572d61e6b2821493f38bbc1dc89d601b37b16058b3ade'
    target, proof = transform(NdsImage.open(source).read_file('/__arm9__.bin'))
    assert sha(target) == 'b92df335942af8db216b149f54c0eac75626ddde2cf573b6f41c20f3e217bda8'
    ROOT.mkdir(parents=True, exist_ok=True)
    save(ROOT / 'preflight.json', {
        'source_candidate': str(source), 'source_candidate_sha256': sha(source.read_bytes()),
        'source_registry_sha256': sha(path.read_bytes()), 'source_registry': previous,
        'canonical_baseline': previous['canonical_baseline'],
        'accepted_layers': previous['accepted_layers'],
        'inherited_profile': previous['profiles']['all-routes-unified-v653'], 'profile': name,
        'previous_goal_turn_classification': 'no progress: user-requested status report only; V665 prepared repair revalidated',
        'all_original_audits_before': {n: read(Path('translations') / n) for n in AUDITS}})
    (ROOT / 'release_stack_before.json').write_bytes(path.read_bytes())
    config = 'translations/village_port_consistency_v1.json'
    save(config, {'format': 'dk4-village-port-consistency-v1', 'proof': proof})
    profile = deepcopy(previous['profiles']['all-routes-unified-v653'])
    profile['description'] = 'Experimental complete V653 plus five existing Town name aliases and two machine-reflowed village clues; prose and graphics unchanged.'
    profile['village_port_consistency'] = config
    stack['profiles'][name] = profile
    save(path, stack)
    restored = read(path)
    del restored['profiles'][name]
    assert restored == previous
    print('V666 registered; previous registry and all three audits snapshotted; seven scoped repairs only.')


if __name__ == '__main__':
    main()
