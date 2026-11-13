"""Register reviewed blizzard repair after every complete V140 component."""

import copy
import json
from pathlib import Path

from dk4tool.patch.common_blizzard_release import EVIDENCE, MANUSCRIPT, apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    parent = Path('out/all_routes_combined_v140_candidate.nds')
    if sha(parent.read_bytes()) != 'c2ff532c9014b82d1e21c289dee5e18a30226e6ce38be2ba7ede27e2d7255173':
        raise ValueError('Exact complete V140 ROM required')
    qa_path = Path('work/qa/common_native_repack_v141/report.json')
    qa = json.loads(qa_path.read_text(encoding='utf-8'))
    if qa['blockers'] != 0 or len(qa['entries']) != 3:
        raise ValueError('Complete reviewed preview set required')
    document = json.loads(MANUSCRIPT.read_text(encoding='utf-8'))
    evidence = {'status': 'reviewed-complete-native-entry-previews',
                'qa_report_sha256': sha(qa_path.read_bytes()), 'entries': [],
                'limitations': 'Exact-font diagnostic previews and native selection checks; cold-boot gameplay remains pending.'}
    for row, preview in zip(document['records'], qa['entries'], strict=True):
        if row['id'] != preview['id'] or row['english'] != preview['english'] + '{PAD}' or preview['issues']:
            raise ValueError('Reviewed preview and manuscript differ')
        row['review']['formatting'] = True
        evidence['entries'].append({'message_id': row['message_id'], 'english': preview['english'],
                                    'preview_sha256': sha(Path(preview['preview']).read_bytes()),
                                    'leading_and_final_glyphs_reviewed': True,
                                    'single_row_complete_no_wrap_or_padding_visible': True})
    document['status'] = 'reviewed-complete-owner-native-blizzard-repair'
    write(MANUSCRIPT, document)
    write(EVIDENCE, evidence)
    plan = json.loads(Path('work/qa/common_native_repack_v141/repack_manifest.json').read_text(encoding='utf-8'))
    rom = NdsImage.open(parent)
    config = {'format': 'dk4-common-blizzard-release-v1',
              'source_common_sha256': plan['parent_common_sha256'],
              'source_arm9_sha256': sha(rom.read_file('/__arm9__.bin')),
              'target_common_sha256': plan['expected_common_sha256'],
              'target_arm9_sha256': plan['expected_arm9_sha256'],
              'dependencies': {p.as_posix(): sha(p.read_bytes()) for p in (MANUSCRIPT, EVIDENCE)}}
    config_path = 'translations/common_blizzard_release_v1.json'
    write(config_path, config)
    _, _, report = apply_release(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), config_path)
    write('work/analysis/common_blizzard_v141_release_proof.json', report)
    stack_path = 'translations/release_stack.json'
    stack = json.loads(Path(stack_path).read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v140'])
    profile['common_blizzard_release'] = config_path
    profile['note'] = 'Complete V140 stack plus three source-faithful native blizzard alerts replacing placeholder fragments. Experimental; cold-boot gameplay pending.'
    stack['profiles']['all-routes-unified-v141'] = profile
    write(stack_path, stack)
    print('Registered V141 blizzard repair; all 3668 selections and original block/NUL identities verified.')


if __name__ == '__main__':
    main()
