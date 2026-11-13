"""Register the existing guarded word wrapper for the complete regional family."""

import copy
from pathlib import Path

from dk4tool.patch.regional_policy_wrap import transform
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save


def main():
    source = NdsImage.open('out/all_routes_combined_v615_candidate.nds').read_file('/__arm9__.bin')
    _, proof = transform(source)
    evidence = read('work/analysis/regional_fleet_v616/native_dispatch_proof.json')
    assert evidence['transform'] == proof and evidence['all3668_native_IDs_exercised']
    assert evidence['unrelated_IDs_exact'] == 3660 and len(evidence['other_parent_negative_controls']) == 40
    save('translations/regional_policy_wrap_v1.json', {'format': 'dk4-regional-policy-wrap-v1', 'proof': proof})
    path = Path('translations/release_stack.json')
    registry = read(path)
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v615'])
    profile.update({'regional_policy_wrap': 'translations/regional_policy_wrap_v1.json',
                    'description': 'Complete V615 plus shared guarded word wrapping for all eight regional policy notices; original321/327 and every other message/caller preserved,zero growth.',
                    'note': 'Experimental. V615 actual Patrol/Dock notices split words despite preview QA. V616 reuses the existing original-expander/guarded wrapper for IDs127..134. Actual native pixels and original full graphics scope remain required.'})
    if 'all-routes-unified-v616' in registry['profiles']:
        assert registry['profiles']['all-routes-unified-v616'] == profile
    registry['profiles']['all-routes-unified-v616'] = profile
    save(path, registry)
    print('Registered V616:source-pinned128-byte existing wrapper,8 added IDs,3660 unrelated IDs and40 parent controls exact.')


if __name__ == '__main__':
    main()
