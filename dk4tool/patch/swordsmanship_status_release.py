"""Localize the complete duel statistics display with locked native evidence."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.movement_notice_release import status_wrapper
from dk4tool.patch.ordinary_name_fidelity_release import BASE, POOL, STAGE, cstring
from dk4tool.patch.village_promised_words_release import resident_components
from scripts.probe_common_display_name_hook import branch_link

SOURCE = '9ea488296bf96f47522c90eb09cdea75bd5bc33e86854a25619805767a949a2c'
CLEAN = '0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731'
TEMPLATE = 'Fencing %d HP %d %s'
INHERITED_TRACKING_WRAPPER = 0x01FF9FCC
TRACKING_WRAPPER = 0x01FF9FE0
DESCRIPTOR = 0x1145B8
BITMAP_WIDTH = 156


def compiled_template():
    """Encode two twelve-cell columns before the complete health-state suffix."""
    # The prose stays natural and unpositioned. These spaces are generated
    # bitmap-column allocation, not authored dialogue or visible placeholders.
    first = 'Fencing %3d '
    second = 'HP %5d'
    return first + second + ' ' * (12 - (len('HP ') + 5)) + '%s'


def formatted(skill, hp, state):
    return compiled_template() % (skill, hp, state)


def transform(image, clean_image):
    source, clean = image.read_file('/__arm9__.bin'), clean_image.read_file('/__arm9__.bin')
    if sha(source) != SOURCE or sha(clean) != CLEAN:
        raise ValueError('Exact V156 and clean Japanese required')
    pointer = struct.unpack_from('<I', clean, 0xE310)[0]
    original = cstring(clean, pointer - BASE)
    if struct.unpack_from('<I', source, 0xE310)[0] != pointer or cstring(source, pointer - BASE) != original:
        raise ValueError('Original swordsmanship template already changed')
    owners = []
    for name, base, raw in resident_components(image):
        for at in range(len(raw) - 3):
            value = struct.unpack_from('<I', raw, at)[0]
            if pointer <= value <= pointer + len(original):
                owners.append((name, base + at, value - pointer))
    if owners != [('arm9_section_0', BASE + 0xE310, 0)]:
        raise ValueError('Swordsmanship template has unclassified owners: ' + str(owners))
    descriptors = [(-1, 4, 8, 0, 0, 60, 12), (-1, 4, 20, 60, 0, 60, 12), (-1, 72, 24, 120, 0, 24, 12)]
    if source[DESCRIPTOR:DESCRIPTOR + 84] != b''.join(struct.pack('<7i', *r) for r in descriptors):
        raise ValueError('Original duel composition descriptors differ')
    descriptor_owners = []
    for name, base, raw in resident_components(image):
        for at in range(len(raw) - 3):
            value = struct.unpack_from('<I', raw, at)[0]
            if BASE + DESCRIPTOR <= value < BASE + DESCRIPTOR + 84:
                descriptor_owners.append((name, base + at, value - BASE - DESCRIPTOR))
    if descriptor_owners != [('arm9_section_0', BASE + 0xE28C, 0)]:
        raise ValueError('Composition descriptor has unclassified owners')
    if source[0xE378:0xE37C] != struct.pack('<I', 0xE3A01090):
        raise ValueError('Original duel text bitmap width differs')
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    if (len(code.sections) != 4 or len(before[1]) != 8160 or len(before[3]) != 3312
            or code.sections[3].ramAddress != STAGE
            or before[1][INHERITED_TRACKING_WRAPPER - 0x01FF8000:] != status_wrapper(INHERITED_TRACKING_WRAPPER)
            or struct.unpack_from('<I', source, 0xE2FC)[0] != branch_link(BASE + 0xE2FC, BASE + 0xD5200)):
        raise ValueError('Inherited staged storage or native tracking wrapper differs')
    packed = bytearray(before[3][:-48])
    target = POOL + len(packed)
    packed.extend(compiled_template().encode('ascii') + b'\0')
    used = len(packed)
    size = (used + 31) & ~31
    packed.extend(bytes(size - used))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
    copy_entry = STAGE + size
    # D5200's third variadic value is on the caller stack. A push/BL/pop
    # wrapper would substitute its saved HP/LR for that suffix pointer.
    # Set tracking and tail-call with the original SP, LR and R0-R3 unchanged.
    tail = struct.pack('<3I', 0xE3E0C000, 0xE580C01C,
                       branch_link(TRACKING_WRAPPER + 8, BASE + 0xD5200) ^ 0x01000000)
    code.sections[1].data.extend(tail)
    low = (code.sections[1].ramAddress + len(code.sections[1].data) + 31) & ~31
    if low != 0x01FFA000:
        raise ValueError('Stats helper reservation differs or overlaps the overlay')
    for at, value in ((0xE310, target), (0xE2FC, branch_link(BASE + 0xE2FC, TRACKING_WRAPPER)),
                      (0x8E4, branch_link(BASE + 0x8E4, copy_entry)), (0xE45DC, POOL + size), (0xE45E4, low),
                      (0xE378, 0xE3A01000 | BITMAP_WIDTH), (DESCRIPTOR + 56 + 4, 66), (DESCRIPTOR + 56 + 20, 36)):
        struct.pack_into('<I', code.sections[0].data, at, value)
    saved = bytes(code.save())
    loaded = MainCodeFile(saved, BASE)
    restored = bytearray(loaded.sections[0].data)
    for at in (0xE310, 0xE2FC, 0x8E4, 0xE45DC, 0xE45E4, 0xE378, DESCRIPTOR + 60, DESCRIPTOR + 76):
        restored[at:at + 4] = source[at:at + 4]
    off = code.codeSettingsOffs
    restored[off:off + 12] = source[off:off + 12]
    if (bytes(restored) != before[0] or bytes(loaded.sections[1].data) != before[1] + tail
            or bytes(loaded.sections[2].data) != before[2] or packed[:3264] != before[3][:3264]):
        raise ValueError('Swordsmanship research changes unrelated bytes or inherited helpers')
    row = {'id': 'SWORDSMANSHIP_HP_STATUS', 'field': 0xE310, 'source_pointer': pointer,
           'source_hex': original.hex(), 'japanese': original.decode('cp932'), 'english': TEMPLATE,
           'target_pointer': target, 'speaker': 'Duel statistics interface',
           'compiled_template_hex': compiled_template().encode('ascii').hex(),
           'formatter': 'duel-stat-bitmap-columns-v1',
           'source_meaning': 'Sword fighting skill, current hit points, and the selected crew member\'s health state.',
           'context': 'Actual two-actor duel UI: 0200D54C selects parent+3C+index*A4 and actor parent+34+index*4, then calls 0200E290. The bitmap is cropped into three parent regions by 0200E1B0/020D470C/020CFC14. Effective skill caps at 500; HP is an unsigned halfword.',
           'localization_note': 'Fencing is a natural complete English term for sword fighting skill. Both numeric values and complete health-state suffix are retained. The formatter generates two twelve-cell columns with three/five digit widths, then a complete state. Extend only the native text view and third crop, placing the complete suffix inside the existing 104-pixel parent slot. A tail-call helper preserves the variadic stack argument.',
           'review': {g: g != 'formatting' for g in ('source', 'context', 'localization', 'naturalness', 'formatting')}}
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved), 'records': [row],
                   'owner_references': owners, 'pool_payload_bytes': size, 'pool_used_bytes': used,
                   'inherited_pool_bytes_preserved': 3264, 'copy_entry': copy_entry,
                   'final_pool_span': [POOL, POOL + size], 'staging_span': [STAGE, STAGE + size + 48],
                   'tracking_tail_helper': TRACKING_WRAPPER, 'itcm_bytes': 8172,
                   'reserved_arena_low': low, 'native_geometry': [BITMAP_WIDTH, 12],
                   'composition_descriptor_owners': descriptor_owners,
                   'source_composition_descriptors': descriptors,
                   'target_composition_descriptors': descriptors[:2] + [(-1, 66, 24, 120, 0, 36, 12)],
                   'status': 'research-prose-reviewed-native-layout-and-integration-pending'}


def apply_release(image, clean_image, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-swordsmanship-status-release-v1':
        raise ValueError('Wrong duel statistics release format')
    saved, plan = transform(image, clean_image)
    if config['source_arm9_sha256'] != SOURCE or config['target_arm9_sha256'] != sha(saved):
        raise ValueError('Duel release identities differ')

    def locked(key):
        path = Path(config[key])
        if sha(path.read_bytes()) != config[key + '_sha256']:
            raise ValueError('Duel evidence changed: ' + key)
        return json.loads(path.read_text(encoding='utf-8'))

    manuscript = locked('manuscript')
    validate_natural_dialogue_batch(manuscript)
    if (manuscript.get('translation_policy') != 'natural-dialogue-v2'
            or manuscript['source_arm9_sha256'] != CLEAN or len(manuscript['records']) != 1
            or {k: v for k, v in manuscript['records'][0].items() if k != 'review'}
            != {k: v for k, v in plan['records'][0].items() if k != 'review'}):
        raise ValueError('Complete duel source/prose review differs')
    proof = locked('native_proof')
    if (proof['source_arm9_sha256'] != SOURCE or proof['target_arm9_sha256'] != sha(saved)
            or [len(proof[k]) for k in ('native_pixel_cases', 'effective_skill_clamp',
                                       'inherited_movement_callers', 'inherited_village_callers',
                                       'inherited_monthly_scope_cases', 'inherited_sailing_status_pixels',
                                       'inherited_names', 'inherited_shared_owners')]
            != [64, 9, 24, 54, 9, 2, 207, 239]
            or proof['shared_copy_alignment_cases'] != 704
            or proof['common_selected_entries_preserved'] != 3668
            or [r['actual_constructor_stack_arguments'] for r in proof['geometry']] != [[156, 12, 0, 0]] * 2):
        raise ValueError('Duel native coverage incomplete')
    suffixes = ('Healthy', 'Tired', 'Wounded', 'Injured', 'Dying', 'Sick', 'Dead', '')
    expected = [(index, mode, skill, hp, state, formatted(skill, hp, suffix))
                for skill, hp in ((0, 0), (500, 65535))
                for state, suffix in zip((*range(7), 255), suffixes, strict=True)
                for index in (0, 1) for mode in (4, 16)]
    for row, values in zip(proof['native_pixel_cases'], expected, strict=True):
        if (tuple(row[k] for k in ('duel_actor_index', 'mode', 'effective_skill', 'hp', 'state', 'complete_formatted_text')) != values
                or not all(row[k] for k in ('complete_glyphs_bounds_and_independent_pixels',
                                           'native_owner_slot_caller_hp_state_getters_sprintf_and_renderer_execute',
                                           'native_stack_and_callee_saved_registers_preserved',
                                           'complete_non_space_glyphs_fit_native_parent_crops'))):
            raise ValueError('Complete duel native text, glyphs or parent crops differ')
    parent = proof['native_parent_composition']
    if (not all(parent[k] for k in ('native_primary_constructor_dispatch_and_crop_execute',
                                    'all_source_and_destination_bounds_pass', 'draw_stack_and_saved_registers_preserved'))
            or parent['source_canvas'] != [464, 96] or len(parent['actor_slots']) != 2
            or any(r['source_size'] != [156, 12] for r in parent['actor_slots'])
            or proof['native_initial_arenas']['low'][0] != plan['final_pool_span'][1]
            or proof['native_initial_arenas']['low'][3] != plan['reserved_arena_low']
            or proof['resident_arena_bounds']['resident_end'] != 0x01FF9FEC):
        raise ValueError('Duel parent or arena ownership incomplete')
    for index, slot in enumerate(parent['actor_slots']):
        left = 152 if index == 0 else 0
        expected_requests = [{'image': 0x022BD83C, 'layer': 0, 'flags': 0,
                              'source_origin': [x, 24 + index * 12], 'size': [width, 12],
                              'destination_origin': [left + destx, desty]}
                             for x, width, destx, desty in ((0, 60, 4, 103), (60, 60, 4, 115), (120, 36, 66, 119))]
        if (slot['index'] != index or slot['parent_rectangle'] != [left, 95, left + 104, 135]
                or slot['source_origin'] != [0, 24 + index * 12]
                or slot['draw_requests'] != expected_requests):
            raise ValueError('Duel complete three-crop composition differs')
    boot = proof['boot']
    if (boot['arm7_source_changed_bytes_after_arm9_autoload']
            or not all(r['matches_original'] for r in boot['arm7_native_loaded_sections'])
            or not all(boot[k] for k in ('repaired_pool_matches_complete_payload',
                                        'repair_returns_with_stack_preserved', 'actual_startup_call_preserves_r0_r3'))):
        raise ValueError('Duel staged boot ownership evidence incomplete')
    visual = proof['visual_review']
    if (not visual['complete'] or len(visual['sheets']) != 2
            or any(sha(Path(r['path']).read_bytes()) != r['sha256'] for r in visual['sheets'])):
        raise ValueError('Duel reviewed raster sheets changed or review incomplete')
    return saved, {**{k: v for k, v in plan.items() if k not in ('records', 'owner_references', 'status')},
                   'changed_records': ['SWORDSMANSHIP_HP_STATUS', 'DUEL_BITMAP_WIDTH_AND_COMPLETE_STATE_CROP',
                                       'DUEL_VARIADIC_TRACKING_TAIL', 'DUEL_STAGED_POOL_AND_ARENAS'],
                   'native_pixel_cases': 64, 'native_actor_slots': 2,
                   'inherited_movement_callers_preserved': 24, 'inherited_village_callers_preserved': 54,
                   'inherited_monthly_scope_cases_preserved': 9, 'shared_copy_alignment_cases': 704,
                   'common_selected_entries_preserved': 3668, 'physical_gameplay_verified': False}
