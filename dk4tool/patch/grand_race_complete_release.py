"""Canonical-source components for all reviewed race UI and its native dependencies."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import GATES, sha
from dk4tool.patch.grand_race_waiting_widget import rewrite_function
from dk4tool.rom.nds import NdsImage
from scripts.compile_grand_race_complete_ui_proposal import compile_ui
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE, CANDIDATE_SHA, subtract_ranges

MANUSCRIPT = Path('translations/grand_race_complete_ui_manuscript_v2.json')
DRAFT = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
ALLOCATION = Path('work/analysis/grand_race_ui_allocation_v136/report.json')
PROPOSAL_SHA = '13f89291781011e0835acc025870a0c748299075ea45e713c96bdc9676aae9ab'
SOURCE_SHA = '9a79c25d4a7cf03678a8b5444c3f685a9f675be879109817adb01643141768f5'
DATA = 'translations/grand_race_complete_ui_arm9_v2.json'
CODE = 'translations/grand_race_waiting_widget_arm9_v1.json'
DEPENDENCIES = (DATA, CODE, 'translations/grand_race_help_shared_menu_titles_v2.json',
                'translations/grand_race_menu_arm9_v2.json',
                'translations/grand_race_transition_status_arm9_v2.json',
                'translations/name_editor_atomic_append_arm9_v1.json')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def compile_components(source):
    if sha(source) != SOURCE_SHA or sha(CANDIDATE.read_bytes()) != CANDIDATE_SHA:
        raise ValueError('Complete UI canonical/candidate source differs')
    if sha(DRAFT.read_bytes()) != '15868e00763421462651ddd9b35ac9c671f9576f4982e5271f848fd1423999ca':
        raise ValueError('Original complete prose/source manuscript differs')
    manuscript, draft, allocation = read(MANUSCRIPT), read(DRAFT), read(ALLOCATION)
    if manuscript.get('translation_policy') != 'natural-dialogue-v2' or manuscript.get('target_locale') != 'en-US':
        raise ValueError('Complete UI requires natural English policy')
    if len(manuscript['records']) != 51:
        raise ValueError('All fifty-one complete messages required')
    for row, original in zip(manuscript['records'], draft['records'], strict=True):
        if any(row.get(key) != original.get(key) for key in
               ('id', 'english', 'source_parts_in_reading_order', 'context', 'source_meaning', 'localization_note')):
            raise ValueError('Reviewed complete prose/source/context changed')
        if any(row.get('review', {}).get(gate) is not True for gate in GATES):
            raise ValueError('Complete UI has an incomplete editorial gate')
        for part in row['source_parts_in_reading_order']:
            lo, size = part['offset'], part['aligned_source_bytes_including_nul']
            raw = bytes.fromhex(part['source_hex'])
            if source[lo:lo + size] != raw.ljust(size, b'\0'):
                raise ValueError('Canonical source text/padding differs')
    if allocation['candidate_sha256'] != CANDIDATE_SHA or allocation['manuscript_sha256'] != sha(DRAFT.read_bytes()):
        raise ValueError('Complete allocation lineage differs')
    current = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    proposed, _ = compile_ui(current, allocation, manuscript)
    if sha(proposed) != PROPOSAL_SHA:
        raise ValueError('Complete native-reviewed proposal differs')
    for evidence in manuscript['result_formatting_evidence'].values():
        if sha(Path(evidence['path']).read_bytes()) != evidence['sha256']:
            raise ValueError('Native result proof changed after review')
    _, instructions = rewrite_function(current)
    code_ranges = [(row['offset'], row['offset'] + 4) for row in instructions]
    data_ranges = [tuple(span) for span in subtract_ranges(
        allocation['owned_ranges'], allocation['inherited_reserved_spans'])]
    fields = {field for selection in allocation['selections'] for field in selection['pointer_fields']}
    data_ranges.extend((field, field + 4) for field in sorted(fields)
                       if proposed[field:field + 4] != current[field:field + 4])
    # The third-widget pointer table occupies an already owned pool span.
    if not any(lo <= 0x16B470 and 0x16B47C <= hi for lo, hi in data_ranges):
        raise ValueError('Third-widget table lacks source pool ownership')
    data_ranges.extend(((0xF89DC, 0xF89E0), (0x12ED04, 0x12ED08)))
    # Distinct owner records are mandatory, even when pointers land inside shared strings.
    occupied = set()
    compiled = {}
    for kind, ranges in (('data', sorted(data_ranges)), ('code', sorted(code_ranges))):
        records = []
        for lo, hi in ranges:
            if occupied.intersection(range(lo, hi)):
                raise ValueError('Complete release components overlap')
            occupied.update(range(lo, hi))
            record = {'id': f'GRAND_RACE_COMPLETE_{kind.upper()}_{lo:06X}', 'offset': lo,
                      'source_hex': source[lo:hi].hex().upper(),
                      'replacement_hex': proposed[lo:hi].hex().upper()}
            if kind == 'code':
                record['runtime_address'] = 0x02000000 + lo
            records.append(record)
        compiled[kind] = records
    return compiled, proposed


def validate_release_batch(batch, source, paths):
    policy = batch['native_complete_race_ui']
    if any(Path(path) not in paths for path in DEPENDENCIES):
        raise ValueError('Complete race UI requires all six release dependencies')
    if Path('translations/grand_race_help_arm9_v2.json') in paths:
        raise ValueError('Complete race UI requires shared help variant in place of original help')
    for key, path in (('manuscript', MANUSCRIPT), ('allocation', ALLOCATION)):
        if policy.get(key) != path.as_posix() or policy.get(key + '_sha256') != sha(path.read_bytes()):
            raise ValueError('Complete UI manuscript/allocation is missing or stale')
    dependencies = policy.get('dependencies', {})
    expected = {path: sha(Path(path).read_bytes()) for path in DEPENDENCIES if path not in (DATA, CODE)}
    if dependencies != expected:
        raise ValueError('Complete UI sibling dependencies changed')
    compiled, _ = compile_components(source)
    kind = policy.get('component')
    if kind not in compiled or batch['records'] != compiled[kind]:
        raise ValueError('Complete release records differ from reviewed source/prose/geometry/code')
    if (kind == 'code') != (batch.get('content_type') == 'arm9-inline-code-v1'):
        raise ValueError('Complete UI code must use inline instruction gates')
