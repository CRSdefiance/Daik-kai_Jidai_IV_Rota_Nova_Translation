"""Lock reviewed native movement evidence and register complete V156."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.movement_notice_release import apply_release
from dk4tool.rom.nds import NdsImage


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    proof_path = 'work/analysis/movement_notices_native_proof.json'
    proof = json.loads(Path(proof_path).read_text(encoding='utf-8'))
    sheet = 'work/qa/movement_notices_native/native_sheet.png'
    proof['visual_review'] = {'complete': True, 'sheets': [{'path': sheet, 'sha256': sha(Path(sheet).read_bytes())}],
                              'note': 'All 14 unique panels visually inspected; complete natural-English prose, whole words and intact first/final letters. Auto Sail and Fast Sail retain a visible gap in their native cells.'}
    write(proof_path, proof)
    manuscript_path = 'translations/movement_notices_manuscript_v1.json'
    manuscript = json.loads(Path(manuscript_path).read_text(encoding='utf-8'))
    for row in manuscript['records']:
        row['review']['formatting'] = True
    manuscript['status'] = 'reviewed-prose-and-native-formatting-experimental-physical-gameplay-pending'
    write(manuscript_path, manuscript)
    config = {'format': 'dk4-movement-notices-release-v1',
              **{key: proof[key] for key in ('source_arm9_sha256', 'target_arm9_sha256',
                                            'source_common_sha256', 'target_common_sha256')},
              'status': 'experimental-physical-cold-boot-and-composition-pending'}
    for key, path in (('manuscript', manuscript_path), ('native_proof', proof_path)):
        config[key] = path
        config[key + '_sha256'] = sha(Path(path).read_bytes())
    config_path = 'translations/movement_notices_release_v1.json'
    write(config_path, config)
    apply_release(NdsImage.open('out/all_routes_combined_v155_candidate.nds'), NdsImage.open('work/clean.nds'), config_path)
    stack_path = 'translations/release_stack.json'
    stack = json.loads(Path(stack_path).read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v155'])
    profile.update({'status': 'experimental', 'movement_notice_release': config_path,
                    'description': 'Complete 435-batch stack and V155 village repair plus nine reviewed movement/shortage strings. Actual native callers, exact-template literal scope, both status cells, copy alignment and safe staged boot verified. Physical gameplay pending.',
                    'note': 'Preserves confirmed shared-copy and Ceuta selector repairs; no canonical promotion.'})
    if 'all-routes-unified-v156' in stack['profiles'] and stack['profiles']['all-routes-unified-v156'] != profile:
        raise ValueError('Existing V156 profile differs; investigate')
    stack['profiles']['all-routes-unified-v156'] = profile
    write(stack_path, stack)
    print('Registered complete experimental V156 with nine reviewed movement/shortage records.')


if __name__ == '__main__':
    main()
