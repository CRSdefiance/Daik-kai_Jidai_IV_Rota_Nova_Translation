"""Source-locked natural English for Gallery and shared item-detail labels.

Research only until every native consumer, parent view and release gate is reviewed.
"""

import json
import struct
import textwrap
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.gallery_description_release import CLEAN, compile_rows
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ordinary_name_fidelity_release import BASE, POOL, STAGE, cstring
from dk4tool.patch.village_promised_words_release import resident_components
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_common_display_name_hook import branch_link

SOURCE = 'cf2af4679fb30135b62d0388bbdcc5781d27114d79d47758dc901d9ba4da28a5'
ROWS = (
    ('ITEMS_ACQUIRED', (0x451E0,), 'Items Acquired %d/%d',
     'The number of acquired items out of the complete collection.',
     'Retain both counts. The compiler supplies the original three-character number fields; the native caller supplies total 198.'),
    ('ITEM_ADVICE', (0x45664, 0x4D254), 'Advice',
     'The advice heading for an item.',
     'Retain the command label. Native constructors select it conditionally in menu descriptors; the actual command consumer still needs tracing.'),
    ('ITEM_EFFECT', (0x4D864, 0x4E530), 'Effect',
     'The item effect magnitude.',
     'Retain the effect subject. The formatter provides separate category, role, effect and value columns with narrow tracking.'),
    ('ITEM_EQUIPPED_BY', (0x4D86C,), 'Equipped By',
     'The person currently equipped with the item.',
     'Retain the equipped-person heading. The native name shares this row, so its column moves to x88; do not invent an ownership or family relationship.'),
    ('ITEM_USE', (0x4D874,), 'Use',
     'Use, the heading for an unassigned or usable item.',
     'Retain the native branch meaning. This label is also distinct from the price branch.'),
    ('ITEM_EQUIPPED_SHIP', (0x4D884,), 'Equipped Ship',
     'The ship currently equipped with the item.',
     'Retain ship as the category. The native name shares this row, so its column moves to x88 with a four-pixel gap after the complete heading.'),
)
CATEGORIES = ('Local Product', 'Navigation Gear', 'Weapon', 'Armor', 'Equipment',
              'Figurehead', 'Mystery Item', 'Gift', 'Proof', 'Proof Map', 'Ruin Map', 'Other', 'Ancient Map')
ROLES = ('Captain', 'First Mate', 'Strategist', 'Purser', 'Surveyor', 'Sail Handler',
         'Helmsman', 'Lookout', 'Boarding Leader', 'Gunner', 'Missionary', 'Surgeon',
         'Chief Cook', 'Shipwright', 'Animal Keeper', 'Deckhand')
CATEGORY_MEANINGS = ('A product native to a region.', 'An item used for navigation or sailing.',
                     'A weapon.', 'Protective armor.', 'An item of equipment.',
                     'An ornamental figure mounted at the bow of a ship.', 'A mysterious small object.',
                     'A gift.', 'A regional proof of supremacy.', 'A map to a proof of supremacy.',
                     'A map to a historic ruin.', 'An item in the remaining category.', 'An ancient map.')
ROLE_MEANINGS = ('The commander of a ship.', 'The officer assisting the captain.',
                 'The crew member responsible for strategy.', 'The crew member responsible for accounts and supplies.',
                 'The crew member responsible for surveying.', 'The crew member who handles the sails.',
                 'The crew member who steers the ship.', 'The crew member who keeps watch.',
                 'The leader of the boarding party.', 'The crew member responsible for cannon fire.',
                 'A person who spreads their faith.', 'The physician aboard the ship.',
                 'The crew member responsible for cooking.', 'The worker who builds and repairs ships.',
                 'The crew member who cares for animals.', 'A crew member who performs general deck work.')
