"""Register the exact five approved designs as an isolated integrated successor."""

import copy
import json
from pathlib import Path

from dk4tool.patch.ascii_punctuation_all_20261027 import GLYPHS, propose
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.preview_other_punctuation_20261027 import PROPOSALS

ROOT = Path('work/font_punctuation_all_20261027')
CONFIG = Path('translations/ascii_punctuation_all_20261027_v1.json')
PROFILE = 'font-v2-all-punctuation-one-pixel-20261027'
PARENT = Path('out/font_v2_punctuation_one_pixel_20261027_test.nds')
ROM = Path('out/font_v2_all_punctuation_one_pixel_20261027_test.nds')


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ROOT.mkdir(parents=True, exist_ok=False)
    assert GLYPHS == {char: item['rows'] for char, item in PROPOSALS.items()}
    assert sha(PARENT.read_bytes()) == '9c2494830c3a60655fb09ab5cc67842851cbdbe8609083084ec447b81b363258'
    source = NdsImage.open(PARENT).read_file('/__arm9__.bin')
    target, proof = propose(source)
    (ROOT / 'proposed_ARM9.bin').write_bytes(target)
    dependencies = ['dk4tool/patch/ascii_punctuation_all_20261027.py', 'scripts/preview_other_punctuation_20261027.py']
    assert not CONFIG.exists()
    save(CONFIG, dict(format='dk4-ascii-punctuation-all-20261027-v1', status='experimental',
        predecessor_rom=str(PARENT), predecessor_rom_sha256=sha(PARENT.read_bytes()),
        source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target), proof=proof,
        exact_designs_match_user_reviewed_pixel_sheet=True,
        approved_characters=list(GLYPHS), dependencies={p: sha(Path(p).read_bytes()) for p in dependencies}))
    registry = Path('translations/release_stack.json')
    original = registry.read_bytes()
    (ROOT / 'release_stack_before_registration.json').write_bytes(original)
    stack = json.loads(original)
    assert PROFILE not in stack['profiles']
    profile = copy.deepcopy(stack['profiles']['font-v2-punctuation-one-pixel-20261027'])
    assert profile['status'] == 'experimental'
    profile['description'] = 'User-approved five punctuation designs; full comma/question/improved-letter stack; Y+1 and all spacing unchanged. Experimental test ROM, no main promotion.'
    profile['ascii_punctuation_all_20261027'] = str(CONFIG)
    stack['profiles'][PROFILE] = profile
    assert registry.read_bytes() == original
    save(registry, stack)
    (ROOT / 'release_stack_snapshot.json').write_bytes(registry.read_bytes())
    print(json.dumps(dict(profile=PROFILE, proof=proof), indent=2))
