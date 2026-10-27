"""Localize movement labels and shortage prose with locked native evidence."""

import bisect
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ordinary_name_fidelity_release import BASE, POOL, STAGE, cstring
from dk4tool.patch.village_promised_words_release import resident_components
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_repack import repack_native_records
from scripts.probe_common_display_name_hook import branch_link
from scripts.probe_common_scoped_word_wrap_hook import wrapper_bytes
from scripts.probe_common_tribute_guarded_wrap import wrap_expanded

SOURCE = '4ff287fff60a49186ad421a68d5117d863c1a4c749534f4c4e585df580f45849'
COMMON = 'e916f6356187d935d18d9fb629be33f2b3db70ee4c4b5b2c913d0e68ceeb53b8'
CLEAN = '0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731'
LABELS = [
    (0x782CC, 'water and food', 'Water and food, a shared supply-name parameter.'),
    (0x782D0, 'automatic travel', 'Automatic movement, the interrupted action parameter.'),
    (0x68A20, 'Auto Sail', 'Automatic movement is in progress, shown as a sailing-mode status.'),
    (0x68A24, 'Fast Sail', 'High-speed movement is in progress, shown as a sailing-mode status.'),
    (0x99638, 'Automatic travel is unavailable.', 'Automatic movement is not possible.'),
]
SHORTAGES = {
    610: ("We've run out of %s. We're stopping %s.", 'The supply has run out; the current movement action will stop.'),
    611: ("No %s left... Stopping %s.", 'The speaker notes that the supply has run out and stops the current action.'),
    612: ("We're out of %s. We'll stop %s.", 'An older speaker states that the supply has run out and they will stop the current action.'),
    613: ("We're out of %s. I'll stop %s.", 'The speaker informally notes the depleted supply and personally stops the current action.'),
}


