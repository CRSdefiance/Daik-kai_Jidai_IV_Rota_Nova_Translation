"""Save complete native formatting approval and reproducible release evidence."""

import json
from pathlib import Path

from dk4tool.patch.golden_route_viewer_release import CONFIG, EVIDENCE, apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_golden_route_viewer_formatting import TARGET_SHA, approve
from scripts.prepare_golden_route_viewer import MANUSCRIPT, SOURCE_SHA


def main():
    paths = {name: Path(f'work/analysis/golden_route_{part}_v138_proof.json')
             for name, part in (('headings', 'heading'), ('footer', 'footer'), ('empty', 'empty'))}
    evidence = {name: json.loads(path.read_text()) for name, path in paths.items()}
    raw = MANUSCRIPT.read_bytes()
    if sha(raw) != evidence['headings']['manuscript_sha256']:
        raise ValueError('Original source-reviewed Golden Route manuscript changed')
    document = approve(json.loads(raw), evidence)
    document['source_reviewed_manuscript_sha256'] = sha(raw)
    document['native_evidence_sha256'] = {name: sha(path.read_bytes()) for name, path in paths.items()}
    MANUSCRIPT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    EVIDENCE.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    config = {'format': 'dk4-golden-route-viewer-release-v1', 'source_arm9_sha256': SOURCE_SHA,
              'target_arm9_sha256': TARGET_SHA, 'stage': 'after-complete-scene-caption-release',
              'status': 'prepared-experimental-unregistered-runtime-pending',
              'dependencies': {path.as_posix(): sha(path.read_bytes()) for path in (MANUSCRIPT, EVIDENCE)}}
    CONFIG.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    source = NdsImage.open('out/all_routes_combined_v138_candidate.nds').read_file('/__arm9__.bin')
    proposed, report = apply_release(source, CONFIG)
    directory = Path('work/analysis/golden_route_viewer_release_preparation_v138')
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'proposed_arm9.bin').write_bytes(proposed)
    (directory / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('All six native viewer formatting reviews approved; strict complete release reproduces target; runtime remains pending.')


if __name__ == '__main__':
    main()
