"""Record visual review of refreshed V155 BGM evidence without changing a ROM."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha


def main():
    directory = Path('work/qa/bgm_native_titles_v155')
    path = directory / 'report.json'
    report = json.loads(path.read_text(encoding='utf-8'))
    earlier = json.loads(Path('translations/bgm_title_native_layout_evidence_v1.json').read_text(encoding='utf-8'))
    if report['cases'] != earlier['cases'] or len(report['cases']) != 76:
        raise ValueError('BGM native pixels/geometry differ from earlier reviewed title evidence')
    if sha(Path(report['native_lookup_proof']).read_bytes()) != report['native_lookup_proof_sha256']:
        raise ValueError('Refreshed BGM lookup proof changed')
    report.update({'status': 'pass-native-bgm-title-layout-visually-reviewed-gameplay-pending',
                   'visual_review': {'complete': True, 'sheet': str(directory / 'native_sheet.png'),
                                     'sheet_sha256': sha((directory / 'native_sheet.png').read_bytes()),
                                     'note': 'All 38 complete titles inspected; longest title retains both edges in the native 128-pixel panel.'},
                   'all_76_cases_identical_to_previously_reviewed_layout': True,
                   'previous_reviewed_evidence_sha256': sha(Path('translations/bgm_title_native_layout_evidence_v1.json').read_bytes())})
    path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    Path('translations/bgm_title_native_layout_evidence_v155.json').write_text(
        json.dumps({'format': 'dk4-bgm-native-layout-evidence-v2', **report}, indent=2) + '\n', encoding='utf-8')
    print('V155 BGM review saved: 76 identical native rasters and 38 ARM946-modeled lookups; physical gameplay pending.')


if __name__ == '__main__':
    main()
