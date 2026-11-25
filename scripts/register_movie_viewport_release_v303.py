"""Inherit the complete naming/art stack and add native-width movie subtitles."""

import copy
import json
from pathlib import Path

from scripts.prepare_movie_viewport_release_v303 import ROOT


def main():
    preparation = json.loads((ROOT / 'preparation.json').read_text(encoding='utf-8'))
    path = Path('translations/release_stack.json')
    stack = json.loads(path.read_text(encoding='utf-8'))
    parent = stack['profiles']['all-routes-unified-v299']
    profile = copy.deepcopy(parent)
    profile['batches'] += preparation['batches']
    profile['status'] = 'experimental'
    profile['note'] = ('Full V299 inherited naming/art/actor stack plus four movie subtitles authored in native FLS widths. '
                       'M22 missing42 caption pixels corrected without shortening; M24 inference preserved. '
                       'Current cold-boot movie verification pending; all18 plaque audits remain open; Online low-resolution images exempt.')
    existing = stack['profiles'].get('all-routes-unified-v303')
    assert existing is None or existing == profile
    stack['profiles']['all-routes-unified-v303'] = profile
    assert len(profile['batches']) == len(parent['batches']) + 2
    path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('V303 registered: all467 inherited batches plus two canonical-source FLS batches.')


if __name__ == '__main__':
    main()
