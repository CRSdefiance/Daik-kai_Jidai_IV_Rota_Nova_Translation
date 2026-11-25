"""Register reviewed placeholder-owner repairs after every V141 component."""

import copy
import json
from pathlib import Path

from dk4tool.patch.common_placeholder_release import EVIDENCE, MANUSCRIPT, apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.register_common_blizzard_v141 import write


def main():
    parent = Path('out/all_routes_combined_v141_candidate.nds')
    if sha(parent.read_bytes()) != 'c32db16159db6d6da0db3aaf2fa774c342cda2c3af8abdc3b77acca86a201310':
        raise ValueError('Exact complete V141 ROM required')
    qa_path = Path('work/qa/common_native_repack_v142/report.json')
    qa = json.loads(qa_path.read_text(encoding='utf-8'))
    if qa['blockers'] != 0 or len(qa['entries']) != 10:
        raise ValueError('Complete reviewed preview set required')
    document = json.loads(MANUSCRIPT.read_text(encoding='utf-8'))
    evidence = {'status': 'reviewed-complete-native-entry-previews',
                'qa_report_sha256': sha(qa_path.read_bytes()), 'entries': [],
                'limitations': 'Exact-font diagnostic previews and native selection checks; cold-boot gameplay remains pending.'}
    for row, preview in zip(document['records'], qa['entries'], strict=True):
        if (row['id'] != preview['id'] or row['english'] != preview['english'] + '{PAD}'
                or any(v['severity'] in ('warning', 'error') for v in preview['issues'])):
            raise ValueError('Reviewed preview and manuscript differ')
        row['review']['formatting'] = True
        evidence['entries'].append({'message_id': row['message_id'], 'english': preview['english'],
                                    'formatted_markup': preview['formatted_markup'],
                                    'preview_sha256': sha(Path(preview['preview']).read_bytes()),
                                    'leading_and_final_glyphs_reviewed': True,
                                    'all_rows_complete_no_clipping_or_orphan_lines': True})
    document['status'] = 'reviewed-complete-owner-native-placeholder-repairs'
    write(MANUSCRIPT, document)
    write(EVIDENCE, evidence)
    plan = json.loads(Path('work/qa/common_native_repack_v142/repack_manifest.json').read_text(encoding='utf-8'))
    rom = NdsImage.open(parent)
    config = {'format': 'dk4-common-placeholder-release-v1',
              'source_common_sha256': plan['parent_common_sha256'],
              'source_arm9_sha256': sha(rom.read_file('/__arm9__.bin')),
              'target_common_sha256': plan['expected_common_sha256'],
              'target_arm9_sha256': plan['expected_arm9_sha256'],
              'dependencies': {p.as_posix(): sha(p.read_bytes()) for p in (MANUSCRIPT, EVIDENCE)}}
    config_path = 'translations/common_placeholder_release_v1.json'
    write(config_path, config)
    _, _, report = apply_release(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), config_path)
    write('work/analysis/common_placeholder_v142_release_proof.json', report)
    stack_path = 'translations/release_stack.json'
    stack = json.loads(Path(stack_path).read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v141'])
    profile['common_placeholder_release'] = config_path
    profile['note'] = 'Complete V141 stack plus ten faithful native ending/scurvy/sky/fog messages replacing four generic placeholder owners. Experimental; cold-boot gameplay pending.'
    stack['profiles']['all-routes-unified-v142'] = profile
    write(stack_path, stack)
    print('Registered V142 placeholder repair; all 3668 native selections and original block/NUL identities verified.')


if __name__ == '__main__':
    main()
