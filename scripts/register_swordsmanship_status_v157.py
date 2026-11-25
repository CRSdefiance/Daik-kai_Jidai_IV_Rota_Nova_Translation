"""Lock visually reviewed complete duel panels and register experimental V157."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.swordsmanship_status_release import apply_release
from dk4tool.rom.nds import NdsImage


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    proof_path = 'work/analysis/swordsmanship_status_native_proof.json'
    proof = json.loads(Path(proof_path).read_text(encoding='utf-8'))
    sheets = ['work/qa/swordsmanship_status_native/' + name + '.png' for name in ('native_sheet', 'parent_sheet')]
    proof['visual_review'] = {'complete': True,
                              'sheets': [{'path': p, 'sha256': sha(Path(p).read_bytes())} for p in sheets],
                              'note': 'All sixteen local and sixteen paired parent panels inspected. Complete skill/HP values and health words survive all three crops, with space before the right border. Parent previews compose the actual native GPU requests on the CPU; hardware gameplay remains pending.'}
    write(proof_path, proof)
    manuscript_path = 'translations/swordsmanship_status_manuscript_v1.json'
    manuscript = json.loads(Path(manuscript_path).read_text(encoding='utf-8'))
    manuscript['records'][0]['review']['formatting'] = True
    manuscript['status'] = 'reviewed-natural-prose-and-native-parent-crops-physical-gameplay-pending'
    write(manuscript_path, manuscript)
    config = {'format': 'dk4-swordsmanship-status-release-v1',
              'source_arm9_sha256': proof['source_arm9_sha256'], 'target_arm9_sha256': proof['target_arm9_sha256'],
              'status': 'experimental-physical-cold-boot-and-gameplay-pending'}
    for key, path in (('manuscript', manuscript_path), ('native_proof', proof_path)):
        config[key] = path
        config[key + '_sha256'] = sha(Path(path).read_bytes())
    config_path = 'translations/swordsmanship_status_release_v1.json'
    write(config_path, config)
    apply_release(NdsImage.open('out/all_routes_combined_v156_candidate.nds'), NdsImage.open('work/clean.nds'), config_path)
    stack_path = 'translations/release_stack.json'
    stack = json.loads(Path(stack_path).read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v156'])
    profile.update({'status': 'experimental', 'swordsmanship_status_release': config_path,
                    'description': 'Complete 435-batch stack and all V156 stages plus natural Fencing/HP/state text. Both native duel slot constructors, three primary crops, full state/numeric pixels, inherited paths and staged boot verified. Physical gameplay pending.',
                    'note': 'Preserves confirmed shared-copy and Ceuta selector repairs; no canonical promotion.'})
    if 'all-routes-unified-v157' in stack['profiles'] and stack['profiles']['all-routes-unified-v157'] != profile:
        raise ValueError('Existing V157 profile differs; investigate')
    stack['profiles']['all-routes-unified-v157'] = profile
    write(stack_path, stack)
    print('Registered experimental V157 with complete natural-English duel statistics and native crop repair.')


if __name__ == '__main__':
    main()
