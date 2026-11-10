"""Freeze the requested v2 mockup and register a complete V4749 successor."""

import copy
import json
from pathlib import Path

from dk4tool.dialogue.font_audit import ASCII_FONT_OFFSET, GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.preview_descender_font_20261022_v2 import edited_font

ROOT = Path('work/font_test_20261027')
CONFIG = Path('translations/experimental_ascii_font_20261027_v2.json')
PROFILE = 'font-descenders-symbols-v2-20261027'
PARENT = Path('out/all_routes_combined_v4749_candidate.nds')
ASSET = Path('translations/fonts/ascii_descenders_symbols_v2.bin')


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    ROOT.mkdir(exist_ok=False)
    registry = Path('translations/release_stack.json')
    old = registry.read_bytes()
    stack = json.loads(old)
    assert PROFILE not in stack['profiles'] and not CONFIG.exists() and not ASSET.exists()
    arm = NdsImage.open(PARENT).read_file('/__arm9__.bin')
    manifest = json.loads(PARENT.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    assert sha(PARENT.read_bytes()) == manifest['candidate_sha256']
    original = GameAsciiFont.from_arm9(arm)
    proposed, _ = edited_font(original)
    mockup = Path('work/font_descender_mockup_20261022_v2')
    assert original.glyphs == (mockup / 'original_ascii_font.bin').read_bytes()
    assert proposed.glyphs == (mockup / 'proposed_ascii_font.bin').read_bytes()
    ASSET.parent.mkdir(exist_ok=True)
    ASSET.write_bytes(proposed.glyphs)
    after = arm[:ASCII_FONT_OFFSET] + proposed.glyphs + arm[ASCII_FONT_OFFSET + len(proposed.glyphs):]
    deps = [ASSET, Path('dk4tool/patch/experimental_ascii_font_v2.py'),
            Path('scripts/preview_descender_font_20261022_v2.py'),
            Path('dk4tool/dialogue/font_audit.py')]
    save(CONFIG, dict(format='dk4-experimental-ascii-font-v2', status='experimental',
        predecessor_profile=manifest['profile'], predecessor_rom=str(PARENT),
        predecessor_rom_sha256=manifest['candidate_sha256'],
        font_asset=str(ASSET), offset=ASCII_FONT_OFFSET,
        source_font_sha256=sha(original.glyphs), target_font_sha256=sha(proposed.glyphs),
        source_ARM9_sha256=sha(arm), target_ARM9_sha256=sha(after),
        design_specification=str(mockup / 'mockup_specification.json'),
        design_specification_sha256=sha((mockup / 'mockup_specification.json').read_bytes()),
        dependencies={str(p): sha(p.read_bytes()) for p in deps}))
    profile = copy.deepcopy(stack['profiles'][manifest['profile']])
    profile['experimental_ascii_font_v2'] = str(CONFIG)
    profile['description'] = ('Complete V4749 translation and repair stack plus the exact user-requested v2 '
        '6x11 ASCII font mockup: raised ordinary glyphs, restored gjpqy descenders and [](){}$_ strokes. '
        'No native code, width, wrapping, line spacing, textbox origin or Japanese font changes. '
        'Experimental test only; promoted main and canonical baseline retained.')
    stack['profiles'][PROFILE] = profile
    (ROOT / 'release_stack_before.json').write_bytes(old)
    save(registry, stack)
    (ROOT / 'release_stack_snapshot.json').write_bytes(registry.read_bytes())
    save(ROOT / 'registration.json', dict(profile=PROFILE, registry_before_sha256=sha(old),
        registry_snapshot_sha256=sha(registry.read_bytes()), parent=str(PARENT),
        parent_sha256=manifest['candidate_sha256'], parent_manifest_sha256=sha(PARENT.with_suffix('.manifest.json').read_bytes()),
        builder_sha256=sha(Path('scripts/build_integrated_release.py').read_bytes()),
        canonical_baseline=stack['canonical_baseline'], promoted_main=stack['latest_promoted_build'],
        accepted_layers_preserved=True, source_profiles_preserved=True))
    print('Registered', PROFILE, 'with exact mockup font', sha(proposed.glyphs))


if __name__ == '__main__':
    main()
