"""Prepare reproducible full-caption release gates; do not write a ROM."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.scene_caption_release import (
    CONFIG,
    EVIDENCE,
    MANUSCRIPT,
    SOURCE_SHA,
    TARGET_SHA,
    apply_release,
)
from dk4tool.rom.nds import NdsImage
from scripts.approve_scene_caption_formatting import RASTER, WRAPPERS, approve


def main():
    evidence = {name: json.loads(path.read_text()) for name, path in (('raster', RASTER), ('wrappers', WRAPPERS))}
    document = approve(json.loads(MANUSCRIPT.read_text(encoding='utf-8')), evidence['raster'], evidence['wrappers'])
    MANUSCRIPT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    EVIDENCE.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    config = {'format': 'dk4-scene-caption-release-v1', 'source_arm9_sha256': SOURCE_SHA,
              'target_arm9_sha256': TARGET_SHA, 'status': 'prepared-experimental-unregistered-runtime-pending',
              'dependencies': {path.as_posix(): sha(path.read_bytes()) for path in (MANUSCRIPT, EVIDENCE)},
              'stage': 'after-complete-common-native-reblocking',
              'scope': 'All 164 complete native scene captions; separate COMMON copies remain pending.'}
    CONFIG.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    source = NdsImage.open('out/all_routes_combined_v137_candidate.nds').read_file('/__arm9__.bin')
    proposed, report = apply_release(source, CONFIG)
    directory = Path('work/analysis/scene_caption_release_preparation_v137')
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'proposed_arm9.bin').write_bytes(proposed)
    (directory / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Strict full-caption release reproduces reviewed target; registration/build/gameplay remain pending.')


if __name__ == '__main__':
    main()
