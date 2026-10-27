"""Source-locked complete Guild diplomacy menu captions in existing allocations."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from scripts.probe_common_display_name_hook import branch_link

SOURCE = 'c7a57c51239d92fa843d21f49f7af04e220df8231ebcc451db93b8d6e4a0f016'
SPECS = [(0x143CAC, 12, 0x118C84, '協定締結', 'Sign Pact'),
         (0x143CB8, 12, 0x118C94, '協定破約', 'Break Pact'),
         (0x143CC4, 12, 0x118CB4, '宣戦布告', 'Declare War'),
         (0x143CD0, 12, 0x118C74, '親善交歓', 'Goodwill'),
         (0x143CFC, 20, 0x118C64, '交渉文書の発送', 'Send Documents')]

EXTRA_SPECS = [(0x143C8C, 8, 0x118CA4, '停戦', 'Truce'),
               (0x143C94, 8, 0x118CC4, '威圧', 'Threaten')]


def transform(source, clean, canonical, *, all_seven=False):
    assert sha(source) == SOURCE
    target = bytearray(source)
    rows = []
    specs = SPECS + EXTRA_SPECS if all_seven else SPECS
    for offset, capacity, field, japanese, english in specs:
        original = japanese.encode('cp932') + bytes(capacity - len(japanese.encode('cp932')))
        replacement = (english.encode('ascii') + bytes(capacity - len(english))
                       if len(english) < capacity else original)
        for arm in (source, clean, canonical):
            assert arm[offset:offset + capacity] == original
            assert struct.unpack_from('<I', arm, field)[0] == 0x02000000 + offset
        target[offset:offset + capacity] = replacement
        rows.append({'offset': offset, 'capacity': capacity, 'pointer_field': field,
                     'Japanese': japanese, 'English': english,
                     'before_hex': original.hex(), 'after_hex': replacement.hex()})
    restored = bytearray(target)
    for offset, capacity, *_ in specs:
        restored[offset:offset + capacity] = source[offset:offset + capacity]
    assert bytes(restored) == source
    saved = bytes(target)
    extra = {}
    if all_seven:
        # Threaten needs its own terminator beyond the original eight-byte slot.
        # Keep the complete word and retain that original Japanese string.
        code = MainCodeFile(saved, BASE)
        before = [bytes(section.data) for section in code.sections]
        cache_plan(saved)
        packed = bytearray(before[3][:-48])
        preserved = len(packed)
        pointer = POOL + len(packed)
        packed.extend(b'Threaten\0')
        packed.extend(bytes(-len(packed) % 32))
        size = len(packed) + 64
        assert POOL + size <= STAGE and STAGE + size + 48 <= 0x023F4000
        packed.extend(wrapper(STAGE + len(packed), STAGE + size, size, saved))
        code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
        changes = []
        for offset, value in [(0x118CC4, pointer),
                              (0x8E4, branch_link(BASE + 0x8E4, STAGE + size - 64)),
                              (0xE45DC, POOL + size)]:
            changes.append({'offset': offset, 'before': struct.unpack_from('<I', saved, offset)[0], 'after': value})
            struct.pack_into('<I', code.sections[0].data, offset, value)
        saved = bytes(code.save())
        parsed = MainCodeFile(saved, BASE)
        restored = bytearray(parsed.sections[0].data)
        for row in changes:
            off = row['offset']
            restored[off:off + 4] = before[0][off:off + 4]
        off = code.codeSettingsOffs
        restored[off:off + 12] = before[0][off:off + 12]
        assert bytes(restored) == before[0]
        assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2))
        assert bytes(parsed.sections[3].data[:preserved]) == before[3][:-48]
        extra = {'Threaten_complete_word_relocated': pointer, 'changes': changes,
                 'inherited_pool_bytes_preserved': preserved, 'cache': cache_plan(saved)}
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved),
                           'records': rows, 'in_place_caption_changes_only_except_declared_Threaten_relocation': True,
                           'additional_Threaten_storage': extra,
                           'changed_records': ['DK4_GUILD_DIPLOMACY_' + str(i) for i in range(len(specs))]}


def apply_release(source, clean, canonical, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] in ('dk4-guild-diplomacy-labels-release-v1', 'dk4-guild-diplomacy-labels-release-v2')
    for name, digest in config['verification_evidence_sha256'].items():
        assert sha(Path(name).read_bytes()) == digest
    saved, plan = transform(source, clean, canonical, all_seven=config['format'].endswith('-v2'))
    assert sha(saved) == config['target_arm9_sha256']
    return saved, plan
