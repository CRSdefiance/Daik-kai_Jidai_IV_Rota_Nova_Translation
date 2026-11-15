"""Restore source-locked native blizzard alerts after the complete V140 stack."""

import json
from pathlib import Path

from dk4tool.dialogue.qa import audit_native_common_entry
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_repack import repack_native_records
from scripts.prepare_common_blizzard_repair import TEXT

MANUSCRIPT = Path('translations/common_blizzard_repair_manuscript_v2.json')
EVIDENCE = Path('translations/common_blizzard_preview_evidence_v1.json')
SOURCE_ARM9 = 'd937be33b97b654038d03f1aed57ae30a2a49e0afce7d96ae1e2c972c1b758b3'
SOURCE_COMMON = '254c48e8e9b5aa13821dcda089dc29ab5c86b0b0aa23acbb20828a77c2b63032'


def apply_release(common, arm9, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-common-blizzard-release-v1':
        raise ValueError('Unknown blizzard repair release format')
    if (sha(common) != SOURCE_COMMON or sha(arm9) != SOURCE_ARM9
            or config['source_common_sha256'] != SOURCE_COMMON
            or config['source_arm9_sha256'] != SOURCE_ARM9):
        raise ValueError('Complete V140 blizzard repair parent differs')
    for path in (MANUSCRIPT, EVIDENCE):
        if config['dependencies'].get(path.as_posix()) != sha(path.read_bytes()):
            raise ValueError('Blizzard manuscript/preview review changed')
    document = json.loads(MANUSCRIPT.read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(document)
    evidence = json.loads(EVIDENCE.read_text(encoding='utf-8'))
    if evidence.get('status') != 'reviewed-complete-native-entry-previews':
        raise ValueError('Blizzard preview review is required')
    clean = NdsImage.open('work/clean.nds')
    clean_arm9, clean_common = clean.read_file('/__arm9__.bin'), clean.read_file('/COMMON/MESFILE.DK4')
    source = common_message_entries(clean_common, clean_arm9)
    rows = document['records']
    if len(rows) != 3 or {r['message_id'] for r in rows} != set(TEXT):
        raise ValueError('Complete blizzard owner requires all three native IDs')
    encoded = {}
    reviews = {r['message_id']: r for r in evidence['entries']}
    for row in rows:
        i = row['message_id']
        if bytes.fromhex(row['source_hex']) != source[i].text or (row['block'], row['record']) != (5, 30):
            raise ValueError('Blizzard clean source/owner differs')
        if row['english'] != TEXT[i][0] + '{PAD}':
            raise ValueError('Fresh-source reviewed blizzard wording differs')
        raw = TEXT[i][0].encode('cp932')
        audit = audit_native_common_entry(b' ' * len(raw), row['english'])
        if audit['issues'] or audit['formatted_markup'] != TEXT[i][0] or len(raw) > 36:
            raise ValueError('Blizzard alert must fit one complete native row')
        review = reviews.get(i, {})
        if review.get('english') != TEXT[i][0] or review.get('leading_and_final_glyphs_reviewed') is not True:
            raise ValueError('Complete blizzard preview approval differs')
        encoded[i] = raw
    first = source[389]
    prefix = IlnkContainer.parse(clean_common).blocks[5].split(b'\0')[30][:first.start]
    result = repack_native_records(common, arm9, encoded, {(5, 30): prefix})
    if sha(result.common) != config['target_common_sha256'] or sha(result.arm9) != config['target_arm9_sha256']:
        raise ValueError('Reviewed blizzard repair output differs')
    report = {'status': 'pass-source-reviewed-blizzard-repair-gameplay-pending',
              'authored_ids': sorted(encoded), 'changed_records': sorted(result.changed_records),
              'changed_offsets': sorted(result.changed_offsets),
              'all_native_entries_compared': len(result.entries),
              'parent_common_sha256': SOURCE_COMMON, 'parent_arm9_sha256': SOURCE_ARM9,
              'expected_common_sha256': sha(result.common), 'expected_arm9_sha256': sha(result.arm9),
              'expected_selected_hex': {str(i): raw.hex().upper() for i, raw in encoded.items()},
              'runtime_verified': False}
    return result.common, result.arm9, report
