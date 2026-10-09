"""Save the exact source/context review without weakening conditional row gates."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

DRAFT = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
DRAFT_SHA = '15868e00763421462651ddd9b35ac9c671f9576f4982e5271f848fd1423999ca'
OUTPUT = Path('translations/grand_race_complete_ui_manuscript_v2.json')


def review(draft, clean, coverage, allocation):
    if (draft['translation_policy'] != 'natural-dialogue-v2'
            or draft['target_locale'] != 'en-US' or len(draft['records']) != 51):
        raise ValueError('Exact complete localized manuscript required')
    if sha(clean) != draft['clean_arm9_sha256']:
        raise ValueError('Clean Japanese source differs')
    mapped = {row['id']: row for row in coverage['records']}
    lines = {}
    for selection in allocation['selections']:
        lines.setdefault('GRAND_RACE_UI_' + selection['message'], []).append(selection)
    reviewed = copy.deepcopy(draft)
    pending = []
    for row in reviewed['records']:
        identity = row['id']
        if identity not in mapped or not mapped[identity]['consumer_evidence']:
            raise ValueError('Screen context has no mapped consumer evidence')
        if mapped[identity]['english'] != row['english']:
            raise ValueError('Consumer evidence covers different English')
        for part in row['source_parts_in_reading_order']:
            raw = bytes.fromhex(part['source_hex'])
            offset, size = part['offset'], part['aligned_source_bytes_including_nul']
            if size < len(raw) or clean[offset:offset + size] != raw.ljust(size, b'\0'):
                raise ValueError('Original Japanese or padding differs')
            raw.rstrip(b'\0').decode('cp932')
        ordered = sorted(lines[identity], key=lambda selection: int(selection['key'].rsplit(':', 1)[1]))
        if ' '.join(selection['line'] for selection in ordered) != row['english']:
            raise ValueError('Complete prose is not preserved by allocation')
        for selection in ordered:
            if bytes.fromhex(selection['raw_hex']) != selection['line'].encode('ascii') + b'\0':
                raise ValueError('Saved line leading bytes or terminator differ')
        conditional = mapped[identity]['conditional_result_row']
        row['review'] = {'source': True, 'context': True, 'localization': True,
                         'naturalness': True, 'formatting': not conditional}
        row['review_evidence'] = {
            'consumer_reports': mapped[identity]['consumer_evidence'],
            'presentation': 'Complete prose allocated automatically; mapped native consumer/font previews reviewed.',
            'runtime_verified': False,
            'pending': ['Result-name producer/transfer and widened-frame release gate.'] if conditional else []}
        if conditional:
            pending.append(identity)
    reviewed['status'] = 'source-context-localization-reviewed-eight-result-formatting-gates-pending'
    reviewed['pending_formatting_records'] = pending
    reviewed['integration_blockers'] = [
        'Eight compound result-row formatting gates remain conditional on complete native names and widened frame.',
        'Strict release ownership/dependency validation and registration remain pending.',
        'Full screen/gameplay checks are separate from source/text/font review; no runtime acceptance.']
    reviewed['reviewed_record_counts'] = {'source_context_localization_naturalness': 51,
                                        'native_text_formatting': 43, 'formatting_pending': 8}
    return reviewed


def main():
    if sha(DRAFT.read_bytes()) != DRAFT_SHA:
        raise ValueError('Previously reviewed wording changed; a fresh editorial review is required')
    coverage_path = Path('work/analysis/grand_race_ui_coverage_v136.json')
    allocation_path = Path('work/analysis/grand_race_ui_allocation_v136/report.json')
    coverage, allocation = (json.loads(path.read_text()) for path in (coverage_path, allocation_path))
    if coverage['manuscript_sha256'] != DRAFT_SHA or allocation['manuscript_sha256'] != DRAFT_SHA:
        raise ValueError('Mapped evidence is stale')
    for report in coverage['evidence_reports']:
        if sha(Path(report['path']).read_bytes()) != report['sha256']:
            raise ValueError('Reviewed consumer report changed')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    result = review(json.loads(DRAFT.read_text(encoding='utf-8')), clean, coverage, allocation)
    result['review_lineage'] = {'draft_path': DRAFT.as_posix(), 'draft_sha256': DRAFT_SHA,
                              'coverage_sha256': sha(coverage_path.read_bytes()),
                              'allocation_sha256': sha(allocation_path.read_bytes())}
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('51 source/context/localization reviews saved; 43 native formatting gates approved; eight result rows pending.')


if __name__ == '__main__':
    main()
