"""Snapshot reviewed fleet evidence and verify the strict production transform."""

import json
from pathlib import Path

from dk4tool.patch.fleet_name_release import SOURCE, apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    proof = json.loads(Path('work/analysis/fleet_names_v148_native_proof.json').read_text(encoding='utf-8'))
    if sha(Path(proof['native_sheet']).read_bytes()) != proof['native_sheet_sha256']:
        raise ValueError('Inspected fleet ink changed')
    manuscript = 'translations/fleet_name_manuscript_v1.json'
    document = json.loads(Path(manuscript).read_text(encoding='utf-8'))
    for row in document['records']:
        row['review']['formatting'] = True
        row['localization_note'] = ('Complete natural American English preserves affiliation uncertainty and pirate identity. '
                                    'Two mapped displays pass 456 native selector/getter/formatter/glyph cases and ten '
                                    'reviewed panels without clipped or dropped characters. Gameplay and other consumers pending.')
    evidence = 'translations/fleet_name_native_review_v1.json'
    document['review_evidence'] = evidence
    write(manuscript, document)
    write(evidence, proof)
    config = 'translations/fleet_name_release_v1.json'
    write(config, {'format': 'dk4-fleet-name-release-v1', 'source_arm9_sha256': SOURCE,
                   'target_arm9_sha256': proof['research_arm9_sha256'],
                   'manuscript': manuscript, 'native_review': evidence,
                   'dependencies': {p: sha(Path(p).read_bytes()) for p in (manuscript, evidence)}})
    source = NdsImage.open('out/all_routes_combined_v148_candidate.nds').read_file('/__arm9__.bin')
    saved, report = apply_release(source, config)
    if saved != Path('work/analysis/fleet_names_v148_research_arm9.bin').read_bytes():
        raise ValueError('Strict fleet output differs from native research')
    write('work/analysis/fleet_name_release_preparation.json', report)
    print('Strict full fleet-label release prepared; combined integration pending.')


if __name__ == '__main__':
    main()
