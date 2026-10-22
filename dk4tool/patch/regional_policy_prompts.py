"""Repair complete regional-policy native COMMON entries without cache growth."""

import json
from pathlib import Path

from dk4tool.dialogue.qa import audit_native_common_entry
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_repack import repack_native_records

MANUSCRIPT = 'translations/regional_policy_prompts_manuscript_v1.json'
SOURCE_ARM = '58f41352f68457bfd6679d4aa996b1c2089b3e765ad6402e95a52b292fc81b64'


def transform(common, arm):
    if sha(arm) != SOURCE_ARM:
        raise ValueError('Regional prompts require the complete V613 plus Shipyard labels')
    source_rom = NdsImage.open('out/all_routes_combined_v613_candidate.nds')
    if common != source_rom.read_file('/COMMON/MESFILE.DK4'):
        raise ValueError('Regional prompts require exact V613 COMMON')
    manuscript_bytes = Path(MANUSCRIPT).read_bytes()
    manuscript = json.loads(manuscript_bytes.decode('utf-8'))
    validate_natural_dialogue_batch(manuscript)
    clean = NdsImage.open('work/clean.nds')
    original = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    entries = common_message_entries(common, arm, clean=False)
    rows = manuscript['records']
    assert [row['message_id'] for row in rows] == list(range(127, 135))
    authored, prefixes = {}, {}
    for row in rows:
        mid = row['message_id']
        selected = original[mid]
        assert selected.message_id == mid and selected.text.hex() == row['source_hex'].lower()
        assert selected.text.decode('cp932') == row['japanese']
        assert (selected.block, selected.record_index) == (row['block'], row['record'])
        entry = entries[mid]
        owner = (entry.block, entry.record_index)
        if owner not in prefixes:
            raw = IlnkContainer.parse(common).blocks[entry.block].split(b'\0')[entry.record_index]
            assert raw[entry.start:entry.start + len(entry.text)] == entry.text
            prefixes[owner] = raw[:entry.start]
        authored[mid] = row['english'].removesuffix('{PAD}').encode('ascii')
    result = repack_native_records(common, arm, authored, prefixes)
    audits = []
    for row in rows:
        entry = result.entries[row['message_id']]
        audit = audit_native_common_entry(entry.text, row['english'])
        if any(issue['severity'] in ('error', 'warning') for issue in audit['issues']):
            raise ValueError(f"Regional prompt {entry.message_id} fails exhaustive QA: {audit['issues']}")
        audits.append({'message_id': entry.message_id, 'audit': audit})
    old_blocks, new_blocks = IlnkContainer.parse(common).blocks, IlnkContainer.parse(result.common).blocks
    assert all(len(a) == len(b) and a.count(b'\0') == b.count(b'\0')
               for a, b in zip(old_blocks, new_blocks, strict=True))
    proof = {'source_common_sha256': sha(common), 'source_arm9_sha256': sha(arm),
             'target_common_sha256': sha(result.common), 'target_arm9_sha256': sha(result.arm9),
             'manuscript': MANUSCRIPT, 'manuscript_sha256': sha(manuscript_bytes),
             'authored_native_IDs': list(authored), 'changed_NUL_owners': sorted(result.changed_records),
             'native_offset_fields': sorted(result.changed_offsets), 'audits': audits,
             'all3668_native_IDs_owners_and_other_text_preserved_except_terminal_padding': True,
             'all41_cache_extents_NUL_counts_and_loader_code_preserved': True,
             'changed_records': [row['id'] for row in rows],
             'experimental': True, 'actual_native_prompt_verification_pending': True, 'full_goal_complete': False}
    # Use JSON-native lists for stable config comparisons after serialization.
    return result.common, result.arm9, json.loads(json.dumps(proof))


def apply_release(common, arm, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-regional-policy-prompts-v1'
    target_common, target_arm, proof = transform(common, arm)
    if config['proof'] != proof:
        raise ValueError('Regional prompt source,manuscript,QA or complete result differs')
    return target_common, target_arm, proof
