"""Register the isolated repair without changing the canonical or promoted build."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.square_font_scratch_20261027 import propose
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/lisbon_square_freeze_20261027')
CONFIG = Path('translations/square_font_scratch_20261027_v1.json')
PROFILE = 'font-v2-square-scratch-fix-20261027'
PREDECESSOR = 'font-v2-all-punctuation-one-pixel-20261027'


def main():
    registry = Path('translations/release_stack.json')
    before = registry.read_bytes()
    stack = json.loads(before)
    assert PROFILE not in stack['profiles'] and not CONFIG.exists()
    rom = Path('out/font_v2_all_punctuation_one_pixel_20261027_test.nds')
    assert sha(rom.read_bytes()) == 'fbbd68ee7d1af28ec4656262e53836c52b502c3c2cd0a3dbeddd2646e98342fe'
    source = NdsImage.open(rom).read_file('/__arm9__.bin')
    target, proof = propose(source)
    dependencies = ['dk4tool/patch/square_font_scratch_20261027.py',
                    'dk4tool/patch/square_caption_cells.py']
    config = dict(format='dk4-square-font-scratch-20261027-v1',
        dependencies={p: sha(Path(p).read_bytes()) for p in dependencies},
        source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target), proof=proof)
    profile = copy.deepcopy(stack['profiles'][PREDECESSOR])
    profile.update(status='experimental',
        description='Complete approved-design font/punctuation stack with per-call Square bitmap scratch; no promotion.',
        note='Repairs the user-confirmed Lisbon square overwrite of ASCII helper instructions. All earlier text and font designs preserved.',
        square_font_scratch_20261027=CONFIG.as_posix())
    stack['profiles'][PROFILE] = profile
    revoked = []
    for name, old_profile in stack['profiles'].items():
        if name == PROFILE:
            continue
        if old_profile.get('ascii_draw_offset_one_20261027'):
            old_profile['status'] = 'revoked'
            old_profile['revocation_reason'] = ('2026-10-27 user LisbonFreeze.dst and native regression confirm '
                'Square scratch 01FFC1A0..01FFC360 overwrites the ASCII helper 01FFC200..01FFC300. '
                'Preserved for reproduction; use font-v2-square-scratch-fix-20261027 for testing.')
            revoked.append(name)
    newline = '\r\n' if b'\r\n' in before else '\n'
    encoded = (json.dumps(stack, ensure_ascii=False, indent=2) + '\n').replace('\n', newline).encode()
    assert registry.read_bytes() == before
    (ROOT / 'release_stack_before.json').write_bytes(before)
    CONFIG.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    registry.write_bytes(encoded)
    (ROOT / 'release_stack_after.json').write_bytes(encoded)
    (ROOT / 'registry_change.json').write_text(json.dumps(dict(
        before_sha256=sha(before), after_sha256=sha(encoded), profile=PROFILE,
        inherited_profile=PREDECESSOR, revoked_profiles=revoked,
        canonical_and_accepted_and_promoted_unchanged=True), indent=2) + '\n')
    print(PROFILE, 'registered; revoked runtime-overlap profiles:', ', '.join(revoked))


if __name__ == '__main__':
    main()
