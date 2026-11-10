"""Freeze and register the exact requested drawing-offset successor."""

import copy
import json
from pathlib import Path

from dk4tool.patch.ascii_draw_offset_20261027_v2 import propose
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/font_offset_test_20261027_v2')
CONFIG = Path('translations/ascii_draw_offset_20261027_v2.json')
PROFILE = 'font-v2-draw-down-two-v2-20261027'
PARENT = Path('out/font_descenders_symbols_v2_20261027_test.nds')


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ROOT.mkdir(exist_ok=False)
    registry = Path('translations/release_stack.json')
    before = registry.read_bytes()
    stack = json.loads(before)
    assert PROFILE not in stack['profiles'] and not CONFIG.exists()
    manifest = json.loads(PARENT.with_suffix('.manifest.json').read_text())
    assert manifest['candidate_sha256'] == sha(PARENT.read_bytes())
    arm = NdsImage.open(PARENT).read_file('/__arm9__.bin')
    target, proof = propose(arm)
    dependencies = ['dk4tool/patch/ascii_draw_offset_20261027_v2.py']
    save(CONFIG, dict(format='dk4-ascii-draw-offset-20261027-v2', status='experimental',
        predecessor_rom=str(PARENT), predecessor_rom_sha256=manifest['candidate_sha256'],
        source_ARM9_sha256=sha(arm), target_ARM9_sha256=sha(target), proof=proof,
        dependencies={p: sha(Path(p).read_bytes()) for p in dependencies}))
    (ROOT / 'proposed_ARM9.bin').write_bytes(target)
    profile = copy.deepcopy(stack['profiles'][manifest['profile']])
    profile['ascii_draw_offset_20261027_v2'] = str(CONFIG)
    profile['description'] = ('Complete previous V4749/font-v2 test stack plus global ASCII drawing Y+2 '
        'with backing-image row bounds and14-row footer labels in a cached1792-byte native heap allocation. '
        'Original improved font bytes retained; no DTCM/SDK overwrites, pool or autoload growth. '
        'Experimental; promoted main retained.')
    stack['profiles'][PROFILE] = profile
    (ROOT / 'release_stack_before.json').write_bytes(before)
    save(registry, stack)
    (ROOT / 'release_stack_snapshot.json').write_bytes(registry.read_bytes())
    save(ROOT / 'registration.json', dict(profile=PROFILE, source_registry_sha256=sha(before),
        registry_snapshot_sha256=sha(registry.read_bytes()), predecessor_sha256=manifest['candidate_sha256'],
        builder_sha256=sha(Path('scripts/build_integrated_release.py').read_bytes()), proof=proof))
    print('Registered', PROFILE, 'target ARM9', sha(target))
