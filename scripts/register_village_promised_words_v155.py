"""Lock completed village reviews and register the complete experimental V155."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_promised_words_release import SOURCE, apply_release
from dk4tool.rom.nds import NdsImage


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    target = sha(Path('work/analysis/village_promised_words_research_arm9.bin').read_bytes())
    for name, sheets in (
            ('native', ['native_sheet.png']),
            ('title', ['editor_title.png', 'answer_sheet.png'])):
        path = f'work/analysis/village_promised_words_{name}_proof.json'
        proof = json.loads(Path(path).read_text(encoding='utf-8'))
        if proof.get('target_arm9_sha256', proof.get('arm9_sha256')) != target:
            raise ValueError('Village reviewed binary differs')
        proof['visual_review'] = {
            'complete': True,
            'sheets': [{'path': 'work/qa/village_promised_words_native/' + sheet,
                        'sha256': sha(Path('work/qa/village_promised_words_native/' + sheet).read_bytes())}
                       for sheet in sheets],
            'note': 'All 28 dialogue/prompt panels, title and 24 answers visually inspected; complete leading/final glyphs, natural word wrapping and readable spacing.'}
        write(path, proof)
    path = 'translations/village_promised_words_manuscript_v1.json'
    manuscript = json.loads(Path(path).read_text(encoding='utf-8'))
    for row in manuscript['records']:
        row['review']['formatting'] = True
    manuscript['status'] = 'reviewed-prose-and-native-formatting-experimental-physical-gameplay-pending'
    write(path, manuscript)
    config = {'format': 'dk4-village-promised-words-release-v1',
              'source_arm9_sha256': SOURCE, 'target_arm9_sha256': target,
              'status': 'experimental-physical-cold-boot-and-village-composition-pending'}
    for key, evidence_path in (
            ('manuscript', path),
            ('native_proof', 'work/analysis/village_promised_words_native_proof.json'),
            ('keyboard_proof', 'work/analysis/village_promised_words_keyboard_proof.json'),
            ('title_proof', 'work/analysis/village_promised_words_title_proof.json')):
        config[key] = evidence_path
        config[key + '_sha256'] = sha(Path(evidence_path).read_bytes())
    config_path = 'translations/village_promised_words_release_v1.json'
    write(config_path, config)
    saved, _ = apply_release(NdsImage.open('out/all_routes_combined_v154_candidate.nds'),
                             NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'), config_path)
    if sha(saved) != target:
        raise ValueError('Registered village output differs')
    stack_path = 'translations/release_stack.json'
    stack = json.loads(Path(stack_path).read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v154'])
    profile.update({'status': 'experimental', 'village_promised_words_release': config_path,
                    'description': 'Complete 435-batch combined stack plus 54 village answer/clue/message/title strings; native keyboard normalization, literal template scope, pixels and safe staged allocation verified. Physical gameplay pending.',
                    'note': 'Retains confirmed Ceuta selector and shared-copy fixes; no canonical promotion.'})
    if 'all-routes-unified-v155' in stack['profiles'] and stack['profiles']['all-routes-unified-v155'] != profile:
        raise ValueError('Existing V155 profile differs; investigate')
    stack['profiles']['all-routes-unified-v155'] = profile
    write(stack_path, stack)
    print('Registered complete experimental V155 with 54 reviewed village records.')


if __name__ == '__main__':
    main()
