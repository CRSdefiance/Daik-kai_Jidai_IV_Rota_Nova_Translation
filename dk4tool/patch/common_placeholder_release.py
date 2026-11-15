"""Restore source-locked generic-placeholder owners after the complete V141 stack."""

import json
from pathlib import Path

from dk4tool.dialogue.qa import audit_native_common_entry
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_repack import repack_native_records
from scripts.prepare_common_placeholder_repairs import TEXT

MANUSCRIPT = Path('translations/common_placeholder_repairs_manuscript_v2.json')
EVIDENCE = Path('translations/common_placeholder_preview_evidence_v1.json')
SOURCE_ARM9 = 'e8728fa77fbc37d39b2bcb99aa796b8cc11cde07c67934d59692621ff6676c4b'
SOURCE_COMMON = '6080ef4e113871609c806e7dc088e7138c1b4a85534aad53be4d492588622485'


def apply_release(common, arm9, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-common-placeholder-release-v1':
        raise ValueError('Unknown placeholder repair release format')
    if (sha(common) != SOURCE_COMMON or sha(arm9) != SOURCE_ARM9
            or config['source_common_sha256'] != SOURCE_COMMON
            or config['source_arm9_sha256'] != SOURCE_ARM9):
        raise ValueError('Complete V141 placeholder repair parent differs')
    for path in (MANUSCRIPT, EVIDENCE):
        if config['dependencies'].get(path.as_posix()) != sha(path.read_bytes()):
            raise ValueError('Placeholder manuscript/preview review changed')
    document = json.loads(MANUSCRIPT.read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(document)
    evidence = json.loads(EVIDENCE.read_text(encoding='utf-8'))
    if evidence.get('status') != 'reviewed-complete-native-entry-previews':
        raise ValueError('Placeholder preview review is required')
    clean = NdsImage.open('work/clean.nds')
    clean_common = clean.read_file('/COMMON/MESFILE.DK4')
    source = common_message_entries(clean_common, clean.read_file('/__arm9__.bin'))
    rows = document['records']
    if len(rows) != len(TEXT) or {r['message_id'] for r in rows} != set(TEXT):
        raise ValueError('Complete placeholder owners require all ten native IDs')
    encoded = {}
    reviews = {r['message_id']: r for r in evidence['entries']}
    for row in rows:
        i = row['message_id']
        if bytes.fromhex(row['source_hex']) != source[i].text or (row['block'], row['record']) != (source[i].block, source[i].record_index):
            raise ValueError('Placeholder clean source/owner differs')
        english = TEXT[i][0].replace('I', 'Ｉ').replace('F', 'Ｆ')
        if row['english'] != english + '{PAD}':
            raise ValueError('Fresh-source reviewed placeholder wording differs')
        raw = english.encode('cp932')
        audit = audit_native_common_entry(b' ' * len(raw), row['english'])
        if any(v['severity'] in ('warning', 'error') for v in audit['issues']):
            raise ValueError('Placeholder native formatting has blockers')
        review = reviews.get(i, {})
        if (review.get('english') != english
                or review.get('formatted_markup') != audit['formatted_markup']
                or review.get('leading_and_final_glyphs_reviewed') is not True):
            raise ValueError('Complete placeholder preview approval differs')
        encoded[i] = raw
    blocks = IlnkContainer.parse(clean_common).blocks
    owners = {(source[i].block, source[i].record_index) for i in encoded}
    prefixes = {}
    for owner in owners:
        first = next(e for e in source if (e.block, e.record_index) == owner)
        prefixes[owner] = blocks[owner[0]].split(b'\0')[owner[1]][:first.start]
    result = repack_native_records(common, arm9, encoded, prefixes)
    if sha(result.common) != config['target_common_sha256'] or sha(result.arm9) != config['target_arm9_sha256']:
        raise ValueError('Reviewed placeholder repair output differs')
    report = {'status': 'pass-source-reviewed-placeholder-repair-gameplay-pending',
              'authored_ids': sorted(encoded), 'changed_records': sorted(result.changed_records),
              'changed_offsets': sorted(result.changed_offsets),
              'all_native_entries_compared': len(result.entries),
              'parent_common_sha256': SOURCE_COMMON, 'parent_arm9_sha256': SOURCE_ARM9,
              'expected_common_sha256': sha(result.common), 'expected_arm9_sha256': sha(result.arm9),
              'expected_selected_hex': {str(i): raw.hex().upper() for i, raw in encoded.items()},
              'runtime_verified': False}
    return result.common, result.arm9, report
