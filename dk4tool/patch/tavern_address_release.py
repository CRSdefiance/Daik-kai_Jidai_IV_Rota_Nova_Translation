"""Shared Tavern addresses and whole-word portrait dialogue within existing bounds."""

import json
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries

TEXTS = {865: 'Drinks for everyone!',
         871: 'Bravo! A round of applause for %s!',
         873: "With your skills, %s, you'll find it for sure."}


def transform(common, arm, manuscript, slots):
    validate_natural_dialogue_batch(manuscript)
    assert {r['message_id']: r['english'].removesuffix('{PAD}') for r in manuscript['records']} == TEXTS
    before = common_message_entries(common, arm, clean=False)
    blocks = IlnkContainer.parse(common)
    for index, text in TEXTS.items():
        row = before[index]
        raw = text.encode('ascii')
        assert len(raw) <= len(row.text)
        data = bytearray(blocks.blocks[row.block])
        data[row.block_offset:row.block_offset + len(row.text)] = raw.ljust(len(row.text), b' ')
        blocks.blocks[row.block] = bytes(data)
    target = blocks.to_bytes()
    mapped = bytearray(arm)
    assert len(slots) == 8
    for n, row in enumerate(slots):
        pos = row['offset']
        assert pos == 0x143BD0 + n * 8
        assert arm[pos:pos + 8] == bytes.fromhex(row['source_hex'])
        value = b'Sir' if n % 2 == 0 else b"Ma'am"
        mapped[pos:pos + 8] = (value + b'\0').ljust(8, b'\0')
    code = MainCodeFile(bytes(mapped), 0x02000000)
    original = [bytes(s.data) for s in code.sections]
    section = code.sections[4]
    assert section.ramAddress == 0x01FFC000 and len(section.data) == 4080
    prior = Path('dk4tool/patch/local_reputation_rumors.asm').read_text(encoding='utf-8')
    source = Path(__file__).with_suffix('.asm').read_text(encoding='utf-8')
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    assert bytes(section.data[3900:]) == bytes(ks.asm(prior, 0x01FFCF3C)[0])
    suffix = bytes(ks.asm(source, 0x01FFCF3C)[0])
    assert len(suffix) == 192
    section.data[3900:] = suffix
    final_arm = bytes(code.save())
    parsed = MainCodeFile(final_arm, 0x02000000)
    assert len(parsed.sections[4].data) == 4092
    assert len(parsed.sections[4].data) <= 4096
    assert bytes(parsed.sections[4].data[:3900]) == original[4][:3900]
    assert all(bytes(parsed.sections[i].data) == original[i] for i in (1, 2, 3))
    main = bytearray(parsed.sections[0].data)
    main[code.codeSettingsOffs:code.codeSettingsOffs + 12] = original[0][code.codeSettingsOffs:code.codeSettingsOffs + 12]
    assert bytes(main) == original[0]
    after = common_message_entries(target, final_arm, clean=False)
    assert len(target) == len(common)
    for a, b in zip(before, after):
        assert (a.block_offset, a.copy_end, a.block) == (b.block_offset, b.copy_end, b.block)
        expected = TEXTS[a.message_id].encode() if a.message_id in TEXTS else a.text
        assert b.text.rstrip() == expected if a.message_id in TEXTS else b.text == expected
    return target, final_arm, {'changed_records': [f'COMMON_MESSAGE_{i}' for i in TEXTS],
                              'address_slot_offsets': [r['offset'] for r in slots],
                              'portrait_wrap_ids': [820, 821, 870, 871, 872, 873],
                              'all_COMMON_offsets_and_cache_sizes_unchanged': True,
                              'existing_equipment_and_first3900_ITCM_bytes_exact': True,
                              'SDK_section4_bytes': 4092, 'arena_limits_unchanged': True,
                              'unused_original_applause_address_argument_preserved': True,
                              'status': 'experimental'}


def apply_release(common, arm, path):
    c = json.loads(Path(path).read_text(encoding='utf-8'))
    assert sha(common) == c['source_common_sha256'] and sha(arm) == c['source_arm9_sha256']
    assert sha(Path(c['manuscript']).read_bytes()) == c['manuscript_sha256']
    assert sha(Path(__file__).with_suffix('.asm').read_bytes()) == c['wrapper_asm_sha256']
    doc = json.loads(Path(c['manuscript']).read_text(encoding='utf-8'))
    common, arm, report = transform(common, arm, doc, c['address_slots'])
    assert sha(common) == c['target_common_sha256'] and sha(arm) == c['target_arm9_sha256']
    return common, arm, report
