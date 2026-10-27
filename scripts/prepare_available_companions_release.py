"""Make durable reviewed release inputs; does not register or build a ROM."""

import json
from pathlib import Path

from dk4tool.patch.available_companions_release import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    proof = read('work/analysis/available_companions_proof.json')
    visual = proof['native_ink_visual_review']
    if (visual['panels_reviewed'] != 1
            or visual['single_row_full_sentence_exclamation_and_leading_final_glyphs'] is not True
            or sha(Path('work/qa/available_companions_native/native_sheet.png').read_bytes())
            != visual['native_sheet_sha256']):
        raise ValueError('Exact inspected companion native ink required')
    manuscript = 'translations/available_companions_manuscript_v1.json'
    document = read(manuscript)
    document['records'][0]['review']['formatting'] = True
    write(manuscript, document)
    pool = 'translations/available_companions_pool_v1.json'
    write(pool, proof['allocation'])
    evidence = 'translations/available_companions_native_review_v1.json'
    proof['status'] = 'reviewed-native-companion-layout-gameplay-pending'
    proof['canonical_acceptance'] = False
    write(evidence, proof)
    config = 'translations/available_companions_release_v1.json'
    write(config, {'format': 'dk4-available-companions-release-v1',
                   'target_arm9_sha256': proof['research_arm9_sha256'],
                   'manuscript': manuscript, 'pool': pool, 'native_review': evidence,
                   'dependencies': {p: sha(Path(p).read_bytes()) for p in (manuscript, pool, evidence)}})
    source = NdsImage.open('out/all_routes_combined_v146_candidate.nds').read_file('/__arm9__.bin')
    saved, report = apply_release(source, config)
    if saved != Path('work/analysis/available_companions_arm9.bin').read_bytes():
        raise ValueError('Production differs from actual native research')
    write('work/analysis/available_companions_release_preparation.json', report)
    print('Strict companion release prepared; all inherited pool owners preserved. ROM integration pending.')


if __name__ == '__main__':
    main()
