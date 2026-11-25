"""Register the shared source-origin correction after the complete V617 stack."""

import copy
import json
from pathlib import Path

from dk4tool.patch.compact_bitmap_origin import transform
from dk4tool.rom.nds import NdsImage


def main():
    source = NdsImage.open('out/all_routes_combined_v617_candidate.nds').read_file('/__arm9__.bin')
    _, proof = transform(source)
    evidence = json.loads(Path('work/analysis/compact_origin_v621/actual_parent_proof.json').read_text())
    assert evidence['transform'] == proof
    assert evidence['old_callback_reproduces_name_row_overwrite']
    assert evidence['new_callback_preserves_both_original_stat_row_origins']
    config = {'format': 'dk4-compact-bitmap-origin-v1', 'proof': proof}
    Path('translations/compact_bitmap_origin_v1.json').write_text(
        json.dumps(config, indent=2) + '\n', encoding='utf-8')
    path = Path('translations/release_stack.json')
    registry = json.loads(path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v617'])
    profile.update({
        'compact_bitmap_origin': 'translations/compact_bitmap_origin_v1.json',
        'description': 'Complete V617 plus shared compact ASCII source-view origins using the existing verified Market callback.',
        'note': 'Experimental. V620 actual duel exposes compact text overwriting source name rows. Reuse C71C for the shared bitmap font; one callback pointer changes, with no helper or pool growth. Full native and gameplay regression required.'})
    if 'all-routes-unified-v621' in registry['profiles']:
        assert registry['profiles']['all-routes-unified-v621'] == profile
    registry['profiles']['all-routes-unified-v621'] = profile
    path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Registered complete experimental V621 stack; one existing font callback corrected.')


if __name__ == '__main__':
    main()
