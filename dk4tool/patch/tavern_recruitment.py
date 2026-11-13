"""Restore complete independent recruiting voices within the existing cache."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.dialogue.qa import audit_native_common_entry
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_repack import repack_native_records

ARM = '282ef872ceb9fbf9f0c27a8c315f4ea403f0e68746c5c1c7f3883e63df923651'
COMMON = '378950832d373ae32ec90ae37b9186addb77c6cdab5a8c95fc544086872a759f'
MANUSCRIPT = Path('translations/tavern_recruitment_manuscript_v1.json')
TABLE, CMP = 0x02118360, 0x01FFC668


def transform(common, arm):
    if sha(arm) != ARM or sha(common) != COMMON:
        raise ValueError('Recruitment voices require complete pinned V626')
    manuscript = json.loads(MANUSCRIPT.read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(manuscript)
    rows = manuscript['records']
    assert [r['message_id'] for r in rows] == list(range(897, 904))
    clean = NdsImage.open('work/clean.nds')
    clean_arm = clean.read_file('/__arm9__.bin')
    japanese = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean_arm, clean=True)
    before = common_message_entries(common, arm, clean=False)
    source_blocks = IlnkContainer.parse(common)
    assert struct.unpack_from('<8I', arm, TABLE - 0x02000000) == (897, 0xFFFFFFFF, 898, 899, 900, 901, 902, 903)
    assert arm[0x57408:0x576C4] == clean_arm[0x57408:0x576C4]
    encoded, prefixes, audits = {}, {}, []
    for row in rows:
        n = row['message_id']
        assert row['source_hex'] == japanese[n].text.hex()
        assert row['japanese'] == japanese[n].text.decode('cp932')
        text = row['english'].removesuffix('{PAD}').replace('I', 'Ｉ').replace('F', 'Ｆ')
        raw = text.encode('cp932')
        audit = audit_native_common_entry(b' ' * len(raw), text + '{PAD}')
        assert not [r for r in audit['issues'] if r['severity'] in ('warning', 'error')]
        encoded[n] = raw
        owner = before[n].block, before[n].record_index
        first = next(e for e in before if (e.block, e.record_index) == owner)
        prefixes[owner] = source_blocks.blocks[owner[0]].split(b'\0')[owner[1]][:first.start]
        audits.append({'message_id': n, 'native_entry_audit': audit})
    result = repack_native_records(common, arm, encoded, prefixes)
    code = MainCodeFile(result.arm9, 0x02000000)
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    at = CMP - code.sections[4].ramAddress
    old = bytes(ks.asm('cmp r3,#352', CMP)[0])
    new = bytes(ks.asm('cmp r3,#384', CMP)[0])
    assert bytes(code.sections[4].data[at:at + 4]) == old
    code.sections[4].data[at:at + 4] = new
    target_arm = bytes(code.save())
    old_sections = MainCodeFile(arm, 0x02000000).sections
    new_sections = MainCodeFile(target_arm, 0x02000000).sections
    for i, s in enumerate(new_sections):
        restored = bytearray(s.data)
        if i == 0:
            for offset in result.changed_offsets:
                restored[offset:offset + 2] = old_sections[0].data[offset:offset + 2]
        if i == 4:
            restored[at:at + 4] = old
        assert restored == old_sections[i].data
    after_blocks = IlnkContainer.parse(result.common)
    assert len(result.common) == len(common)
    for a, b in zip(source_blocks.blocks, after_blocks.blocks, strict=True):
        assert len(a) == len(b) and a.count(b'\0') == b.count(b'\0')
    return result.common, target_arm, {
        'source_arm9_sha256': ARM, 'source_common_sha256': COMMON,
        'target_arm9_sha256': sha(target_arm), 'target_common_sha256': sha(result.common),
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'records': rows, 'all7_native_entry_audits': audits,
        'all3668_native_message_identities_and_all41_cache_extents_NUL_counts_preserved': True,
        'changed_native_uint16_offsets': sorted(result.changed_offsets),
        'changed_packed_NUL_records': [list(x) for x in sorted(result.changed_records)],
        'source_recruitment_voice_table': TABLE, 'source_role_call': 0x020575BC,
        'original_queued_dispatch_cmp': CMP, 'added_only_original_recruitment_table': TABLE,
        'all_other_helper_code_section_extents_staged_pool_cache_startup_and_arenas_exact': True,
        'all_other_messages_preserved_except_reviewed_terminal_space_donors': True,
        'changed_records': [r['id'] for r in rows] + ['RECRUITMENT_QUEUED_VOICE_WORD_WRAP'],
        'experimental': True, 'full_goal_complete': False}


def apply_release(common, arm, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-tavern-recruitment-v1'
    target_common, target_arm, proof = transform(common, arm)
    assert config['proof'] == proof
    return target_common, target_arm, proof
