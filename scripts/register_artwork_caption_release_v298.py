"""Inherit every V296 release layer and add only the reviewed caption stage."""

import copy
import json
from pathlib import Path


def main():
    path = Path('translations/release_stack.json')
    stack = json.loads(path.read_text(encoding='utf-8'))
    parent = stack['profiles']['all-routes-unified-v296']
    profile = copy.deepcopy(parent)
    profile['status'] = 'experimental'
    profile['artwork_name_captions_release'] = 'translations/artwork_name_captions_release_v1.json'
    profile['note'] = ('Complete V296 inherited stack plus 16 source-reviewed Rafael/Camille artwork captions. '
                       'Native selector/font proofs pass; live unlocked Gallery/scene navigation and all18 plaque audits remain open. '
                       'V297 route prose and shared-name integration remains pending. Online low-resolution images exempt.')
    existing = stack['profiles'].get('all-routes-unified-v298')
    assert existing is None or existing == profile
    stack['profiles']['all-routes-unified-v298'] = profile
    assert profile['batches'] == parent['batches']
    path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'V298 registered: all {len(profile["batches"])} inherited profile batches unchanged.')


if __name__ == '__main__':
    main()
