"""Prepare strict release inputs after inspecting complete native name ink."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.residual_character_name_release import SOURCE, TARGET, apply_release
from dk4tool.rom.nds import NdsImage


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    evidence = 'translations/residual_character_names_native_review_v1.json'
    sheet = 'work/qa/residual_character_names_native/native_sheet.png'
    review = {'getters': read('work/analysis/residual_character_names_proof.json'),
              'paired': read('work/analysis/residual_character_names_paired_pixels_proof.json'),
              'native_ink_visual_review': {'sheet': sheet, 'sheet_sha256': sha(Path(sheet).read_bytes()),
                                          'panels_reviewed': 2, 'rows_reviewed': 4,
                                          'complete_leading_and_final_glyphs': True,
                                          'no_clipping_or_row_overlap': True,
                                          'scope': 'Native fixtures; physical gameplay not claimed.'},
              'physical_gameplay_verified': False, 'canonical_acceptance': False,
              'spelling_basis': {'Vels': 'Established Raphael SC0 block 24 record 8, raphael_deep_route_v89.json.',
                                 'Akaboo': 'Phonetic localization of clean アカブー; no official Latin spelling claimed.'}}
    write(evidence, review)
    manuscript = 'translations/residual_character_names_manuscript_v1.json'
    document = read(manuscript)
    document['review_evidence'] = evidence
    for row in document['records']:
        row['review']['formatting'] = True
        row['localization_note'] += ' Both native paired rows and two fleet displays preserve all characters; physical gameplay pending.'
    write(manuscript, document)
    config = 'translations/residual_character_names_release_v1.json'
    write(config, {'format': 'dk4-residual-character-name-release-v1',
                   'source_arm9_sha256': SOURCE, 'target_arm9_sha256': TARGET,
                   'manuscript': manuscript, 'native_review': evidence,
                   'dependencies': {p: sha(Path(p).read_bytes()) for p in (manuscript, evidence)}})
    source = NdsImage.open('out/all_routes_combined_v149_candidate.nds').read_file('/__arm9__.bin')
    saved, report = apply_release(source, config)
    if saved != Path('work/analysis/residual_character_names_arm9.bin').read_bytes():
        raise ValueError('Strict release differs from native research')
    write('work/analysis/residual_character_names_release_preparation.json', report)
    print('Strict Vels/Akaboo release prepared; full integration pending.')


if __name__ == '__main__':
    main()
