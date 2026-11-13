"""Record native text-formatting review after formatter/frame proofs pass."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

MANUSCRIPT = Path('translations/grand_race_complete_ui_manuscript_v2.json')
PROOFS = {
    'printf': Path('work/analysis/grand_race_native_printf_v136_proof.json'),
    'frame': Path('work/analysis/grand_race_native_frame_v136_proof.json'),
    'name_pipeline': Path('work/analysis/grand_race_name_pipeline_v136_proof.json'),
}


def approve(document, proofs):
    printf, frame, pipeline = (proofs[key] for key in ('printf', 'frame', 'name_pipeline'))
    if (printf['status'] != 'pass-actual-native-sprintf-all-reached-helpers'
            or len(printf['cases']) != 320 or printf['case_count'] != 320
            or len(frame['cases']) != 640 or frame['case_count'] != 640
            or frame['status'] != 'pass-native-result-frame-geometry-and-full-glyph-dispatch-with-draw-contracts'
            or printf['proposed_arm9_sha256'] != frame['proposed_arm9_sha256']):
        raise ValueError('Complete native printf/frame proofs required')
    if pipeline['sender_count'] != 40 or pipeline['receiver_count'] != 160 or len(pipeline['cases']) != 40:
        raise ValueError('Complete valid-name caller pipeline required')
    if printf['max_output_bytes_with_nul'] > 32 or printf['max_width_pixels'] > 180:
        raise ValueError('Compound row exceeds its native limits')
    if {(case['place'], case['player']) for case in printf['cases']} != {
            (place, player) for place in range(1, 5) for player in range(1, 5)}:
        raise ValueError('Missing compound result label coverage')
    if any(not case['stack_balanced'] or not case['callee_registers_preserved'] for case in printf['cases']):
        raise ValueError('Printf caller state failed')
    if any(not case['stack_and_callee_registers_preserved'] or not case['renderer_flag_restored']
           or case['text_end_x'] > case['x'] + case['width'] for case in frame['cases']):
        raise ValueError('Native frame bounds or state failed')
    result = copy.deepcopy(document)
    expected = {f'GRAND_RACE_UI_{kind}_{number}' for kind in ('PLACE', 'NUMBER') for number in range(1, 5)}
    found = set()
    for row in result['records']:
        if row['id'] in expected:
            if not all(row['review'][gate] for gate in ('source', 'context', 'localization', 'naturalness')):
                raise ValueError('Editorial review is incomplete')
            row['review']['formatting'] = True
            row['review_evidence']['pending'] = []
            row['review_evidence']['native_result_formatting'] = {
                'complete_printf': True, 'native_frame_geometry_and_glyph_dispatch': True,
                'valid_native_names_up_to_16_bytes': True,
                'conditions': 'Valid terminated native names and successful storage; image/artwork/pixel contracts are explicit.',
                'runtime_verified': False}
            found.add(row['id'])
    if found != expected or len(result['records']) != 51:
        raise ValueError('Complete scoped manuscript and eight result labels required')
    if any(not all(row['review'][gate] for gate in ('source', 'context', 'localization', 'naturalness', 'formatting'))
           for row in result['records']):
        raise ValueError('All fifty-one reviewed native text records are required')
    result['pending_formatting_records'] = []
    result['status'] = 'reviewed-native-text-formatting-experimental-runtime-pending'
    result['reviewed_record_counts'] = {'source_context_localization_naturalness': 51,
                                       'native_text_formatting': 51, 'formatting_pending': 0}
    result['integration_blockers'] = [
        'Strict source/pool/code/geometry ownership and dependency release gates and registration remain pending.',
        'Complete artwork/frame pixel composition, physical save/network behavior and cold-boot gameplay remain unverified.',
        'This approves native text bytes/geometry/dispatch for valid fields; it is not runtime acceptance or goal completion.']
    return result


def main():
    proofs = {name: json.loads(path.read_text()) for name, path in PROOFS.items()}
    if proofs['frame']['printf_proof_sha256'] != sha(PROOFS['printf'].read_bytes()):
        raise ValueError('Frame proof printf lineage differs')
    proposal = Path('work/analysis/grand_race_complete_ui_proposal_v136/proposed_arm9.bin')
    if sha(proposal.read_bytes()) != proofs['printf']['proposed_arm9_sha256']:
        raise ValueError('Actual complete proposal source differs')
    document = approve(json.loads(MANUSCRIPT.read_text(encoding='utf-8')), proofs)
    document['result_formatting_evidence'] = {name: {'path': path.as_posix(), 'sha256': sha(path.read_bytes())}
                                             for name, path in PROOFS.items()}
    MANUSCRIPT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('All 51 native text-formatting reviews recorded; release ownership/dependency and cold-boot gates remain.')


if __name__ == '__main__':
    main()
