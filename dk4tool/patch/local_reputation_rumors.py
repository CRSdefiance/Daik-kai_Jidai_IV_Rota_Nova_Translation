"""Two source-reviewed rumors, borrowing only neighboring trailing padding."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries

TEXTS = {820: '%s of %s is a well-known local %s.',
         821: '%s of %s is an influential local %s.'}


def transform(common, arm, manuscript):
    validate_natural_dialogue_batch(manuscript)
    authored = {r['message_id']: r['english'].removesuffix('{PAD}') for r in manuscript['records']}
    assert authored == TEXTS
    entries = common_message_entries(common, arm, clean=False)
    assert entries[820].text.rstrip() == entries[821].text == b'%s serves %s as %s.'
    assert all(entries[i].block == 10 for i in range(820, 825))
    container = IlnkContainer.parse(common)
    block = bytearray(container.blocks[10])
    first = entries[820]
    block[first.block_offset:first.block_offset + len(first.text)] = TEXTS[820].encode().ljust(len(first.text), b' ')
    a, b, c, following = [entries[i] for i in (821, 822, 823, 824)]
    assert a.copy_end == b.block_offset and b.copy_end == c.block_offset
    assert c.copy_end == following.block_offset
    assert len(a.text) == 19 and a.copy_end - a.block_offset == 20
    raw = TEXTS[821].encode()
    new_span = (len(raw) + 1 + 3) & ~3
    extra = new_span - (a.copy_end - a.block_offset)
    assert new_span == 40 and extra == 20
    assert c.text.endswith(b' ' * extra)
    # Preserve 822 verbatim, the 823 prose and its existing NUL/alignment bytes.
    tail = bytes(block[c.block_offset:c.copy_end])
    assert tail[:len(c.text)] == c.text
    tail = tail[:len(c.text) - extra] + tail[len(c.text):]
    replacement = raw.ljust(new_span - 1, b' ') + b'\0' + bytes(block[b.block_offset:c.block_offset]) + tail
    assert len(replacement) == following.block_offset - a.block_offset
    block[a.block_offset:following.block_offset] = replacement
    container.blocks[10] = bytes(block)
    target = container.to_bytes()
    mapped = bytearray(arm)
    for entry in (b, c):
        assert struct.unpack_from('<H', arm, entry.table_offset)[0] == entry.block_offset
        struct.pack_into('<H', mapped, entry.table_offset, entry.block_offset + extra)
    after = common_message_entries(target, bytes(mapped), clean=False)
    assert len(target) == len(common) and len(mapped) == len(arm)
    assert [r.message_id for r, s in zip(entries, after) if r.text != s.text] == [820, 821, 823]
    for before, current in zip(entries, after):
        expected = TEXTS[before.message_id].encode() if before.message_id in TEXTS else before.text.rstrip()
        assert current.text.rstrip() == expected
        if before.message_id not in (821, 822, 823):
            assert (before.block, before.block_offset, before.copy_end) == (current.block, current.block_offset, current.copy_end)
    allowed = {entry.table_offset + n for entry in (b, c) for n in range(2)}
    assert all(x == y or i in allowed for i, (x, y) in enumerate(zip(arm, mapped)))
    assert arm[0x14186C:0x141910] == bytes(mapped[0x14186C:0x141910])
    # Portrait rumors use 54058/54160, not the equipment modal parent.
    code = MainCodeFile(bytes(mapped), 0x02000000)
    old_sections = [bytes(s.data) for s in code.sections]
    section = code.sections[4]
    assert section.ramAddress == 0x01FFC000 and len(section.data) == 3900
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    field = 0x54160
    old_call = bytes(code.sections[0].data[field:field + 4])
    assert old_call == bytes(ks.asm('bl 0x01ff9edc', 0x02054160)[0])
    entry = section.ramAddress + len(section.data)
    source = Path(__file__).with_suffix('.asm').read_text(encoding='utf-8')
    suffix = bytes(ks.asm(source, entry)[0])
    assert len(suffix) == 180 and len(section.data) + len(suffix) <= 4096
    code.sections[0].data[field:field + 4] = bytes(ks.asm(f'bl {entry}', 0x02054160)[0])
    section.data.extend(suffix)
    wrapped_arm = bytes(code.save())
    parsed = MainCodeFile(wrapped_arm, 0x02000000)
    assert all(bytes(parsed.sections[i].data) == old_sections[i] for i in (1, 2, 3))
    assert bytes(parsed.sections[4].data[:3900]) == old_sections[4]
    main = bytearray(parsed.sections[0].data)
    main[field:field + 4] = old_call
    main[code.codeSettingsOffs:code.codeSettingsOffs + 12] = old_sections[0][code.codeSettingsOffs:code.codeSettingsOffs + 12]
    assert bytes(main) == old_sections[0]
    report = {'changed_records': ['COMMON_MESSAGE_820', 'COMMON_MESSAGE_821', 'COMMON_MESSAGE_823_PADDING'],
              'changed_ARM9_offset_fields': [b.table_offset, c.table_offset],
              'borrowed_only_message823_trailing_spaces': extra,
              'all3668_visible_selections_preserved_except_two_reviewed_rumors': True,
              'all_other_blocks_and_cache_directory_sizes_unchanged': True,
              'COMMON_file_and_cache_sizes_unchanged': True,
              'post_substitution_word_wrap_message_scope': [820, 821],
              'portrait_parent_return': 0x02054014, 'portrait_macro_call': field,
              'equipment_wrapper_and_all_existing_ITCM_bytes_preserved': True,
              'formatter_first_row_guard_is_scoped_not_authored_prose': True,
              'autoload_suffix_bytes': len(suffix), 'autoload_total_bytes': 4080,
              'all_palettes_fonts_and_arena_limits_unchanged': True,
              'status': 'experimental'}
    return target, wrapped_arm, report


def apply_release(common, arm, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-local-reputation-rumors-v1'
    assert sha(Path(__file__).with_suffix('.asm').read_bytes()) == config['wrapper_asm_sha256']
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    document = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    assert sha(Path(config['manuscript']).read_bytes()) == config['manuscript_sha256']
    common, arm, report = transform(common, arm, document)
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return common, arm, report
