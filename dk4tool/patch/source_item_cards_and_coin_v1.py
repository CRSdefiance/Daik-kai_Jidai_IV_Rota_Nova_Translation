"""Build source-owned item paragraphs and scope the coin prompt wrapper."""

from struct import pack_into
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.dialogue.layout import format_markup
from dk4tool.dialogue.profiles import DialogueProfile
from dk4tool.patch import rumor_and_cooperation_wrap_v1 as portrait
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from scripts.probe_common_display_name_hook import branch_link


SOURCE = '1dc68b208e3308a1d92da22019c1ce70f2485714bb60d33873ecc65cac7493a3'
PRIOR = 0x01FFE094
HOOK, PARAGRAPH = portrait.HOOK, portrait.PARAGRAPH
DYNAMIC = {(0x02054014, 0x274): (2814,)}
assembly = FunctionType(portrait.assembly.__code__, vars(portrait) | globals())
coin_wrapper = FunctionType(portrait.transform.__code__, vars(portrait) | globals() | {'previous': portrait.previous})
ITEM = DialogueProfile('item-catalogue-native-v1', 235, 3, default_ascii_width=5, line_height_px=12,
                       guard_linebreaks=False, balanced_wrapping=True,
                       metrics_source='240-pixel native advice canvas with minus-one ASCII tracking and three rows')


PROTECTED_PHRASES = ('Southeast Asia', 'New World', 'East Africa', 'southern China',
                     'queen of fruits', 'long oval leaves', 'by hand and foot')


def compile_item(english):
    assert '_' not in english
    markup = english
    for phrase in PROTECTED_PHRASES:
        markup = markup.replace(phrase, phrase.replace(' ', '_'))
    lines = format_markup(markup, ITEM).replace('_', ' ').split('{LB}')
    assert 1 <= len(lines) <= 3 and all(0 < len(line) <= 47 for line in lines), (english, lines)
    assert ' '.join(lines) == english and all(line.isascii() for line in lines)
    return lines, b'\0'.join(line.encode('ascii') for line in lines) + b'\0\0'


def extend_item_payload(source, records, table, pointers, payload):
    before = MainCodeFile(source, BASE)
    assert bytes(before.save()) == source and len(before.sections) == 6
    section = before.sections[3]
    original = bytes(section.data)
    assert section.ramAddress == STAGE and original[:-48] == payload
    parent_cache = cache_plan(source)
    assert parent_cache['payload_bytes'] == len(payload)
    packed, decisions = bytearray(payload), []
    for row in records:
        ident = row['item_ID']
        field = table - POOL + 4 * ident
        old = bytes.fromhex(row['prior_private_hex'])
        at = pointers[ident] - POOL
        assert at >= 0 and payload[at:at + len(old)] == old
        assert row['private_pointer_field'] == table + 4 * ident and pointers[ident] == row['prior_private_pointer']
        lines, compiled = compile_item(row['english'])
        pointer = pointers[ident]
        if compiled != old:
            pointer = POOL + len(packed)
            packed.extend(compiled)
            pack_into('<I', packed, field, pointer)
        decisions.append(dict(item_ID=ident, message_ID=row['message_ID'], field=table + 4 * ident,
            old_pointer=pointers[ident], new_pointer=pointer, compiled_rows=lines, compiled_hex=compiled.hex()))

    packed.extend(bytes(-len(packed) % 32))
    size = len(packed) + 64
    assert POOL + size <= STAGE
    assert STAGE + size + 48 <= 0x02400000
    entry, copy_entry = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(entry, copy_entry, size, source))
    assert len(packed) == size
    section.data = packed + original[-48:-4] + size.to_bytes(4, 'little')
    for at, word in ((0x8E4, branch_link(BASE + 0x8E4, entry)), (0xE45DC, POOL + size)):
        pack_into('<I', before.sections[0].data, at, word)
    target = bytes(before.save())
    new = MainCodeFile(target, BASE)
    parent = MainCodeFile(source, BASE)
    cache = cache_plan(target)
    assert cache['payload_bytes'] == size and len(new.sections) == len(parent.sections)
    assert all((a.ramAddress, a.bssSize) == (b.ramAddress, b.bssSize)
               for a, b in zip(parent.sections, new.sections, strict=True))
    prefix = bytearray(new.sections[3].data[:len(payload)])
    for row in decisions:
        pack_into('<I', prefix, row['field'] - POOL, row['old_pointer'])
    assert prefix == payload
    assert bytes(new.sections[3].data[-48:-4]) == original[-48:-4]
    assert all(bytes(a.data) == bytes(b.data) for i, (a, b) in enumerate(zip(parent.sections, new.sections, strict=True))
               if i not in (0, 3))
    for at, width in ((0x8E4, 4), (0xE45DC, 4), (parent.codeSettingsOffs, 12)):
        new.sections[0].data[at:at + width] = parent.sections[0].data[at:at + width]
    assert new.sections[0].data == parent.sections[0].data
    new.sections[3].data = bytearray(original)
    assert bytes(new.save()) == source
    return target, dict(old_payload_bytes=len(payload), new_payload_bytes=size, new_cache_plan=cache,
        item_paragraphs=decisions, exact_parent_ARM9_inverse=True,
        previous_payload_except_selected_live_pointers_preserved=True)

