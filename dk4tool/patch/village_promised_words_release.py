"""Source-owned village localization with locked native consumer/input evidence."""

import bisect
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ordinary_name_fidelity_release import BASE, POOL, STAGE, cstring
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_tribute_guarded_wrap import wrap_expanded

SOURCE = '6730a45c7b1b74d3125c885f41425bb63442748aec22a1f7844808abfab70764'
CLEAN = '0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731'
PAIRS = [
    ('Aurora', 'the name of the stairway to heaven'),
    ('Kilauea', 'the name of the mountain of fire'),
    ('Sugarloaf Mountain', 'the name of the bell-shaped rock jutting out into the sea'),
    ('Beluga', 'a white whale'),
    ('Moai', 'the stone statues on Easter Island'),
    ('Alaska', 'the name of the great land'),
    ('Champlain', 'the name of the Frenchman who first visited this land'),
    ('Magellan', 'the name of the man who named this land'),
    ('Hekla', 'the name of the mountain that breathes fire'),
    ('Kalahari', 'the desert'),
    ('Erik', 'the name of the hero who discovered this land'),
    ('Bora Bora', 'the name of the island'),
    ('Baikal', 'the name of the lake'),
    ('Terceira', 'the island where Angra do Heroismo is located'),
    ('Yosemite', 'the beautiful valley'),
    ('Svartisen', 'the glacier called Black Ice'),
    ('Purnululu', 'the land covered with sandstone'),
    ('Tawantinsuyu', 'the proper name of the Inca Empire'),
    ('Kamui', 'the name of a god'),
    ('Pinnacles', 'the plain of stone pillars'),
    ('Latte', 'the name of the mysterious stone pillars'),
    ('Tundra', 'the land that never thaws'),
    ('Avacha', 'the name of the mountain of fire in Kamchatka'),
    ('Moa', 'the elusive giant bird'),
]
PREFIX, SUFFIX = 'They say it means ', '.'
MESSAGES = [
    (0x78C48, 0x147E54, 'Captain, the village chief asks to hear the promised words.'),
    (0x78C50, 0x147E8C, PREFIX + '%s' + SUFFIX),
    (0x78C54, 0x147EA4, 'Starting with your next visit, you can use the trading post, tavern, and other facilities.'),
    (0x78C58, 0x147EE4, 'The village chief has left.'),
    (0xAEA40, 0x156058, 'Enter the promised words.'),
    (0xAEA3C, 0x156074, 'Promised Words'),
]
PROPER_NAME_SOURCES = {
    'Sugarloaf Mountain': 'https://whc.unesco.org/en/list/1100/',
    'Erik': 'https://visitgreenland.com/articles/erik-the-red/',
    'Svartisen': 'https://www.visitnorway.com/listings/svartisen-glacier/211934/',
    'Purnululu': 'https://whc.unesco.org/en/list/1094/',
    'Tawantinsuyu': 'https://mnaahp.cultura.pe/exposiciones/salas-permanentes/tawantinsuyu',
}