COLUMNS = (
    (0x4D698, 0xE3A02034, 0xE3A02058), (0x4E494, 0xE3A02034, 0xE3A02058),
    (0x4D6C4, 0xE3A02068, 0xE3A020B4), (0x4E4C0, 0xE3A02068, 0xE3A020B4),
    (0x4D6D4, 0xE3A03086, 0xE3A030DA), (0x4E4D0, 0xE3A03084, 0xE3A030DA),
    (0x4D800, 0xE3A02030, 0xE3A02058),
    (0x4D5E0, 0xE3A00001, 0xE3E00000), (0x4D5E4, 0xE58D003C, 0xE58D0028),
    (0x4E42C, 0xE3A00001, 0xE3E00000), (0x4E430, 0xE58D0030, 0xE58D001C),
    (0x4D5F0, 0xE3A02006, 0xE3A02005),
)
TYPE_CALLS, ROLE_CALLS = (0x4D660, 0x4E464), (0x4D690, 0x4E48C)
ADVICE_CALLS, RECT_FIELDS = (0x4D834, 0x4E50C), (0x4D88C, 0x4E538)
PARAGRAPH_CALLS = (0x4D840, 0x4E518)


def transform(image, clean_image):
    source, clean = [rom.read_file('/__arm9__.bin') for rom in (image, clean_image)]
    if sha(source) != SOURCE or sha(clean) != CLEAN:
        raise ValueError('Exact V158 and clean Japanese required')
    records, spans = [], []
    for row_id, fields, english, meaning, note in ROWS:
        originals = []
        for field in fields:
            pointer = struct.unpack_from('<I', clean, field)[0]
            raw = cstring(clean, pointer - BASE)
            if struct.unpack_from('<I', source, field)[0] != pointer or cstring(source, pointer - BASE) != raw:
                raise ValueError('Item label Japanese source/owner differs')
            originals.append({'field': field, 'source_pointer': pointer,
                              'source_hex': raw.hex(), 'japanese': raw.decode('cp932')})
            spans.append((field, pointer, pointer + len(raw)))
        compiled = english.replace('%d', '%3d') if row_id == 'ITEMS_ACQUIRED' else compile_rows(english, 1, 40)[0]
        records.append({'id': row_id, 'source_fields': originals, 'japanese': originals[0]['japanese'],
                        'english': english, 'compiled': compiled, 'speaker': 'Item interface',
                        'context': 'Gallery item counter native 02044F6C-02044F9C in a 144x36 view; shared detail native 0204D594 in a 240x96 canvas, and standalone 0204E3F0. Existing Items title is centered around x120/y84. Advice is a separate conditional menu command selected by native constructors; its actual consumer remains pending. Item-only category and crew-role projections occupy x0 and x88, with Effect at x180 and its byte value at x218. Native detail contexts use tracking -1; initial color1 is retained. Owner heading and name share y24; the name moves to x88. Actual resource providers, longer real names and parent composition still need verification.',
                        'source_meaning': meaning, 'localization_note': note,
                        'review': {g: g != 'formatting' for g in ('source', 'context', 'localization', 'naturalness', 'formatting')}})
    owners = []
    for component, base, raw in resident_components(image):
        for at in range(len(raw) - 3):
            pointer = struct.unpack_from('<I', raw, at)[0]
            for field, lo, hi in spans:
                if lo <= pointer <= hi:
                    owners.append((component, base + at, pointer - lo, field))
    if sorted(owners) != sorted(('arm9_section_0', BASE + f, 0, f) for f, lo, hi in spans):
        raise ValueError('Item label has unclassified complete/interior owners')
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    if len(before) != 4 or len(before[3]) != 3632 or code.sections[3].ramAddress != STAGE:
        raise ValueError('Inherited V158 allocation differs')
    packed, moves = bytearray(before[3][:-48]), []
    for row in records:
        pointer = POOL + len(packed)
        raw = row['compiled'].encode('ascii') + b'\0'
        packed.extend(raw)
        for original in row['source_fields']:
            field = original['field']
            struct.pack_into('<I', code.sections[0].data, field, pointer)
            moves.append({'field': field, 'target_pointer': pointer, 'compiled_hex': raw.hex()})
    projected = []
    role_source_table = struct.unpack_from('<I', clean, 0x86334)[0] - BASE
    for kind, table, words in (('CATEGORY', 0x13C350, CATEGORIES), ('ROLE', role_source_table, ROLES)):
        pointers = []
        for index, english in enumerate(words):
            field = table + index * 4
            pointer = struct.unpack_from('<I', clean, field)[0]
            original = cstring(clean, pointer - BASE)
            if struct.unpack_from('<I', source, field)[0] != pointer:
                raise ValueError('Item category/role source getter table differs')
            compiled = compile_rows(english, 1, 16)[0]
            target = POOL + len(packed)
            packed.extend(compiled.encode('ascii') + b'\0')
            pointers.append(target)
            records.append({'id': f'ITEM_{kind}_{index:02d}', 'kind': kind, 'index': index,
                            'source_fields': [{'field': field, 'source_pointer': pointer,
                                               'source_hex': original.hex(), 'japanese': original.decode('cp932')}],
                            'japanese': original.decode('cp932'), 'english': english, 'compiled': compiled,
                            'speaker': 'Item interface',
                            'context': 'Item-only presentation projection in native 0204D594/0204E3F0. Category x0, role x88, effect x180, byte value x218; tracking -1. Global category/role tables and every unrelated getter consumer remain unchanged.',
                            'source_meaning': (CATEGORY_MEANINGS if kind == 'CATEGORY' else ROLE_MEANINGS)[index],
                            'localization_note': 'Complete natural English from the clean source. Figurehead retains the bow ornament; Boarding Leader retains the team leader without inventing a captain rank. Original non-item displays are unchanged pending their own consumer audit.',
                            'review': {g: g != 'formatting' for g in ('source', 'context', 'localization', 'naturalness', 'formatting')}})
        packed.extend(bytes((-len(packed)) % 4))
        target_table = POOL + len(packed)
        packed.extend(struct.pack('<' + 'I' * len(pointers), *pointers))
        projected.append({'kind': kind, 'source_table': BASE + table, 'target_table': target_table,
                          'compiled_pointers': pointers, 'logical_records': len(words)})
    type_table, role_table = [row['target_table'] for row in projected]
    # Private copies preserve the native lookup ABI without changing global
    # type/role getters or consuming more ITCM. Their late pool is reserved by
    # the native main arena and loaded before either item consumer executes.
    role_getter = POOL + len(packed)
    code_role = bytearray(source[0x86314:0x86338])
    struct.pack_into('<I', code_role, 0x20, role_table)
    packed.extend(code_role)
    type_getter = POOL + len(packed)
    code_type = bytearray(source[0x4A740:0x4A768])
    struct.pack_into('<I', code_type, 0x20, type_table)
    packed.extend(code_type)
    type_wrapper = POOL + len(packed)
    code_wrapper = bytearray(source[0x4A430:0x4A448])
    struct.pack_into('<I', code_wrapper, 8, branch_link(type_wrapper + 8, BASE + 0x4A448))
    struct.pack_into('<I', code_wrapper, 12, branch_link(type_wrapper + 12, type_getter))
    packed.extend(code_wrapper)
    common = image.read_file('/COMMON/MESFILE.DK4')
    if sha(common) != 'ea978f466496f8593f13fb97f17b9bac174beea5665c57f1f5e358b2808776c9':
        raise ValueError('Exact inherited COMMON advice required')
    entries = common_message_entries(common, source, clean=False)
    advice, advice_pointers = [], []
    for index in range(198):
        original = entries[index + 0xAFF].text
        if any(byte < 32 and byte != 10 for byte in original):
            raise ValueError('Item advice has an unmapped executable control')
        logical = ' '.join(original.decode('cp932').split())
        # Legacy uppercase macro escapes are display encodings. The private
        # presentation runs after COMMON selection/copy and has no macro pass.
        logical = ''.join(chr(ord(char) - 0xFEE0) if '\uFF21' <= char <= '\uFF3A' else char for char in logical)
        if any(ord(char) > 126 for char in logical):
            raise ValueError('Item advice contains an unclassified CP932 token')
        if not logical or any(ord(char) < 32 for char in logical):
            raise ValueError('Item advice is not a mapped logical ASCII paragraph')
        lines = textwrap.wrap(logical, width=47, break_long_words=False, break_on_hyphens=False)
        if len(lines) > 3 or any(len(line) > 47 for line in lines):
            raise ValueError('Complete item advice exceeds its actual window')
        compiled = '\n'.join(lines)
        if ' '.join(compiled.splitlines()) != logical:
            raise ValueError('Item advice formatter alters existing words')
        pointer = POOL + len(packed)
        packed.extend(compiled.replace('\n', '\0').encode('ascii') + b'\0\0')
        advice_pointers.append(pointer)
        advice.append({'message_id': index + 0xAFF, 'source_hex': original.hex(),
                       'logical': logical, 'compiled': compiled, 'pointer': pointer})
    packed.extend(bytes((-len(packed)) % 4))
    advice_table = POOL + len(packed)
    packed.extend(struct.pack('<198I', *advice_pointers))
    advice_getter = POOL + len(packed)
    # Execute the original native COMMON copy before choosing the item-only
    # formatted presentation. Out-of-range IDs retain the original pointer.
    advice_code = struct.pack('<12I', 0xE92D4010, 0xE1A04000,
                              branch_link(advice_getter + 8, BASE + 0x5528C),
                              0xE59F1014, 0xE0444001, 0xE35400C6, 0x2A000001,
                              0xE59F1008, 0xE7910104, 0xE8BD8010, 0xAFF, advice_table)
    packed.extend(advice_code)
    paragraph_draw = POOL + len(packed)
    # D5404's narrow dispatch renders one line. Draw each compiler-produced
    # NUL-terminated line through that exact native painter with x reset to
    # the rectangle origin and y advanced by the original 12-pixel line height.
    paragraph_code = struct.pack('<19I', 0xE92D4070, 0xE1A04000, 0xE1A05001,
                                 0xE1A00004, 0xE1A01005,
                                 branch_link(paragraph_draw + 20, BASE + 0xD5404),
                                 0xE4D56001, 0xE3560000, 0x1AFFFFFC,
                                 0xE5D56000, 0xE3560000, 0x0A000005,
                                 0xE5942028, 0xE282200C, 0xE5842028,
                                 0xE5942004, 0xE5842024, 0xEAFFFFF0, 0xE8BD8070)
    packed.extend(paragraph_code)
    rectangle_moves = []
    for field, y, bottom in zip(RECT_FIELDS, (36, 24), (72, 60)):
        original = struct.unpack_from('<I', source, field)[0]
        if struct.unpack_from('<4I', source, original - BASE) != (0, y, 240, bottom):
            raise ValueError('Original item advice rectangle differs')
        pointer = POOL + len(packed)
        packed.extend(struct.pack('<4I', 0, y, 239, bottom))
        struct.pack_into('<I', code.sections[0].data, field, pointer)
        rectangle_moves.append({'field': field, 'pointer': pointer, 'rectangle': [0, y, 239, bottom]})
    for fields, original, target in ((TYPE_CALLS, BASE + 0x4A430, type_wrapper),
                                     (ROLE_CALLS, BASE + 0x86314, role_getter),
                                     (ADVICE_CALLS, BASE + 0x5528C, advice_getter),
                                     (PARAGRAPH_CALLS, BASE + 0xD5404, paragraph_draw)):
        for field in fields:
            if struct.unpack_from('<I', source, field)[0] != branch_link(BASE + field, original):
                raise ValueError('Item projection call site differs')
            struct.pack_into('<I', code.sections[0].data, field, branch_link(BASE + field, target))
    for field, expected, replacement in COLUMNS:
        if struct.unpack_from('<I', source, field)[0] != expected:
            raise ValueError('Original effect column differs')
        struct.pack_into('<I', code.sections[0].data, field, replacement)
    used = len(packed)
    size = (used + 31) & ~31
    packed.extend(bytes(size - used))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
    copy_entry = STAGE + size
    for field, value in ((0x8E4, branch_link(BASE + 0x8E4, copy_entry)), (0xE45DC, POOL + size)):
        struct.pack_into('<I', code.sections[0].data, field, value)
    saved = bytes(code.save())
    loaded = MainCodeFile(saved, BASE)
    restored = bytearray(loaded.sections[0].data)
    for field in [r['field'] for r in moves] + [f for f, expected, replacement in COLUMNS] + list(TYPE_CALLS + ROLE_CALLS + ADVICE_CALLS + PARAGRAPH_CALLS + RECT_FIELDS) + [0x8E4, 0xE45DC]:
        restored[field:field + 4] = source[field:field + 4]
    offset = code.codeSettingsOffs
    restored[offset:offset + 12] = source[offset:offset + 12]
    if (bytes(restored) != before[0] or bytes(loaded.sections[1].data) != before[1]
            or bytes(loaded.sections[2].data) != before[2] or packed[:3584] != before[3][:3584]):
        raise ValueError('Item research changes unrelated code/data or inherited pool')
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved),
                   'records': records, 'pointer_moves': moves, 'source_owners': owners,
                   'item_only_projection': projected,
                   'main_pool_helpers': [{'kind': 'role_lookup', 'start': role_getter, 'bytes': len(code_role)},
                                         {'kind': 'type_lookup', 'start': type_getter, 'bytes': len(code_type)},
                                         {'kind': 'type_wrapper', 'start': type_wrapper, 'bytes': len(code_wrapper)},
                                         {'kind': 'advice_lookup', 'start': advice_getter, 'bytes': len(advice_code)},
                                         {'kind': 'paragraph_draw', 'start': paragraph_draw, 'bytes': len(paragraph_code)}],
                   'item_advice_projection': advice, 'advice_table': advice_table,
                   'source_common_sha256': sha(common), 'rectangle_moves': rectangle_moves,
                   'projection_calls': [{'field': f, 'target': type_wrapper} for f in TYPE_CALLS]
                                       + [{'field': f, 'target': role_getter} for f in ROLE_CALLS]
                                       + [{'field': f, 'target': advice_getter} for f in ADVICE_CALLS]
                                       + [{'field': f, 'target': paragraph_draw} for f in PARAGRAPH_CALLS],
                   'layout_instructions': [{'field': f, 'original': expected, 'replacement': replacement}
                                           for f, expected, replacement in COLUMNS],
                   'effect_label_x': 180, 'effect_numeric_x': 218, 'role_x': 88,
                   'owner_name_x': 88, 'detail_tracking': -1,
                   'pool_payload_bytes': size, 'pool_used_bytes': used,
                   'inherited_pool_bytes_preserved': 3584, 'copy_entry': copy_entry,
                   'final_pool_span': [POOL, POOL + size], 'staging_span': [STAGE, STAGE + size + 48],
                   'itcm_bytes': len(before[1]), 'reserved_arena_low': 0x01FFA000,
                   'status': 'research-native-consumers-and-integration-pending'}


def prepare():
    from dk4tool.rom.nds import NdsImage

    saved, plan = transform(NdsImage.open('out/all_routes_combined_v158_candidate.nds'), NdsImage.open('work/clean.nds'))
    Path('work/analysis/item_interface_research_arm9.bin').write_bytes(saved)
    Path('work/analysis/item_interface_plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    manuscript = {'format': 'dk4-item-interface-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
                  'target_locale': 'en-US', 'encoder': 'dialogue-relocatable-v1', 'source_arm9_sha256': CLEAN,
                  'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
                  'records': plan['records'], 'status': plan['status']}
    Path('translations/item_interface_manuscript_v1.json').write_text(json.dumps(manuscript, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared 35 source-reviewed item records: six labels and private 13-category/16-role projections; complete narrow columns; research only.')
