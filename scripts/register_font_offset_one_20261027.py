"""Register a complete one-pixel-offset candidate without using a revoked parent."""

import copy
import json
from pathlib import Path

from dk4tool.patch.ascii_draw_offset_one_20261027 import propose
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/font_offset_one_20261027')
CONFIG = Path('translations/ascii_draw_offset_one_20261027_v1.json')
PROFILE = 'font-v2-draw-down-one-20261027'
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
    assert stack['profiles'][manifest['profile']]['status'] == 'experimental'
    assert sha(PARENT.read_bytes()) == manifest['candidate_sha256']
    source = NdsImage.open(PARENT).read_file('/__arm9__.bin')
    arm, proof = propose(source)
    diagnosis = Path('work/font_baseline_diagnosis_20261027/offset_one_RESEARCH_ONLY.nds')
    assert arm == NdsImage.open(diagnosis).read_file('/__arm9__.bin')
    deps = ['dk4tool/patch/ascii_draw_offset_one_20261027.py',
            'dk4tool/patch/ascii_draw_offset_20261027_v2.py']
    save(CONFIG, dict(format='dk4-ascii-draw-offset-one-20261027-v1', status='experimental',
        predecessor_rom=str(PARENT), predecessor_rom_sha256=manifest['candidate_sha256'],
        source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(arm), proof=proof,
        dependencies={p: sha(Path(p).read_bytes()) for p in deps}))
    (ROOT / 'proposed_ARM9.bin').write_bytes(arm)
    profile = copy.deepcopy(stack['profiles'][manifest['profile']])
    profile['ascii_draw_offset_one_20261027'] = str(CONFIG)
    profile['description'] = ('Complete V4749/improved-font test stack with guarded ASCII drawingY+1 '
        'to fit original12-pixel glyph cells. Same improved letters and complete footer tails; '
        'biography line spacing and all other layout settings retained. Cached lazy1792-byte '
        'footer allocation and14-row copy preserved. Experimental; promoted main unchanged.')
    stack['profiles'][PROFILE] = profile
    (ROOT / 'release_stack_before.json').write_bytes(before)
    save(registry, stack)
    (ROOT / 'release_stack_snapshot.json').write_bytes(registry.read_bytes())
    save(ROOT / 'registration.json', dict(profile=PROFILE, registry_before_sha256=sha(before),
        registry_snapshot_sha256=sha(registry.read_bytes()), source_profile=manifest['profile'],
        predecessor_sha256=manifest['candidate_sha256'], proof=proof,
        no_revoked_ROM_or_research_ROM_used_as_construction_parent=True,
        compiled_ARM9_equals_confirmed_research_probe=True,
        builder_sha256=sha(Path('scripts/build_integrated_release.py').read_bytes())))
    print('Registered', PROFILE, 'ARM9', sha(arm))