def literal_wrapper(address, previous, pointers):
    """Bypass legacy bare F/I macros for exactly four newly compiled templates."""
    words = [0xE92D4038]  # preserve r3-r5,lr, aligned 16-byte frame
    loads, branches = [], []
    for pointer in pointers:
        loads.append((len(words), pointer))
        words.extend((0, 0xE1590003, 0))  # LDR r3; CMP r9,r3; BEQ literal
        branches.append(len(words) - 1)
    words.append(0xE8BD4038)
    at = address + len(words) * 4
    words.append(0xEA000000 | (((previous - at - 8) // 4) & 0xFFFFFF))
    literal = len(words)
    words.extend((0xE1A04000, 0xE1A05001))
    loop = len(words)
    words.extend((0xE4D53001, 0xE4C43001, 0xE3530000,
                  0x1A000000 | ((loop - len(words) - 5) & 0xFFFFFF),
                  0xE3A00000, 0xE8BD8038))
    for at in branches:
        words[at] = 0x0A000000 | ((literal - at - 2) & 0xFFFFFF)
    for at, pointer in loads:
        pool_at = len(words)
        words.append(pointer)
        words[at] = 0xE59F3000 | ((pool_at - at - 2) * 4)
    return struct.pack(f'<{len(words)}I', *words)


def input_marker_wrapper(address, header, marker):
    words = [0xE59FC010, 0xE153000C, 0x1A000001, 0xE59FC008, 0xE580C004,
             0xEA000000 | (((BASE + 0xAFBB0 - address - 5 * 4 - 8) // 4) & 0xFFFFFF),
             header, marker]
    return struct.pack('<8I', *words)


def keyboard_ascii_wrapper(address, marker):
    """Convert one full-width key only on the marked village editor instance."""
    words, labels, branches = [], {}, []

    def emit(word):
        words.append(word)

    def jump(label, condition=14):
        branches.append((len(words), label, condition))
        emit(0)

    emit(0xE510C034)  # child r0 = parent+38; provider pointer at parent+4
    marker_load = len(words)
    emit(0)
    emit(0xE15C0002)
    jump('delegate', 1)
    emit(0xE5D1C002)  # one complete two-byte key plus NUL
    emit(0xE35C0000)
    jump('delegate', 1)
    emit(0xE5D1C000)
    emit(0xE5D12001)
    emit(0xE35C0082)
    jump('space', 1)
    emit(0xE3520060)
    jump('digits', 3)
    emit(0xE3520079)
    jump('upper', 9)
    emit(0xE3520081)
    jump('delegate', 3)
    emit(0xE352009A)
    jump('delegate', 8)
    emit(0xE2422020)
    jump('converted')
    labels['digits'] = len(words)
    emit(0xE352004F)
    jump('delegate', 3)
    emit(0xE3520058)
    jump('delegate', 8)
    emit(0xE242201F)
    jump('converted')
    labels['upper'] = len(words)
    emit(0xE242201F)
    jump('converted')
    labels['space'] = len(words)
    emit(0xE35C0081)
    jump('delegate', 1)
    emit(0xE3520040)
    jump('delegate', 1)
    emit(0xE3A02020)
    labels['converted'] = len(words)
    emit(0xE5C12000)
    emit(0xE3A0C000)
    emit(0xE5C1C001)
    labels['delegate'] = len(words)
    at = address + len(words) * 4
    emit(0xEA000000 | (((BASE + 0xB08D8 - at - 8) // 4) & 0xFFFFFF))
    pool_at = len(words)
    emit(marker)
    words[marker_load] = 0xE59F2000 | ((pool_at - marker_load - 2) * 4)
    for at, label, condition in branches:
        words[at] = (condition << 28) | 0x0A000000 | ((labels[label] - at - 2) & 0xFFFFFF)
    return struct.pack(f'<{len(words)}I', *words)


def records(source, clean):
    result = []

    def add(kind, index, field, english, compiled, gloss, note):
        pointer = struct.unpack_from('<I', clean, field)[0]
        if struct.unpack_from('<I', source, field)[0] != pointer:
            raise ValueError('Village owner already relocated; investigate before authoring')
        original = cstring(clean, pointer - BASE)
        if cstring(source, pointer - BASE) != original:
            raise ValueError('Village clean-source bytes differ')
        result.append({'id': f'VILLAGE_{kind}_{index}', 'kind': kind, 'index': index,
                       'field': field, 'source_pointer': pointer, 'source_hex': original.hex(),
                       'japanese': original.decode('cp932'), 'english': english,
                       'compiled_hex': compiled.encode('ascii').hex(),
                       'speaker': 'Village chief conversation' if kind != 'ANSWER' else 'Player password input',
                       'context': 'Native 24-village promise-word tables and input branch at 020788C0; success unlocks facilities on the next visit.',
                       'source_meaning': gloss, 'localization_note': note,
                       'review': {g: g != 'formatting' for g in ('source', 'context', 'localization', 'naturalness', 'formatting')}})

    for index, (answer, meaning) in enumerate(PAIRS):
        if not answer.isascii() or len(answer.encode('ascii')) > 18:
            raise ValueError('Complete village answer exceeds actual native 18-byte input limit')
        note = 'Localize the accepted answer together with its paired clue; preserve native case-sensitive comparison.'
        if index == 2:
            note += ' Japanese phonetics and coastal rock clue identify Pao de Acucar; use its established English name. Deliberately omit the source answer\'s trailing ASCII space.'
        if answer in PROPER_NAME_SOURCES:
            note += ' Proper-name reference: ' + PROPER_NAME_SOURCES[answer] + ' (geographic identification is an inference from the Japanese answer and clue).'
        add('ANSWER', index, 0x1192A8 + 4 * index, answer, answer,
            'Accepted proper name ' + cstring(clean, struct.unpack_from('<I', clean, 0x1192A8 + 4 * index)[0] - BASE).decode('cp932') + '.', note)
        clue = '"' + meaning + '"'
        expanded = wrap_expanded(PREFIX + clue + SUFFIX)
        if not expanded.startswith(PREFIX) or not expanded.endswith(SUFFIX):
            raise ValueError('Clue compilation breaks the common template prefix/suffix')
        compiled = expanded[len(PREFIX):-len(SUFFIX)]
        if compiled.replace('\n  ', ' ') != clue:
            raise ValueError('Compiler changes clue prose')
        add('CLUE', index, 0x1191E8 + 4 * index, clue, compiled,
            'The promised word refers to ' + meaning + '.',
            'Retain the quoted descriptive clue and its paired accepted answer. English remains one paragraph; the compiler budgets the native template prefix and final period before inserting guarded breaks.')
    for index, (field, offset, english) in enumerate(MESSAGES):
        if struct.unpack_from('<I', clean, field)[0] != BASE + offset:
            raise ValueError('Mapped village message pointer differs')
        compiled = english if '%s' in english or index == 5 else wrap_expanded(english)
        gloss = ['The captain is told that the village chief asks to hear the promised words.',
                 'The words reportedly refer to the substituted quoted description.',
                 'From the next port visit, use of the trading, tavern and other facilities will be permitted.',
                 'The village chief has gone away.', 'Please enter the promised words.', 'Promised words.'][index]
        add('MESSAGE', index, field, english, compiled, gloss,
            'Natural English preserves the original request, description, next-visit timing, departure or input-label meaning; no shortening to source allocation.')
    return result


def resident_components(image):
    code = MainCodeFile(image.read_file('/__arm9__.bin'), BASE)
    result = [(f'arm9_section_{n}', section.ramAddress, bytes(section.data)) for n, section in enumerate(code.sections)]
    overlays = loadOverlayTable(image.rom.arm9OverlayTable, lambda oid, fid: image.files[fid])
    result.extend((f'arm9_overlay_{oid}', overlay.ramAddress, bytes(overlay.data)) for oid, overlay in overlays.items())
    return result


def transform(image, clean):
    source = image.read_file('/__arm9__.bin')
    if sha(source) != SOURCE or sha(clean) != CLEAN:
        raise ValueError('Exact complete V154 and clean Japanese required')
    rows = records(source, clean)
    # Exhaustive byte-position scan includes unaligned and interior address words.
    starts = sorted((r['source_pointer'], r) for r in rows)
    addresses = [p for p, _ in starts]
    found = []
    for name, base, raw in resident_components(image):
        for at in range(len(raw) - 3):
            pointer = struct.unpack_from('<I', raw, at)[0]
            n = bisect.bisect_right(addresses, pointer) - 1
            if n >= 0:
                lo, row = starts[n]
                if lo <= pointer <= lo + len(bytes.fromhex(row['source_hex'])):
                    found.append((row['id'], name, base + at, pointer - lo))
    expected = sorted((r['id'], 'arm9_section_0', BASE + r['field'], 0) for r in rows)
    # One pointer-like word straddles MOV r1,r6 / BL 020B4DD8, not a literal.
    # Lock both complete opcodes; do not broadly exempt unaligned references.
    coincidence = ('VILLAGE_CLUE_6', 'arm9_section_0', BASE + 0x2FBDF, 9)
    if source[0x2FBDC:0x2FBE4] != bytes.fromhex('0610a0e17c1402eb'):
        raise ValueError('Reviewed cross-instruction coincidence changed')
    if sorted(found) != sorted(expected + [coincidence]):
        raise ValueError('Village owner has unclassified additional/interior references: ' + str(set(found) - set(expected) - {coincidence}))
    code = MainCodeFile(source, BASE)
    old = bytes(code.sections[3].data)
    if len(old) != 1616 or code.sections[3].ramAddress != STAGE or struct.unpack_from('<I', source, 0xE45DC)[0] != POOL + 1568:
        raise ValueError('V154 staged pool/heap ownership differs')
    packed = bytearray(old[:1568])
    for row in rows:
        while len(packed) % 4:
            packed.append(0)
        row['target_pointer'] = POOL + len(packed)
        packed.extend(bytes.fromhex(row['compiled_hex']) + b'\0')
        struct.pack_into('<I', code.sections[0].data, row['field'], row['target_pointer'])
    used = len(packed)
    size = (used + 31) & ~31
    packed.extend(bytes(size - used))
    entry = STAGE + size
    stub = old[1568:-4] + struct.pack('<I', size)
    if len(stub) != 48 or packed[:1568] != old[:1568] or POOL + size >= STAGE:
        raise ValueError('Village expansion changes inherited storage or overlaps staging')
    code.sections[3].data = packed + stub
    struct.pack_into('<I', code.sections[0].data, 0x8E4, 0xEB000000 | (((entry - BASE - 0x8E4 - 8) // 4) & 0xFFFFFF))
    struct.pack_into('<I', code.sections[0].data, 0xE45DC, POOL + size)
    # The original macro pass treats any bare capital I or F as a command.
    # Complete English proper names must remain literal without changing other
    # callers or Japanese macro semantics. Chain all other templates to V154.
    previous_call = struct.unpack_from('<I', source, 0x54160)[0]
    displacement = previous_call & 0xFFFFFF
    if displacement & 0x800000:
        displacement -= 1 << 24
    previous_target = BASE + 0x54160 + 8 + displacement * 4
    if previous_call >> 24 != 0xEB or not 0x01FF8000 <= previous_target < 0x01FFA000:
        raise ValueError('Inherited monthly hook differs')
    resident = code.sections[1]
    wrapper_address = resident.ramAddress + len(resident.data)
    pointers = [r['target_pointer'] for r in rows if r['kind'] == 'MESSAGE' and r['index'] < 4]
    helper = literal_wrapper(wrapper_address, previous_target, pointers)
    literal_size = len(helper)
    # Native Latin-page cells are full-width CP932. Mark only the editor whose
    # title is this relocated village label, using a semantically identical
    # provider vtable; normalize its selected Latin/digit/space key before the
    # inherited whole-character insertion/capacity check.
    marker_entry = wrapper_address + len(helper)
    marker_table = marker_entry + 32
    keyboard_entry = marker_table + 8
    header = next(r['target_pointer'] for r in rows if r['kind'] == 'MESSAGE' and r['index'] == 5)
    provider = struct.unpack_from('<I', source, 0xB0854)[0]
    if source[provider - BASE:provider - BASE + 8] != struct.pack('<2I', BASE + 0xB10D4, BASE + 0xAE8B8):
        raise ValueError('Original keyboard provider methods differ')
    if any(struct.unpack_from('<I', source, at)[0] != 0xEB000000 | (((target - BASE - at - 8) // 4) & 0xFFFFFF)
           for at, target in ((0xAEBE0, BASE + 0xAFBB0), (0xAED2C, BASE + 0xB08D8))):
        raise ValueError('Native input constructor or key-insertion call differs')
    keyboard_payload = (input_marker_wrapper(marker_entry, header, marker_table)
                        + source[provider - BASE:provider - BASE + 8]
                        + keyboard_ascii_wrapper(keyboard_entry, marker_table))
    helper += keyboard_payload
    resident.data.extend(helper)
    arena_low = (resident.ramAddress + len(resident.data) + 31) & ~31
    if arena_low > 0x01FFA000:
        raise ValueError('Village literal wrapper overlaps overlay allocation')
    struct.pack_into('<I', code.sections[0].data, 0x54160,
                     0xEB000000 | (((wrapper_address - BASE - 0x54160 - 8) // 4) & 0xFFFFFF))
    struct.pack_into('<I', code.sections[0].data, 0xE45E4, arena_low)
    for at, target in ((0xAEBE0, marker_entry), (0xAED2C, keyboard_entry)):
        struct.pack_into('<I', code.sections[0].data, at,
                         0xEB000000 | (((target - BASE - at - 8) // 4) & 0xFFFFFF))
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for at in (0x8E4, 0xE45DC, 0x54160, 0xE45E4, 0xAEBE0, 0xAED2C, *(r['field'] for r in rows)):
        restored[at:at + 4] = source[at:at + 4]
    off = code.codeSettingsOffs
    restored[off:off + 12] = source[off:off + 12]
    original_code = MainCodeFile(source, BASE)
    if (bytes(restored) != bytes(original_code.sections[0].data)
            or bytes(parsed.sections[2].data) != bytes(original_code.sections[2].data)
            or bytes(parsed.sections[1].data) != bytes(original_code.sections[1].data) + helper):
        raise ValueError('Research changes unrelated code, source text, font or renderer bytes')
    plan = {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved), 'records': rows,
            'owner_reference_count': len(expected), 'all_byte_position_references': found,
            'cross_instruction_coincidence': {'reference': coincidence, 'span': [0x2FBDC, 0x2FBE4],
                                              'exact_hex': '0610a0e17c1402eb', 'instructions': ['MOV r1,r6', 'BL 020B4DD8']},
            'copy_entry': entry, 'pool_used_bytes': used, 'pool_payload_bytes': size,
            'final_pool_span': [POOL, POOL + size], 'staging_span': [STAGE, STAGE + size + 48],
            'inherited_pool_bytes_preserved': 1568, 'native_input_capacity_bytes': 18,
            'literal_wrapper': {'entry': wrapper_address, 'size': literal_size, 'payload_hex': helper[:literal_size].hex(),
                                'previous_target': previous_target, 'exact_template_pointers': pointers,
                                'itcm_bytes': len(resident.data), 'reserved_arena_low': arena_low},
            'resident_append_bytes': len(helper), 'resident_append_hex': helper.hex(),
            'keyboard_wrapper': {'marker_entry': marker_entry, 'provider_vtable': marker_table,
                                 'insertion_entry': keyboard_entry, 'header_pointer': header,
                                 'original_provider_vtable': provider, 'payload_hex': keyboard_payload.hex(),
                                 'capacity_alias': {'parent_offset': 0xD8, 'child_offset': 0x38, 'child_capacity_offset': 0xA0}},
            'native_comparison_case_sensitive_preserved': True,
            'status': 'research-only-native-consumer-and-formatting-review-pending'}
    return saved, plan


def apply_release(image: NdsImage, clean: bytes, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-village-promised-words-release-v1':
        raise ValueError('Wrong village release format')
    saved, plan = transform(image, clean)
    if config['source_arm9_sha256'] != SOURCE or config['target_arm9_sha256'] != sha(saved):
        raise ValueError('Village release identities differ')

    def locked(key):
        path = Path(config[key])
        if sha(path.read_bytes()) != config[key + '_sha256']:
            raise ValueError('Village evidence changed: ' + key)
        return json.loads(path.read_text(encoding='utf-8'))

    manuscript = locked('manuscript')
    validate_natural_dialogue_batch(manuscript)
    if (manuscript['translation_policy'] != 'natural-dialogue-v2'
            or manuscript['target_locale'] != 'en-US' or manuscript['source_arm9_sha256'] != CLEAN
            or len(manuscript['records']) != 54):
        raise ValueError('Village clean-source editorial coverage differs')
    for row, expected in zip(manuscript['records'], plan['records'], strict=True):
        if ({k: v for k, v in row.items() if k != 'review'}
                != {k: v for k, v in expected.items() if k != 'review'}):
            raise ValueError('Village complete source/compiled-text review differs')
    native, keyboard, title = [locked(key) for key in ('native_proof', 'keyboard_proof', 'title_proof')]
    if (native['source_arm9_sha256'] != SOURCE or native['target_arm9_sha256'] != sha(saved)
            or keyboard['arm9_sha256'] != sha(saved) or title['arm9_sha256'] != sha(saved)
            or [len(native[k]) for k in ('comparisons', 'incremental_answer_entry', 'boundary_cases',
                                        'native_preparation_cases', 'paired_pixel_cases',
                                        'inherited_monthly_and_unrelated_scope_cases',
                                        'inherited_names', 'inherited_shared_owners')]
            != [96, 24, 38, 54, 56, 9, 207, 239]
            or native['common_selections_preserved'] != 3668
            or native['shared_copy_alignment_cases'] != 704
            or [len(keyboard[k]) for k in ('key_cases', 'complete_answer_cases', 'boundary_cases')] != [156, 24, 15]
            or keyboard['actual_capacity_alias']['parent_D8'] != 18
            or keyboard['actual_capacity_alias']['child_38_plus_A0'] != 18
            or len(title['cases']) != 2 or len(title['actual_input_redraw_cases']) != 48
            or title['actual_bitmap_stack_arguments'] != [108, 12, 1, 0]):
        raise ValueError('Village native/input/pixel coverage incomplete')
    if (not all(r['guards_and_stack_intact'] for r in keyboard['key_cases'] + keyboard['boundary_cases'])
            or not all(r['native_completion_copy_and_19_byte_destination_intact'] for r in keyboard['complete_answer_cases'])
            or native['native_initial_arenas']['low'][0] != plan['final_pool_span'][1]
            or native['native_initial_arenas']['low'][3] != plan['literal_wrapper']['reserved_arena_low']):
        raise ValueError('Village keyboard capacity or reserved arena evidence incomplete')
    boot = native['boot']
    if (boot['arm7_source_changed_bytes_after_arm9_autoload']
            or not all(r['matches_original'] for r in boot['arm7_native_loaded_sections'])
            or not all(boot[k] for k in ('repaired_pool_matches_complete_payload',
                                        'repair_returns_with_stack_preserved', 'actual_startup_call_preserves_r0_r3'))):
        raise ValueError('Village staged boot ownership evidence incomplete')
    for proof in (native, title):
        visual = proof['visual_review']
        if not visual['complete'] or any(sha(Path(r['path']).read_bytes()) != r['sha256'] for r in visual['sheets']):
            raise ValueError('Village reviewed raster sheet changed or review incomplete')
    return saved, {**{k: v for k, v in plan.items() if k not in ('records', 'all_byte_position_references', 'status')},
                   'changed_records': [r['id'] for r in plan['records']],
                   'native_dialogue_pixel_cases': 56, 'native_title_input_pixel_cases': 50,
                   'actual_complete_keyboard_answers': 24, 'shared_copy_alignment_cases': 704,
                   'inherited_names_preserved': 207, 'inherited_shared_owners_preserved': 239,
                   'common_selections_preserved': 3668, 'physical_gameplay_verified': False}