def scoped_wrapper(address, previous, template_table):
    """Delegate with original SP unless the exact actor-table caller matches."""
    active = address + 100
    body = bytearray(wrapper_bytes(active, 0x01FF9BC8, monthly=True))
    # The existing assembler's final literals lock the portrait caller/table.
    if body[-8:] != struct.pack('<2I', BASE + 0x53F40, BASE + 0x1189C0):
        raise ValueError('Shared word-wrap wrapper literal layout differs')
    body[-8:] = struct.pack('<2I', BASE + 0x53DB8, BASE + 0x118580)
    table_load = struct.pack('<I', 0xE59D0374)
    if body.count(table_load) != 1:
        raise ValueError('Shared wrapper table-stack load differs')
    body = body.replace(table_load, struct.pack('<I', 0xE59D037C))
    delegate = active + len(body)
    literal_copy = delegate + 4
    literals = literal_copy + 20
    if struct.unpack_from('<I', body, 12)[0] != branch_link(active + 12, BASE + 0x53914):
        raise ValueError('Active wrapper macro call differs')
    struct.pack_into('<I', body, 12, branch_link(active + 12, literal_copy))
    words = [0xE59DC264, 0, 0xE15C0003, 0, 0xE59DC27C, 0, 0xE15C0003, 0]
    for at, literal in ((1, literals), (5, literals + 4)):
        words[at] = 0xE59F3000 | (literal - address - at * 4 - 8)
    for at in (3, 7):
        words[at] = 0x1A000000 | (((delegate - address - at * 4 - 8) // 4) & 0xFFFFFF)
    # Even a malformed/unclassified actor index may not enable literal handling:
    # compare the complete NUL-ended selected template against all four exact
    # compiled paragraphs. Preserve all macro arguments and the original SP.
    guard = [0xE92D40F8, 0, 0xE3A05004, 0xE4946004, 0xE1A07009,
             0xE4D63001, 0xE4D7C001, 0xE153000C, 0x1A000003,
             0xE3530000, 0x1AFFFFF9, 0xE8BD40F8, 0,
             0xE2555001, 0x1AFFFFF3, 0xE8BD40F8, 0]
    guard_address = address + 32
    guard[1] = 0xE59F4000 | (literals + 8 - guard_address - 4 - 8)
    for at, target in ((12, active), (16, delegate)):
        guard[at] = 0xEA000000 | (((target - guard_address - at * 4 - 8) // 4) & 0xFFFFFF)
    jump = 0xEA000000 | (((previous - delegate - 8) // 4) & 0xFFFFFF)
    copy = struct.pack('<5I', 0xE4D13001, 0xE4C03001, 0xE3530000, 0x1AFFFFFB, 0xE12FFF1E)
    return (struct.pack('<8I', *words) + struct.pack('<17I', *guard) + body
            + struct.pack('<I', jump) + copy
            + struct.pack('<3I', BASE + 0x53DB8, BASE + 0x118580, template_table))


def status_wrapper(address):
    # Native D5200 is called in the same local context for both 60-pixel labels.
    # Select tracking -1 only at this exact caller; preserve original arguments.
    words = [0xE92D4008, 0xE3E0C000, 0xE580C01C,
             branch_link(address + 12, BASE + 0xD5200), 0xE8BD8008]
    return struct.pack('<5I', *words)


def transform(image, clean_image):
    source = image.read_file('/__arm9__.bin')
    common = image.read_file('/COMMON/MESFILE.DK4')
    clean = clean_image.read_file('/__arm9__.bin')
    if sha(source) != SOURCE or sha(common) != COMMON or sha(clean) != CLEAN:
        raise ValueError('Complete V155 and exact clean Japanese required')
    rows = []
    for field, english, gloss in LABELS:
        pointer = struct.unpack_from('<I', clean, field)[0]
        original = cstring(clean, pointer - BASE)
        if struct.unpack_from('<I', source, field)[0] != pointer or cstring(source, pointer - BASE) != original:
            raise ValueError('Movement label is already changed')
        rows.append({'id': f'MOVEMENT_LABEL_{field:06X}', 'field': field, 'source_pointer': pointer,
                     'source_hex': original.hex(), 'japanese': original.decode('cp932'), 'english': english,
                     'source_meaning': gloss, 'speaker': 'Sailing interface or automatic-travel notice',
                     'context': 'Actual native movement shortage caller 02078260/02078278, sailing bitmap constructor 020687B0 and failure modal 020995C8.',
                     'localization_note': 'Retain complete action/supply meaning. Sailing-mode labels use the existing native five-pixel ASCII tracking in their exact 60-pixel cells; no prose shortened to a byte slot.',
                     'review': {g: g != 'formatting' for g in ('source', 'context', 'localization', 'naturalness', 'formatting')}})
    starts = sorted((r['source_pointer'], r) for r in rows)
    addresses = [a for a, _ in starts]
    owners = []
    for name, base, raw in resident_components(image):
        for at in range(len(raw) - 3):
            pointer = struct.unpack_from('<I', raw, at)[0]
            n = bisect.bisect_right(addresses, pointer) - 1
            if n >= 0:
                lo, row = starts[n]
                if lo <= pointer <= lo + len(bytes.fromhex(row['source_hex'])):
                    owners.append((row['id'], name, base + at, pointer - lo))
    expected = [(r['id'], 'arm9_section_0', BASE + r['field'], 0) for r in rows]
    if sorted(owners) != sorted(expected):
        raise ValueError('Movement strings have unclassified owners: ' + str(set(owners) - set(expected)))
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    if len(code.sections) != 4 or code.sections[3].ramAddress != STAGE or len(before[3]) != 3056:
        raise ValueError('Complete inherited V155 staged payload differs')
    packed = bytearray(before[3][:-48])
    for row in rows:
        while len(packed) % 4:
            packed.append(0)
        row['target_pointer'] = POOL + len(packed)
        packed.extend(row['english'].encode('ascii') + b'\0')
        struct.pack_into('<I', code.sections[0].data, row['field'], row['target_pointer'])
    template_pointers = []
    for english, _ in SHORTAGES.values():
        while len(packed) % 4:
            packed.append(0)
        template_pointers.append(POOL + len(packed))
        packed.extend(english.encode('ascii') + b'\0')
    while len(packed) % 4:
        packed.append(0)
    template_table = POOL + len(packed)
    packed.extend(struct.pack('<4I', *template_pointers))
    used = len(packed)
    size = (used + 31) & ~31
    packed.extend(bytes(size - used))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
    copy_entry = STAGE + size
    struct.pack_into('<I', code.sections[0].data, 0x8E4, branch_link(BASE + 0x8E4, copy_entry))
    struct.pack_into('<I', code.sections[0].data, 0xE45DC, POOL + size)
    old_call = struct.unpack_from('<I', source, 0x54160)[0]
    displacement = old_call & 0xFFFFFF
    if displacement & 0x800000:
        displacement -= 1 << 24
    previous = BASE + 0x54160 + 8 + 4 * displacement
    if old_call >> 24 != 0xEB or previous != 0x01FF9DAC:
        raise ValueError('V155 village/tribute hook dependency differs')
    resident = code.sections[1]
    wrapper = resident.ramAddress + len(resident.data)
    helper = scoped_wrapper(wrapper, previous, template_table)
    status_entry = wrapper + len(helper)
    helper += status_wrapper(status_entry)
    if struct.unpack_from('<I', source, 0x6880C)[0] != branch_link(BASE + 0x6880C, BASE + 0xD5200):
        raise ValueError('Native sailing status formatter call differs')
    resident.data.extend(helper)
    low = (resident.ramAddress + len(resident.data) + 31) & ~31
    if low > 0x01FFA000:
        raise ValueError('Movement helpers overlap overlay arena')
    for field, value in ((0x54160, branch_link(BASE + 0x54160, wrapper)),
                         (0x6880C, branch_link(BASE + 0x6880C, status_entry)), (0xE45E4, low)):
        struct.pack_into('<I', code.sections[0].data, field, value)
    staged = bytes(code.save())
    loaded = MainCodeFile(staged, BASE)
    restored = bytearray(loaded.sections[0].data)
    for field in (0x8E4, 0xE45DC, 0x54160, 0x6880C, 0xE45E4, *(r['field'] for r in rows)):
        restored[field:field + 4] = source[field:field + 4]
    off = code.codeSettingsOffs
    restored[off:off + 12] = source[off:off + 12]
    if (bytes(restored) != before[0] or bytes(loaded.sections[1].data) != before[1] + helper
            or bytes(loaded.sections[2].data) != before[2] or packed[:3008] != before[3][:3008]):
        raise ValueError('Movement research changes unrelated code/data or inherited payload')
    source_entries = common_message_entries(clean_image.read_file('/COMMON/MESFILE.DK4'), clean)
    current = common_message_entries(common, source, clean=False)
    prose = []
    for mid, (english, gloss) in SHORTAGES.items():
        original = source_entries[mid]
        prose.append({'id': f'MOVEMENT_SHORTAGE_{mid}', 'message_id': mid,
                      'source_hex': original.text.hex(), 'japanese': original.text.decode('cp932'),
                      'english': english, 'source_meaning': gloss, 'speaker': 'Selected crew member',
                      'context': 'Actual actor-variant table 02118580 and varargs wrapper 02053D44, selected by the automatic-travel interruption caller.',
                      'localization_note': 'Retain supply depletion and stopping the current action. Two original substitutions are preserved. Runtime wrapping occurs after complete substitution; prose is one paragraph.',
                      'review': {g: g != 'formatting' for g in ('source', 'context', 'localization', 'naturalness', 'formatting')}})
    target_owners = {(current[mid].block, current[mid].record_index) for mid in SHORTAGES}
    preserved = {e.message_id: e.text for e in current
                 if (e.block, e.record_index) in target_owners and e.message_id not in SHORTAGES}
    blocks = IlnkContainer.parse(common).blocks
    prefixes = {}
    for owner in target_owners:
        first = next(e for e in current if (e.block, e.record_index) == owner)
        prefixes[owner] = blocks[owner[0]].split(b'\0')[owner[1]][:first.start]
    result = repack_native_records(common, staged, {mid: text.encode('ascii') for mid, (text, _) in SHORTAGES.items()},
                                   prefixes, preserved_packed_neighbors=preserved, spare_padding_before_first_entry=True)
    return result.arm9, result.common, {
        'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(result.arm9),
        'source_common_sha256': COMMON, 'target_common_sha256': sha(result.common),
        'records': rows + prose, 'owner_references': owners,
        'preserved_packed_neighbors': {mid: raw.hex() for mid, raw in preserved.items()},
        'common_changed_records': sorted(result.changed_records), 'common_changed_offsets': sorted(result.changed_offsets),
        'pool_payload_bytes': size, 'pool_used_bytes': used, 'copy_entry': copy_entry,
        'final_pool_span': [POOL, POOL + size], 'staging_span': [STAGE, STAGE + size + 48],
        'portrait_wrapper': wrapper, 'previous_portrait_wrapper': previous, 'status_wrapper': status_entry,
        'exact_template_table': template_table, 'exact_template_pointers': template_pointers,
        'resident_append_bytes': len(helper), 'itcm_bytes': len(resident.data), 'reserved_arena_low': low,
        'status': 'research-prose-reviewed-native-input-layout-and-integration-pending'}


def apply_release(image, clean_image, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-movement-notices-release-v1':
        raise ValueError('Wrong movement release format')
    saved, common, plan = transform(image, clean_image)
    for key, expected in (('source_arm9_sha256', SOURCE), ('source_common_sha256', COMMON),
                          ('target_arm9_sha256', sha(saved)), ('target_common_sha256', sha(common))):
        if config[key] != expected:
            raise ValueError('Movement release identities differ')

    def locked(key):
        path = Path(config[key])
        if sha(path.read_bytes()) != config[key + '_sha256']:
            raise ValueError('Movement evidence changed: ' + key)
        return json.loads(path.read_text(encoding='utf-8'))

    manuscript = locked('manuscript')
    validate_natural_dialogue_batch(manuscript)
    if (manuscript['translation_policy'] != 'natural-dialogue-v2' or manuscript['target_locale'] != 'en-US'
            or manuscript['source_arm9_sha256'] != CLEAN or len(manuscript['records']) != 9):
        raise ValueError('Movement clean-source editorial coverage differs')
    for row, expected in zip(manuscript['records'], plan['records'], strict=True):
        if ({k: v for k, v in row.items() if k != 'review'}
                != {k: v for k, v in expected.items() if k != 'review'}):
            raise ValueError('Movement complete source/prose review differs')
    proof = locked('native_proof')
    if (any(proof[k] != config[k] for k in ('source_arm9_sha256', 'target_arm9_sha256',
                                           'source_common_sha256', 'target_common_sha256'))
            or [len(proof[k]) for k in ('native_preparation_cases', 'paired_pixel_cases',
                                       'inherited_monthly_scope_cases', 'complete_template_rejection_cases',
                                       'inherited_village_callers', 'inherited_names', 'inherited_shared_owners',
                                       'native_block7_warm_cold_arm946_copies')] != [24, 28, 9, 4, 54, 207, 239, 208]
            or proof['common_selected_entries_verified'] != 3668
            or proof['common_changed_ids'] != list(SHORTAGES) or proof['shared_copy_alignment_cases'] != 704
            or not proof['common_directory_block_sizes_and_nul_counts_preserved']
            or proof['sailing_bitmap_geometry']['actual_constructor_arguments'] != [256, 32, 0, 0]):
        raise ValueError('Movement native coverage incomplete')
    expected_selection = (610, 610, 610, 610, 611, 612, 613, 610)
    expected_cases = [(supply, variant) for supply in (None, 0, 1) for variant in range(8)]
    for row, (supply, variant) in zip(proof['native_preparation_cases'], expected_cases, strict=True):
        supply_text = 'water and food' if supply is None else ('Water', 'Food')[supply]
        paragraph = SHORTAGES[expected_selection[variant]][0].replace('%s', supply_text, 1).replace('%s', 'automatic travel', 1)
        if (row['variant'] != variant or row['supply_selector'] != supply
                or row['message_id'] != expected_selection[variant]
                or row['complete_prepared_text'] != wrap_expanded(paragraph)
                or not row['buffer_canaries_and_stack_intact']
                or not row['native_caller_captain_selector_actor_table_common_lookup_sprintf_literal_copy_and_wrap_execute']):
            raise ValueError('Movement complete native preparation differs')
    if (not all(row['complete_glyphs_bounds_independent_pixels_and_whole_words'] for row in proof['paired_pixel_cases'])
            or proof['native_initial_arenas']['low'][0] != plan['final_pool_span'][1]
            or proof['native_initial_arenas']['low'][3] != plan['reserved_arena_low']
            or proof['resident_arena_bounds']['resident_end'] != 0x01FF9FE0):
        raise ValueError('Movement native pixels or arena ownership incomplete')
    boot = proof['boot']
    if (boot['arm7_source_changed_bytes_after_arm9_autoload']
            or not all(row['matches_original'] for row in boot['arm7_native_loaded_sections'])
            or not all(boot[k] for k in ('repaired_pool_matches_complete_payload',
                                        'repair_returns_with_stack_preserved', 'actual_startup_call_preserves_r0_r3'))):
        raise ValueError('Movement staged boot ownership evidence incomplete')
    visual = proof['visual_review']
    if not visual['complete'] or not visual['sheets'] or any(
            sha(Path(row['path']).read_bytes()) != row['sha256'] for row in visual['sheets']):
        raise ValueError('Movement reviewed raster sheet changed or review incomplete')
    return saved, common, {
        **{k: v for k, v in plan.items() if k not in ('records', 'owner_references', 'status')},
        'changed_records': [row['id'] for row in plan['records']],
        'arm9_changed_records': [row['id'] for row in plan['records'][:5]] +
            ['MOVEMENT_LITERAL_TEMPLATE_SCOPE', 'SAILING_STATUS_TRACKING', 'MOVEMENT_STAGED_POOL_AND_ARENAS'] +
            ['MOVEMENT_NATIVE_OFFSET_' + str(offset) for offset in plan['common_changed_offsets']],
        'common_changed_ids': list(SHORTAGES), 'native_preparation_cases': 24,
        'native_pixel_cases': 28, 'native_block7_warm_cold_arm946_copies': 208,
        'inherited_village_callers_preserved': 54, 'shared_copy_alignment_cases': 704,
        'inherited_names_preserved': 207, 'inherited_shared_owners_preserved': 239,
        'common_selected_entries_verified': 3668, 'physical_gameplay_verified': False}
