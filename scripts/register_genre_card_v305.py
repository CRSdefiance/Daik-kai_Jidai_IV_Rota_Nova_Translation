"""Inherit the full subtitle/naming/art stack and restore native genre layout."""

import copy
import json
from pathlib import Path

from scripts.prepare_genre_card_v305 import BATCH


def main():
    path = Path('translations/release_stack.json')
    stack = json.loads(path.read_text(encoding='utf-8'))
    parent = stack['profiles']['all-routes-unified-v303']
    profile = copy.deepcopy(parent)
    profile['batches'].append(str(BATCH))
    profile['status'] = 'experimental'
    profile['note'] = ('Full V303 inherited stack plus native256x192 genre lettering. '
                       'Established wording retained, original ink width/center matched; only one logo texture slot changes. '
                       'Current startup verification pending; all18 plaque audits and legacy display gates remain open; Online low-resolution images exempt.')
    existing = stack['profiles'].get('all-routes-unified-v305')
    assert existing is None or existing == profile
    stack['profiles']['all-routes-unified-v305'] = profile
    assert len(profile['batches']) == len(parent['batches']) + 1
    path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('V305 registered: all469 inherited batches plus one native-height genre batch.')


if __name__ == '__main__':
    main()
