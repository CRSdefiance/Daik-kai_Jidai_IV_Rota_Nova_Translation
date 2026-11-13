"""Prepare a registered caption stage from reviewed clean-source manuscripts."""

import json
from pathlib import Path

from dk4tool.patch.artwork_name_captions import transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/artwork_caption_release_v298')
CONFIG = Path('translations/artwork_name_captions_release_v1.json')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source_rom = Path('out/all_routes_combined_v296_candidate.nds')
    assert sha(source_rom.read_bytes()) == '6096fb457d460c53964f1fe3c7aac33e152ac7eef28fefe6309e202760497833'
    source = NdsImage.open(source_rom).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    review = 'translations/artwork_name_caption_review_v283.json'
    manuscripts = ['translations/scene_caption_manuscript_v2.json',
                   'translations/gallery_description_manuscript_v1.json']
    target, proof = transform(source, clean, read(review), [read(p) for p in manuscripts])
    previous = Path('work/analysis/artwork_name_captions_v283/proposed_arm9_research_only.bin').read_bytes()
    assert target == previous and sha(target) == read(review)['target_arm9_sha256']
    (ROOT / 'proposed_arm9_research_only.bin').write_bytes(target)
    proof['prior_reviewed_native_selector_target_exact'] = True
    (ROOT / 'transform_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    config = {'format': 'dk4-artwork-name-captions-release-v1', 'review': review, 'manuscripts': manuscripts,
              'dependencies_sha256': {p: sha(Path(p).read_bytes()) for p in [review, *manuscripts]},
              'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
              'status': 'experimental-native-caption-proofs-complete-live-unlocked-scenes-pending'}
    CONFIG.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    print(f'16 source-locked captions; target exact prior native proof; {proof["pool_payload_bytes"]} bytes.')


if __name__ == '__main__':
    main()
