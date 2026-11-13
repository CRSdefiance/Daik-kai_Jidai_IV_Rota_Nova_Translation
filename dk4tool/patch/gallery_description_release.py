"""Translate Gallery headings/descriptions as complete logical English records."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ordinary_name_fidelity_release import BASE, POOL, STAGE, cstring
from dk4tool.patch.village_promised_words_release import resident_components
from scripts.probe_common_display_name_hook import branch_link

SOURCE = 'ab08d6e267e512e5f1dc3998930f8a3699809be784d712395ced60dc23ea91ad'
CLEAN = '0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731'
ROWS = [
    ('EVENT_SCENES_TITLE', (0x432C8,), 'Event Scenes', 42,
     'The Gallery section showing memorable scenes for each protagonist.',
     'Natural complete heading for the event-scene collection; retain Scenes as the section subject.'),
    ('EVENT_SCENES_DESCRIPTION', (0x432CC, 0x432D0),
     "Relive memorable scenes from each captain's story.", 34,
     'An invitation to see each protagonist\'s memorable scenes again.',
     'Relive expresses seeing the scenes again. Captain follows the established game terminology. The formatter divides the complete paragraph across the two native rows.'),
    ('HISTORIC_SITES_TITLE', (0x4423C,), 'Historic Sites', 42,
     'The Gallery section for historical sites.',
     'Natural complete English heading; the following description identifies the ruins and churches.'),
    ('HISTORIC_SITES_DESCRIPTION', (0x44240, 0x44244),
     "View the ruins and churches you've discovered.", 40,
     'You can review the ruins and churches you have discovered so far.',
     'Retain both categories and the already-discovered condition. The formatter divides this one logical paragraph across the two native rows.'),
    *[(f'EVENT_SCENES_{name.upper()}_DESCRIPTION', (0x115678 + index * 4,),
       f"Memorable scenes from {name}'s story.", 40,
       f'Memorable scenes from the story of {name}.',
       'Retain the selected captain and memorable-scene subject in a complete natural-English label. Native array lookup selects this description at x8/y20.')
      for index, name in enumerate(('Raphael', 'Hodram', 'Lil', 'Maria'))],
]
PAGES = ('events', 'event-0', 'event-1', 'event-2', 'event-3', 'sites', 'site-name')


def expected_page_draws(plan, page):
    fields = {move['field']: move for move in plan['pointer_moves']}
    selected = [(0x432C8, None, 2)] if page.startswith('event') else [(0x4423C, None, 2)]
    if page == 'events':
        selected += [(0x432CC, 48, 80), (0x432D0, 48, 96)]
    elif page.startswith('event-'):
        selected += [(0x115678 + int(page[-1]) * 4, 8, 20)]
    else:
        selected += [(0x44240, 8, 20), (0x44244, 8, 32)]
    result = []
    for field, x, y in selected:
        row = fields[field]
        text = bytes.fromhex(row['compiled_hex'])[:-1].decode('ascii')
        result.append({'pointer': row['target_pointer'], 'text': text,
                       'x': (256 - 6 * len(text)) // 2 if x is None else x, 'y': y, 'tracking': 0})
    if page == 'site-name':
        result.append({'pointer': 0x02400300, 'text': 'Lisbon', 'x': 110, 'y': 70, 'tracking': 0})
    return result


def compile_rows(english, count, capacity):
    """Balance complete words across the fixed native rows; no authored breaks."""
    def pair_safe(row):
        # D5404 consumes ASCII pairs; an odd final byte makes its next NUL
        # appear as a synthetic space glyph. Encode that tail cell explicitly.
        padded = row + (' ' if len(row) % 2 else '')
        if len(padded) > capacity:
            raise ValueError('Pair-safe Gallery row exceeds its native capacity')
        return padded

    if count == 1:
        if len(english) > capacity:
            raise ValueError('Gallery title exceeds its native row')
        return [pair_safe(english)]
    words = english.split(' ')
    options = [(' '.join(words[:at]), ' '.join(words[at:])) for at in range(1, len(words))]
    options = [rows for rows in options if all(len(row) <= capacity for row in rows)]
    if count != 2 or not options:
        raise ValueError('Complete Gallery paragraph does not fit its mapped native rows')
    weak_ends = {'and', 'or', 'the', 'a', 'an', 'of', 'to', 'from', 'with', 'for', 'in', 'on', 'at'}
    chosen = min(options, key=lambda rows: (rows[0].split()[-1].lower() in weak_ends,
                                            max(map(len, rows)), abs(len(rows[0]) - len(rows[1]))))
    if ' '.join(chosen) != english:
        raise ValueError('Gallery formatter loses source prose')
    return [pair_safe(row) for row in chosen]


def transform(image, clean_image):
    source, clean = [rom.read_file('/__arm9__.bin') for rom in (image, clean_image)]
    if sha(source) != SOURCE or sha(clean) != CLEAN:
        raise ValueError('Exact V157 and clean Japanese required')
    records, moves, spans = [], [], []
    for row_id, fields, english, capacity, meaning, note in ROWS:
        originals = []
        compiled = compile_rows(english, len(fields), capacity)
        for field in fields:
            pointer = struct.unpack_from('<I', clean, field)[0]
            raw = cstring(clean, pointer - BASE)
            if struct.unpack_from('<I', source, field)[0] != pointer or cstring(source, pointer - BASE) != raw:
                raise ValueError('Gallery Japanese owner differs or was already changed')
            originals.append({'field': field, 'source_pointer': pointer,
                              'source_hex': raw.hex(), 'japanese': raw.decode('cp932')})
            spans.append((field, pointer, pointer + len(raw)))
        records.append({'id': row_id, 'source_fields': originals,
                        'japanese': ''.join(r['japanese'] for r in originals), 'english': english,
                        'compiled_rows': compiled, 'formatter': 'gallery-native-balanced-rows-pair-safe-v1',
                        'capacity_ascii_characters': capacity, 'speaker': 'Gallery interface',
                        'source_meaning': meaning, 'localization_note': note,
                        'context': 'Event initial rows: title centered at y2, description x48 at y80/96; selected-event redraw reuses the title and indexes the four-captain table 02115678 through literal 02043304, drawing at x8/y20. Historic Sites native 02044158: title centered at y2, description x8 at y20/32, optional selected site centered at y70. All use 020456A0 and a 256x192 primary bitmap.',
                        'review': {g: g != 'formatting' for g in ('source', 'context', 'localization', 'naturalness', 'formatting')}})
    owners = []
    for component, base, raw in resident_components(image):
        for at in range(len(raw) - 3):
            pointer = struct.unpack_from('<I', raw, at)[0]
            for field, lo, hi in spans:
                if lo <= pointer <= hi:
                    owners.append((component, base + at, pointer - lo, field))
    expected = [('arm9_section_0', BASE + field, 0, field) for field, lo, hi in spans]
    if sorted(owners) != sorted(expected):
        raise ValueError('Gallery labels have unclassified complete/interior owners')
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    if len(before) != 4 or len(before[3]) != 3344 or code.sections[3].ramAddress != STAGE:
        raise ValueError('Inherited V157 allocation differs')
    packed = bytearray(before[3][:-48])
    for row in records:
        for original, compiled in zip(row['source_fields'], row['compiled_rows'], strict=True):
            pointer = POOL + len(packed)
            raw = compiled.encode('ascii') + b'\0'
            packed.extend(raw)
            struct.pack_into('<I', code.sections[0].data, original['field'], pointer)
            moves.append({'field': original['field'], 'target_pointer': pointer, 'compiled_hex': raw.hex()})
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
    for field in [r['field'] for r in moves] + [0x8E4, 0xE45DC]:
        restored[field:field + 4] = source[field:field + 4]
    off = code.codeSettingsOffs
    restored[off:off + 12] = source[off:off + 12]
    if (bytes(restored) != before[0] or bytes(loaded.sections[1].data) != before[1]
            or bytes(loaded.sections[2].data) != before[2] or packed[:3296] != before[3][:3296]):
        raise ValueError('Gallery transform changes unrelated data, helpers or inherited pool')
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved),
                   'records': records, 'pointer_moves': moves, 'source_owners': owners,
                   'pool_payload_bytes': size, 'pool_used_bytes': used, 'inherited_pool_bytes_preserved': 3296,
                   'copy_entry': copy_entry, 'final_pool_span': [POOL, POOL + size],
                   'staging_span': [STAGE, STAGE + size + 48], 'itcm_bytes': len(before[1]),
                   'reserved_arena_low': 0x01FFA000, 'native_geometry': [256, 192],
                   'status': 'research-prose-reviewed-native-caller-parent-pixels-and-integration-pending'}


def apply_release(image, clean_image, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-gallery-descriptions-release-v1':
        raise ValueError('Wrong Gallery release format')
    saved, plan = transform(image, clean_image)
    if config['source_arm9_sha256'] != SOURCE or config['target_arm9_sha256'] != sha(saved):
        raise ValueError('Gallery release identities differ')

    def locked(key):
        path = Path(config[key])
        if sha(path.read_bytes()) != config[key + '_sha256']:
            raise ValueError('Gallery evidence changed: ' + key)
        return json.loads(path.read_text(encoding='utf-8'))

    manuscript = locked('manuscript')
    validate_natural_dialogue_batch(manuscript)
    if (manuscript.get('translation_policy') != 'natural-dialogue-v2'
            or manuscript['source_arm9_sha256'] != CLEAN or len(manuscript['records']) != 8):
        raise ValueError('Gallery complete source review differs')
    for row, expected in zip(manuscript['records'], plan['records'], strict=True):
        if {k: v for k, v in row.items() if k != 'review'} != {k: v for k, v in expected.items() if k != 'review'}:
            raise ValueError('Gallery complete source/prose review differs')
    proof = locked('native_proof')
    if (proof['source_arm9_sha256'] != SOURCE or proof['target_arm9_sha256'] != sha(saved)
            or [len(proof[k]) for k in ('native_pixel_cases', 'inherited_duel_pixels', 'inherited_movement_callers',
                                       'inherited_village_callers', 'inherited_monthly_scope_cases',
                                       'inherited_sailing_status_pixels', 'inherited_names', 'inherited_shared_owners')]
            != [14, 64, 24, 54, 9, 2, 207, 239]
            or proof['shared_copy_alignment_cases'] != 704 or proof['common_selected_entries_preserved'] != 3668):
        raise ValueError('Gallery native coverage incomplete')
    for row, (page, mode) in zip(proof['native_pixel_cases'], [(p, m) for p in PAGES for m in (4, 16)], strict=True):
        if (row['page'] != page or row['mode'] != mode or row['draws'] != expected_page_draws(plan, page)
                or not all(row[k] for k in ('complete_glyphs_bounds_and_independent_pixels',
                                           'actual_native_selection_centering_context_renderer_and_cleanup_execute',
                                           'native_stack_and_caller_state_preserved'))):
            raise ValueError('Gallery complete native field selection, prose or pixels differ')
    parent = proof['native_parent_composition']
    overlays = loadOverlayTable(image.rom.arm9OverlayTable, lambda oid, fid: image.files[fid])
    if (parent['native_geometry'] != [256, 192]
            or parent['native_overlay'] != {'base': 0x01FFA000, 'sha256': sha(bytes(overlays[0].data))}
            or parent['draw_requests'] != [{'image': 0x02466014, 'layer': 1, 'flags': 0,
                                           'source_origin': [0, 0], 'size': [256, 192], 'destination_origin': [0, 0]}]
            or not all(parent[k] for k in ('native_constructor_clear_and_primary_composition_execute',
                                          'all_source_and_screen_bounds_pass',
                                          'nonzero_canvas_seed_cleared_and_object_canaries_preserved'))
            or proof['native_initial_arenas']['low'][0] != plan['final_pool_span'][1]
            or proof['resident_arena_bounds']['resident_end'] != 0x01FF9FEC
            or proof['resident_arena_bounds']['native_arena_low'] != 0x01FFA000):
        raise ValueError('Gallery native clear, complete primary composition or ownership incomplete')
    boot = proof['boot']
    if (boot['arm7_source_changed_bytes_after_arm9_autoload']
            or not all(r['matches_original'] for r in boot['arm7_native_loaded_sections'])
            or not all(boot[k] for k in ('repaired_pool_matches_complete_payload',
                                        'repair_returns_with_stack_preserved', 'actual_startup_call_preserves_r0_r3'))):
        raise ValueError('Gallery staged SDK/ARM7 ownership evidence incomplete')
    visual = proof['visual_review']
    if (not visual['complete'] or len(visual['sheets']) != 1
            or any(sha(Path(r['path']).read_bytes()) != r['sha256'] for r in visual['sheets'])):
        raise ValueError('Gallery raster sheet changed or visual review incomplete')
    return saved, {**{k: v for k, v in plan.items() if k not in ('records', 'source_owners', 'status')},
                   'changed_records': [r['id'] for r in plan['records']] + ['GALLERY_STAGED_POOL_AND_ARENA'],
                   'localized_logical_records': 8, 'native_pointer_fields': 10, 'native_pixel_cases': 14,
                   'inherited_duel_pixels_preserved': 64, 'inherited_movement_callers_preserved': 24,
                   'inherited_village_callers_preserved': 54, 'inherited_monthly_scope_cases_preserved': 9,
                   'common_selected_entries_preserved': 3668, 'shared_copy_alignment_cases': 704,
                   'physical_gameplay_verified': False}


def prepare():
    from dk4tool.rom.nds import NdsImage

    source, plan = transform(NdsImage.open('out/all_routes_combined_v157_candidate.nds'), NdsImage.open('work/clean.nds'))
    Path('work/analysis/gallery_description_research_arm9.bin').write_bytes(source)
    Path('work/analysis/gallery_description_plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    manuscript = {'format': 'dk4-gallery-description-manuscript-v1',
                  'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                  'encoder': 'dialogue-relocatable-v1', 'source_arm9_sha256': CLEAN,
                  'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
                  'records': plan['records'], 'status': plan['status']}
    Path('translations/gallery_description_manuscript_v1.json').write_text(json.dumps(manuscript, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared eight complete Gallery headings/paragraphs across ten native fields; no new resident helper.')
