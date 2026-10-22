"""Register complete original regional notification guards and numbered labels."""

import copy
from pathlib import Path

from dk4tool.patch.regional_assignment_wrap import transform
from dk4tool.patch.regional_fleet_ordinal_label import transform as ordinal_transform
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save


def main():
    source = NdsImage.open('out/all_routes_combined_v616_candidate.nds').read_file('/__arm9__.bin')
    guarded, guards = transform(source)
    _, ordinal = ordinal_transform(guarded)
    evidence = read('work/analysis/regional_missions_v617/native_guarded_assignment_proof.json')
    assert evidence['guard_transform'] == guards and evidence['ordinal_transform'] == ordinal
    assert evidence['all3668_native_ID_dispatch_outputs_exact'] == 3668
    assert len(evidence['four_original_composed_notifications']) == 4 and len(evidence['complete_field_variants']) == 112
    save('translations/regional_assignment_wrap_v1.json', {'format': 'dk4-regional-assignment-wrap-v1', 'proof': guards})
    save('translations/regional_fleet_ordinal_label_v1.json', {'format': 'dk4-regional-fleet-ordinal-label-v1', 'proof': ordinal})
    path = Path('translations/release_stack.json')
    registry = read(path)
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v616'])
    profile.update({'regional_assignment_wrap': 'translations/regional_assignment_wrap_v1.json',
                    'regional_fleet_ordinal_label': 'translations/regional_fleet_ordinal_label_v1.json',
                    'description': 'Complete V616 plus scoped whole-assignment newline guards for all four policies and source-correct Fleet number word order; proper fleet names and all other callers preserved.',
                    'note': 'Experimental. V616 actual Patrol confirmation loses the initial S from Stockholm at a bare LF. V617 guards the original three fields after expansion,with exact parent/caller scope and zero section/pool growth. All four assignment displays,mission/contract/war variants and previous graphics gates require native evidence.'})
    if 'all-routes-unified-v617' in registry['profiles']:
        assert registry['profiles']['all-routes-unified-v617'] == profile
    registry['profiles']['all-routes-unified-v617'] = profile
    save(path, registry)
    print('Registered complete V617 assignment family and source-separated numbered fleet label; full V616 stack retained.')


if __name__ == '__main__':
    main()
