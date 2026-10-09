"""Lock reviewed complete Gallery canvases and register experimental V158."""

import copy
import json
from pathlib import Path

from dk4tool.patch.gallery_description_release import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    proof_path = 'work/analysis/gallery_descriptions_native_proof.json'
    proof = json.loads(Path(proof_path).read_text(encoding='utf-8'))
    sheets = ['work/qa/gallery_descriptions_native/native_sheet.png']
    proof['visual_review'] = {'complete': True,
                              'sheets': [{'path': p, 'sha256': sha(Path(p).read_bytes())} for p in sheets],
                              'note': 'All seven complete Gallery text canvases inspected: initial Event Scenes, all four selected captains, Historic Sites and selected-site display. Complete words, first/final letters and native positions are readable. Physical surrounding artwork, GPU output and gameplay remain pending.'}
    write(proof_path, proof)
    manuscript_path = 'translations/gallery_description_manuscript_v1.json'
    manuscript = json.loads(Path(manuscript_path).read_text(encoding='utf-8'))
    for row in manuscript['records']:
        row['review']['formatting'] = True
    manuscript['status'] = 'reviewed-natural-prose-and-native-parent-crops-physical-gameplay-pending'
    write(manuscript_path, manuscript)
    config = {'format': 'dk4-gallery-descriptions-release-v1',
              'source_arm9_sha256': proof['source_arm9_sha256'], 'target_arm9_sha256': proof['target_arm9_sha256'],
              'status': 'experimental-physical-cold-boot-and-gameplay-pending'}
    for key, path in (('manuscript', manuscript_path), ('native_proof', proof_path)):
        config[key] = path
        config[key + '_sha256'] = sha(Path(path).read_bytes())
    config_path = 'translations/gallery_description_release_v1.json'
    write(config_path, config)
    apply_release(NdsImage.open('out/all_routes_combined_v157_candidate.nds'), NdsImage.open('work/clean.nds'), config_path)
    stack_path = 'translations/release_stack.json'
    stack = json.loads(Path(stack_path).read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v157'])
    profile.update({'status': 'experimental', 'gallery_description_release': config_path,
                    'description': 'Complete 435-batch stack and all V157 stages plus eight natural-English Gallery records. Native initial/redraw/captain array selection, title centering, complete pixels, real primary constructor/overlay clear and safe staged boot verified. Physical gameplay pending.',
                    'note': 'Preserves confirmed shared-copy and Ceuta selector repairs; no canonical promotion.'})
    if 'all-routes-unified-v158' in stack['profiles'] and stack['profiles']['all-routes-unified-v158'] != profile:
        raise ValueError('Existing V158 profile differs; investigate')
    stack['profiles']['all-routes-unified-v158'] = profile
    write(stack_path, stack)
    print('Registered experimental V158 with eight natural-English Gallery records across ten active fields.')


if __name__ == '__main__':
    main()
